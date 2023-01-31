#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for warranty duration calculation
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 08/11/2022    Ashutoshkumar Mishra       0             -Initial Version
# 10/18/2022    Ishika Bhattacharya        4             -Incorporated Translation
# 11/04/2022	Dhruv				   	   5			 -SQL translation,Transacrtion type
#												  		  check implemented
# 01/14/2023   Aditi Sharma                       -Added condition check for Preparing status
# 01/17/2023   Sumandrita                         -Modified RQ check 
#-----------------------------------------------------------------------------


import GM_TRANSLATIONS    # Added by Ishika

# Declaring variables "Added by Ishika
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
quote_status_ID = context.Quote.StatusId #Added by Aditi 14th Jan

if quote_status_ID==32:  #Modified by Dhruv #Modified by Aditi 14th Jan
    opp_country = context.Quote.GetCustomField('CF_Country').Value
    _OpportunityType = context.Quote.GetCustomField("CF_Opportunity_Type").Value
    _TransactionType = SqlHelper.GetFirst("SELECT * FROM CT_TRANSACTION_TYPE WHERE OpportunityType = '{0}' ".format(_OpportunityType))
    if _TransactionType.TransactionType == "RQ":

        if opp_country:
            query = SqlHelper.GetFirst("SELECT * FROM CT_WARRANTY_DURATION WHERE Country = '"+str(opp_country)+"' and LanguageKey = '"+str(lv_LanguageKey)+"'") #Modified by Dhruv

            if query.Warranty_Duration is not None:

                if context.Quote.GetCustomField('Warranty Duration(in months)').Value == "":
                    context.Quote.GetCustomField('Warranty Duration(in months)').Value = str(query.Warranty_Duration)
                #context.Quote.GetCustomField("CF_Quote Number").Value = str(query.Warranty_Duration)