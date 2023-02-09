import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
#CXCPQ-35440 start
getdate = SqlHelper.GetFirst("SELECT GETDATE() as todaysdate ")
context.Quote.GetCustomField('CF_BOOK_TO_SAP_TIMESTRAP').Value = getdate.todaysdate
##CXCPQ-35440 end

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Modified by Dhruv
    context.Quote.GetCustomField('CF_Booking_Admin').Value = User.UserName