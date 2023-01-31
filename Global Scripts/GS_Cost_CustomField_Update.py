#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#Cost Calculation for transfer cost and total cost
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
#   9/6/2022    Sumandrita Moitra     0             -Initial Version
# 10/17/2022    Isha Sharma           46            -Replaced Hardcodings
#                                                   -Incorporated Translation
##03/11/2022    Srijaydhurga          48            -Script translation changes
# 04/11/2022    Sumandrita            49            -Added condition for Write_in parent
# 01/14/2023   Aditi Sharma                         -Added condition check for Preparing status
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS       #Added by Isha

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)           #Added by Isha

lc_prod_labor = GM_TRANSLATIONS.GetText('000118', lv_LanguageKey, '', '', '', '', '')     #Added by Isha
#lc_op_type = GM_TRANSLATIONS.GetText('000024', lv_LanguageKey, '', '', '', '', '')        #commneted by Dhurga
#if(context.Quote.GetCustomField('CF_Opportunity_Type').Value) == lc_op_type:  #commneted by Dhurga
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') # Added by Dhurga 000175
lc_write_in = GM_TRANSLATIONS.GetText('000175', lv_LanguageKey, '', '', '', '', '') #Added by Sumandrita
quote_status_ID = context.Quote.StatusId

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type and quote_status_ID==32: #Added by Dhurga #Modified by Aditi 14th Jan
    for i in context.Quote.GetAllItems():
        #if i.ProductTypeName == "Labor":  #commented by krishna
        if i.ProductTypeName == lc_prod_labor:     #Added by Krishna
            query_desc_type = SqlHelper.GetList("SELECT * FROM CT_ACTIVITY_TYPE WHERE Ser_Material = '{}' and LanguageKey='{}'".format(i.PartNumber,lv_LanguageKey))#Added by Dhurga
            if query_desc_type.Count>0:
                for qrytyp in query_desc_type:
                    i['QI_SAP_Activity_Type'] = str(qrytyp.SAP_Activity_Type)
                # Trace.Write("actvType111:"+str(i['QI_SAP_Activity_Type']))             Commented by Isha

        if i['QI_Unit_Cost_Base_Currency'] is not None and i['QI_Exchange_Rate'] is not None:
            #Trace.Write("baseAndExc:"+str(i['QI_Unit_Cost_Base_Currency'])+" "+str(i['QI_Exchange_Rate']))
            #Commented by Aditi 3rd Oct 2022, since CT_Thirdparty_Pricebook is no longer used, instead refer CT_TP_Price
            '''
            if i.ProductTypeName == "Third Party":
                part_nbr = i.PartNumber
                query_desc = SqlHelper.GetList("SELECT * FROM CT_Thirdparty_Pricebook WHERE Part_No = '"+str(part_nbr)+"' ")
                if query_desc:
                    for qry in query_desc:
                        #i['QI_Unit_Cost_Base_Currency'] = str(qry.Unit_Cost_Base_Currency)
                        if i['QI_Unit_Cost_Base_Currency']:
                            if i['QI_Exchange_Rate'] == 0:
                                i['QI_TransferCost'] = i['QI_Unit_Cost_Base_Currency'] * 1
                            else:
                                i['QI_TransferCost'] = i['QI_Unit_Cost_Base_Currency'] * i['QI_Exchange_Rate']
                            i['QI_Total_Cost'] = i['QI_TransferCost'] * (i.Quantity)

            if i.ProductTypeName == "First Party Material" or i.ProductTypeName == "Labor":
                part_nbr = i.PartNumber
                query_desc = SqlHelper.GetList("SELECT * FROM CT_MATERIALS_CDE_VALIDATION WHERE Part_no = '{}'".format(part_nbr))
                if query_desc:
                    for qry in query_desc:
                        #i['QI_Unit_Cost_Base_Currency'] = str(float(qry.Standard_Price)/float(qry.Price_Unit))
                        if i['QI_Unit_Cost_Base_Currency']:
                            if i['QI_Exchange_Rate'] == 0:
                                i['QI_TransferCost'] = i['QI_Unit_Cost_Base_Currency'] * 1
                            else:
                                i['QI_TransferCost'] = i['QI_Unit_Cost_Base_Currency'] * i['QI_Exchange_Rate']
                            i['QI_Total_Cost'] = i['QI_TransferCost'] * (i.Quantity)
                i['QI_Total_Cost'] = i['QI_TransferCost'] * (i.Quantity)
            '''
            #Comment End

            #Aditi: The below calculation will run for all product types
            if i['QI_Unit_Cost_Base_Currency']:
                if i['QI_Exchange_Rate'] == 0:
                    i['QI_TransferCost'] = i['QI_Unit_Cost_Base_Currency'] * 1
                else :
                    i['QI_TransferCost'] = i['QI_Unit_Cost_Base_Currency'] * i['QI_Exchange_Rate']
                if  i['QI_Product_Type'] != lc_write_in : #Added by Sumandrita
                    i['QI_Total_Cost'] = i['QI_TransferCost'] * (i.Quantity)
                    
            #Log.Info("=== GS_Cost_CustomField_Update Sell Price ====",str(i.NetPrice))
        if i.NetPrice and i['QI_WTW_COST']!=None:
            i['QI_WTW_Margin'] = i.NetPrice - i['QI_WTW_COST']
            #Log.Info("=== GS_Cost_CustomField_Update QI_WTW_Margin ====",str(i['QI_WTW_Margin']))
            #Log.Info("=== GS_Cost_CustomField_Update QI_WTW_COST ====",str(i['QI_WTW_COST']))