# -----------------------------------------------------------------------------
#			Change History Log
# -----------------------------------------------------------------------------
# Description:
# This script is used to calculate the exchange rate
# -----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
# -----------------------------------------------------------------------------
# 08/16/2022    Sumandrita Moitra     0         -initial version
# 11/5/2022  	Ishika BHattacharya	  26	    -Replaced Hardcodings
#										        -Incorporated Translation
# 11/08/2022    Aditi Sharma          30        -changes for exchange rate from
#                                                non-USD to non-USD conversion
# 12/19/2022    Sumandrita Moitra     41        -Replaced i.ProductTypeName with i['QI_Product_Type']. By Sumandrita
# 12/22/2022    Karthik Raj           44        -changes to fetch cost based on labor sub loaction. By karthik
# 12/26/2022    Aditi Sharma          45        -Modified default currency from USD to quote_currency
# 12/29/2022    Sumandrita            48        -Added Condition for 3rd Party product without Pricing Condition
# 01/14/2023   Aditi Sharma                       -Added condition check for Preparing status
# 01/19/2023   Ashutosh                          -Removed all rounding
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
import GM_TRANSLATIONS  # Added by Ishika
from datetime import date

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
quote_status_ID = context.Quote.StatusId #Added by Aditi 14th Jan

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type and quote_status_ID==32:  # Added by Ishika #Modified by Aditi 14th Jan
    lc_FP_Material = GM_TRANSLATIONS.GetText('000020', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
    lc_Labor = GM_TRANSLATIONS.GetText('000040', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
    lc_Honeywell_Hardware = GM_TRANSLATIONS.GetText('000027', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
    lc_Honeywell_Labor = GM_TRANSLATIONS.GetText('000118', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
    lc_Undefined = GM_TRANSLATIONS.GetText('000183', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
    lc_ZSRV = GM_TRANSLATIONS.GetText('000119', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
    lc_None = GM_TRANSLATIONS.GetText('000108', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
    lc_USD = GM_TRANSLATIONS.GetText('000120', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika 
    lc_Write_In = GM_TRANSLATIONS.GetText('000175', lv_LanguageKey, '', '', '', '', '')
    lc_Adhoc = GM_TRANSLATIONS.GetText('000111', lv_LanguageKey, '', '', '', '', '')

    today = date.today()
    quote_currency = context.Quote.GetCustomField('CF_Quote_Currency').Value
    quote_org = context.Quote.GetCustomField('CF_Sales_Org').Value
    lv_opp_cntry = context.Quote.GetCustomField('CF_Country').Value
    date = date.today()
    exc_to_usd = 0
    exc_from_usd = 0
    for i in context.Quote.GetAllItems():
        part_nbr = i.PartNumber
        query_desc = ""
        # Commented by Aditi 3rd Oct 2022, since CT_Thirdparty_Pricebook is no longer used, instead refer CT_TP_Price
        '''if i.ProductTypeName == "Third Party":
            query_desc = SqlHelper.GetList("SELECT * FROM CT_Thirdparty_Pricebook WHERE Part_No = '{}'".format(part_nbr))
        elif i.ProductTypeName == "First Party Material" or i.ProductTypeName == "Labor":
            query_desc = SqlHelper.GetList("SELECT * FROM CT_MATERIALS_CDE_VALIDATION WHERE Part_no = '{}'".format(part_nbr))'''
        # Comment End
        # Aditi: 6th Oct: Product type will be Honeywell Hardware instead of First party material, so modified the condition
        #if i.ProductTypeName == "First Party Material" or i.ProductTypeName == "Labor" or i.ProductTypeName == "Honeywell Hardware" or i.ProductTypeName == 'Honeywell Labor' or i.ProductTypeName == "Undefined":   #Commneted by Ishika 
        if i['QI_Product_Type'] == lc_FP_Material or i['QI_Product_Type'] == lc_Labor or i['QI_Product_Type'] == lc_Honeywell_Hardware or i['QI_Product_Type'] == lc_Honeywell_Labor or i['QI_Product_Type'] == lc_Undefined or ((i['QI_Product_Type'] == 'Third Party') and (i.VCItemPricingPayload is not None)): #Added by ishika #Replaced i.ProductTypeName with i['QI_Product_Type']. By Sumandrita

            # query_desc = SqlHelper.GetList("SELECT * FROM CT_MATERIALS_CDE_VALIDATION WHERE Part_no = '{}'".format(part_nbr)) "Commented by Dhruv
            query_desc = SqlHelper.GetList("SELECT * FROM CT_PRODUCT_SALES WHERE PARTNUMBER = '{}' and SALESORG = '{}'".format(part_nbr, quote_org))
            #query_desc = SqlHelper.GetList("SELECT * FROM CT_PRODUCT_SALES WHERE PARTNUMBER = '{}' and SALESORG = '{}' and LanguageKey = '{}'".format(part_nbr,quote_org, lv_LanguageKey)) #Added by ishika

        if query_desc:
            #Trace.Write("Yes")
            for qry in query_desc:
                # if qry.Material_Type == 'ZSRV' and quote_org!=None:		"Commented by Dhruv
                #if qry.MATERIAL_TYPE == 'ZSRV' and quote_org != None:     #Commented by ishika
                if qry.MATERIAL_TYPE == lc_ZSRV and quote_org != lc_None:  #Added by ishika
                    # ls_actvt_type = SqlHelper.GetList("SELECT * FROM CT_ACTIVITY_TYPE WHERE Ser_Material = '" + str(part_nbr) + "'")   #Commented by ishika
                    ls_actvt_type = SqlHelper.GetList(
                        "SELECT * FROM CT_ACTIVITY_TYPE WHERE Ser_Material = '" + str(part_nbr) + "' ")  #Added by ishika
                    if ls_actvt_type.Count > 0:
                        lv_actc_typ = ' '
                        for actvt in ls_actvt_type:
                            lv_actvt_type = str(actvt.SAP_Activity_Type)
                            break
                        '''query_labor = SqlHelper.GetList("SELECT * FROM CT_LABOR_COST WHERE Sales_Org = '{}' and Distribution_Channel = '{}' and Division = '{}' and Activity_Type = '{}' and Profit_Center = '{}' ".format(
                                quote_org, '10', '10', lv_actvt_type,
                                str(context.Quote.GetCustomField("CF_Profit_Center_ID").Value)))''' #Commented by ishika
                        query_labor = SqlHelper.GetList(
                            "SELECT * FROM CT_LABOR_COST WHERE Sales_Org = '{}' and Distribution_Channel = '{}' and Division = '{}' and Activity_Type = '{}' and Profit_Center = '{}' ".format(quote_org, '10', '10', lv_actvt_type,str(i["CFI_SUB_LOCATION"])))  #Added by ishika#changed by karthik
                        for curr in query_labor:
                            Trace.Write("PartNumber----->"+str(part_nbr))
                            Trace.Write("CFI_SUB_LOCATION----->"+str(i["CFI_SUB_LOCATION"]))
                            if curr.Object_Currency:
                                i['QI_Cost_Currency'] = str(curr.Object_Currency)
                                i['QI_Unit_Cost_Base_Currency'] = curr.ActivityRateCurMonth_1
                            else:
                                # i['QI_Cost_Currency'] = str("USD")   #Commented by ishika
                                i['QI_Cost_Currency'] = lc_USD  #Added by ishika
                else:
                    if qry.CURRENCY_KEY:
                        i['QI_Cost_Currency'] = str(qry.CURRENCY_KEY)
                        i['QI_Unit_Cost_Base_Currency'] = str(float(qry.STANDARD_PRICE) / float(qry.PRICE_UNIT))
                    else:
                        # i['QI_Cost_Currency'] = str("USD")   #Commented by ishika
                        i['QI_Cost_Currency'] = lc_USD  # Added by ishika
                        i['QI_Unit_Cost_Base_Currency'] = str(float(qry.STANDARD_PRICE) / float(qry.PRICE_UNIT))
                        
        #condition for Thirdparty without pricing condition added by Sumandrita
        elif i['QI_Product_Type'] == 'Third Party' and (i.VCItemPricingPayload is None):   
            lv_price = SqlHelper.GetFirst(" SELECT DISTINCT * FROM CT_TP_PRICE WHERE PartNumber = '{0}' and CountryCode = '{1}'".format(i.PartNumber, lv_opp_cntry))
            if lv_price:
                i['QI_Cost_Currency'] = lv_price.Currency
        #end of changes done by Sumandrita
            
        elif i['QI_Product_Type'] == lc_Write_In and i['QI_Cost_Currency']=='': #Replaced i.ProductTypeName with i['QI_Product_Type']. By Sumandrita
            i['QI_Cost_Currency'] = str(quote_currency)
        elif i.PartNumber == lc_Adhoc and i['QI_Cost_Currency']=='':
            i['QI_Cost_Currency'] = str(quote_currency)
        elif (i['QI_Product_Type'] != lc_Write_In or i.PartNumber != lc_Adhoc) and i['QI_Cost_Currency']=='': #Replaced i.ProductTypeName with i['QI_Product_Type']. By Sumandrita
            i['QI_Cost_Currency'] = str(quote_currency) #str("USD") #Modified by Aditi 26th Dec

        base_currency = i['QI_Cost_Currency']
        if str(quote_currency) == str(base_currency) or str(quote_currency) == "" or str(base_currency) == "":
            i['QI_Exchange_Rate'] = 1
        elif str(quote_currency) != str(base_currency) and str(base_currency)==lc_USD and str(quote_currency)!=lc_USD: #Added by Aditi 8Nov2022
            '''query_exchange = SqlHelper.GetList(
                "SELECT TOP 1 * FROM CT_EXCHANGE_RATE  WHERE FROM_CURRENCY = '{}' AND TO_CURRENCY = '{}' ORDER BY [Date] Desc".format(
                    base_currency, quote_currency))''' #Commented by ishika
            query_exchange = SqlHelper.GetList(
                "SELECT TOP 1 * FROM CT_EXCHANGE_RATE  WHERE FROM_CURRENCY = '{}' AND TO_CURRENCY = '{}' ORDER BY [Date] Desc".format(
                    base_currency, quote_currency))   #Added by ishika
            if query_exchange:
                for qry in query_exchange:
                    #i['QI_Exchange_Rate'] = round(qry.RATE, 2)
                    i['QI_Exchange_Rate'] = qry.RATE
                    Trace.Write("Ex Rate" + str(i['QI_Exchange_Rate']))
        elif str(quote_currency) != str(base_currency) and str(base_currency)!=lc_USD and str(quote_currency)!=lc_USD: #Added by Aditi 8Nov2022
            query_exchange_toUSD = SqlHelper.GetList(
                "SELECT TOP 1 * FROM CT_EXCHANGE_RATE  WHERE FROM_CURRENCY = '{}' AND TO_CURRENCY = '{}' ORDER BY [Date] Desc".format(
                    base_currency, lc_USD))
            if query_exchange_toUSD:
                for qry in query_exchange_toUSD:
                    #exc_to_usd = round(qry.RATE, 2)
                    exc_to_usd = qry.RATE
                    Trace.Write("To USD Ex Rate" + str(exc_to_usd))
            query_exchange_fromUSD = SqlHelper.GetList(
                "SELECT TOP 1 * FROM CT_EXCHANGE_RATE  WHERE FROM_CURRENCY = '{}' AND TO_CURRENCY = '{}' ORDER BY [Date] Desc".format(
                    lc_USD, quote_currency))
            if query_exchange_fromUSD:
                for qry in query_exchange_fromUSD:
                    #exc_from_usd = round(qry.RATE, 2)
                    exc_from_usd = qry.RATE
                    Trace.Write("From USD Ex Rate" + str(exc_from_usd))
            #i['QI_Exchange_Rate'] = round(exc_to_usd * exc_from_usd, 2)
            i['QI_Exchange_Rate'] = exc_to_usd * exc_from_usd
        elif str(quote_currency) != str(base_currency) and str(base_currency)!=lc_USD and str(quote_currency)==lc_USD: #Added by Aditi 9Nov2022
            query_exchange_toUSD = SqlHelper.GetList(
                "SELECT TOP 1 * FROM CT_EXCHANGE_RATE  WHERE FROM_CURRENCY = '{}' AND TO_CURRENCY = '{}' ORDER BY [Date] Desc".format(
                    base_currency, lc_USD))
            if query_exchange_toUSD:
                for qry in query_exchange_toUSD:
                    #exc_to_usd = round(qry.RATE, 2)
                    exc_to_usd = qry.RATE
                    Trace.Write("To USD Ex Rate" + str(exc_to_usd))
            #i['QI_Exchange_Rate'] = round(exc_to_usd, 2)
            i['QI_Exchange_Rate'] = exc_to_usd