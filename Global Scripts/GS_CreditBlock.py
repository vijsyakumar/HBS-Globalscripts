#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#Credit Block Booking check
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 09/14/2022	Sreenivas Mucharla	0			-Initial Creation
# 10/18/2022	Dhruv Bhatnagar		16			-Replaced Hardcodings
#				 								-Incorporated Translation
#-----------------------------------------------------------------------------
from Scripting.Quote import MessageLevel
import GM_TRANSLATIONS												#Added by Dhruv
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)				#Added by Dhruv
lc_msg1 = GM_TRANSLATIONS.GetText('000007', lv_LanguageKey, '', '', '', '', '')	#Added by Dhruv
lc_status_name = GM_TRANSLATIONS.GetText('000050', lv_LanguageKey, '', '', '', '', '')	#Added by Dhruv
lc_customercredit = GM_TRANSLATIONS.GetText('000048', lv_LanguageKey, '', '', '', '', '')#Added by Dhruv

def clearmsg():
    exitmsgs = context.Quote.Messages
    if exitmsgs.Count > 0:
        for msges in exitmsgs:
            #if  "True Booking is not allowed due to credit block on the Account" in str(msges.Content):	#Commented by Dhruv
            if  lc_msg1 in str(msges.Content):				#Added by Dhruv
                context.Quote.DeleteMessage(msges.Id)
#Log.Info("**** GS_CreditBlock is triggered ****")		    #Commented by Dhruv
context.Quote.GetCustomField('CF_TEST_RUN').Value = ""
#context.Quote.GetCustomField('CF_Customer_Credit').Value = "error"
customercredit = context.Quote.GetCustomField('CF_Customer_Credit').Value
creditcheck = context.Quote.GetCustomField('CF_Credit Check Required').Value
#Log.Info("**** GS_CreditBlock is triggered creditcheck****",str(creditcheck))	#Commented by Dhruv
if(creditcheck):
    creditcheck = creditcheck.lower()
    #Log.Info("**** GS_CreditBlock is triggered inside creditcheck****",str(creditcheck))	#Commented by Dhruv
    #if context.Quote.StatusName == "Customer Accepted" and (customercredit == "True"):		#Commented by Dhruv
        #Log.Info("**** GS_CreditBlock is triggered required condition met****",str(creditcheck))	#Commented by Dhruv
        #msg = 'True Booking is not allowed due to credit block on the Account'		#Commented by Dhruv
    if context.Quote.StatusName == lc_status_name and (customercredit == lc_customercredit):	#Added by Dhruv
        msg = lc_msg1		#Added by Dhruv
        clearmsg()
        context.Quote.AddMessage(msg,MessageLevel.Error,True)
    else:
        context.Quote.GetCustomField('CF_TEST_RUN').Value = ""
        clearmsg()