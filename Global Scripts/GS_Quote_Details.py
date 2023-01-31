#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for Quote Details table calculation, at quote level.
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 9/1/2022      Ishika Bhattacharya        0             -Initial Version
# 10/18/2022    Ishika Bhattacharya        35            -Replaced Hardcodings
#                                                        -Incorporated Translation
#
#10/20/2022     Sumandrita Moitra          36            - put a condition to eliminate optional products from calculation
##10/29/2022     Sumandrita Moitra          36            - put a condition to eliminate Write-in parent  item from calculation
# 01/20/2023     Aditi Sharma                             -Added sell price check for rounding issue
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS    # Added by Ishika
#ScriptExecutor.Execute("GS_Parent_Child")
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User) # Added by Ishika
lc_op_type = GM_TRANSLATIONS.GetText('000024', lv_LanguageKey, '', '', '', '', '') # Added by Ishika
lc_mand_charges = GM_TRANSLATIONS.GetText('000213', lv_LanguageKey, '', '', '', '', '')

def sellPrice_check():
    total_Sell_Price = 0
    discAmount_difference = 0
    if context.Quote.GetCustomField('CF_SellPrice_Value_Check').Value != '':
        sellP_check = float(context.Quote.GetCustomField('CF_SellPrice_Value_Check').Value)
        for i in context.Quote.GetAllItems():
            if i.ProductSystemId != 'RQ_Mandatory_Charges_cpq' and i.IsOptional == False and i['QI_Product_Type'] != 'Write-In' and i['QI_Product_Type'] != '':
                total_Sell_Price+=i.NetPrice
        if total_Sell_Price!=sellP_check:
            discAmount_difference = sellP_check - total_Sell_Price
            Log.Write("SPCheck----DiscDifference: "+str(discAmount_difference))
        Log.Write("SPCheck----SellPriceCheck: "+str(sellP_check))
        Log.Write("SPCheck----TotalSellPrice: "+str(total_Sell_Price))
        
        a=context.Quote.GetAllItems()
        n=len(context.Quote.GetAllItems())-1
        a1=a[n]
        #calculation of discount amount for last product
        Log.Write("SPCheck----LastProductDisc1: "+str(a1.DiscountAmount))
        a1.DiscountAmount = a1.DiscountAmount - discAmount_difference
        Log.Write("SPCheck----LastProductDisc2: "+str(a1.DiscountAmount))
        #calculation of discount percent for last product
        Log.Write("SPCheck----LastProductDiscPer1: "+str(a1.DiscountPercent))
        if a1['QI_Recommended_Sell_Price'] > 0:
            a1.DiscountPercent = (a1.DiscountAmount/a1['QI_Recommended_Sell_Price'])*100
        Log.Write("SPCheck----LastProductDiscPer2: "+str(a1.DiscountPercent))
        #calculation of unit sell price for last product
        Log.Write("SPCheck----LastProductUnitPrice1: "+str(a1["QI_Unit_Sell_Price"]))
        a1["QI_Unit_Sell_Price"] = a1["QI_Recommended_Unit_Sell_Price"] - a1.DiscountAmount
        Log.Write("SPCheck----LastProductUnitPrice2: "+str(a1["QI_Unit_Sell_Price"]))
        #calculation of total net price for last product
        Log.Write("SPCheck----LastProductNetPrice1: "+str(a1.NetPrice))
        a1.NetPrice = (a1["QI_Recommended_Unit_Sell_Price"] - a1.DiscountAmount) * a1.Quantity
        Log.Write("SPCheck----LastProductNetPrice2: "+str(a1.NetPrice))
    #initializing the custom field
    context.Quote.GetCustomField('CF_SellPrice_Value_Check').Value = ''


if (context.Quote.GetCustomField('CF_Opportunity_Type').Value) == lc_op_type: # Added by Ishika
    sellPrice_check()
    a = context.Quote.GetAllItems()
    totalListPrice = 0
    totalSellPrice = 0
    actualDiscPer = 0
    totalCost = 0
    totalDiscAmt = 0
    totalMarginPerc = 0
    totalDiscPerc = 0
    totalMarginAmt = 0
    totalCSPAamount = 0
    totalCSPAdiscountPer = 0
    totalRecommendedPrice = 0
    totalRecommendedDiscPerc = 0
    recommendedUnitSellPriceSum = 0
    discAmtSum = 0
    totalMarginPercentage = 0
    totalUnitListPrice = 0

    for i in a:
        if i.IsOptional == False and i['QI_Product_Type'] != 'Write-In' and i['QI_Product_Type'] != '' and  i.ProductSystemId != 'RQ_Mandatory_Charges_cpq' :
            Trace.Write('qi sell price:{}'.format(i['QI_Sell_Price']))
            # discAmtSum += i.DiscountAmount
            if i["QI_List_Price"]:
                totalUnitListPrice += i["QI_List_Price"]
                Trace.Write("List price" +str(totalUnitListPrice))
                if i['QI_Recommended_Unit_Sell_Price']:
                    recommendedUnitSellPriceSum += float(i['QI_Recommended_Unit_Sell_Price'])

            if i['QI_Recommended_Sell_Price']:
                totalRecommendedPrice += float(i['QI_Recommended_Sell_Price'])
            if i['QI_Recommended_DiscountP']:
                totalRecommendedDiscPerc += float(i['QI_Recommended_DiscountP'])
            if i['QI_CSPA_DiscountAmount'] and i['QI_SpecialPriceP']:
                totalCSPAamount += float((i['QI_CSPA_DiscountAmount'] * i.Quantity))
                totalCSPAdiscountPer += float(i['QI_SpecialPriceP'])
            if i['QI_MARGIN_PERCENTAGE']!=None and i['QI_MARGIN_AMOUNT']!=None:
                totalListPrice += i["QI_List_Price_Total"]
                totalSellPrice += i.NetPrice
                Trace.Write("total sell price " +str(totalSellPrice))
                totalDiscAmt += (i.DiscountAmount * i.Quantity)
                totalMarginPerc += i['QI_MARGIN_PERCENTAGE']
                totalDiscPerc += i.DiscountPercent
                totalMarginAmt += i['QI_MARGIN_AMOUNT']
            if i["QI_TOTAL_QUOTE_COST"] != None:
                totalCost += i["QI_TOTAL_QUOTE_COST"]

    if totalSellPrice:
        totalMarginPercentage = (totalMarginAmt / totalSellPrice) * 100
        Trace.Write("total sell price 1 " +str(totalSellPrice))
        Trace.Write("True1")

    if totalRecommendedPrice:
        Trace.Write("Y")
        actualDiscPer = (totalDiscAmt / totalRecommendedPrice) * 100
        Trace.Write("True2")

    if totalUnitListPrice and totalListPrice:
        totalCSPAdiscountPer = (totalCSPAamount / totalListPrice) * 100
        Trace.Write("CSPA" +str(totalCSPAdiscountPer))
    #changes start hear srinivas
    discper = ''
    quote_table_financial = context.Quote.QuoteTables['Financial_Summary'].Rows
    for rowi in quote_table_financial:
        if rowi['Summary'] == 'Maximum Discount % Recommended':
            discper = rowi['Quote_Currency']
    if discper != '':
        percentage = discper.replace('%','')
        RecommendedDiscPerc = float(percentage)
    else:
        RecommendedDiscPerc = totalRecommendedDiscPerc
    # Ends hear
    quote_table=context.Quote.QuoteTables['Quote_Details']
    quote_table.Rows.Clear()
    if len(a):
        newRow = quote_table.AddNewRow()
        newRow['Recommended_Price'] = totalRecommendedPrice
        newRow['QT_Total_List_Price'] = totalListPrice
        newRow['QT_Total_Discount_Amount'] = totalDiscAmt
        newRow['QT_Total_Discount_Percent'] = actualDiscPer
        newRow['QT_Total_Sell_Price'] = totalSellPrice
        newRow['QT_Total_Cost'] = totalCost
        if i['QI_MARGIN_PERCENTAGE']!=None and i['QI_MARGIN_AMOUNT']!=None:
            newRow['QT_Total_Margin_Amount'] = totalMarginAmt
            newRow['QT_Total_Margin_Percent'] = totalMarginPercentage
        newRow['CSPA_Discount_Amount'] = totalCSPAamount
        newRow['CSPA_Discount_'] = totalCSPAdiscountPer
        newRow['Recommended_Discount_'] = RecommendedDiscPerc