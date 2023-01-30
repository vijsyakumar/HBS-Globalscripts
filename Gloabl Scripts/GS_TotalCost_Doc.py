#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for cost calculation for document purpose
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 09/29/2022    Sreenivasa Mucharla        0             -Initial Version
# 10/18/2022    Ishika Bhattacharya        5             -Incorporated Translation
#
# 11/04/2022	Dhruv Bhatnagar			   6		 	 -SQL translation,Transacrtion type
#												         check implemented
# 11/24/2022    Ishika Bhattacharya        7             - Assigning value to a custom field
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  #Modified by Dhruv
    context.Quote.GetCustomField('CF_Warranty_Duration_Months').Value = context.Quote.GetCustomField('Warranty Duration(in months)').Value
    quote_table = context.Quote.QuoteTables['QT_Quote_Summary']
    totalcost = 0
    for row in quote_table.Rows:
        totalcost += row['Cost']
    # context.Quote.GetCustomField('CF_TotalCost_Doc').Value = round(totalcost,2)
    context.Quote.GetCustomField('CF_TotalCost_QuoteSummary').Value = round(totalcost,2)  #Added by ishika 24 Nov
    count =0
    for row1 in quote_table.Rows:
        if row1['Cost'] != 0 and totalcost:
            row1['Costper'] = round((row1['Cost']/totalcost)*100,2)
        else:
            row1['Costper'] = 0

