#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for GSA Approval message
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 9/26/2022     Payal Gupta                0             -Initial Version
# 10/17/2022    Ishika Bhattacharya        7             -Replaced Hardcodings
#                                                        -Incorporated Translation
# 11/04/2022	Srinivasan Dorairaj		   10			 -Script Translation changes
#-----------------------------------------------------------------------------


import GM_TRANSLATIONS    # Added by Ishika
from Scripting.Quote import MessageLevel

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Srinivasan Dorairaj
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Modified by Srinivasan Dorairaj
    # Declaring variables "Added by Ishika
    lc_US = GM_TRANSLATIONS.GetText('000056', lv_LanguageKey, '', '', '', '', '')
    lc_GSA = GM_TRANSLATIONS.GetText('000122', lv_LanguageKey, '', '', '', '', '')
    lc_0 = GM_TRANSLATIONS.GetText('000077', lv_LanguageKey, '', '', '', '', '')
    lc_GSA_approval_message = GM_TRANSLATIONS.GetText('000123', lv_LanguageKey, '', '', '', '', '')

    ###----- Getting values for Country and Buying Method -----###

    country = context.Quote.GetCustomField('CF_Country').Value
    buying_method = context.Quote.GetCustomField('CF_Buying_Method').Value

    ###----- Condition for checking country and buying method -----###

    # if country == 'US' and 'GSA' in buying_method:   "Commented by Ishika
    if country == lc_US and lc_GSA in buying_method:    #Added by Ishika

        ###----- Custom Field for mapping in SFDC -----###
        # context.Quote.GetCustomField('CF_GSA_Approval').Value = "0"    "Commented by Ishika
        context.Quote.GetCustomField('CF_GSA_Approval').Value = lc_0     # Added by Ishika

    ###----- Display message in quote for country 'US' and buying method 'GSA' -----###
        # message = "GSA Approval requested in NEX"   "Commented by Ishika
        message = lc_GSA_approval_message             #Added by Ishika
        exitmsg = context.Quote.Messages
        if exitmsg.Count > 0:
            for msg in exitmsg:
                if message in str(msg.Content):
                    context.Quote.DeleteMessage(msg.Id)
        context.Quote.AddMessage(message,MessageLevel.Warning,False)