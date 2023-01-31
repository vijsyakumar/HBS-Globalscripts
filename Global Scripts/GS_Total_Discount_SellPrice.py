#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for total sell price and discount % calculation at the header
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 9/1/2022      Vijay jaganathan           0             -Initial Version
# 10/18/2022    Ishika Bhattacharya        18            -Incorporated Translation
#10/20/2022     Sumandrita Moitra          19            - put a condition for eliminate optional products from calculation
#10/29/2022     Sumandrita Moitra          20            - put a condition to eliminate Write-in parent  item from calculation
# 11/03/2022    Sumandrita Moitra          21            -Replaced lc_op_type with lc_trans_type
#                                                   to remove dependency on multiple opp types
#11/04/2022     Sumandrita                          event Changed
# 01/14/2023   Aditi Sharma                         -Added condition check for Preparing status
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User) # Added by Ishika
#lc_op_type = GM_TRANSLATIONS.GetText('000024', lv_LanguageKey, '', '', '', '', '') # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')
quote_status_ID = context.Quote.StatusId

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type and quote_status_ID==32: # Added by Ishika #Modified by Aditi 14th Jan

    totalSellPrice = 0
    recommendedUnitSellPriceSum = 0
    discAmtSum = 0
    actualDiscPer = 0
    totalRecommendedPrice = 0

    Dis_per = context.Quote.GetCustomField('CF_Total_Discount_Percent').Value
    sel_per = context.Quote.GetCustomField('CF_Total_Sell_Price').Value
    a = context.Quote.GetAllItems()
    for i in a:
        
        #Log.Write("Is Optional-->" +str(i.IsOptional) + "Product Type" +str(i['QI_Product_Type']))
        if i.IsOptional == False and i['QI_Product_Type'] != 'Write-In' and i['QI_Product_Type'] != '' and i.ProductSystemId != 'RQ_Mandatory_Charges_cpq':
            discAmtSum += (i.DiscountAmount * i.Quantity)
            totalSellPrice += i.NetPrice
            #Log.Write("Total sell Price 1--->" +str(totalSellPrice))
            if i['QI_Recommended_Sell_Price']:
                totalRecommendedPrice += float(i['QI_Recommended_Sell_Price'])
            

    if totalRecommendedPrice:
        actualDiscPer = '%.2f' % ((discAmtSum / totalRecommendedPrice) * 100)
        Trace.Write('actual dis per:{}'.format(actualDiscPer))

    totalSellPrice = '%.2f' % totalSellPrice
    context.Quote.GetCustomField('CF_Total_Discount_Percent').Value = actualDiscPer
    context.Quote.GetCustomField('CF_Total_Sell_Price').Value = totalSellPrice
    Log.Write("Total sell Price 2--->" +str(totalSellPrice))
    