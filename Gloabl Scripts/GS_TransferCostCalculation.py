#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for transfer cost calculation
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 08/18/2022    Aditi Sharma               0             -Initial Version
# 10/18/2022    Ishika Bhattacharya        18            -Incorporated Translation
# 11/04/2022	Dhruv				   	   19	 		 -SQL translation,Transacrtion type
#														  check implemented
# 01/14/2023   Aditi Sharma                              -Added condition check for Preparing status
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
quote_status_ID = context.Quote.StatusId #Added by Aditi 14th Jan

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type and quote_status_ID==32:  #Modified by Dhruv #Modified by Aditi 14th Jan
    lc_prod_type1 = GM_TRANSLATIONS.GetText('000027', lv_LanguageKey, '', '', '', '', '')
    lc_prod_type2 = GM_TRANSLATIONS.GetText('000118', lv_LanguageKey, '', '', '', '', '')
    #Log.Info("=== GS_TransferCostCalculation ====")
    lv_WTW_Factor = SqlHelper.GetFirst("SELECT WTW_FACTOR FROM CT_WTW_COST where LanguageKey='{}'".format(lv_LanguageKey)) #modified by Dhruv
    for qitem in context.Quote.GetAllItems():
        pr_type = qitem['QI_Product_Type']
        if qitem['QI_Unit_Cost_Base_Currency']:
            if qitem['QI_Exchange_Rate'] == 0:
                qitem['QI_TransferCost'] = qitem['QI_Unit_Cost_Base_Currency'] * 1
            else:
                qitem['QI_TransferCost'] = qitem['QI_Unit_Cost_Base_Currency'] * qitem['QI_Exchange_Rate']
                #qitem['QI_TransferCost'] = qitem['QI_Unit_Cost_Base_Currency'] * qitem['QI_Exchange_Rate']
            if qitem['QI_TransferCost'] and (pr_type == lc_prod_type1 or pr_type == lc_prod_type2) :
                #Trace.Write("Yes")
                qitem['QI_WTW_FACTOR']= lv_WTW_Factor.WTW_FACTOR
                qitem['QI_UNIT_WTW_COST'] = qitem['QI_TransferCost'] * float(lv_WTW_Factor.WTW_FACTOR)
                if qitem['QI_UNIT_WTW_COST']:
                    qitem['QI_WTW_COST'] = qitem['QI_UNIT_WTW_COST'] * qitem.Quantity