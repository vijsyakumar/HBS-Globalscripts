# -----------------------------------------------------------------------------
#			Change History Log
# -----------------------------------------------------------------------------
# Description:
# GS Booking
# -----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
# -----------------------------------------------------------------------------
# 9/2/2022    sreenivasa mucharla    0          -initial version
# 11/6/2022    Ishika BHattacharya	  16        -Replaced Hardcodings
#										        -Incorporated Translation
# -----------------------------------------------------------------------------
import GM_TRANSLATIONS  # Added by krishna
from Scripting.Quote import MessageLevel
import clr
from System.Net import HttpWebRequest
clr.AddReference("System.Xml")
import sys
from math import ceil
from System.Text import Encoding

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by krishna
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')  # Added by ishika

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  # Added by ishika
    lc_msg = GM_TRANSLATIONS.GetText('000194', lv_LanguageKey, '', '', '', '', '')  # Added by ishika

    def clear_error_message():
        exitmsgs = context.Quote.Messages
        if exitmsgs.Count > 0:
            for msges in exitmsgs:
                #if  "Booking percent is greater than 100 percent please check" in str(msges.Content):  #Commented by ishika
                if lc_msg in str(msges.Content):  #Added by ishika
                    context.Quote.DeleteMessage(msges.Id)
    try:
        #Log.Info("====GS_Book is triggered=====")
        Booking1= context.Quote.GetCustomField('CF_EID_1_Rate').Value
        Booking2= context.Quote.GetCustomField('CF_EID_2_Rate').Value
        Booking3= context.Quote.GetCustomField('CF_EID_3_Rate').Value
        Booking4= context.Quote.GetCustomField('CF_EID_4_Rate').Value
        Booking5= context.Quote.GetCustomField('CF_EID_5_Rate').Value
        if Booking1 is None or Booking1=="":
            Booking1 = 0.0
        if Booking2 is None or Booking2=="":
            Booking2 = "0.0"
        if Booking3 is None or Booking3=="":
            Booking3 = "0.0"
        if Booking4 is None or Booking4=="":
            Booking4 = "0.0"
        if Booking5 is None or Booking5=="":
            Booking5 = "0.0"
        finalbooking = float(Booking1)+float(Booking2)+float(Booking3)+float(Booking4)+float(Booking5)
        Log.Info("====GS_Book finalbooking=====",str(finalbooking))
        context.Quote.GetCustomField('CF_EID_Total_Rate').Value = str(finalbooking)
        Log.Info("*** GS_Book Total Booking value****",context.Quote.GetCustomField('CF_EID_Total_Rate').Value)
        if finalbooking > 100:
            #msg = "Booking percent is greater than 100 percent please check"  #Commented by ishika
            msg = lc_msg  #added by ishika
            """exitmsgs = context.Quote.Messages
            if exitmsgs.Count > 0:
                for msges in exitmsgs:
                    if  "Booking percent is greater than 100 percent please check" in str(msges.Content):
                        context.Quote.DeleteMessage(msges.Id)"""
            clear_error_message()
            #context.Quote.AddMessage(msg,MessageLevel.Error,False)
        else:
            clear_error_message()
    except Exception as ex:
        Log.Info("=== GS_Book exceptionoccured ===",str(ex))