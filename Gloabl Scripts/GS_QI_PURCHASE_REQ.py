# -----------------------------------------------------------------------------
#			Change History Log
# -----------------------------------------------------------------------------
# Description:
# this script is used for purchase request
# -----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
# -----------------------------------------------------------------------------
# 11/4/2022    sreenivasa mucharla    0          -initial version
# 11/6/2022    Ishika BHattacharya	  3	         -Replaced Hardcodings
#										         -Incorporated Translation
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------


import GM_TRANSLATIONS

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')
lc_pur_req_never = GM_TRANSLATIONS.GetText('000176', lv_LanguageKey, '', '', '', '', '')


if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type :
    for item in context.Quote.GetAllItems():
        item['QI_PURCHASE_REQ'] = lc_pur_req_never