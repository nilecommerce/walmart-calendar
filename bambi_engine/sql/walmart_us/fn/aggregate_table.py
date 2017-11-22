
def sales(startwk, endwk, rollup=''):
    item_col = 'Item Nbr' if rollup == 'detail' else 'Prime Item Nbr'

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
	WHERE [WM Week] BETWEEN {startweek} AND {endweek}
	GROUP BY i.[{item_column}]
    '''.format(
        item_column = item_col,
        startweek = startwk,
        endweek = endwk
    )
    return sql


def inventory():
    return 'sql'

def inventory_current():
    return 'sql' 
