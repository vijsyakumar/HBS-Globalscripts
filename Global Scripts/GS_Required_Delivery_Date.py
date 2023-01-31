#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script does not allow past dates on Required delivery date field
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 03/01/2023    Ishika Bhattacharya    0             -Initial Version
#
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS    # Added by Ishika
import datetime
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika

getdate = SqlHelper.GetFirst("SELECT GETDATE() as todaysdate ")

Trace.Write('getdate:{}'.format(getdate.todaysdate))

lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') 
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : 
    #date_today = UserPersonalizationHelper.ToUserFormat(getdate.todaysdate)
    #Trace.Write('date_today:{}'.format(date_today))

    required_delivery_date = context.Quote.GetCustomField('CF_Required_Delivery_Date').Value
    if required_delivery_date:
        req_delv_date = UserPersonalizationHelper.CovertToDate(required_delivery_date)
        #uf = UserPersonalizationHelper.ToUserFormat(req_delv_date)
        Trace.Write('delivery date:{}'.format(req_delv_date))

        #convert = UserPersonalizationHelper.CovertToDate(date_today)
        #Trace.Write('convert:{}'.format(convert))
        if req_delv_date < getdate.todaysdate:
            context.Quote.GetCustomField('CF_Required_Delivery_Date').Value = getdate.todaysdate
            context.Quote.AddMessage("Past date is not allowed for this field", MessageLevel.Error, False)