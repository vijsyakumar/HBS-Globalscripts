#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script Assigns Customer Signed Date from Customer PO Date
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 08/06/2022    KarthikRaj                 0             -Initial Version
# 10/18/2022    Ishika Bhattacharya        3             -Incorporated Translation
#11/03/2022    Srijaydhurga                4               -Script Translation
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS    # Added by Ishika
import datetime
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika

getdate = SqlHelper.GetFirst("SELECT GETDATE() as todaysdate ")
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') # Added by Dhurga
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Added by Dhurga
    pdate = context.Quote.GetCustomField('CF_PO_Date').Value
    if pdate != "":
        po_date = UserPersonalizationHelper.CovertToDate(context.Quote.GetCustomField('CF_PO_Date').Value)
        
        xdate = UserPersonalizationHelper.ToUserFormat(po_date)
        if getdate.todaysdate >= po_date:
            
            
       		context.Quote.GetCustomField('CF_Customer_Signed_Date').Value = po_date
        else:
            context.Quote.GetCustomField('CF_PO_Date').Value =getdate.todaysdate
            po_reset_date = UserPersonalizationHelper.CovertToDate(context.Quote.GetCustomField('CF_PO_Date').Value)
            
            context.Quote.GetCustomField('CF_Customer_Signed_Date').Value = po_reset_date
