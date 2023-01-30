#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#It is not allowing the booking for the customers whose credit is blocked.
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
#  7/31/2022    Sumandrita Moitra     0             -Initial Version
# 10/17/2022    Isha Sharma           14            -Replaced Hardcodings
#                                                   -Incorporated Translation
##03/11/2022     Srijaydhurga         20            -Script translation changes
#-----------------------------------------------------------------------------
from Scripting.Quote import MessageLevel
import GM_TRANSLATIONS                                                                  #Added by Isha
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)									#Added by Isha
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') # Added by Dhurga
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Added by Dhurga

    lc_message = GM_TRANSLATIONS.GetText('000007', lv_LanguageKey, '', '', '', '', '')
    lc_accpeted = GM_TRANSLATIONS.GetText('000050', lv_LanguageKey, '', '', '', '', '')
    lc_true = GM_TRANSLATIONS.GetText('000048', lv_LanguageKey, '', '', '', '', '')
    lc_except = GM_TRANSLATIONS.GetText('000069', lv_LanguageKey, '', '', '', '', '')

    try:
        def clearmsg():
            exitmsgs = context.Quote.Messages
            if exitmsgs.Count > 0:
                for msges in exitmsgs:
                    message = lc_message                                                                           #Added by Krishna
                    #if  "Booking is not allowed due to credit block on the Account" in str(msges.Content):        #Commented by krishna
                    if  message in str(msges.Content):
                        context.Quote.DeleteMessage(msges.Id)
        #Log.Info("**** GS_Credit_Block is triggered ****")                                                       #Commented by Isha
        #context.Quote.GetCustomField('CF_Customer_Credit').Value = "error"                                        #Commented by Isha
        creditcheck = context.Quote.GetCustomField('CF_Customer_Credit').Value
        #Log.Info("**** GS_CreditBlock is triggered creditcheck****",str(creditcheck))                             #Commented by Isha
        if(creditcheck):
            creditcheck = creditcheck.lower()
            #Log.Info("**** GS_Credit_Block is triggered inside creditcheck****",str(creditcheck))                  #Commented by Isha
            #if context.Quote.StatusName == "Customer Accepted" and (creditcheck == "true" ):                        #Commented by Isha
            if context.Quote.StatusName == lc_accpeted and (creditcheck == lc_true ):                                 #Added by Isha
                #Log.Info("**** GS_Credit_Block is triggered required condition met****",str(creditcheck))           #Commented by Isha
                #msg = 'Booking is not allowed due to credit block on the Account'                                    #Commented by Isha
                msg = lc_message                                                                                       #Added by Isha
                clearmsg()
                context.Quote.AddMessage(msg,MessageLevel.Error,False)
            else:
                clearmsg()

    except Exception as ex:
        #Log.Error('Exception occurred:{}'.format(ex))									#Commented by Dhruv
        Log.Error(lc_except.format(ex))													#Inserted by Dhruv