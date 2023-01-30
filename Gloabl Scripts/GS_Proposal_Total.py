#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script defines total value for Material and Labor present in Proposal Template These total values are calculated after all the selections are done in commercial info tab.
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 9/20/2022    Payal Gupta               0             -Initial Version
# 10/17/2022    Krishna Chaitanya        1            -Replaced Hardcodings
#                                                -Incorporated Translation
# 11/03/2022	Srinivasan Dorairaj		 3		 -Script Translation changes
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS                   
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)   
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Srinivasan Dorairaj
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Modified by Srinivasan Dorairaj

    final_total_labor = 0
    table_total_list_labor = []

    final_total_bom = 0
    table_total_list_bom = []

    ###-----Calculating total for Labor proposal template-----###

    final_table_labor = context.Quote.QuoteTables["QT_LABOR_PT"].Rows
    for row in final_table_labor:
        table_total_list_labor.append(row)
    for t in range(len(table_total_list_labor)):
        table_total_row = table_total_list_labor[t]
        table_total = table_total_row["TOTAL"]
        final_total_labor += table_total
    context.Quote.GetCustomField('CF_TOTAL_LABOR').Value = '%.2f' %final_total_labor

    ###-----Calculating total for BOM proposal template-----###

    final_table_bom = context.Quote.QuoteTables["QT_Materials"].Rows
    for row in final_table_bom:
        table_total_list_bom.append(row)
    for t in range(len(table_total_list_bom)):
        table_total_row = table_total_list_bom[t]
        table_total = table_total_row["TOTAL"]
        final_total_bom += table_total
    context.Quote.GetCustomField('CF_TOTAL_MATERIAL').Value = '%.2f' %final_total_bom