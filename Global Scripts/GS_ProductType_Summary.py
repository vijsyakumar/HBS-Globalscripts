#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for product type table
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 08/26/2022    Sumandrita Moitra          0             -Initial Version
# 10/18/2022    Ishika Bhattacharya        47            -Incorporated Translation
# 11/03/2022	Srinivasan Dorairaj		   58			 -Script Translation changes
#-----------------------------------------------------------------------------


import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Srinivasan Dorairaj
lc_mand_charges = GM_TRANSLATIONS.GetText('000213', lv_LanguageKey, '', '', '', '', '')
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Modified by Srinivasan Dorairaj
    ptList = []
    quote_table = context.Quote.QuoteTables['QT_Quote_Summary']
    quote_table.Rows.Clear()

    for num, i in enumerate(context.Quote.GetAllItems(), start=1):
        if i.IsOptional == False and i.ProductSystemId != 'RQ_Mandatory_Charges_cpq':
            if num == 1 or ( i['QI_Product_Type'] not in ptList ):
                newRow = quote_table.AddNewRow()
                ptList.append(i['QI_Product_Type'])
                Log.Write("SK ptlist : "+str(ptList))
                pr_Type = i.ProductTypeName
                Trace.Write("SK Quote Item : "+str(i.QuoteItem))
                newRow['Product_Type_Rows'] = i['QI_Product_Type']
                newRow['Sell_Price'] = i.NetPrice
                newRow['Discount_Amount'] = (i.DiscountAmount)*(i.Quantity)
                newRow['Recommended_Price'] = i["QI_Recommended_Sell_Price"]
                newRow['List_Price'] = i["QI_List_Price_Total"]
                if i['QI_Total_Cost'] > 0:
                    newRow['Cost'] = i["QI_TOTAL_QUOTE_COST"]
                if i['QI_INFLATION_AMOUNT'] > 0 :
                    newRow['Inflation_Factor'] = i['QI_INFLATION_AMOUNT']
                if i['QI_hours'] > 0:
                    newRow['Hours'] =  i['QI_hours']
            
                Trace.Write("ffed" +str(newRow['Cost']))
                newRow['Discount_'] = i.DiscountPercent
                newRow['CSPA_DIscount_Amount'] = i["QI_CSPA_DiscountAmount"]
                if i["QI_List_Price_Total"] != 0 and newRow['CSPA_DIscount_Amount']!=None and i["QI_List_Price_Total"]!=None:
                    newRow['CSPA_Discount_'] =newRow['CSPA_DIscount_Amount'] /float(i["QI_List_Price_Total"])*100
                if (i.NetPrice) != 0  :
                    newRow['Actual_Gross_Margin_'] = (i.NetPrice -(i["QI_TOTAL_QUOTE_COST"]))/i.NetPrice * 100
                if (i.NetPrice) != 0 and i["QI_WTW_Margin"] != None:
                    newRow['W2W_Margin_'] = float(i['QI_WTW_Margin']) / float(i.NetPrice)*100
            
            else:
                for r in quote_table.Rows:
                    if r['Product_Type_Rows'] == i['QI_Product_Type'] :
                        Trace.Write("SK Inside Else - Product Type : "+str(i.ProductTypeName))
                        r['Sell_Price'] = r['Sell_Price'] + i.NetPrice
                        if i["QI_Recommended_Sell_Price"]!=None:
                            r['Recommended_Price'] = r['Recommended_Price'] + i["QI_Recommended_Sell_Price"]
                        r['Discount_Amount'] = r['Discount_Amount'] + ((i.DiscountAmount)*(i.Quantity))
                        if i["QI_List_Price_Total"]!=None:
                            r['List_Price'] = r['List_Price'] + i["QI_List_Price_Total"]
                        if i["QI_Total_Cost"]!=None:
                            r['Cost'] = r['Cost'] + i["QI_TOTAL_QUOTE_COST"]
                        if i["QI_INFLATION_AMOUNT"]!=None:
                            r['Inflation_Factor'] = r['Inflation_Factor']+ i['QI_INFLATION_AMOUNT']
                        if i['QI_hours']!=None:
                            r['Hours'] = r['Hours'] + i['QI_hours']
                        if r['Recommended_Price'] != 0 :
                            r['Discount_'] = (r['Discount_Amount']/r['Recommended_Price'])*100
                        if i["QI_CSPA_DiscountAmount"]!=None:
                            r['CSPA_DIscount_Amount'] = r['CSPA_DIscount_Amount'] + i["QI_CSPA_DiscountAmount"]
                        if (r['Sell_Price'] + i.NetPrice) != 0 :
                            r['Actual_Gross_Margin_'] = (r['Sell_Price']- r['Cost'])/r['Sell_Price'] * 100
                        if r['List_Price'] != 0 :
                            r['CSPA_Discount_'] = (r['CSPA_DIscount_Amount']/float(r['List_Price']))*100
                        if (i.NetPrice) != 0 and i["QI_WTW_Margin"] != None:
                            r['W2W_Margin_'] = r['W2W_Margin_'] + (float(i['QI_WTW_Margin']) / float(i.NetPrice)) * 100
                    #Trace.Write("df" +str(r['CSPA_Discount_']) )
                    #Trace.Write("df" +str(r['Inflation_Factor']) )




