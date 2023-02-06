#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used to set the target sell price to user number format
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 12/27/2022    Aditi Sharma               0             -Initial Version
# 12/29/2022    Aditi Sharma               1             -Incorporated RQ check and translation
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:

    if context.Quote.GetCustomField('CF_Sell Price').Value:
        target_SP = float(context.Quote.GetCustomField('CF_Sell Price').Value)
        context.Quote.GetCustomField('CF_Sell Price').Value = UserPersonalizationHelper.ToUserFormat(target_SP)
        #Trace.Write("Target SP "+str(context.Quote.GetCustomField('CF_Sell Price').Value))