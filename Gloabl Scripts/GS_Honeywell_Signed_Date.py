#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script Assigns Customer Signed Date from Customer PO Date
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------

#12/19/2022    Srijaydhurga                1               -Date Validation
#-----------------------------------------------------------------------------
#cxcpq-34880 start
import GM_TRANSLATIONS    # Added by Ishika
import datetime
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  

getdate = SqlHelper.GetFirst("SELECT GETDATE() as todaysdate ")
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') 
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : 
    cust_sign_date = context.Quote.GetCustomField('CF_Honeywell_Signed_Date').Value
    if cust_sign_date != "":
        cust_sign_date = UserPersonalizationHelper.CovertToDate(context.Quote.GetCustomField('CF_Honeywell_Signed_Date').Value)
        if getdate.todaysdate >= cust_sign_date:
       		context.Quote.GetCustomField('CF_Honeywell_Signed_Date').Value = cust_sign_date
        else:
            context.Quote.GetCustomField('CF_Honeywell_Signed_Date').Value =getdate.todaysdate#cxcpq-34880 end
