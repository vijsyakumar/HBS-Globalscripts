#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is being used for updating quote currency with opportunity currency.
#-----------------------------------------------------------------------------
# Date            Name                Version     Comments(Changes done)
#-----------------------------------------------------------------------------
# 07/01/2022    Abhilash                 0       -Initial Version
# 10/17/2022    Krishna Chaitanya        79      -Replaced Hardcodings
#                                                -Incorporated Translation
# 11/03/2022	Srinivasan Dorairaj		 18		 -Script Translation changes
# 12/01/2023    Ishika Bhattacharya      19      -Added a validation check at the start to prevent None Type Error
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Srinivasan Dorairaj

if context.Quote:
    opp_currency = context.Quote.GetCustomField('CF_Opportunity Currency').Value
    if opp_currency:
        if context.Quote.GetCustomField("CF_Quote_Currency").Value == "":
            context.Quote.GetCustomField("CF_Quote_Currency").Value = str(opp_currency)