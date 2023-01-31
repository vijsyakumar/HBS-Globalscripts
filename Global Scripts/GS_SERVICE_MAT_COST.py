#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for service material cost calculation
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 09/21/2022    Dhruv Bhatnagar            0             -Initial Version
# 10/18/2022    Ishika Bhattacharya        1             -Incorporated Translation
# 11/04/2022	Dhruv				   	   2		     -Transacrtion type
#												  		  check implemented
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)   # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  #Modified by Dhruv
    for i in context.Quote.GetAllItems():
        if i['QI_SAP_Activity_Type']:
            i['QI_Total_Cost'] = i['QI_TransferCost'] * i.Quantity