#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for Frieght amount calculation
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 08/19/2022    Aditi Sharma               0             -Initial Version
# 10/19/2022    Ishika Bhattacharya        2             -Replaced Hardcodings
#                                                        -Incorporated Translation
# 01/14/2023   Aditi Sharma                              -Added condition check for Preparing status and transaction type
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)   # Added by Ishika
lc_airport_RQ = GM_TRANSLATIONS.GetText('000061', lv_LanguageKey, '', '', '', '', '') # Added by Ishika
lc_RQ = GM_TRANSLATIONS.GetText('000024', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
lc_energy_RQ = GM_TRANSLATIONS.GetText('000062', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')
oppType = context.Quote.GetCustomField('CF_Opportunity_Type').Value
#allowedOppTypes = ['Airport Reactive Quoted (235)','Reactive Quoted (230)','Energy Reactive Quoted (230/252)']  #Commented by Ishika
allowedOppTypes = [lc_airport_RQ,lc_RQ,lc_energy_RQ]  #Added by Ishika
quote_status_ID = context.Quote.StatusId #Added by Aditi 14th Jan

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type and quote_status_ID==32: #Modified by Aditi 14th Jan
    for qitem in context.Quote.GetAllItems():
        if qitem['QI_Total_Cost'] and qitem['QI_FREIGHT_PERCENT']:
            qitem['QI_FREIGHT_AMOUNT'] = (qitem['QI_Total_Cost']*qitem['QI_FREIGHT_PERCENT'])/100