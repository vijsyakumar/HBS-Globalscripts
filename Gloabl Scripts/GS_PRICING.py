# -----------------------------------------------------------------------------
#			Change History Log
# -----------------------------------------------------------------------------
# Description:
# GS PRICING
# -----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
# -----------------------------------------------------------------------------
# 8/18/2022    Anil Poply            0          -initial version
# 11/5/2022    Ishika BHattacharya	  6	        -Replaced Hardcodings
#										        -Incorporated Translation
# 12/1/2022    Shweta Kandwal	      94        -Incorporated Translation
# 12/2/2022    Aditi Sharma           95        -Corrected the condition for ZDIS
# 12/2/2022    Aditi Sharma           96        -Removed LanguageKey filter from exchange rate query
# 12/2/2022    Aditi Sharma           97        -Corrected the exchange rate calculation, defined new method getExchRate()
# 12/2/2022    Aditi Sharma           98        -Replaced conditionRate by conditionValue
# 12/9/2022    Aditi Sharma           101       -Fixed Discount Amount rounding issue
# 01/12/2023   Karthik T              102       -Added Condirion before QI_SpecialPriceP assign
# 01/13/2023   Aditi Sharma           112       -Added condition check for Preparing status
# 01/19/2023   Aditi Sharma                     -Removed all rounding
# 01/23/2023   Aditi Sharma                     -Added pricing logic for ZHGS conditionType along with ZIFP
# 01/28/2023   Aditi Sharma                     -Added explicit overall calculation of special price
# -----------------------------------------------------------------------------

from Scripting.Quote import MessageLevel
import GM_TRANSLATIONS  # Added by krishna
b_mtd = context.Quote.GetCustomField('CF_Buying_Method').Value
#Trace.Write("BMTD: "+str(b_mtd))
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by krishna
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
lc_GSA = GM_TRANSLATIONS.GetText('000122', lv_LanguageKey, '', '', '', '', '')
lc_ZIFP = GM_TRANSLATIONS.GetText('000230', lv_LanguageKey, '', '', '', '', '')
gsa_flag = False
transaction_type = context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value
quote_status_ID = context.Quote.StatusId  #Added by Aditi 13th Jan
Log.Info('29--pricing call')
def getExchRate(from_curr,to_curr): #Added by Aditi 2nd Dec 2022
    exr = 1
    if from_curr == to_curr:
        exr = 1
    else:
        query_desc = SqlHelper.GetList("SELECT TOP 1 * FROM CT_EXCHANGE_RATE  WHERE FROM_CURRENCY = '" + str(from_curr) + "' AND TO_CURRENCY = '" + str(to_curr) + "' ORDER BY [Date] Desc")
        if query_desc:
            for qry in query_desc:
                #exr = round((qry.RATE), 2)
                exr = qry.RATE
    return exr

def calculateMargin(): #Added by Aditi 6th Jan
    lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)   # Added by Ishika
    lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
    if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type and quote_status_ID==32:  #Modified by Dhruv  #Modified by Aditi 13th Jan
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
                #Log.Write(str(i['QI_TOTAL_QUOTE_COST']))

            if (i.NetPrice is not None) and (i['QI_TOTAL_QUOTE_COST'] is not None) and (i["QI_Recommended_Unit_Sell_Price"] is not None):
                #Trace.Write("if-----")
                #i.NetPrice = (i["QI_Recommended_Unit_Sell_Price"] - (round(i.DiscountAmount,2))) * (i.Quantity)
                i.NetPrice = (i["QI_Recommended_Unit_Sell_Price"] - i.DiscountAmount) * (i.Quantity)
                i['QI_MARGIN_AMOUNT'] = i.NetPrice - i['QI_TOTAL_QUOTE_COST']
                #Log.Write("MGAmountGS-Pricing----"+str(i.NetPrice)+" "+str(i['QI_TOTAL_QUOTE_COST'])+" "+str(i['QI_MARGIN_AMOUNT'])+" "+str(i.PartNumber))

                #if (sell_price > 0) and (i['QI_TOTAL_QUOTE_COST'] > 0):
                if i.NetPrice > 0:
                    i['QI_MARGIN_PERCENTAGE'] = i['QI_MARGIN_AMOUNT'] / i.NetPrice * 100
                    #Log.Write("MGPercentGS-Pricing----"+str(i.NetPrice)+" "+str(i['QI_TOTAL_QUOTE_COST'])+" "+str(i['QI_MARGIN_PERCENTAGE'])+" "+str(i.PartNumber))

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type and quote_status_ID==32:  # Added by ishika
    Log.Write("BeforeRendering-Script Execution----")
    lc_Honeywell_hardware = GM_TRANSLATIONS.GetText('000027', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
    lc_Honeywell_Labor = GM_TRANSLATIONS.GetText('000118', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
    lc_FP_Material = GM_TRANSLATIONS.GetText('000020', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
    lc_Labor = GM_TRANSLATIONS.GetText('000040', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
    lc_TP = GM_TRANSLATIONS.GetText('000065', lv_LanguageKey, '', '', '', '', '') #added by Shweta
    lc_True = GM_TRANSLATIONS.GetText('000048', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
    lc_False = GM_TRANSLATIONS.GetText('000068', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
    lc_null = GM_TRANSLATIONS.GetText('000102', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
    lc_ZP00 = GM_TRANSLATIONS.GetText('000104', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
    lc_ZCSP = GM_TRANSLATIONS.GetText('000103', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
    lc_ZDIS = GM_TRANSLATIONS.GetText('000105', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
    lc_ZHGS = GM_TRANSLATIONS.GetText('000106', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
    lc_None = GM_TRANSLATIONS.GetText('000108', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
    lc_C = GM_TRANSLATIONS.GetText('000101', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
    lc_S = GM_TRANSLATIONS.GetText('000030', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
    #if transaction_type == 'RQ': #Commented by ishika
    # transaction_type = 'RQ'
    a = 0
    special_bmethods = []

    # valid_prod_types = ['Honeywell Hardware', 'Honeywell Labor', 'First Party Material', 'Labor']
    valid_prod_types = [lc_Honeywell_hardware, lc_Honeywell_Labor, lc_FP_Material, lc_Labor, lc_TP]
    special_query = SqlHelper.GetList("SELECT * FROM CT_BUYING_METHODS WHERE SPECIAL_PRICING='Y'")

    for sp_row in special_query:
        special_bmethods.append(sp_row.BUYING_METHOD)

    #Trace.Write('buying methods:{}'.format(special_bmethods))

    buying_method = context.Quote.GetCustomField('CF_Buying_Method').Value
    #Trace.Write('CF_SPECIAL_PRICING value:{}'.format(buying_method))

    if buying_method in special_bmethods:
        #context.Quote.GetCustomField('CF_SPECIAL_PRICING').Value = 'True'  #Commented by ishika
        context.Quote.GetCustomField('CF_SPECIAL_PRICING').Value = lc_True  #Added by Ishika
    else:
        #context.Quote.GetCustomField('CF_SPECIAL_PRICING').Value = 'False'  #Commented by ishika
        context.Quote.GetCustomField('CF_SPECIAL_PRICING').Value = lc_False #Added by Ishika

    quote_currency = context.Quote.GetCustomField('CF_Quote_Currency').Value

    lt_partners = context.Quote.GetInvolvedParties()
    flag_buyhoneywell = ''
    for ls_partner in lt_partners:
        #if ('C' in str(ls_partner.ExternalId)) or ('S' in str(ls_partner.ExternalId)):    #Commented by ishika
        if (lc_C in str(ls_partner.ExternalId)) or (lc_S in str(ls_partner.ExternalId)):   #Added by ishika
            # flag_buyhoneywell = 'True'  #Commented by ishika
            flag_buyhoneywell = lc_True  #Added by Ishika
            # i["QI_SpecialPricingFlag"] = 'True'

    AllQuotes = context.Quote.GetAllItems()
    for i in AllQuotes:
        condition_type = []
        if ( ( i.ProductTypeName in valid_prod_types ) and (i.VCItemPricingPayload is not None) ):
            quote_currency = context.Quote.GetCustomField("CF_Quote_Currency").Value
            #commented by Aditi 2nd Dec
            #base_currency = i['QI_Cost_Currency']
            # quote_currency = i['QI_TransferCost']
            '''query_desc = SqlHelper.GetList("SELECT TOP 1 * FROM CT_EXCHANGE_RATE  WHERE FROM_CURRENCY = '" + str(
                base_currency) + "' AND TO_CURRENCY = '" + str(quote_currency) + "' ORDER BY [Date] Desc")'''   #Commented by ishika
            #query_desc = SqlHelper.GetList("SELECT TOP 1 * FROM CT_EXCHANGE_RATE  WHERE FROM_CURRENCY = '" + str(base_currency) + "' AND TO_CURRENCY = '" + str(quote_currency) + "' ORDER BY [Date] Desc")  #Added by ishika
            #if query_desc:
                #for qry in query_desc:
                    #a = round((qry.RATE), 2)

            k = i.VCItemPricingPayload.Conditions
            # lv_specialPrice = 'False' #Commented by ishika
            lv_specialPrice = lc_False  # Added by Ishika
            lv_speicalPriceV = ''
            lv_speicalPriceP = ''
            lv_ListPrice = ''
            lv_csp = ''
            lv_discount = ' '
            i["QI_List_Price"] = 0
            i["QI_List_Price_Total"] = 0
            i["QI_CSP"] = 0
            i["QI_SpecialPriceV"] = 0
            i["QI_CSPA_DiscountAmount"] = 0
            if b_mtd.lower() != "buy honeywell hon to hon":
                i["QI_SpecialPriceP"] = str(0)
            i["QI_DiscountP"] = str(0)
            i["QI_Recommended_DiscountP"] = str(0)
            i["QI_Recommended_Discount"] = 0
            i["QI_Recommended_Unit_Sell_Price"] = 0
            i["QI_Recommended_Sell_Price"] = 0
            condition_type = [j.ConditionType for j in k]
            Trace.Write("list" +str(i.PartNumber)+" "+str(condition_type))
            for j in k:
                #condition_type.append(j.ConditionType)
                #Trace.Write("list" + str(condition_type))
                '''if j.ConditionType != 'null' and float(j.ConditionRate) != 0 and float(
                        j.ConditionValue) != 0 and j.ConditionTypeDescription != '' and ('ZCSP' not in condition_type):'''  #Commneted by ishika
                if j.ConditionType != lc_null and float(j.ConditionRate) != 0 and float(j.ConditionValue) != 0 and j.ConditionTypeDescription != '' and (lc_ZCSP not in condition_type) and ((lc_ZDIS in condition_type) or (lc_ZHGS in condition_type) or (lc_ZIFP in condition_type)): # Added by ishika
                    #Trace.Write("True")
                    #if j.ConditionType == 'ZP00':  #Commented by ishika
                    if j.ConditionType == lc_ZP00: #Added by ishika
                        #ex_rate = getExchRate(j.ConditionCurrency,quote_currency)
                        i["QI_List_Price"] = float(j.ConditionValue)/i.Quantity #float(j.ConditionRate) * ex_rate
                        i["QI_List_Price_Total"] = float(j.ConditionValue) #float(j.ConditionRate) * ex_rate * i.Quantity
                        # Trace.Write("exrate"+str(i["QI_Exchange_Rate"]))
                        # Trace.Write("Unit List Price "+str(i["QI_List_Price"]))
                        # Trace.Write("List Price "+str(i["QI_List_Price_Total"]))
                        lv_ListPrice = float(j.ConditionValue)/i.Quantity
                    '''if j.ConditionType == 'ZCSP':
                        i["QI_CSP"] = j.ConditionValue
                        i["QI_SpecialPriceV"] = i["QI_List_Price"]-float(j.ConditionValue)
                        #Trace.Write("gh" +str(i["QI_SpecialPriceV"]))
                        lv_price = j.ConditionValue'''
                    # lv_specialPrice ='True'
                    # lv_csp = 'True'
                    #if j.ConditionType == 'ZDIS':  #Commented by ishika
                    if j.ConditionType == lc_ZDIS and not (lc_ZHGS in condition_type and lc_GSA.lower() in b_mtd.lower()): #and lc_ZHGS not in condition_type: #Added by ishika
                        buying_method = context.Quote.GetCustomField('CF_Buying_Method').Value
                        if buying_method in special_bmethods:
                            if b_mtd.lower() != "buy honeywell hon to hon":
                                i["QI_SpecialPriceP"] = j.ConditionRate.strip("-")
                            i["QI_CSPA_DiscountAmount"] = (float(i["QI_SpecialPriceP"]) * float(
                                i["QI_List_Price"])) / 100
                            i["QI_SpecialPriceV"] = float(i["QI_List_Price"]) - float(i["QI_CSPA_DiscountAmount"])
                            i["QI_Recommended_Unit_Sell_Price"] = float(i["QI_List_Price"]) - float(
                                i["QI_CSPA_DiscountAmount"])
                            i["QI_Recommended_Sell_Price"] = i["QI_Recommended_Unit_Sell_Price"] * i.Quantity
                            context.Quote.GetCustomField('CF_SPECIAL_PRICING').Value = 'True'
                        else:
                            if b_mtd.lower() != "buy honeywell hon to hon":
                                i["QI_SpecialPriceP"] = str(0)
                                i["QI_CSPA_DiscountAmount"] = 0.0
                            i["QI_SpecialPriceV"] = 0.0
                            i["QI_Recommended_Unit_Sell_Price"] = float(i["QI_List_Price"])
                            i["QI_Recommended_Sell_Price"] = i["QI_Recommended_Unit_Sell_Price"] * i.Quantity
                            # context.Quote.GetCustomField('CF_SPECIAL_PRICING').Value = 'False'
                        # i["QI_DiscountP"] = j.ConditionRate.strip("-")
                        # i["QI_Recommended_DiscountP"] = j.ConditionRate.strip("-")
                        lv_speicalPriceV = j.ConditionRate.strip("-")
                        lv_speicalPriceP = j.ConditionRate.strip("-")
                        #lv_discount = 'True'    #Commented by ishika
                        lv_discount = lc_True    #Added by ishika
                    #if j.ConditionType == 'ZHGS':   #Commented by ishika
                    if j.ConditionType == lc_ZHGS: #Modified by Aditi 24Jan2023
                        Trace.Write("----ZHGS1-----")
                        i["QI_GSA"] = j.ConditionValue
                        # lv_specialPrice = 'True'  #Commented by ishika
                        lv_specialPrice = lc_True  #Added by Ishika
                        #j.ConditionValue = j.ConditionValue #commented by Aditi 23Jan
                        if b_mtd.lower() != "buy honeywell hon to hon" and (lc_GSA.lower() in b_mtd.lower()):
                            Trace.Write("----ZHGS2-----")
                            i["QI_SpecialPriceP"] = ''
                            i["QI_CSPA_DiscountAmount"] = ''
                            i["QI_SpecialPriceV"] = str(float(j.ConditionValue)/i.Quantity)
                            i["QI_Recommended_Unit_Sell_Price"] = float(j.ConditionValue)/i.Quantity
                            i["QI_Recommended_Sell_Price"] = float(j.ConditionValue)
                            context.Quote.GetCustomField('CF_SPECIAL_PRICING').Value = 'True'
                            gsa_flag = True
                    
                    if j.ConditionType == lc_ZIFP: #Added by Aditi 24Jan2023
                        if b_mtd.lower() != "buy honeywell hon to hon" and (lc_GSA.lower() in b_mtd.lower()) and gsa_flag:
                            Trace.Write("----ZHGS3-----")
                            #Trace.Write("ZHGS3--specialP: "+str((float(j.ConditionRate) / i["QI_List_Price"])*100))
                            ifp_price = (float(j.ConditionRate) * float(i["QI_SpecialPriceV"])) / 100
                            i["QI_IFP"] = ifp_price
                            if ifp_price != 0:
                                i["QI_SpecialPriceV"] = str(float(i["QI_SpecialPriceV"]) + ifp_price)
                                i["QI_SpecialPriceP"] = ''
                                i["QI_CSPA_DiscountAmount"] = ''
                                i["QI_Recommended_Unit_Sell_Price"] = float(i["QI_SpecialPriceV"])
                                i["QI_Recommended_Sell_Price"] = float(i["QI_Recommended_Unit_Sell_Price"]) * i.Quantity
                                gsa_flag = False

                    # if j.ConditionTypeDescription == 'Net Value':
                    # i["QI_Recommended_Unit_Sell_Price"] = float(j.ConditionRate)
                    # i["QI_Recommended_Sell_Price"] = j.ConditionValue
                    #if lv_specialPrice == 'True' or flag_buyhoneywell == 'True':   #Commented by ishika
                    if lv_specialPrice == lc_True or flag_buyhoneywell == lc_True:  #Added by Ishika
                        if b_mtd.lower() != "buy honeywell hon to hon":
                            i["QI_SpecialPriceP"] = i["QI_DiscountP"]
                        # discount = (float(i["QI_DiscountP"]) * float(i["QI_List_Price"]) ) /100
                        # i["QI_SpecialPriceV"] = float(i["QI_List_Price"]) - discount
                        # i["QI_SpecialPriceV"] = float(i["QI_DiscountP"]) * float(i["QI_List_Price"])

                        #i["QI_Special_Pricing"] = 'True'  #Commented by ishika
                        i["QI_Special_Pricing"] = lc_True  #Added by ishika
                        # context.Quote.GetCustomField('CF_SPECIAL_PRICING').Value = 'True'
                    # if lv_csp == 'True':  # and lv_discount == 'True':  #Commented by ishika
                    if lv_csp == lc_True:  # and lv_discount == 'True':   #Added by ishika
                        # i["QI_SpecialPriceV"] = i["QI_CSP"]
                        if b_mtd.lower() != "buy honeywell hon to hon":
                            i["QI_SpecialPriceP"] = ''
                        i["QI_DiscountP"] = ''
                        i["QI_Recommended_DiscountP"] = ''
                        (i["QI_Recommended_Discount"]) = ''
                    if i["QI_Recommended_DiscountP"] != '':
                        i["QI_Recommended_Discount"] = (float(i["QI_DiscountP"]) * float(i["QI_List_Price"])) / 100
                        lv_speicalPriceV = ''

                    if i.DiscountPercent != None and i.NetPrice != None:
                        #Log.Info("i.DiscountAmount111 bef---->"+str(i.DiscountAmount))
                        i.DiscountAmount = (i["QI_Recommended_Unit_Sell_Price"] * (i.DiscountPercent)) / 100
                        #Log.Info("i.DiscountAmount111 aft---->"+str(i.DiscountAmount))
                        i["QI_Unit_Sell_Price"] = i["QI_Recommended_Unit_Sell_Price"] - i.DiscountAmount#(round(i.DiscountAmount,2))
                        i.NetPrice = (i["QI_Recommended_Unit_Sell_Price"] - i.DiscountAmount) * (i.Quantity) #(round(i.DiscountAmount,2))) * (i.Quantity)
                        # i.DiscountAmount = i.DiscountAmount * (i.Quantity)
                        #Trace.Write("SEll Price " + str(i.NetPrice))

                '''if j.ConditionType != 'null' and float(j.ConditionRate) != 0 and float(
                        j.ConditionValue) != 0 and j.ConditionTypeDescription != '' and ('ZCSP' in condition_type):
                    Trace.Write("False")''' # Commented by ishika
                if j.ConditionType != lc_null and float(j.ConditionRate) != 0 and float(j.ConditionValue) != 0 and j.ConditionTypeDescription != '' and (lc_ZCSP in condition_type):  #Added by ishika
                    #Trace.Write("False")
                    # if j.ConditionType == 'ZP00':  # Commented by ishika
                    if j.ConditionType == lc_ZP00:  #Added by ishika
                        #ex_rate = getExchRate(j.ConditionCurrency,quote_currency)
                        i["QI_List_Price"] = float(j.ConditionValue)/i.Quantity #float(j.ConditionRate) * ex_rate
                        i["QI_List_Price_Total"] = float(j.ConditionValue) #float(j.ConditionRate) * ex_rate * i.Quantity
                        # Trace.Write("exrate"+str(i["QI_Exchange_Rate"]))
                        # Trace.Write("Unit List Price "+str(i["QI_List_Price"]))
                        # Trace.Write("List Price "+str(i["QI_List_Price_Total"]))
                        lv_ListPrice = float(j.ConditionValue)/i.Quantity #j.ConditionRate
                    #if j.ConditionType == 'ZCSP':  #Commented by ishika
                    if j.ConditionType == lc_ZCSP and not (lc_ZHGS in condition_type and lc_GSA.lower() in b_mtd.lower()): #and lc_ZHGS not in condition_type:  #Added by ishika
                        #ex_rate = getExchRate(j.ConditionCurrency,quote_currency)
                        i["QI_CSP"] = j.ConditionValue
                        i["QI_SpecialPriceV"] = float(j.ConditionRate)
                        # Trace.Write("gh" +str(i["QI_SpecialPriceV"]))
                        lv_price = j.ConditionValue
                        #lv_specialPrice = 'True'  #Commented by ishika
                        lv_specialPrice = lc_True   #Added by ishika
                        #lv_csp = 'True'    #Commented by ishika
                        lv_csp = lc_True    #Added by ishika

                        # i["QI_DiscountP"] = j.ConditionRate.strip("-")
                        # i["QI_Recommended_DiscountP"] = j.ConditionRate.strip("-")
                        lv_speicalPriceV = j.ConditionRate.strip("-")
                        lv_speicalPriceP = j.ConditionRate.strip("-")
                        #lv_discount = 'True'   #Commented by ishika
                        lv_discount = lc_True  #Added by ishika
                        i["QI_Recommended_Unit_Sell_Price"] = float(j.ConditionValue)/i.Quantity #float(j.ConditionRate) * ex_rate
                        i["QI_Recommended_Sell_Price"] = float(j.ConditionValue) #float(j.ConditionRate) * ex_rate * i.Quantity
                        # context.Quote.GetCustomField('CF_SPECIAL_PRICING').Value = 'True'  #Commented by ishika
                        context.Quote.GetCustomField('CF_SPECIAL_PRICING').Value = lc_True  #Added by ishika
                    #if j.ConditionType == 'ZHGS': #Commented by ishika
                    if j.ConditionType == lc_ZHGS: #Modified by Aditi 24Jan2023
                        Trace.Write("----ZHGS1-----")
                        i["QI_GSA"] = j.ConditionValue
                        # lv_specialPrice = 'True'  #Commented by ishika
                        lv_specialPrice = lc_True  #Added by Ishika
                        #j.ConditionValue = j.ConditionValue #commented by Aditi 23Jan
                        if b_mtd.lower() != "buy honeywell hon to hon" and (lc_GSA.lower() in b_mtd.lower()):
                            Trace.Write("----ZHGS2-----")
                            i["QI_SpecialPriceP"] = ''
                            i["QI_CSPA_DiscountAmount"] = ''
                            i["QI_SpecialPriceV"] = str(float(j.ConditionValue)/i.Quantity)
                            i["QI_Recommended_Unit_Sell_Price"] = float(j.ConditionValue)/i.Quantity
                            i["QI_Recommended_Sell_Price"] = float(j.ConditionValue)
                            context.Quote.GetCustomField('CF_SPECIAL_PRICING').Value = 'True'
                            gsa_flag = True
                    
                    if j.ConditionType == lc_ZIFP: #Added by Aditi 24Jan2023
                        if b_mtd.lower() != "buy honeywell hon to hon" and (lc_GSA.lower() in b_mtd.lower()) and gsa_flag:
                            Trace.Write("----ZHGS3-----")
                            #Trace.Write("ZHGS3--specialP: "+str((float(j.ConditionRate) / i["QI_List_Price"])*100))
                            ifp_price = (float(j.ConditionRate) * float(i["QI_SpecialPriceV"])) / 100
                            i["QI_IFP"] = ifp_price
                            if ifp_price != 0:
                                i["QI_SpecialPriceV"] = str(float(i["QI_SpecialPriceV"]) + ifp_price)
                                i["QI_SpecialPriceP"] = ''
                                i["QI_CSPA_DiscountAmount"] = ''
                                i["QI_Recommended_Unit_Sell_Price"] = float(i["QI_SpecialPriceV"])
                                i["QI_Recommended_Sell_Price"] = float(i["QI_Recommended_Unit_Sell_Price"]) * i.Quantity
                                gsa_flag = False
                        # ConditionTypeDescription
                    # if j.ConditionTypeDescription == 'Net Value':
                    # i["QI_Recommended_Unit_Sell_Price"] = float(j.ConditionRate)
                    # i["QI_Recommended_Sell_Price"] = j.ConditionValue
                    #if lv_specialPrice == 'True' or flag_buyhoneywell == 'True':    #Commented by ishika
                    if lv_specialPrice == lc_True or flag_buyhoneywell == lc_True:  # added by ishika
                        if b_mtd.lower() != "buy honeywell hon to hon":
                            i["QI_SpecialPriceP"] = i["QI_DiscountP"]
                        # discount = (float(i["QI_DiscountP"]) * float(i["QI_List_Price"]) ) /100
                        # i["QI_SpecialPriceV"] = float(i["QI_List_Price"]) - discount
                        # i["QI_SpecialPriceV"] = float(i["QI_DiscountP"]) * float(i["QI_List_Price"])

                        #i["QI_Special_Pricing"] = 'True' #Commented by ishika
                        i["QI_Special_Pricing"] = lc_True   #Added by ishika
                        # context.Quote.GetCustomField('CF_SPECIAL_PRICING').Value = 'True'
                    #if lv_csp == 'True':  # and lv_discount == 'True':  #Commented by ishika
                    if lv_csp == lc_True:  # and lv_discount == 'True':  # added by ishika
                        # i["QI_SpecialPriceV"] = i["QI_CSP"]
                        if b_mtd.lower() != "buy honeywell hon to hon":
                            i["QI_SpecialPriceP"] = ''
                        i["QI_DiscountP"] = ''
                        i["QI_Recommended_DiscountP"] = ''
                        (i["QI_Recommended_Discount"]) = ''
                    if i["QI_Recommended_DiscountP"] != '':
                        i["QI_Recommended_Discount"] = (float(i["QI_DiscountP"]) * float(i["QI_List_Price"])) / 100
                        lv_speicalPriceV = ''

                    if i.DiscountPercent != None and i.NetPrice != None:
                        #Log.Info("i.DiscountAmount222 bef---->"+str(i.DiscountAmount))
                        i.DiscountAmount = (i["QI_Recommended_Unit_Sell_Price"] * (i.DiscountPercent)) / 100
                        #Log.Info("i.DiscountAmount222 aft---->"+str(i.DiscountAmount))
                        i["QI_Unit_Sell_Price"] = i["QI_Recommended_Unit_Sell_Price"] - i.DiscountAmount #(round(i.DiscountAmount,2))
                        i.NetPrice = (i["QI_Recommended_Unit_Sell_Price"] - i.DiscountAmount) * (i.Quantity) #(round(i.DiscountAmount,2))) * (i.Quantity)
                        # i.DiscountAmount = i.DiscountAmount * (i.Quantity)
                        #Trace.Write("SEll Price " + str(i.NetPrice))

                '''if j.ConditionType != 'null' and float(j.ConditionRate) != 0 and j.ConditionTypeDescription != '' and (
                    'ZCSP' not in condition_type) and ('ZDIS' not in condition_type):''' #commented by ishika
                if j.ConditionType != lc_null and float(j.ConditionRate) != 0 and j.ConditionTypeDescription != '' and (lc_ZCSP not in condition_type) and (lc_ZDIS not in condition_type) and (lc_ZHGS not in condition_type) and (lc_ZIFP not in condition_type):  #Added by ishika
                    #if j.ConditionType == 'ZP00':  #Commented by ishika
                    if j.ConditionType == lc_ZP00:  #Added by ishika
                        #ex_rate = getExchRate(j.ConditionCurrency,quote_currency)
                        i["QI_List_Price"] = float(j.ConditionValue)/i.Quantity #float(j.ConditionRate) * ex_rate
                        Trace.Write("ZPentered")
                        Trace.Write("Unit List Price "+str(i["QI_List_Price"]))
                        i["QI_List_Price_Total"] = float(j.ConditionValue) #float(j.ConditionRate) * ex_rate * i.Quantity
                        i["QI_Recommended_Unit_Sell_Price"] = float(j.ConditionValue)/i.Quantity #float(j.ConditionRate) * ex_rate
                        i["QI_Recommended_Sell_Price"] = float(j.ConditionValue) #float(j.ConditionRate) * ex_rate * i.Quantity
                        #Trace.Write("List Price "+str(i["QI_List_Price_Total"]))
                        lv_ListPrice = float(j.ConditionValue)/i.Quantity #j.ConditionRate
                    
                    if i.DiscountPercent != None and i.NetPrice != None:
                        #Log.Info("i.DiscountAmount333 bef---->"+str(i.DiscountAmount))
                        i.DiscountAmount = (i["QI_Recommended_Unit_Sell_Price"] * (i.DiscountPercent)) / 100
                        #Log.Info("i.DiscountAmount333 aft---->"+str(i.DiscountAmount))
                        i["QI_Unit_Sell_Price"] = i["QI_Recommended_Unit_Sell_Price"] - i.DiscountAmount #(round(i.DiscountAmount,2))
                        i.NetPrice = (i["QI_Recommended_Unit_Sell_Price"] - i.DiscountAmount) * (i.Quantity) #(round(i.DiscountAmount,2))) * (i.Quantity)
                        # i.DiscountAmount = i.DiscountAmount * (i.Quantity)
                        #Trace.Write("SEll Price " + str(i.NetPrice))
                if j.ConditionType != lc_null and j.ConditionTypeDescription != '' and (lc_ZHGS in condition_type) and (lc_ZCSP not in condition_type) and (lc_ZDIS not in condition_type):
                    if j.ConditionType == lc_ZHGS: #Modified by Aditi 24Jan2023
                        Trace.Write("----ZHGS1-----")
                        i["QI_GSA"] = j.ConditionValue
                        # lv_specialPrice = 'True'  #Commented by ishika
                        lv_specialPrice = lc_True  #Added by Ishika
                        #j.ConditionValue = j.ConditionValue #commented by Aditi 23Jan
                        if b_mtd.lower() != "buy honeywell hon to hon" and (lc_GSA.lower() in b_mtd.lower()):
                            Trace.Write("----ZHGS2-----")
                            i["QI_SpecialPriceP"] = ''
                            i["QI_CSPA_DiscountAmount"] = ''
                            i["QI_SpecialPriceV"] = str(float(j.ConditionValue)/i.Quantity)
                            i["QI_Recommended_Unit_Sell_Price"] = float(j.ConditionValue)/i.Quantity
                            i["QI_Recommended_Sell_Price"] = float(j.ConditionValue)
                            context.Quote.GetCustomField('CF_SPECIAL_PRICING').Value = 'True'
                            gsa_flag = True
                    
                    if j.ConditionType == lc_ZIFP: #Added by Aditi 24Jan2023
                        if b_mtd.lower() != "buy honeywell hon to hon" and (lc_GSA.lower() in b_mtd.lower()) and gsa_flag:
                            Trace.Write("----ZHGS3-----")
                            #Trace.Write("ZHGS3--specialP: "+str((float(j.ConditionRate) / i["QI_List_Price"])*100))
                            ifp_price = (float(j.ConditionRate) * float(i["QI_SpecialPriceV"])) / 100
                            i["QI_IFP"] = ifp_price
                            if ifp_price != 0:
                                i["QI_SpecialPriceV"] = str(float(i["QI_SpecialPriceV"]) + ifp_price)
                                i["QI_SpecialPriceP"] = ''
                                i["QI_CSPA_DiscountAmount"] = ''
                                i["QI_Recommended_Unit_Sell_Price"] = float(i["QI_SpecialPriceV"])
                                i["QI_Recommended_Sell_Price"] = float(i["QI_Recommended_Unit_Sell_Price"]) * i.Quantity
                                gsa_flag = False
                    
                    if i.DiscountPercent != None and i.NetPrice != None:
                        #Log.Info("i.DiscountAmount333 bef---->"+str(i.DiscountAmount))
                        i.DiscountAmount = (i["QI_Recommended_Unit_Sell_Price"] * (i.DiscountPercent)) / 100
                        #Log.Info("i.DiscountAmount333 aft---->"+str(i.DiscountAmount))
                        i["QI_Unit_Sell_Price"] = i["QI_Recommended_Unit_Sell_Price"] - i.DiscountAmount #(round(i.DiscountAmount,2))
                        i.NetPrice = (i["QI_Recommended_Unit_Sell_Price"] - i.DiscountAmount) * (i.Quantity) #(round(i.DiscountAmount,2))) * (i.Quantity)
                        # i.DiscountAmount = i.DiscountAmount * (i.Quantity)
                        #Trace.Write("SEll Price " + str(i.NetPrice))

            if i["QI_SpecialPriceP"]!=None and i["QI_SpecialPriceP"]!='' and i["QI_SpecialPriceP"]!='0': #Added by Aditi 28Jan2023
                i["QI_CSPA_DiscountAmount"] = (float(i["QI_SpecialPriceP"]) * float(i["QI_List_Price"])) / 100
                i["QI_SpecialPriceV"] = float(i["QI_List_Price"]) - float(i["QI_CSPA_DiscountAmount"])
                i["QI_Recommended_Unit_Sell_Price"] = float(i["QI_List_Price"]) - float(i["QI_CSPA_DiscountAmount"])
                i["QI_Recommended_Sell_Price"] = i["QI_Recommended_Unit_Sell_Price"] * i.Quantity
            elif i["QI_SpecialPriceP"]=='0':
                i["QI_CSPA_DiscountAmount"] = 0
                i["QI_SpecialPriceV"] = 0
    
    calculateMargin() #Added by Aditi 6th Jan