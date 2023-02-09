#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for displaying message as per the status as booked or 
#customer accpeted
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 10/12/2022    Shweta Kandwal             0             -Initial Version
# 10/19/2022    Ishika Bhattacharya        5             -Replaced Hardcodings
#                                                        -Incorporated Translation
# 11/05/2022	Dhruv Bhatnagar			   6			 -Tranlation corrections
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)   # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
lc_False = GM_TRANSLATIONS.GetText('000068', lv_LanguageKey, '', '', '', '', '') #Added by Dhruv
lc_status_booked = GM_TRANSLATIONS.GetText('000082', lv_LanguageKey, '', '', '', '', '')   # Added by Ishika
lc_status_CustAccepted = GM_TRANSLATIONS.GetText('000050', lv_LanguageKey, '', '', '', '', '')   # Added by Ishika

from Scripting.Quote import MessageLevel


if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Modified by Dhruv
    status = context.Quote.StatusName
    QuoteId = context.Quote.Id
    #Log.Info("Error Message --> "+str(status))
    message = ""
    #if status == 'Booked' or status == 'Customer Accepted' :  #Commented by Ishika
    if status == lc_status_booked or status == lc_status_CustAccepted :    # Added by Ishika
        query = SqlHelper.GetList("SELECT * FROM CT_ORDER_BOOKING_ERROR_LOGS WHERE QUOTE_ID = '"+str(QuoteId)+"' ")
        #insert in quotetable start
        order_booking_logs = context.Quote.QuoteTables["Order_Booking_Error"]
        
        for i in query:
            error_logs = order_booking_logs.AddNewRow()
            error_logs["PART_NUMBER"] = i.MESSAGE_CLASS
            error_logs["ITEM_NUMBER"] =i.MESSAGE_NUMBER
            error_logs["Error_Message"] = i.ERROR_TEXT
            message = message + str(i.ERROR_TEXT) + ". "
        context.Quote.AddMessage(message,MessageLevel.Warning,lc_False)