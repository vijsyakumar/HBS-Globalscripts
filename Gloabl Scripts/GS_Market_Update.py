#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used to set the market(currency)
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 08/11/2022    Sumandrita Moitra          0             -Initial Version
# 10/18/2022    Ishika Bhattacharya        3             -Incorporated Translation
# 11/03/2022	Srinivasan Dorairaj		   5 			 - Script Translation changes
#-----------------------------------------------------------------------------


import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)   # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Added by Srinivasan Dorairaj
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Added by Srinivasan Dorairaj
    q_no =context.Quote.GetCustomField('CF_Quote Number').Value
    currency =context.Quote.GetCustomField('CF_Quote_Currency').Value

    obj = QuoteHelper.Get(q_no)
    obj.SetMarket(currency)