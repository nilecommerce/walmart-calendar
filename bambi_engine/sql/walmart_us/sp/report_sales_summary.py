from wm_calendar.wm_week import lw, wm_week
from ..fn.aggregate_table import sales, inventory, inventory_current
from ..fn.calculate_table import wos, forecast_var

def query():

    last_wk = lw()

    inventory_current_t = 'inventory_current_t table query here'
    inventory_t = 'inventory_t table query here'
    lw_sales_t = sales(last_wk, last_wk)
    lylw_sales_t = 'lylw_sales_t table query here'
    ytd_sales_t = 'ytd_sales_t table query here'
    lyytd_sales_t = 'lyytd_sales_t table query here'
    wos_t = 'wos_t table query here'
    frcst_var_t = 'frcst_var_t table query here'

    sql='''
	SELECT
		-- Item Information
		i.[Prime Item Nbr]
		, [Prime Item Desc]
		, [Vendor Stk Nbr]
		, [UPC]
		, [Effective Date]
		, [Unit Cost]
		, [Unit Retail]
		, [MU %]
		, [Buyer Full Name]
		, [Acct Dept Nbr]
		, [Dept Category Description]
		, [Dept Subcategory Description]
		, [Fineline Description]
		, [Item Status]
		, [Item Type]
		, [Whse Align]
		, [Corp Cancel When Out Flag]
		, [Order book Flag]
		, [VNPK Qty]
		, [WHPK Qty]
		, ' ' AS [Image URL]

		-- Curr Inv Data
		, CASE
			WHEN cinv.[Curr Traited Store/Item Comb] > 0 THEN 'Traited'
			ELSE 'Not Traited'
			END AS [Traited Status]
		, CASE
			WHEN cinv.[Curr Instock %] = 0 THEN NULL
			ELSE cinv.[Curr Instock %]
			END AS [Curr Instock %]
		, CASE
			WHEN cinv.[Curr Repl Instock %] = 0 THEN NULL
			ELSE cinv.[Curr Repl Instock %]
			END AS [Curr Repl Instock %]
		, cinv.[Curr Traited Store/Item Comb]
		, cinv.[Curr Str On Hand Qty]
		, cinv.[Curr Str In Transit Qty]
		, cinv.[Curr Str In Whse Qty]
		, cinv.[Curr Str On Order Qty]
		, cinv.[Curr Whse On Hand Qty]
		, cinv.[Curr Whse SS Order Qty]

		-- Last Week Data
		, lws.[POS Qty]		AS [LW POS Qty]
		, lylws.[POS Qty]     AS [LY LW POS Qty]
		, lws.[POS Sales]	AS [LW POS Sales]
		, lylws.[POS Sales] AS  [LY LW POS Sales]
		, CASE
			WHEN lylws.[POS Qty] IS NULL THEN 1
			WHEN lylws.[POS Qty] = 0 THEN 1
			ELSE (lws.[POS Qty] - lylws.[POS Qty]) / lylws.[POS Qty]
			END AS [LW Sales Qty % Chng]
		, CASE
			WHEN lylws.[POS Sales] IS NULL THEN 1
			WHEN lylws.[POS Sales] = 0 THEN 1
			ELSE (lws.[POS Sales] - lylws.[POS Sales]) / lylws.[POS Sales]
			END AS [LW Sales % Chng]
		, CASE
			WHEN cinv.[Curr Str On Hand Qty] = 0 THEN 0
			ELSE lws.[POS Qty] / cinv.[Curr Str On Hand Qty]
			END AS [Wkly Sell Thru %]
		, CASE
			WHEN lws.[Avg Traited Store/Item Comb] = 0 THEN NULL
			ELSE lws.[POS Qty] / lws.[Avg Traited Store/Item Comb]
			END AS [LW U/S/W]
		, CASE
			WHEN lws.[Avg Traited Store/Item Comb] = 0 THEN NULL
			ELSE (lws.[POS Sales]- lws.[POS Cost]) / lws.[Avg Traited Store/Item Comb]
			END AS [LW P/S/W]
		, CASE
			WHEN lws.[Avg Traited Store/Item Comb] = 0 THEN NULL
			ELSE lws.[POS Sales] / lws.[Avg Traited Store/Item Comb]
			END AS [LW $/S/W]
		, lws.[Gross Ship Qty] AS [LW Gross Ship Qty]
		, lwinv.[52/53 WK FC Units]
		, wos.[Hist WOS]
		, wos.[Frcst WOS]
		, lws.[Cust Def Qty] AS [LW Cust Def Qty]
		, lws.[Total Customer Item Return] AS [LW Total Customer Item Return]
		, lws.[SI Total MUMD $] as [LW SI Total MUMD $]

		-- Year to Date Data
		, ytds.[POS Qty]	AS [YTD POS Qty]
		, lyytds.[POS Qty]	AS [LY YTD POS Qty]
		, ytds.[POS Sales]	AS [YTD POS Sales]
		, lyytds.[POS Sales]AS [LY YTD POS Sales]
		, ytds.[SI Total MUMD $] as [YTD SI Total MUMD $]
		, CASE
			WHEN lyytds.[POS Qty] IS NULL THEN 1
			WHEN lyytds.[POS Qty] = 0 THEN 1
			ELSE (ytds.[POS Qty]- lyytds.[POS Qty]) / lyytds.[POS Qty]
			END AS [YTD Sales Qty % Chng]
		, CASE
			WHEN lyytds.[POS Sales] IS NULL THEN 1
			WHEN lyytds.[POS Sales] = 0 THEN 1
			ELSE (ytds.[POS Sales]- lyytds.[POS Sales]) / lyytds.[POS Sales]
			END AS [YTD Sales % Chng]
		, CASE
			WHEN ytds.[Gross Ship Qty] = 0 THEN 0
			ELSE ytds.[POS Qty] / ytds.[Gross Ship Qty]
			END AS [YTD Sell Thru %]
		, ytds.[Gross Ship Qty] AS [YTD Gross Ship Qty]
		, ytds.[Cust Def Qty] AS [YTD Cust Def Qty]
		, ytds.[Total Customer Item Return] AS [YTD Total Customer Item Return]
		, fcv.[LW Frcst Var]
		, fcv.[L4W Avg Frcst Var]

	FROM Walmart_US.PrimeItems i
		LEFT JOIN ({cinv})	 cinv	 ON i.[Prime Item Nbr] = cinv.[Prime Item Nbr]
		LEFT JOIN ({lwinv})	 lwinv	 ON i.[Prime Item Nbr] = lwinv.[Prime Item Nbr]
		LEFT JOIN ({lws})	 lws     ON i.[Prime Item Nbr] = lws.[Prime Item Nbr]
		LEFT JOIN ({lylws})	 lylws	 ON i.[Prime Item Nbr] = lylws.[Prime Item Nbr]
		LEFT JOIN ({ytds})	 ytds    ON i.[Prime Item Nbr] = ytds.[Prime Item Nbr]
		LEFT JOIN ({lyytds}) lyytds  ON i.[Prime Item Nbr] = lyytds.[Prime Item Nbr]
		LEFT JOIN ({wos})	 wos     ON i.[Prime Item Nbr] = wos.[Prime Item Nbr]
		LEFT JOIN ({fcv})    fcv	 ON i.[Prime Item Nbr] = fcv.[Prime Item Nbr]

    '''.format(
        cinv = inventory_current_t,
        lwinv = inventory_t,
        lws = lw_sales_t,
        lylws = lylw_sales_t,
        ytds = ytd_sales_t,
        lyytds = lyytd_sales_t,
        wos = wos_t,
        fcv = frcst_var_t,
    )
    return sql
