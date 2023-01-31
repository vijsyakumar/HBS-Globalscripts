import GM_TRANSLATIONS

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')
quote_status_ID = context.Quote.StatusId #Added by Aditi 14th Jan
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type and quote_status_ID==32: #Added by Aditi 14th Jan
    for item in context.Quote.GetAllItems():
        item['QI_Final_Sell_Price'] = item.NetPrice