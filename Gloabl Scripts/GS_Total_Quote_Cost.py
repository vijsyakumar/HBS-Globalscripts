#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for calculating the total quote cost
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 08/18/2022    krishna chaitanya          0             -Initial Version
# 10/18/2022    Ishika Bhattacharya        6             -Incorporated Translation
# 11/04/2022	Dhruv				   	  17		     -SQL translation,Transacrtion type
#												          check implemented
# 01/14/2023   Aditi Sharma                              -Added condition check for Preparing status
# 01/19/2023   Aditi Sharma                              -Removed all rounding
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)   # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
quote_status_ID = context.Quote.StatusId

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type and quote_status_ID==32:  #Modified by Dhruv #Modified by Aditi 14th Jan
    for i in context.Quote.GetAllItems():
        #Trace.Write("----=====")
        product_type = i.ProductTypeName
        if i['QI_INFLATION_AMOUNT'] is not None:
            inflation_amount = i['QI_INFLATION_AMOUNT']
            #Trace.Write("inflation_amount====="+str(inflation_amount))
        else:
            inflation_amount = 0.00
            #Trace.Write("elseinflation_amount====="+str(inflation_amount))

        if i['QI_Total_Cost'] is not None:
            total_cost = i['QI_Total_Cost']
            #Trace.Write("total_cost====="+str(total_cost))
        else:
            total_cost = 0.00
            #Trace.Write("elsetotal_cost====="+str(total_cost))

        if i['QI_FREIGHT_AMOUNT'] is not None:
            freight_amount = i['QI_FREIGHT_AMOUNT']
            #Trace.Write("freight_amount====="+str(freight_amount))
        else:
            freight_amount = 0.00
            #Trace.Write("elsefreight_amount====="+str(freight_amount))
        if i['QI_Warranty_P'] is not None:
            i['QI_Warranty_Amt'] = total_cost * i['QI_Warranty_P'] / 100
        if i['QI_Warranty_Amt'] is not None:
            warranty_amount = i['QI_Warranty_Amt']
            #Trace.Write("freight_amount====="+str(warranty_amount))
        else:
            warranty_amount = 0.00
            #Trace.Write("elsefreight_amount====="+str(warranty_amount))
        if i['QI_CUSTOMS_AMOUNT'] is not None:
            customs_amount = i['QI_CUSTOMS_AMOUNT']
            #Trace.Write("freight_amount====="+str(customs_amount))
        else:
            customs_amount = 0.00
            #Trace.Write("elsefreight_amount====="+str(customs_amount))
        if i.NetPrice is not None:
            sell_price = i.NetPrice
            #Trace.Write("sell_price-----"+str(sell_price)) 
        else:
            sell_price = 0.00
            #Trace.Write("elsesell_price-----"+str(sell_price)) 
        '''if i['QI_MARGIN_AMOUNT'] is not None:
            margin_amount = i['QI_MARGIN_AMOUNT']
            #Trace.Write("margin_amount-----"+str(margin_amount))
        else:
            margin_amount = 0.00
            #Trace.Write("elsemargin_amount-----"+str(margin_amount))
        '''

        if (inflation_amount is not None) and (total_cost is not None) and (freight_amount is not None) and (warranty_amount is not None) and (customs_amount is not None):

            Total_Quote_Cost = inflation_amount + total_cost + freight_amount + warranty_amount + customs_amount
            #Trace.Write("====="+str(Total_Quote_Cost))
            i['QI_TOTAL_QUOTE_COST'] = Total_Quote_Cost
            Log.Write(str(i['QI_TOTAL_QUOTE_COST']))

        if (i.NetPrice is not None) and (i['QI_TOTAL_QUOTE_COST'] is not None) and (i["QI_Recommended_Unit_Sell_Price"] is not None):
            Trace.Write("if-----")
            #i.NetPrice = (i["QI_Recommended_Unit_Sell_Price"] - (round(i.DiscountAmount,2))) * (i.Quantity)
            i.NetPrice = (i["QI_Recommended_Unit_Sell_Price"] - i.DiscountAmount) * (i.Quantity)
            i['QI_MARGIN_AMOUNT'] = i.NetPrice - i['QI_TOTAL_QUOTE_COST']
            Log.Write("MGAmountGS----"+str(i.NetPrice)+" "+str(i['QI_TOTAL_QUOTE_COST'])+" "+str(i['QI_MARGIN_AMOUNT'])+" "+str(i.PartNumber))
            
            #if (sell_price > 0) and (i['QI_TOTAL_QUOTE_COST'] > 0):
            if i.NetPrice > 0:
                i['QI_MARGIN_PERCENTAGE'] = i['QI_MARGIN_AMOUNT'] / i.NetPrice * 100
                Log.Write("MGPercentGS----"+str(i.NetPrice)+" "+str(i['QI_TOTAL_QUOTE_COST'])+" "+str(i['QI_MARGIN_PERCENTAGE'])+" "+str(i.PartNumber))
                