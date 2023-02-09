#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for changing the status to preparing
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 07/11/2022    Sumandrita Moitra          0             -Initial Version
# 10/17/2022    Ishika Bhattacharya        3             -Replaced Hardcodings
#                                                        -Incorporated Translation
#
#-----------------------------------------------------------------------------


import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
lc_status = GM_TRANSLATIONS.GetText('000018', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika

# Status Change
#context.Quote.ChangeStatus('Preparing')  #Commented by Ishika
context.Quote.ChangeStatus(lc_status)   #Added by Ishika
context.Quote.GetCustomField('CF_APPROVAL_LEVEL').Value = ""