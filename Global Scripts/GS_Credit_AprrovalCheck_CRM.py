# -----------------------------------------------------------------------------
#			Change History Log
# -----------------------------------------------------------------------------
# Description:
# Script for approval check CRM
# -----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
# -----------------------------------------------------------------------------
# 11/3/2022    sreenivasa mucharla    0          -initial version
# 11/6/2022    Ishika BHattacharya	  1        -Replaced Hardcodings
#										        -Incorporated Translation
# -----------------------------------------------------------------------------
import GM_TRANSLATIONS  # Added by krishna
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by krishna
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')  
lc_RQ_230 = GM_TRANSLATIONS.GetText('000024', lv_LanguageKey, '', '', '', '', '') 
lc_true = GM_TRANSLATIONS.GetText('000048', lv_LanguageKey, '', '', '', '', '')  
lc_false = GM_TRANSLATIONS.GetText('000068', lv_LanguageKey, '', '', '', '', '')  
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:
    Opportunity_Type = context.Quote.GetCustomField('CF_Opportunity_Type').Value
    sellprice = float( context.Quote.GetCustomField('CF_Total_Sell_Price').Value )
    if sellprice > 100000.00:
        context.Quote.GetCustomField('CFH_CreditCheck_Approval').Value = lc_true
    else:
        context.Quote.GetCustomField('CFH_CreditCheck_Approval').Value = lc_false
