#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for financial summary table calculation
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 08/20/2022    Aditi Sharma               0             -Initial Version
# 10/19/2022    Ishika Bhattacharya        75            -Replaced Hardcodings
#                                                        -Incorporated Translation
# 11/01/2022    Aditi Sharma               79            -Replaced lc_op_type with lc_trans_type
#                                                         to remove dependency on multiple opp types
# 11/05/2022   Ishika bhattacharya         81            -Add language key in sql query where clause
#
# 11/14/2022   Aditi Sharma                82            -To populate NEX Mapping fields
# 11/18/2022   Dhruv Bhatnagar			   83            -To Remove Language key Check from 
#														  CT_EXCHANGE_RATE
# 11/22/2022   Aditi Sharma                85            -To calculate approval level based on
#                                                         USD quote sell price
# 11/22/2022   Aditi Sharma                87            -Correction to get correct USD price rounding
# 11/26/2022   Aditi Sharma                89            -To eliminate parent write in from total price calculation
# 12/1/2022    Aditi Sharma                92            -Fixed rounding issues for prices
# 12/16/2022   Ishika Bhattacharya         95            -Added rounding upto 2 decimals for discount variance
# 12/16/2022   Aditi Sharma                96            -removed discVar method (was not being used in script)
# 12/22/2022   Aditi Sharma                97            -Added OR condition for Honeywell Labor as product type
# 12/23/2022   Aditi Sharma                98            -Added condition to avoid duplication of total sell price for mandatory charges parent
# 01/13/2023   Dhruv Bhatnagar			   104			 -CXCPQ-35217:replace pole/region criteria with country for fetching recommended
#														  discounts
# 01/15/2023   Aditi Sharma                105           -Added changes to fetch approval for CSPA-RQ and non-CSPA-parts only
# 01/18/2023   Aditi Sharma                110           -Corrected the margin percent calculation for mandatory charges
#1/19/2023     Srijaydhurga                               Based on user Type
#1/23/2023 Dhruv Bhatnagar								- Added translation keys
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS    # Added by Ishika
import datetime
from Scripting.Quote import MessageLevel

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
#Declaring variable #Added by Ishika
lc_USD = GM_TRANSLATIONS.GetText('000120', lv_LanguageKey, '', '', '', '', '')
#lc_op_type = GM_TRANSLATIONS.GetText('000024', lv_LanguageKey, '', '', '', '', '') #commented by Aditi 1st Nov 2022
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #added by Aditi 1st Nov 2022
lc_quote_list_price = GM_TRANSLATIONS.GetText('000132', lv_LanguageKey, '', '', '', '', '')
lc_quote_sell_price = GM_TRANSLATIONS.GetText('000133', lv_LanguageKey, '', '', '', '', '')
lc_margin_perc = GM_TRANSLATIONS.GetText('000134', lv_LanguageKey, '', '', '', '', '')
lc_margin_amount = GM_TRANSLATIONS.GetText('000135', lv_LanguageKey, '', '', '', '', '')
lc_actual_quote_discount_perc = GM_TRANSLATIONS.GetText('000136', lv_LanguageKey, '', '', '', '', '')
lc_fp_material = GM_TRANSLATIONS.GetText('000020', lv_LanguageKey, '', '', '', '', '')
lc_honeywell_hardware = GM_TRANSLATIONS.GetText('000027', lv_LanguageKey, '', '', '', '', '')
lc_labor = GM_TRANSLATIONS.GetText('000040', lv_LanguageKey, '', '', '', '', '')
lc_honeywell_labor = GM_TRANSLATIONS.GetText('000118', lv_LanguageKey, '', '', '', '', '') #Added by Aditi 22nd Dec 2022
lc_max_disc_per_recommended = GM_TRANSLATIONS.GetText('000137', lv_LanguageKey, '', '', '', '', '')
lc_discount_variance_perc = GM_TRANSLATIONS.GetText('000138', lv_LanguageKey, '', '', '', '', '')
lc_highest_approval_req = GM_TRANSLATIONS.GetText('000139', lv_LanguageKey, '', '', '', '', '')
lc_cspa = GM_TRANSLATIONS.GetText('000187', lv_LanguageKey, '', '', '', '', '')
lc_Auto = GM_TRANSLATIONS.GetText('000158', lv_LanguageKey, '', '', '', '', '')
lc_Discount = GM_TRANSLATIONS.GetText('000188', lv_LanguageKey, '', '', '', '', '')
lc_Y = GM_TRANSLATIONS.GetText('000189', lv_LanguageKey, '', '', '', '', '')
lc_partsOnly = GM_TRANSLATIONS.GetText('000019', lv_LanguageKey, '', '', '', '', '') #added by Aditi 15 Jan 2023
get_user_type= User.UserType.Name #added by dhurga
# a = context.Quote.GetCustomField("CF_APPROVAL_LEVEL").Value
special_bmethods = []
special_query = SqlHelper.GetList("SELECT * FROM CT_BUYING_METHODS WHERE SPECIAL_PRICING='{}' and LANGUAGE_KEY = '{}'".format(lc_Y, lv_LanguageKey))
for sp_row in special_query:
    special_bmethods.append(sp_row.BUYING_METHOD)
    # Trace.Write("special_methods "+str(special_bmethods))


# itemCount = len(context.Quote.GetAllItems())


def getApprovalLevel(qbuying_mth, qsell_price, qdisc_var, qmargin):
    # qmm = qmargin
    maxApproval = ''
    if qbuying_mth in special_bmethods:
        # cspa_query = SqlHelper.GetList("SELECT * FROM SEA_APPROVAL_DISCOUNT_MATRIX WHERE LimitType='CSPA'") #Commented by ishika
        cspa_query = SqlHelper.GetList("SELECT * FROM SEA_APPROVAL_DISCOUNT_MATRIX WHERE ProposalType='{}' and LimitType='{}' and LanguageKey = '{}'".format(lc_trans_type, lc_cspa, lv_LanguageKey))  #added by ishika #modified by aditi 15Jan
        if cspa_query:
            for cspa_row in cspa_query:
                # ccc = cspa_row
                # Trace.Write("1yyyyyyyyy"+str(qmm))
                # Trace.Write("csrow"+str(cspa_row.MinimumLimit)+" "+str(cspa_row.MaximumLimit)+" "+str(cspa_row.MinimumLimit))
                if float(qmargin) >= float(cspa_row.MinimumLimit) and float(qmargin) < float(cspa_row.MaximumLimit):
                    # Trace.Write("1yyyyyyyyy"+str(qmm))
                    if qsell_price >= float(cspa_row.MinimumSellPrice) and qsell_price < float(cspa_row.MaximumSellPrice):
                        Log.Info('106---')
                        # Trace.Write("csrow1"+str(cspa_row.MinimumLimit)+" "+str(cspa_row.MaximumLimit)+" "+str(cspa_row.MinimumSellPrice)+" "+str(cspa_row.MaximumSellPrice))
                        #if cspa_row.ApprovalLevel.startswith('Auto'):
                        if cspa_row.ApprovalLevel.startswith(lc_Auto): #Added by ishika
                            context.Quote.GetCustomField('CF_APPROVAL_LEVEL').Value = 0
                        else:
                            context.Quote.GetCustomField('CF_APPROVAL_LEVEL').Value = float(cspa_row.ApprovalLevel[1:])
                        maxApproval = cspa_row.ApprovalLevel
    else:
        if context.Quote.GetCustomField('CF_Quote_Type') != lc_partsOnly: #added by aditi 15Jan
            # diffBuyM_query = SqlHelper.GetList("SELECT * FROM SEA_APPROVAL_DISCOUNT_MATRIX WHERE LimitType='Discount'")   #Commented by ishika
            diffBuyM_query = SqlHelper.GetList("SELECT * FROM SEA_APPROVAL_DISCOUNT_MATRIX WHERE QuoteType!='{}' and LimitType='{}' and LanguageKey = '{}'".format(lc_partsOnly, lc_Discount, lv_LanguageKey))  #Added by ishika #modified by aditi 15Jan
            #Trace.Write("not_PO")
            if diffBuyM_query:
                for diffB_row in diffBuyM_query:
                    # Trace.Write("1nnnnnnnnn")
                    if float(qdisc_var) > float(diffB_row.MinimumLimit) and float(qdisc_var) <= float(diffB_row.MaximumLimit):
                        if float(qsell_price) >= float(diffB_row.MinimumSellPrice) and float(qsell_price) < float(
                                diffB_row.MaximumSellPrice):
                            # Trace.Write("nnnnnnnnn")
                            #if diffB_row.ApprovalLevel.startswith('Auto'):  #Commented by ishika
                            if diffB_row.ApprovalLevel.startswith(lc_Auto): #Added by ishika
                                context.Quote.GetCustomField('CF_APPROVAL_LEVEL').Value = 0
                            else:
                                context.Quote.GetCustomField('CF_APPROVAL_LEVEL').Value = float(diffB_row.ApprovalLevel[1:])
                            maxApproval = diffB_row.ApprovalLevel
        elif context.Quote.GetCustomField('CF_Quote_Type') == lc_partsOnly: #added by aditi 15Jan
            # diffBuyM_query = SqlHelper.GetList("SELECT * FROM SEA_APPROVAL_DISCOUNT_MATRIX WHERE LimitType='Discount'")   #Commented by ishika
            diffBuyM_query = SqlHelper.GetList("SELECT * FROM SEA_APPROVAL_DISCOUNT_MATRIX WHERE QuoteType='{}' and LimitType='{}' and LanguageKey = '{}'".format(lc_partsOnly, lc_Discount, lv_LanguageKey))  #Added by ishika
            if diffBuyM_query:
                for diffB_row in diffBuyM_query:
                    # Trace.Write("1nnnnnnnnn")
                    if float(qdisc_var) > float(diffB_row.MinimumLimit) and float(qdisc_var) <= float(diffB_row.MaximumLimit):
                        if float(qsell_price) >= float(diffB_row.MinimumSellPrice) and float(qsell_price) < float(
                                diffB_row.MaximumSellPrice):
                            # Trace.Write("nnnnnnnnn")
                            #if diffB_row.ApprovalLevel.startswith('Auto'):  #Commented by ishika
                            if diffB_row.ApprovalLevel.startswith(lc_Auto): #Added by ishika
                                context.Quote.GetCustomField('CF_APPROVAL_LEVEL').Value = 0
                            else:
                                context.Quote.GetCustomField('CF_APPROVAL_LEVEL').Value = float(diffB_row.ApprovalLevel[1:])
                            maxApproval = diffB_row.ApprovalLevel
    return maxApproval


def quote_currency_conversion(USD_value, ToCurrencyCode):
    #Conversion_Rate = SqlHelper.GetFirst(
        #"SELECT * FROM CT_EXCHANGE_RATE WHERE FROM_CURRENCY= '{}' and TO_CURRENCY= '{}' ORDER BY DATE DESC ".format(
            #ToCurrencyCode, 'USD'))  #Commneted by Ishika
    Conversion_Rate = SqlHelper.GetFirst(
        "SELECT * FROM CT_EXCHANGE_RATE WHERE FROM_CURRENCY= '{}' and TO_CURRENCY= '{}' ORDER BY DATE DESC ".format(
            lc_USD,ToCurrencyCode))  #Added by Dhruv #Modified by Aditi 22 Nov

    Value = USD_value / round(Conversion_Rate.RATE,2) #Modified by Aditi 22 Nov
    return Value

#if (context.Quote.GetCustomField('CF_Opportunity_Type').Value) == lc_op_type: #Added by Ishika  #commented by Aditi 1st Nov 2022
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #added by Aditi 1st Nov 2022
    now = datetime.datetime.now()
    date = now.strftime("%y/%m/%d")

    CurrencyCode = context.Quote.GetCustomField('CF_Quote_Currency').Value #context.Quote.SelectedMarket.CurrencyCode

    #Modified by dhurga start
    if str(get_user_type).upper() == "SALES":
        summaryInfoTable = SqlHelper.GetList("SELECT * FROM CT_FinancialSummary_Info where Summary_Info not in ('Margin Amount','Margin %') and LanguageKey = '{}'".format(lv_LanguageKey)) #Added by ishika
    else:
        summaryInfoTable = SqlHelper.GetList("SELECT * FROM CT_FinancialSummary_Info where LanguageKey = '{}'".format(lv_LanguageKey)) #Modified by dhurga end
    finSummTable = context.Quote.QuoteTables["Financial_Summary"]
    finSummTable.Rows.Clear()

    actualRecomSellP = 0
    totFpValue = 0
    totLabValue = 0
    fppcontent = 0
    labcontent = 0
    totQuoteValue = 0
    totalSellPrice = 0
    totalRecomSellP = 0
    actualDiscount_amt = 0
    totMarginValue = 0
    totMarginPer = 0
    actualDiscount_pct = 0
    counter = 0
    for qitem in context.Quote.GetAllItems():
        #Log.Write("MandatoryCH1: "+str(qitem.PartNumber)+str(qitem.NetPrice))
        if qitem.DiscountAmount != None and qitem.NetPrice != None and qitem["QI_Recommended_Unit_Sell_Price"] != None and qitem["QI_MARGIN_PERCENTAGE"] != None and qitem["QI_Recommended_Sell_Price"] != None and qitem['QI_Product_Type'] != 'Write-In' and qitem['QI_Product_Type'] != '' and qitem.IsOptional == False and qitem.ProductSystemId != 'RQ_Mandatory_Charges_cpq': #Modified by Aditi 23rd Dec 
            totQuoteValue += qitem["QI_List_Price_Total"]  # qitem.ExtendedListPrice
            totalSellPrice += qitem.NetPrice
            #Log.Write("MandatoryCH2: "+str(qitem.PartNumber)+str(qitem.NetPrice))
            actualDiscount_amt += qitem.DiscountAmount * qitem.Quantity
            recunitSellP = qitem["QI_Recommended_Unit_Sell_Price"]
            actualRecomSellP += recunitSellP
            totalRecomSellP += qitem["QI_Recommended_Sell_Price"]
            totMarginValue += qitem["QI_MARGIN_AMOUNT"]
            # totMarginPer += qitem["QI_MARGIN_PERCENTAGE"]
            counter += 1
    
    if totQuoteValue:
        context.Quote.GetCustomField('CF_Total_List_Price').Value = totQuoteValue

    if totMarginValue:
        context.Quote.GetCustomField('CF_Margin_Amount').Value = totMarginValue
    
    if counter != 0 and totalRecomSellP != 0: #modified by Aditi 18 Jan 2023
        actualDiscount_pct = float((actualDiscount_amt / totalRecomSellP) * 100)
    if counter != 0 and totalSellPrice != 0: #modified by Aditi 18 Jan 2023
        totMarginPer = (totMarginValue / totalSellPrice) * 100
        context.Quote.GetCustomField('CF_Gross_Margin').Value = round((totMarginPer), 2)
        # totMarginValue = totMarginValue / counter

    for entry in summaryInfoTable:
        row = finSummTable.AddNewRow()
        row['Summary'] = entry.Summary_Info

        #if entry.Summary_Info == "Quote List Price":  #Commented by Ishika
        if entry.Summary_Info == lc_quote_list_price: #Added by Ishika
            #row["USD_Currency"] = 'USD' + " " + str(int(quote_currency_conversion(totQuoteValue, CurrencyCode)))  #Commented by Ishika
            row["USD_Currency"] = lc_USD + " " + str(round(quote_currency_conversion(totQuoteValue, CurrencyCode),2))  #Added by Ishika
            row["Quote_Currency"] = CurrencyCode + " " + str(round(totQuoteValue,2))

        #if entry.Summary_Info == "Quote Sell Price": #Commented by Ishika
        if entry.Summary_Info == lc_quote_sell_price: #Added by Ishika
            #row["USD_Currency"] = 'USD' + " " + str(int(quote_currency_conversion(totalSellPrice, CurrencyCode)))  #Commented by Ishika
            row["USD_Currency"] = lc_USD + " " + str(round(quote_currency_conversion(totalSellPrice, CurrencyCode),2)) #Added by Ishika
            row["Quote_Currency"] = CurrencyCode + " " + str(round(totalSellPrice,2))
        # if entry.Summary_Info == "Highest Approval Level Required":
        # row["Quote_Currency"] = "TBD"

        #if entry.Summary_Info == "Margin %": #Commented by Ishika
        if entry.Summary_Info == lc_margin_perc: #Added by Ishika
            row["Quote_Currency"] = str(round((totMarginPer), 2)) + "%"

        # if entry.Summary_Info == "Discount Variance %":
        # row["Quote_Currency"] = str(calculate_discVar())

        #if entry.Summary_Info == "Margin Amount": #Commneted by Ishika
        if entry.Summary_Info == lc_margin_amount:  #Added by Ishika
            #row["USD_Currency"] = 'USD' + " " + str(int(quote_currency_conversion(totMarginValue, CurrencyCode)))  #Commented by Ishika
            row["USD_Currency"] = lc_USD + " " + str(round(quote_currency_conversion(totMarginValue, CurrencyCode),2)) #Added by Ishika
            row["Quote_Currency"] = CurrencyCode + " " + str(round(totMarginValue,2))

        #if entry.Summary_Info == "Actual Quote Discount %": #Commneted by Ishika
        if entry.Summary_Info == lc_actual_quote_discount_perc:  #Added by Ishika
            row["Quote_Currency"] = str(round((actualDiscount_pct), 2)) + "%"


    pole = context.Quote.GetCustomField("CF_POLE").Value
    region = context.Quote.GetCustomField("CF_REGION").Value
    solnfamily = context.Quote.GetCustomField("CF_Solution Family").Value
    vertical = context.Quote.GetCustomField("CF_Vertical Market").Value
    country = context.Quote.GetCustomField("CF_Country").Value				#Insert By Dhruv CXCPQ-35217

    # Trace.Write("CustomValues:"+str(pole)+","+str(region)+","+str(solnfamily)+","+str(vertical))

    totFpValue = 0
    totLabValue = 0
    fppcontent = 0
    labcontent = 0
    totQuoteValue = 0

    q_items = context.Quote.GetAllItems()
    if len(q_items) > 0:
        for qitem in context.Quote.GetAllItems():
            # Aditi: 6th Oct: Product type will be Honeywell Hardware instead of First party material, so modified the condition
            #if qitem.ProductTypeName == 'First Party Material' or qitem.ProductTypeName == 'Honeywell Hardware': #Commented by Ishika
            if qitem.IsOptional == False and qitem['QI_Product_Type'] != 'Write-In' and qitem['QI_Product_Type'] != '' and qitem.ProductSystemId != 'RQ_Mandatory_Charges_cpq': #Added by Aditi 23rd Dec
                if qitem.ProductTypeName == lc_fp_material or qitem.ProductTypeName == lc_honeywell_hardware: #Added by Ishika
                    totFpValue += qitem.NetPrice
            #elif qitem.ProductTypeName == 'Labor':  #Commented by Ishika
                elif qitem.ProductTypeName == lc_labor or qitem.ProductTypeName == lc_honeywell_labor:  #Added by Ishika  #Modified by Aditi 22nd Dec 2022
                    totLabValue += qitem.NetPrice
                totQuoteValue += qitem.NetPrice
        # Trace.Write("TotalFP:"+" "+str(round(totFpValue))+" "+"TotalLab:"+" "+str(totLabValue)+" "+"TotalQuote:"+" "+str(totQuoteValue))

        if totQuoteValue != 0:
            fppcontent = round((totFpValue / totQuoteValue) * 100)
            labcontent = round((totLabValue / totQuoteValue) * 100)
        # Trace.Write("FPP Content Value: "+str(fppcontent))
        # Trace.Write("Lab Content Value: "+str(labcontent))

        #if pole:								#Commented By Dhruv CXCPQ-35217
            #if region and solnfamily:			#Commented By Dhruv CXCPQ-35217
        if country:								#Inserted By Dhruv CXCPQ-35217
            if solnfamily:						#Inserted By Dhruv CXCPQ-35217
                if vertical:
                    # primaryVerQry = query to fetch recm discount with vertical from primary table where pole, region, solnfamily and vertical match
                    '''primaryVerQry = SqlHelper.GetList(
                        "SELECT * FROM CT_Primary_Recommendations WHERE Pole='{}' AND Region='{}' AND SolutionFamily='{}' AND Vertical='{}'".format(
                        pole, region, solnfamily, vertical))''' #Commenetd by ishika
                    '''primaryVerQry = SqlHelper.GetList(
                        "SELECT * FROM CT_Primary_Recommendations WHERE Pole='{}' AND Region='{}' AND SolutionFamily='{}' AND Vertical='{}' and LanguageKey = '{}'".format(
                            pole, region, solnfamily, vertical, lv_LanguageKey)) #Added by ishika''' #Commented By Dhruv CXCPQ-35217
                    primaryVerQry = SqlHelper.GetList("SELECT * FROM CT_Primary_Recommendations WHERE Country='{}' AND SolutionFamily='{}' AND Vertical='{}' and LanguageKey = '{}'".format(country, solnfamily, vertical, lv_LanguageKey)) #Inserted by Dhruv CXCPQ-35217
                    # Trace.Write("PrimmmVer: "+str(primaryVerQry))
                    if primaryVerQry:
                        matched = False
                        for entry in primaryVerQry:
                            # Trace.Write("PrimmmEntry: "+str(entry))
                            if fppcontent >= entry.FPPContentLowRange and fppcontent <= entry.FPPContentHighRange and labcontent >= entry.LaborContentLowRange and labcontent <= entry.LaborContentHighRange:
                                # Trace.Write("fppLabConditionSatisfied1: "+str(entry.FPPContentLowRange)+","+str(entry.FPPContentHighRange)+" and "+str(entry.LaborContentLowRange)+","+str(entry.LaborContentHighRange))
                                matched = True
                                for fin_row in finSummTable.Rows:
                                    #if fin_row['Summary'] == 'Maximum Discount % Recommended':     #Commeneted by Ishika
                                    if fin_row['Summary'] == lc_max_disc_per_recommended:   #Added by Ishika
                                        # Trace.Write("Found "+str(fin_row['Summary'])+str(entry.NewDiscPercentRecomm))
                                        fin_row['Quote_Currency'] = str(entry.NewDiscPercentRecomm) + "%"
                                        # Trace.Write("MaxDiscount: "+str(fin_row['Quote_Currency']))
                        if not matched:
                            '''secondaryQry = SqlHelper.GetList(
                                "SELECT * FROM CT_Secondary_Recommendations WHERE SC_Pole='{}'".format(pole))''' #Commented by ishika
                            '''secondaryQry = SqlHelper.GetList(
                                "SELECT * FROM CT_Secondary_Recommendations WHERE SC_Pole='{}' and LanguageKey = '{}'".format(pole, lv_LanguageKey))  #Added by ishika'''	#Commented By Dhruv CXCPQ-35217
                            secondaryQry = SqlHelper.GetList(
                                "SELECT * FROM CT_Secondary_Recommendations WHERE Country='{}' and LanguageKey = '{}'".format(country, lv_LanguageKey))  #Inserted by Dhruv CXCPQ-35217
                            # Trace.Write("SecondaryVer: "+str(secondaryQry))
                            if secondaryQry:
                                for entry in secondaryQry:
                                    # Trace.Write("secondaryEntry: "+str(entry))
                                    if fppcontent >= entry.SC_FPPContentLowRange and fppcontent <= entry.SC_FPPContentHighRange:
                                        # Trace.Write("fppConditionSatisfied1: "+str(entry.SC_FPPContentLowRange)+","+str(entry.SC_FPPContentHighRange))
                                        for fin_row in finSummTable.Rows:
                                            #if fin_row['Summary'] == 'Maximum Discount % Recommended':   #Commented by Ishika
                                            if fin_row['Summary'] == lc_max_disc_per_recommended:  #Added by Ishika
                                                # Trace.Write("Sec Found "+str(fin_row['Summary'])+str(entry.SC_NewDiscPercentRecomm))
                                                fin_row['Quote_Currency'] = str(entry.SC_NewDiscPercentRecomm) + "%"
                                                # Trace.Write("MaxDiscount: "+str(fin_row['Quote_Currency']))
                    else:
                        '''secondaryQry = SqlHelper.GetList(
                            "SELECT * FROM CT_Secondary_Recommendations WHERE SC_Pole='{}'".format(pole))''' #Commented by ishika
                        '''secondaryQry = SqlHelper.GetList(
                                "SELECT * FROM CT_Secondary_Recommendations WHERE SC_Pole='{}' and LanguageKey = '{}'".format(pole, lv_LanguageKey))  #Added by ishika'''	#Commented By Dhruv CXCPQ-35217
                        secondaryQry = SqlHelper.GetList(
                                "SELECT * FROM CT_Secondary_Recommendations WHERE Country='{}' and LanguageKey = '{}'".format(country, lv_LanguageKey))  #Inserted by Dhruv CXCPQ-35217
                        # Trace.Write("SecondaryVer: "+str(secondaryQry))
                        if secondaryQry:
                            for entry in secondaryQry:
                                # Trace.Write("secondaryEntry: "+str(entry))
                                if fppcontent >= entry.SC_FPPContentLowRange and fppcontent <= entry.SC_FPPContentHighRange:
                                    # Trace.Write("fppConditionSatisfied1: "+str(entry.SC_FPPContentLowRange)+","+str(entry.SC_FPPContentHighRange))
                                    for fin_row in finSummTable.Rows:
                                        #if fin_row['Summary'] == 'Maximum Discount % Recommended':   #Commented by Ishika
                                        if fin_row['Summary'] == lc_max_disc_per_recommended:  #Added by Ishika
                                            # Trace.Write("Sec Found "+str(fin_row['Summary'])+str(entry.SC_NewDiscPercentRecomm))
                                            fin_row['Quote_Currency'] = str(entry.SC_NewDiscPercentRecomm) + "%"
                                            # Trace.Write("MaxDiscount: "+str(fin_row['Quote_Currency']))
                else:
                    # primaryQry = query to fetch recm discount without vertical from primary table where pole, region, solnfamily match
                    '''primaryQry = SqlHelper.GetList(
                        "SELECT * FROM CT_Primary_Recommendations WHERE Pole='{}' AND Region='{}' AND SolutionFamily='{}'".format(
                            pole, region, solnfamily))''' #Commented by ishika
                    '''primaryQry = SqlHelper.GetList(
                        "SELECT * FROM CT_Primary_Recommendations WHERE Pole='{}' AND Region='{}' AND SolutionFamily='{}' and LanguageKey = '{}'".format(
                            pole, region, solnfamily, lv_LanguageKey))   #Added by ishika''' #Commented By Dhruv CXCPQ-35217
                    primaryQry = SqlHelper.GetList(
                        "SELECT * FROM CT_Primary_Recommendations WHERE Country='{}' AND SolutionFamily='{}' and LanguageKey = '{}'".format(
                            country, solnfamily, lv_LanguageKey))   #Inserted by Dhruv CXCPQ-35217
                    # Trace.Write("PrimmmNonVer: "+str(primaryQry))
                    if primaryQry:
                        matched = False
                        for entry in primaryQry:
                            # Trace.Write("PrimmmNonVerEntry: "+str(entry))
                            if fppcontent >= entry.FPPContentLowRange and fppcontent <= entry.FPPContentHighRange and labcontent >= entry.LaborContentLowRange and labcontent <= entry.LaborContentHighRange:
                                # Trace.Write("fppLabConditionSatisfied2: "+str(entry.FPPContentLowRange)+","+str(entry.FPPContentHighRange)+" and "+str(entry.LaborContentLowRange)+","+str(entry.LaborContentHighRange))
                                matched = True
                                for fin_row in finSummTable.Rows:
                                    #if fin_row['Summary'] == 'Maximum Discount % Recommended':   #Commented by Ishika
                                    if fin_row['Summary'] == lc_max_disc_per_recommended:    #Added by Ishika
                                        # Trace.Write("Found "+str(fin_row['Summary'])+str(entry.NewDiscPercentRecomm))
                                        fin_row['Quote_Currency'] = str(entry.NewDiscPercentRecomm) + "%"
                                        # Trace.Write("MaxDiscount: "+str(fin_row['Quote_Currency']))
                        if not matched:
                            '''secondaryQry = SqlHelper.GetList(
                                "SELECT * FROM CT_Secondary_Recommendations WHERE SC_Pole='{}' and LanguageKey = '{}'".format(pole, lv_LanguageKey))  # modified by ishika'''	#Commented By Dhruv CXCPQ-35217
                            secondaryQry = SqlHelper.GetList(
                                "SELECT * FROM CT_Secondary_Recommendations WHERE Country='{}' and LanguageKey = '{}'".format(country, lv_LanguageKey))  #Inserted by Dhruv CXCPQ-35217
                            # Trace.Write("SecondaryVer: "+str(secondaryQry))
                            if secondaryQry:
                                for entry in secondaryQry:
                                    # Trace.Write("secondaryEntry: "+str(entry))
                                    if fppcontent >= entry.SC_FPPContentLowRange and fppcontent <= entry.SC_FPPContentHighRange:
                                        # Trace.Write("fppConditionSatisfied2: "+str(entry.SC_FPPContentLowRange)+","+str(entry.SC_FPPContentLowRange))
                                        for fin_row in finSummTable.Rows:
                                            #if fin_row['Summary'] == 'Maximum Discount % Recommended':  #Commented by Ishika
                                            if fin_row['Summary'] == lc_max_disc_per_recommended:   #Added by Ishika
                                                # Trace.Write("Sec Found "+str(fin_row['Summary'])+str(entry.SC_NewDiscPercentRecomm))
                                                fin_row['Quote_Currency'] = str(entry.SC_NewDiscPercentRecomm) + "%"
                                                # Trace.Write("MaxDiscount: "+str(fin_row['Quote_Currency']))
            else:
                # query to fetch recm discount from secondary table
                '''secondaryQry = SqlHelper.GetList(
                    "SELECT * FROM CT_Secondary_Recommendations WHERE SC_Pole='{}'".format(pole))'''  #commented by ishika
                '''secondaryQry = SqlHelper.GetList(
                    "SELECT * FROM CT_Secondary_Recommendations WHERE SC_Pole='{}' and LanguageKey = '{}'".format(pole, lv_LanguageKey))  #Added by ishika''' #Commented By Dhruv CXCPQ-35217
                secondaryQry = SqlHelper.GetList(
                    "SELECT * FROM CT_Secondary_Recommendations WHERE Country='{}' and LanguageKey = '{}'".format(country, lv_LanguageKey))  #Inserted by Dhruv CXCPQ-35217
                # Trace.Write("SecondaryVer: "+str(secondaryQry))
                if secondaryQry:
                    for entry in secondaryQry:
                        # Trace.Write("secondaryEntry: "+str(entry))
                        if fppcontent >= entry.SC_FPPContentLowRange and fppcontent <= entry.SC_FPPContentHighRange:
                            # Trace.Write("fppConditionSatisfied3: "+str(entry.SC_FPPContentLowRange)+","+str(entry.SC_FPPContentLowRange))
                            for fin_row in finSummTable.Rows:
                                #if fin_row['Summary'] == 'Maximum Discount % Recommended':   #Commented by Ishika
                                if fin_row['Summary'] == lc_max_disc_per_recommended:  #Added By Ishika
                                    # Trace.Write("Sec Found "+str(fin_row['Summary'])+str(entry.SC_NewDiscPercentRecomm))
                                    fin_row['Quote_Currency'] = str(entry.SC_NewDiscPercentRecomm) + "%"
                                    # Trace.Write("MaxDiscount: "+str(fin_row['Quote_Currency']))
    maxRecDisc = 0
    actDisc = 0
    for fs_row1 in finSummTable.Rows:
        #if fs_row1['Summary'] == 'Maximum Discount % Recommended':   #Commented by Ishika
        if fs_row1['Summary'] == lc_max_disc_per_recommended:  #Added by Ishika
            if fs_row1['Quote_Currency']:
                maxRecDisc = float(fs_row1['Quote_Currency'][:-1])
                context.Quote.GetCustomField('CF_RecommendedDiscPer').Value = maxRecDisc
            else:
                context.Quote.GetCustomField('CF_RecommendedDiscPer').Value = 0
        #if fs_row1['Summary'] == 'Actual Quote Discount %':  #Commented by Ishika
        if fs_row1['Summary'] == lc_actual_quote_discount_perc:  #Added by Ishika
            if fs_row1['Quote_Currency']:
                actDisc = float(fs_row1['Quote_Currency'][:-1])
        #if fs_row1['Summary'] == 'Discount Variance %': #Commented by Ishika
        if fs_row1['Summary'] == lc_discount_variance_perc:  #Added by Ishika
            if maxRecDisc != None and actDisc != None:
                #fs_row1['Quote_Currency'] = actDisc - maxRecDisc   #commented by ishika 16dec
                fs_row1['Quote_Currency'] = round(actDisc - maxRecDisc, 2)   #Added by Ishika 16dec
                fs_row1['Quote_Currency'] = str(fs_row1['Quote_Currency']) + "%"
                # context.Quote.GetCustomField('CF_Discount_Variance').Value = actDisc - maxRecDisc   #commented by ishika 16dec
                context.Quote.GetCustomField('CF_Discount_Variance').Value = round(actDisc - maxRecDisc, 2)   #Added by Ishika 16dec

    qSellPrice = 0
    qDiscVar = 0
    qMargin = 0
    qBuyMethod = context.Quote.GetCustomField('CF_Buying_Method').Value
    for fs_row in finSummTable.Rows:
        #if fs_row['Summary'] == "Quote Sell Price":  #Commented by Ishika
        if fs_row['Summary'] == lc_quote_sell_price:  #Added by Ishika
            if fs_row['Quote_Currency']:
                qSellPrice = float(fs_row['Quote_Currency'][4:])
            if fs_row["USD_Currency"]:
                qSellPrice_USD = float(fs_row['USD_Currency'][4:])
        #if fs_row['Summary'] == "Discount Variance %":  #Commented by Ishika
        if fs_row['Summary'] == lc_discount_variance_perc:  #Added by Ishika
            if fs_row['Quote_Currency']:
                qDiscVar = float(str(fs_row['Quote_Currency'])[:-1])
        #if fs_row['Summary'] == "Margin %":  #Commented by Ishika
        if fs_row['Summary'] == lc_margin_perc:  #Added by Ishika
            if fs_row['Quote_Currency']:
                qMargin = float(fs_row['Quote_Currency'][:-1])

    maxApproval = getApprovalLevel(qBuyMethod, qSellPrice_USD, qDiscVar, qMargin)
    #Trace.Write("MAXappr:"+str(maxApproval))

    for fs_row in finSummTable.Rows:
        #if fs_row['Summary'] == "Highest Approval Level Required":  #Commented by Ishika
        if fs_row['Summary'] == lc_highest_approval_req:  #Added by Ishika
            fs_row['Quote_Currency'] = Translation.Get(maxApproval)			#Translation changes by Dhruv - 01.23.2023
        fs_row['Summary'] = Translation.Get(fs_row['Summary'])		#Translation change by Dhruv - 01.23.2023