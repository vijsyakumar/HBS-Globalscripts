#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script calculates the inflation facto
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 8/16/2022    Krishna Chaitanya         0          -Initial Version
# 10/18/2022   Ishika Bhattacharya       18         -Replaced Hardcodings
#                                                   -Incorporated Translation
# 10/22/2022   Aditi Sharma              19         -Replaced region with pole
# 11/04/2022   Srinivasan Dorairaj		 20			-Script and SQL Translation changes
# 11/13/2022   Aditi Sharma              23         -Changes for Lab and Mat default inflation
# 01/14/2023   Aditi Sharma                         -Added condition check for Preparing status
#-----------------------------------------------------------------------------




'''
context.Quote.GetCustomField('CF_Solution Family').Value = "BMS"
context.Quote.GetCustomField('CF_Opportunity_Type').Value = "Reactive Quoted (230)"
context.Quote.GetCustomField('CF_Country').Value = "Global"
context.Quote.GetCustomField('CF_LOB').Value = "Airport Service"
'''


import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Srinivasan Dorairaj
quote_status_ID = context.Quote.StatusId #Added by Aditi 14th Jan

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type and quote_status_ID==32: #Modified by Srinivasan Dorairaj #Modified by Aditi 14th Jan

    # lc_labor = "Labor"  # Commented by Ishika
    lc_labor = GM_TRANSLATIONS.GetText('000040', lv_LanguageKey, '', '', '', '', '') # Added by Ishika
    lc_honeywell_labor = GM_TRANSLATIONS.GetText('000118', lv_LanguageKey, '', '', '', '', '') #Added by Aditi 13 Nov
    # lc_first_party = "First Party Material"   # Commented by Ishika
    lc_first_party = GM_TRANSLATIONS.GetText('000020', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
    # lc_honeywell_hardware = "Honeywell Hardware"   # Commented by Ishika
    lc_honeywell_hardware = GM_TRANSLATIONS.GetText('000027', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
    opp_type = context.Quote.GetCustomField('CF_Opportunity_Type').Value
    country = context.Quote.GetCustomField('CF_Country').Value
    #region = context.Quote.GetCustomField('CF_REGION').Value #commented by Aditi 10/22/2022
    pole = context.Quote.GetCustomField('CF_POLE').Value #added by Aditi 10/22/2022

    #lob = context.Quote.GetCustomField('CF_LOB').Value

    for i in context.Quote.GetAllItems():
        #Trace.Write("----=====")
        pr_cost = i['QI_Total_Cost']
        #Trace.Write("d" +str(pr_cost))
        product_type = i.ProductTypeName
        part_nbr = i.PartNumber
        #Trace.Write("----"+str(pr_cost))
        if product_type == lc_first_party or product_type == lc_honeywell_hardware:
            #query = SqlHelper.GetFirst("SELECT * FROM CT_MATERIALS_CDE_VALIDATION WHERE Part_no = '{}'".format(part_nbr) ) #commented by Dhruv
            query = SqlHelper.GetFirst("SELECT * FROM CT_PRODUCT_HEADER WHERE PARTNUMBER = '{}'".format(part_nbr)) #Modified by Srinivasan Dorairaj

            if query:
                sol_fm = query.SOLUTION_FAMILY
                sm_text = SqlHelper.GetFirst("SELECT * FROM CT_SM_TEXT WHERE ID = '{}' and LanguageKey='{}'".format(sol_fm,lv_LanguageKey))
                if sm_text:
                    sol_fm = str(sm_text.Text)
                #Trace.Write("dc" +str(sol_fm))
                lv_parent = SqlHelper.GetFirst("SELECT PARENT FROM CT_SOLUTION_FAMILY WHERE SOLUTION_FAMILY = '{}' AND LanguageKey='{}'".format(sol_fm,lv_LanguageKey) ) #Modified by Srinivasan Dorairaj
                mat_query = SqlHelper.GetFirst("SELECT * FROM CT_INFLATION_FACTOR WHERE Opportunity_Type = '{}' and  Solution_Family = '{}' and Country = '{}' and Region = '{}' and LanguageKey='{}'".format(opp_type,lv_parent.PARENT,country,pole,lv_LanguageKey))		#Inserted by Dhruv #changed region to pole by Aditi 10/22/2022 #Modified by Srinivasan Dorairaj
                #mat_query = SqlHelper.GetFirst("SELECT * FROM CT_INFLATION_FACTOR WHERE Opportunity_Type = '{}' and  Solution_Family = '{}' and Country = '{}' and Region = '{}'".format(opp_type,sol_fm,country,region))		#Commented by Dhruv
                if mat_query:
                    #Trace.Write("material------")
                    mtr_fee = float(mat_query.Flat_Fee_Material)
                    mtr_fact = float(mat_query.Material_Inflation_percent)
                    #per_amount = (pr_cost) * (mtr_fact)/100
                    if pr_cost and mtr_fact:
                        mat_inflation_amount = float(pr_cost) * float(mtr_fact) / 100
                        if mat_inflation_amount <= mtr_fee:
                            i['QI_INFLATION_AMOUNT'] = mtr_fee
                            Trace.Write("MatFee" +str(i['QI_INFLATION_AMOUNT']))
                            i['QI_INFLATION_FACTOR'] = ''
                        elif mat_inflation_amount > mtr_fee:
                            i['QI_INFLATION_AMOUNT'] = mat_inflation_amount
                            i['QI_INFLATION_FACTOR'] = mtr_fact
                            #Trace.Write("AmountInf" +str(i['QI_INFLATION_AMOUNT']))
                #To fetch default Inflation if no record exists in table for material
                else:
                    mat_query = SqlHelper.GetFirst("SELECT * FROM CT_INFLATION_FACTOR WHERE Opportunity_Type = '{}' and Country = '{}' and Region = '{}' and LanguageKey='{}'".format(opp_type,country,pole,lv_LanguageKey))		#Inserted by Aditi 11/13/2022
                    if mat_query:
                        #Trace.Write("material------")
                        default_mtr_fact = float(mat_query.Default_Material_Inflation_percent)
                        if pr_cost and default_mtr_fact:
                            mat_inflation_amount = float(pr_cost) * float(default_mtr_fact) / 100
                            i['QI_INFLATION_AMOUNT'] = mat_inflation_amount
                            i['QI_INFLATION_FACTOR'] = default_mtr_fact
                            #Trace.Write("DefaultAmountInf" +str(i['QI_INFLATION_AMOUNT']))
            #To fetch default Inflation if no solution family exists for material
            else:
                mat_query = SqlHelper.GetFirst("SELECT * FROM CT_INFLATION_FACTOR WHERE Opportunity_Type = '{}' and Country = '{}' and Region = '{}' and LanguageKey='{}'".format(opp_type,country,pole,lv_LanguageKey)) #Added by aditi 11/13/2022
                if mat_query:
                    #Trace.Write("material------")
                    default_mtr_fact = float(mat_query.Default_Material_Inflation_percent)
                    if pr_cost and default_mtr_fact:
                        mat_inflation_amount = float(pr_cost) * float(default_mtr_fact) / 100
                        i['QI_INFLATION_AMOUNT'] = mat_inflation_amount
                        i['QI_INFLATION_FACTOR'] = default_mtr_fact
                        #Trace.Write("DefaultAmountInf" +str(i['QI_INFLATION_AMOUNT']))
        
        #Inflation factor for Labor
        elif product_type == lc_labor or product_type == lc_honeywell_labor:
            lab_query = SqlHelper.GetFirst("SELECT * FROM CT_INFLATION_FACTOR WHERE Opportunity_Type = '{}' and Country = '{}' and Region = '{}' and LanguageKey='{}'".format(opp_type,country,pole,lv_LanguageKey))		#Inserted by Dhruv
            #Trace.Write("Labbrr"+str(lab_query.Labor_inflation_percent))
            if lab_query:
                if lab_query.Labor_inflation_percent:
                    lbr_fact = float(lab_query.Labor_inflation_percent)
                elif lab_query.Default_Labor_inflation_percent:
                    lbr_fact = float(lab_query.Flat_Fee_Labor)
                #Trace.Write("Labbrr"+str(lbr_fact))
                if pr_cost and lbr_fact:
                    lab_inflation_amount = float(pr_cost) * float(lbr_fact) / 100
                    i['QI_INFLATION_AMOUNT'] = lab_inflation_amount
                    i['QI_INFLATION_FACTOR'] = lbr_fact
        
        #elif product_type == lc_third_party:				#Logic to be implemented once provided,no third party inflation story