# -----------------------------------------------------------------------------
#			Change History Log
# -----------------------------------------------------------------------------
# Description:
# This script deletes the quote table rows based on product category types
# -----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
# -----------------------------------------------------------------------------
# 10/18/2022    Sumandrita Moitra     0         -initial version
# 11/5/2022  	Ishika BHattacharya	  7	        -Replaced Hardcodings
#										        -Incorporated Translation
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------

import GM_TRANSLATIONS  # Added by ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')  # Added by ishika

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  # Added by ishika
    lc_WriteIn = GM_TRANSLATIONS.GetText('000175', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
    lc_WriteIns = GM_TRANSLATIONS.GetText('000182', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
    lc_Mandatory_charge = GM_TRANSLATIONS.GetText('000213', lv_LanguageKey, '', '', '', '', '')
    quote_table1 = context.Quote.QuoteTables['QT_Quote_Summary']

    for row in quote_table1.Rows:
        DelRow = 0
        if row['Product_Type_Rows'] == "" or row['Product_Type_Rows'] == lc_WriteIn or row['Product_Type_Rows'] == lc_Mandatory_charge:  #Added by ishika
            # if row['Product_Type_Rows'] == "" or row['Product_Type_Rows'] == "Write-In":   #Commented by Ishika
            # Trace.Write("DeleteProdCategory---" + str(row['Product_Type_Rows']))
            DelRow = row.Id

            # Trace.Write("ID" + str(DelRow))
            quote_table1.DeleteRow(DelRow)

    quote_table2 = context.Quote.QuoteTables['QT_Product_Categories']
    for row in quote_table2.Rows:
        DelRow1 = 0
        #if row['Product_Category_Rows'] == "" or row['Product_Category_Rows'] == "Write-Ins":  #commented by Ishika
        if row['Product_Category_Rows'] == "" or row['Product_Category_Rows'] == lc_WriteIns:   #Added by Ishika
            Trace.Write("DeleteProdCategory---" + str(row['Product_Category_Rows']))
            DelRow1 = row.Id

            #Trace.Write("ID" + str(DelRow1))
            quote_table2.DeleteRow(DelRow1)



