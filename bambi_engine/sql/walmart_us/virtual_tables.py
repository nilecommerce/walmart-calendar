from wm_calendar.wm_week import WalmartWeek
from ..utils import get_week_filter, combine_weeks

def sales(weeks, rollup=''):
    '''
    ARGS
        @weeks
        @rollup
    '''

    item_col = 'Item Nbr' if rollup == 'detail' else 'Prime Item Nbr'

    # Build SQL Query string
    sql ='''
    SELECT
		i.[{item_column}],
		SUM([POS Qty]) AS [POS Qty],
		SUM([POS Cost]) AS [POS Cost],
		SUM([POS Sales]) AS [POS Sales],
		AVG(NULLIF([Avg Traited Store/Item Comb], 0)) AS [Avg Traited Store/Item Comb],
		SUM([Gross Ship Qty]) AS [Gross Ship Qty],
		SUM([Gross Ship Cost]) AS [Gross Ship Cost],
		SUM([Cust Def Qty]) AS [Cust Def Qty],
		SUM([SI Total MUMD $]) as [SI Total MUMD $],
		SUM([Total Customer Item Return]) AS [Total Customer Item Return],
		SUM([Total Customer Return Cost]) AS [Total Customer Return Cost],
		SUM([Total Customer Return Retail]) AS [Total Customer Return Retail]
	FROM Walmart_US.Sales s
		LEFT JOIN Walmart_US.Items i ON i.[Item nbr] = s.[Item Nbr]
	WHERE [WM Week] {week_filter}
	GROUP BY i.[{item_column}]
    '''.format(
        item_column = item_col,
        week_filter = get_week_filter(weeks)
    )
    return sql


def inventory(weeks, rollup=''):
    '''
    ARGS
        @weeks
        @rollup
    '''

    item_col = 'Item Nbr' if rollup == 'detail' else 'Prime Item Nbr'
    # Build SQL Query string
    sql = '''
    SELECT
		i.[{item_column}],
		AVG(NULLIF([Rolling 52/53 WK FC Units], 0)) AS [52/53 WK FC Units],
		SUM([Avg On Hand Rtl])/COUNT(DISTINCT inv.[WM Week]) as [Avg On Hand Rtl]
	FROM Walmart_US.Inventory inv
		LEFT JOIN Walmart_US.Items i ON i.[Item nbr] = inv.[Item Nbr]
	WHERE [WM Week] {week_filter}
	GROUP BY i.[{item_column}]
    '''.format(
        item_column = item_col,
        week_filter = get_week_filter(weeks)
    )
    return sql


def inventory_current(rollup=''):

    item_col = 'Item Nbr' if rollup == 'detail' else 'Prime Item Nbr'
    # Build SQL Query string
    sql = '''
    SELECT
		[{item_column}]
		, AVG(NULLIF([Curr Instock %], 0)) AS [Curr Instock %]
		, AVG(NULLIF([Curr Repl Instock %], 0))/100 AS [Curr Repl Instock %]
		, AVG(NULLIF([Curr Traited Store/Item Comb], 0)) AS [Curr Traited Store/Item Comb]
		, SUM([Curr Str On Hand Qty]) AS [Curr Str On Hand Qty]
		, SUM([Curr Str In Transit Qty]) AS [Curr Str In Transit Qty]
		, SUM([Curr Str In Whse Qty]) AS [Curr Str In Whse Qty]
		, SUM([Curr Str On Order Qty]) AS [Curr Str On Order Qty]
		, SUM([Curr Whse On Hand Qty]) AS [Curr Whse On Hand Qty]
		, SUM([Curr Whse SS Order Qty]) AS [Curr Whse SS Order Qty]
	FROM Walmart_US.InventoryCurrent
	GROUP BY [{item_column}]
    '''.format(
        item_column = item_col
    )
    return sql


def forecast(weeks):

    # Build SQL Query string
    sql = '''
    SELECT
		[Prime Item Nbr],
		SUM([Total Forecast]) AS [Total Forecast]
	FROM (
		SELECT
			i.[Prime Item Nbr],
			f.[Sale WM Week] AS [WM Week],
			f.[Total Forecast]
		FROM Walmart_US.Items i
			FULL JOIN Walmart_US.Forecast f ON i.[Item Nbr] = f.[Prime Item Nbr]
		WHERE i.[Prime Item Nbr] IS NOT NULL

		UNION

		-- Used to catch Prime Items that have Item Nbrs different than the Prime Item Nbr
		SELECT
			i.[Prime Item Nbr],
			f.[Sale WM Week] AS [WM Week],
			f.[Total Forecast]
		FROM Walmart_US.PrimeItems i
			LEFT JOIN Walmart_US.Forecast f ON i.[Prime Item Nbr] = f.[Prime Item Nbr]
		WHERE f.[Prime Item Nbr] IN (	SELECT
											F.[Prime Item Nbr]
										FROM Walmart_US.Items i
											FULL JOIN Walmart_US.Forecast f ON i.[Item Nbr] = f.[Prime Item Nbr]
										WHERE i.[Item Nbr] IS NULL )
	) f
	WHERE
		[WM Week] IS NOT NULL AND
		[WM Week] {week_filter}
	GROUP BY
		[Prime Item Nbr]
    '''.format(
        week_filter = get_week_filter(weeks)
    )
    return sql


def wos():
    ww = WalmartWeek()

    # Build SQL Query string
    sql = '''
    SELECT
		[Prime Item Nbr],
		[Item Nbr],
		[Avg POS Qty],
		[Avg Total Forecast],
		[Curr Str On Hand Qty],
		CASE
			WHEN [Avg POS Qty] = 0 THEN NULL
			ELSE [Curr Str On Hand Qty]/[Avg POS Qty]
		END AS [Hist WOS],
		CASE
			WHEN [Avg Total Forecast] = 0 THEN NULL
			ELSE [Curr Str On Hand Qty]/[Avg Total Forecast]
		END AS [Frcst WOS]
	FROM (
		SELECT
			i.[Prime Item Nbr],
			i.[Item Nbr],

			(	SELECT [POS Qty]/4
				FROM ({sales}) s
				WHERE s.[Prime Item Nbr] = i.[Prime Item Nbr]
			) AS [Avg POS Qty],

			(	SELECT [Total Forecast]/4
				FROM ({forecast}) f
				WHERE f.[Prime Item Nbr] = i.[Prime Item Nbr]
			) AS [Avg Total Forecast],

			(	SELECT [Curr Str On Hand Qty]
				FROM ({inventory_current}) inv
				WHERE i.[Prime Item Nbr] = inv.[Prime Item Nbr]
			) AS [Curr Str On Hand Qty]

		FROM Walmart_US.PrimeItems i
	) s
	WHERE [Avg POS Qty] > 50
    '''.format(
        sales = sales(ww.l4w()),
        forecast = forecast(ww.n4w()),
        inventory_current = inventory_current()
    )
    return sql


def forecast_var():
    ww = WalmartWeek()

    # Build SQL Query string
    sql = '''
    SELECT
		[Prime Item Nbr],
		[Item Nbr],
		[LW POS Qty],
		[LW Total Forecast],
		[Avg POS Qty],
		[Avg Total Forecast],
		CASE
			WHEN [LW Total Forecast] = 0 THEN NULL
			ELSE ([LW POS Qty] - [LW Total Forecast])/[LW Total Forecast]
		END AS [LW Frcst Var],
		CASE
			WHEN [Avg Total Forecast] = 0 THEN NULL
			ELSE ([Avg POS Qty] - [Avg Total Forecast])/[Avg Total Forecast]
		END AS [L4W Avg Frcst Var]
	FROM (
		SELECT
			i.[Prime Item Nbr],
			i.[Item Nbr],

			(	SELECT [POS Qty]
				FROM ({lws}) s
				WHERE s.[Prime Item Nbr] = i.[Prime Item Nbr]
			) AS [LW POS Qty],

			(	SELECT [Total Forecast]
				FROM ({lwf}) f
				WHERE f.[Prime Item Nbr] = i.[Prime Item Nbr]
			) AS [LW Total Forecast],

			(	SELECT [POS Qty]/4
				FROM ({l4ws}) s
				WHERE s.[Prime Item Nbr] = i.[Prime Item Nbr]
			) AS [Avg POS Qty],

			(	SELECT [Total Forecast]/4
				FROM ({n4wf}) f
				WHERE f.[Prime Item Nbr] = i.[Prime Item Nbr]
			) AS [Avg Total Forecast]

		FROM Walmart_US.PrimeItems i
	) s
	WHERE [Avg POS Qty] > 50
    '''.format(
        lws = sales(ww.lw()),
        lwf = forecast(ww.lw()),
        l4ws = sales(ww.l4w()),
        n4wf = forecast(ww.n4w())
    )
    return sql
