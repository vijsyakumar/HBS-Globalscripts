#-----------------------------------------------------------------------------
#Description:
#This script is used for assigning date value to CF_Honeywell_Signed_Date
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 09/19/2022    KarthikRaj                 0             -Initial Version
# 10/19/2022    Ishika Bhattacharya        3             -Incorporated Translation
#
#-----------------------------------------------------------------------------
#import GM_TRANSLATIONS    # Added by Ishika
#lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User) # Added by Ishika

#from datetime import date
#from System import DateTime

#today = date.today()
#Trace.Write("today----->"+str(today))
#Aditi: 08 Oct 2022: Modified below format to lower case 'y' in "%d/%m/%y"
#tm = UserPersonalizationHelper.CovertToDate(str(today.strftime("%d/%m/%y")))
#context.Quote.GetCustomField('CF_Honeywell_Signed_Date').Value = tm

#CXCPQ-33427 start
import datetime
getdate = SqlHelper.GetFirst("SELECT GETDATE() as todaysdate")

context.Quote.GetCustomField('CF_Honeywell_Signed_Date').Value =getdate.todaysdate

#CXCPQ-33427 end