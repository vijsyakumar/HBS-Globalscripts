# -----------------------------------------------------------------------------
#            Change History Log
# -----------------------------------------------------------------------------
# Description:
# This script is used for third party pricing
# -----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
# -----------------------------------------------------------------------------
# 09/27/2022    AshutoshKumar Mishra       0             -Initial Version
# 10/18/2022    Ishika Bhattacharya        2             -Incorporated Translation
#                                                        -Replaced Hardcodings
# 11/04/2022	Dhruv Bhatnagar   	   	   3		     -SQL translation,Transacrtion type
#												          check implemented
# 11/07/2022    Aditi Sharma               4             -Change to add calculations for third party that are adhoc
# 11/23/2022	Dhruv Bhatnagar			  19			 -Third Party Pricing Flag added
# 01/14/2023   Aditi Sharma                              -Added condition check for Preparing status
# 01/24/2023   Aditi Sharma                              -Added condition for calculation recommended price and sell prices
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS  # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
b_mtd = context.Quote.GetCustomField('CF_Buying_Method').Value
quote_status_ID = context.Quote.StatusId

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type and quote_status_ID==32:  #Modified by Dhruv #Modified by Aditi 14th Jan
    lc_Third_Party = GM_TRANSLATIONS.GetText('000065', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika

    lv_opp_cntry = context.Quote.GetCustomField("CF_Country").Value
    lv_quot_crncy = context.Quote.GetCustomField("CF_Quote_Currency").Value
    get_cat_fact = 0.0
    for i in context.Quote.GetAllItems():
        # if i['QI_Product_Type'] == 'Third Party':   #Commented by Ishika
        if ( i['QI_Product_Type'] == lc_Third_Party ) and ( i.VCItemPricingPayload is None ):# Modified by Dhruv
            ex_rate = i['QI_Exchange_Rate']
            #Log.Info('31--->'+str(i.PartNumber))
            lv_price = SqlHelper.GetFirst(" SELECT DISTINCT * FROM CT_TP_PRICE WHERE PartNumber = '{0}' and CountryCode = '{1}'".format(i.PartNumber, lv_opp_cntry)) #Modified by Dhruv
            if lv_price:
                # a = 1
                # i['QI_PROD_CATEGORY'] = 'Third Party'   # Commented by Ishika
                i['QI_PROD_CATEGORY'] = lc_Third_Party  # Added by Ishika
                get_selected_category = SqlHelper.GetFirst("SELECT FACTOR FROM CT_CATEGORY_FACTOR where CATEGORY='{}'".format(lc_Third_Party))
                get_cat_fact = get_selected_category.FACTOR
                i['QI_List_Price'] = float(lv_price.Cost)* get_cat_fact * i['QI_Exchange_Rate']
                i['QI_List_Price_Total'] = i['QI_List_Price'] * i.Quantity
                if b_mtd.lower() != "buy honeywell hon to hon" or i["QI_SpecialPriceV"]==str(0) or i["QI_SpecialPriceV"] is None: #Added by Aditi 24Jan2023
                    i['QI_Recommended_Unit_Sell_Price'] = i['QI_List_Price']
                    i["QI_Recommended_Sell_Price"] = i['QI_Recommended_Unit_Sell_Price'] * (i.Quantity)
                    i['QI_Unit_Sell_Price'] = i['QI_List_Price'] - i.DiscountAmount
                    i.NetPrice = i['QI_Unit_Sell_Price'] * (i.Quantity)
                else:
                    i['QI_Recommended_Unit_Sell_Price'] = float(i["QI_SpecialPriceV"]) #Added by Aditi 24Jan2023
                    #Trace.Write("TPH: "+str(i["QI_SpecialPriceV"]))
                    i["QI_Recommended_Sell_Price"] = i['QI_Recommended_Unit_Sell_Price'] * (i.Quantity)
                    i['QI_Unit_Sell_Price'] = i["QI_Recommended_Sell_Price"] - i.DiscountAmount
                    i.NetPrice = i['QI_Unit_Sell_Price'] * (i.Quantity)
                """if i.DiscountAmount!=0:
                    #i.DiscountPercent = float(i['QI_Recommended_Unit_Sell_Price']) - float(i.DiscountAmount)/float(i['QI_Recommended_Unit_Sell_Price'])
                    i.DiscountPercent = float(i.DiscountAmount) / float(i['QI_List_Price']) * 100
                    Log.Write("TPif1-DiscountPercent: "+str(i.DiscountPercent)+" "+str(i.DiscountAmount))
                elif i.DiscountPercent!=0:
                    i.DiscountAmount = float(i['QI_List_Price'] ) * float(i.DiscountPercent) /100
                    Log.Write("TPelif1-Discountamount: "+str(i.DiscountPercent)+" "+str(i.DiscountAmount))"""
                i['QI_Unit_Cost_Base_Currency'] = float(lv_price.Cost)
                i['QI_Cost_Currency'] = lv_price.Currency
                if i['QI_Unit_Cost_Base_Currency']:
                    if i['QI_Exchange_Rate'] == 0:
                        i['QI_TransferCost'] = i['QI_Unit_Cost_Base_Currency'] * 1
                    else :
                        i['QI_TransferCost'] = i['QI_Unit_Cost_Base_Currency'] * i['QI_Exchange_Rate']
                    i['QI_Total_Cost'] = i['QI_TransferCost'] * (i.Quantity)
                i['QI_TOTAL_QUOTE_COST'] = i['QI_Total_Cost'] + i['QI_FREIGHT_AMOUNT'] + i['QI_Warranty_Amt'] + i['QI_CUSTOMS_AMOUNT']
                Log.Info('QI_TOTAL_QUOTE_COST-->'+str(i['QI_TOTAL_QUOTE_COST']))
                i['QI_WTW_Margin'] = 0
                i['QI_WTW_COST'] = 0
                i['QI_UNIT_WTW_COST'] = 0
                #i['QI_Unit_Sell_Price'] = i['QI_List_Price'] - i.DiscountAmount
                i.NetPrice = i['QI_Unit_Sell_Price'] * (i.Quantity)
                i['QI_Final_Sell_Price'] = i.NetPrice
                if (i.NetPrice is not None) and (i['QI_TOTAL_QUOTE_COST'] is not None):
                    i['QI_MARGIN_AMOUNT'] = i.NetPrice - i['QI_TOTAL_QUOTE_COST']
                    #if (sell_price > 0) and (i['QI_TOTAL_QUOTE_COST'] > 0):
                if i.NetPrice > 0:
                    i['QI_MARGIN_PERCENTAGE'] = i['QI_MARGIN_AMOUNT'] / i.NetPrice * 100
            
            #added by Aditi 7 Nov
            else:
                if i['QI_List_Price'] and i["QI_Recommended_Sell_Price"]:
                    get_selected_category = SqlHelper.GetFirst("SELECT FACTOR FROM CT_CATEGORY_FACTOR where CATEGORY='{}'".format(lc_Third_Party))
                    get_cat_fact = get_selected_category.FACTOR
                    i['QI_List_Price'] = i['QI_TransferCost']*get_cat_fact
                    i['QI_List_Price_Total'] = i['QI_List_Price'] * (i.Quantity)
                    if b_mtd.lower() != "buy honeywell hon to hon" or i["QI_SpecialPriceV"]==str(0) or i["QI_SpecialPriceV"] is None: #Added by Aditi 24Jan2023
                        i['QI_Recommended_Unit_Sell_Price'] = i['QI_List_Price']
                        i["QI_Recommended_Sell_Price"] = i['QI_Recommended_Unit_Sell_Price'] * (i.Quantity)
                        i['QI_Unit_Sell_Price'] = i['QI_List_Price'] - i.DiscountAmount
                        i.NetPrice = i['QI_Unit_Sell_Price'] * (i.Quantity)
                    else:
                        i['QI_Recommended_Unit_Sell_Price'] = float(i["QI_SpecialPriceV"]) #Added by Aditi 24Jan2023
                        #Trace.Write("TPH: "+str(i["QI_SpecialPriceV"]))
                        i["QI_Recommended_Sell_Price"] = i['QI_Recommended_Unit_Sell_Price'] * (i.Quantity)
                        i['QI_Unit_Sell_Price'] = i["QI_Recommended_Sell_Price"] - i.DiscountAmount
                        i.NetPrice = i['QI_Unit_Sell_Price'] * (i.Quantity)
                    '''if i.DiscountAmount!=0:
                        #i.DiscountPercent = float(i['QI_Recommended_Unit_Sell_Price']) - float(i.DiscountAmount)/float(i['QI_Recommended_Unit_Sell_Price'])
                        i.DiscountPercent = float(i.DiscountAmount) / float(i['QI_List_Price'])  * 100
                        Log.Write("if2: "+str(i.DiscountPercent))
                    elif i.DiscountPercent!=0:
                        i.DiscountAmount = float(i['QI_List_Price']) * float(i.DiscountPercent) / 100
                        Log.Write("elif2: "+str(i.DiscountPercent))
                    Trace.Write(str(i.DiscountPercent)+" "+str(i.DiscountAmount))'''
                    #i['QI_Unit_Sell_Price'] = i['QI_List_Price'] - i.DiscountAmount
                    i.NetPrice = i['QI_Unit_Sell_Price'] * (i.Quantity)
                    i['QI_Final_Sell_Price'] = i.NetPrice
                    if i['QI_Total_Cost']:
                        if i['QI_FREIGHT_AMOUNT'] == "":
                            i['QI_FREIGHT_AMOUNT'] = 0
                        if i['QI_Warranty_Amt'] == "":
                            i['QI_Warranty_Amt'] = 0
                        if i['QI_CUSTOMS_AMOUNT'] == "":
                            i['QI_CUSTOMS_AMOUNT'] = 0

                        i['QI_TOTAL_QUOTE_COST'] = i['QI_Total_Cost'] + i['QI_FREIGHT_AMOUNT'] + i['QI_Warranty_Amt'] + i['QI_CUSTOMS_AMOUNT']
                    i['QI_WTW_Margin'] = 0
                    i['QI_WTW_COST'] = 0
                    i['QI_UNIT_WTW_COST'] = 0
                    #i['QI_Unit_Sell_Price'] = i['QI_List_Price'] - i.DiscountAmount
                    i.NetPrice = i['QI_Unit_Sell_Price'] * (i.Quantity)
                    i['QI_Final_Sell_Price'] = i.NetPrice
                    if (i.NetPrice is not None) and (i['QI_TOTAL_QUOTE_COST'] is not None):
                        i['QI_MARGIN_AMOUNT'] = i.NetPrice - i['QI_TOTAL_QUOTE_COST']
                    Log.Write('94--QI_TOTAL_QUOTE_COST-->'+str(i['QI_TOTAL_QUOTE_COST']))
                    #if (sell_price > 0) and (i['QI_TOTAL_QUOTE_COST'] > 0):
                    if i.NetPrice > 0:
                        i['QI_MARGIN_PERCENTAGE'] = i['QI_MARGIN_AMOUNT'] / i.NetPrice * 100
                    if i.Description == "Adhoc Product":
                        i.Description = i['QI_Description']
                    if i.Description == "WriteIn" or i.Description == "Write-In":
                        i.Description = i['QI_Description']
                        i.PartNumber = i['QI_Description']