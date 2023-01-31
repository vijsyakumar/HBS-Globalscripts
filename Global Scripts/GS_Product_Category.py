#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for product categories quote table
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 09/4/2022     AshutoshKumar Mishra       0             -Initial Version
# 10/18/2022    Ishika Bhattacharya        14            -Incorporated Translation
# 11/03/2022	Srinivasan Dorairaj 	   26			 -Script Translation changes
# 12/20/2022	Sumandrita Moitra		   51			 - replaced (r['Recommended_price']-r['Sell_Price']) with r['Discount_Amount']
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)   # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')#Modified by Srinivasan Dorairaj
lc_Mand_charges = GM_TRANSLATIONS.GetText('000213', lv_LanguageKey, '', '', '', '', '')
#cxcpq-33770 start
lc_prodType_TP = GM_TRANSLATIONS.GetText('000065', lv_LanguageKey, '', '', '', '', '')
lc_prodType_WI = GM_TRANSLATIONS.GetText('000175', lv_LanguageKey, '', '', '', '', '')
lc_prodType_TPM = GM_TRANSLATIONS.GetText('000214', lv_LanguageKey, '', '', '', '', '')#cxcpq-33770 end
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type :  #Modified by Srinivasan Dorairaj
    CattList = []
    
    quote_table = context.Quote.QuoteTables['QT_Product_Categories']
    quote_table.Rows.Clear()

    for num, i in enumerate(context.Quote.GetAllItems(), start=1):
        pCat = i['QI_Category']
        #Log.Write("Cat" +str(pCat))
        if i.IsOptional == False and  i.ProductSystemId != 'RQ_Mandatory_Charges_cpq' :
            if num == 1 or ( i['QI_Category'] not in CattList ):
                Trace.Write("NewProdCategory---"+str(i['QI_Category']))
                newRow = quote_table.AddNewRow()
                CattList.append(i['QI_Category'])
                Trace.Write("list" +str(CattList))
                newRow['Product_Category_Rows'] = i['QI_Category']
                newRow['Sell_Price'] = i.NetPrice
                newRow['Discount_Amount'] = (i.DiscountAmount)*(i.Quantity)
                if i["QI_Recommended_Sell_Price"] > 0:
                    newRow['Recommended_Price'] = i["QI_Recommended_Sell_Price"]
                newRow['List_Price'] = i["QI_List_Price_Total"]
                newRow['Cost'] = i["QI_TOTAL_QUOTE_COST"]
                if i['QI_INFLATION_AMOUNT'] > 0:
                    newRow['Inflation_Factor'] = i['QI_INFLATION_AMOUNT']
                newRow['Warranty'] = i["QI_Warranty_Amt"]
                if i['QI_FREIGHT_AMOUNT'] > 0:
                    newRow['Freight'] = i['QI_FREIGHT_AMOUNT']
                if i['QI_hours'] > 0:
                    newRow['Hours'] = i['QI_hours']
                
                newRow['Discount_'] = i.DiscountPercent
                newRow['CSPA_DIscount_Amount'] = i["QI_CSPA_DiscountAmount"]
                if i["QI_List_Price_Total"] > 0 and newRow['CSPA_DIscount_Amount'] > 0:
                    Trace.Write("Yes")
                    newRow['CSPA_Discount_'] =newRow['CSPA_DIscount_Amount'] /float(i["QI_List_Price_Total"])*100
                if (i.NetPrice) > 0  :
                    newRow['Gross_Margin_'] = (newRow['Sell_Price'] -newRow['Cost'])/newRow['Sell_Price'] * 100
                    Trace.Write("Gross" +str(newRow['Gross_Margin_']))
                '''if (i.NetPrice) > 0 and i["QI_WTW_Margin"] > 0:
                    newRow['W2W_Margin_'] = float(i['QI_WTW_Margin']) / float(i.NetPrice) * 100'''
            
            else:
                for r in quote_table.Rows:
                    if r['Product_Category_Rows'] == i['QI_Category']:
                        Log.Write("ElseProdCategory---"+str(i['QI_Category']))
                        Trace.Write("True")
                        r['Sell_Price'] = r['Sell_Price'] + i.NetPrice
                        Log.Write("Sell price" +str(r['Sell_Price']))
                        if i["QI_Recommended_Sell_Price"]!=None:
                            r['Recommended_Price'] = r['Recommended_Price'] + i["QI_Recommended_Sell_Price"]
                        r['Discount_Amount'] = r['Discount_Amount'] + ((i.DiscountAmount)*(i.Quantity))
                        if i["QI_List_Price_Total"]!=None:
                            r['List_Price'] = r['List_Price'] + i["QI_List_Price_Total"]
                        if i["QI_TOTAL_QUOTE_COST"]!=None:
                            r['Cost'] = r['Cost'] + i["QI_TOTAL_QUOTE_COST"]
                        if i["QI_INFLATION_AMOUNT"]!=None:
                            r['Inflation_Factor'] = r['Inflation_Factor']+ i['QI_INFLATION_AMOUNT']
                        if i["QI_Warranty_Amt"]!=None:
                            r['Warranty'] = r['Warranty']+ i['QI_Warranty_Amt']
                        if i["QI_FREIGHT_AMOUNT"]!=None:
                            r['Freight'] = r['Freight']+ i['QI_FREIGHT_AMOUNT']
                        r['Hours'] = r['Hours'] + i['QI_hours']
                    
                        if r['Recommended_Price'] != 0 :
                            r['Discount_'] = (r['Discount_Amount']/r['Recommended_Price'])*100 #changed by Sumandrita
                        if i["QI_CSPA_DiscountAmount"]!=None:
                            r['CSPA_DIscount_Amount'] = r['CSPA_DIscount_Amount'] + i["QI_CSPA_DiscountAmount"]
                        if (r['Sell_Price'] + i.NetPrice) > 0 :
                            r['Gross_Margin_'] = ((r['Sell_Price']- r['Cost'])/ r['Sell_Price'] ) * 100
                            Trace.Write("Gross" +str(r['Gross_Margin_']))
                        if r['List_Price'] > 0 :
                            r['CSPA_Discount_'] = (r['CSPA_DIscount_Amount']/float(r['List_Price']))*100

                        if r['Sell_Price'] > 0 and i["QI_WTW_COST"] > 0:
                            r["WTW_Cost"] = r["WTW_Cost"] + i["QI_WTW_COST"]
                        
                        '''if r['Sell_Price'] > 0 and i["QI_WTW_Margin"] != 0:
                            r['W2W_Margin_'] = (r['Sell_Price'] - r["WTW_Cost"]) / r['Sell_Price'] * 100'''


"""quote_table1 = context.Quote.QuoteTables['QT_Product_Categories']
#quote_table2 = context.Quote.QuoteTables['QT_Product_Categories'].Rows

for row in quote_table1.Rows:
    DelRow = 0
    if row['Product_Category_Rows'] == '' or row['Product_Category_Rows'] is None:
        Trace.Write("DeleteProdCategory---"+str(row['Product_Category_Rows']))
        DelRow = row.Id
        quote_table1.DeleteRow(DelRow)"""
