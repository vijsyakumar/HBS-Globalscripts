#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for quote limit alert message
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 06/29/2022    Ayush Martin               0             -Initial Version
# 10/20/2022    Ishika Bhattacharya        22            -Replaced Hardcodings
#                                                        -Incorporated Translation
# 10/30/2022    Ishika Bhattacharya        28            -Replaced Hardcodings
#                                                        -Incorporated Translation
# 11/03/2022 	Srinivasan Dorairaj		   31			 -Script and SQL Translation changes
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS    # Added by Ishika
from Scripting.Quote import MessageLevel

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)   # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Srinivasan Dorairaj
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Modified by Srinivasan Dorairaj
    lc_is_String_in_message = GM_TRANSLATIONS.GetText('000161', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
    lc_USD = GM_TRANSLATIONS.GetText('000120', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika

    quote_type = context.Quote.GetCustomField('CF_Quote_Type').Value

    user_ctry = User.Country

    curr_sym = context.Quote.SelectedMarket.CurrencySign
    amount = context.Quote.GetCustomField('CF_Total_Sell_Price').Value #Replaced context.Quote.Totals.Amount: Aditi 19th Oct 2022
    quote_curr = context.Quote.GetCustomField('CF_Quote_Currency').Value
    exc_rate_query= ''
    query = SqlHelper.GetFirst("SELECT * FROM CT_Quote_Limit WHERE Country = '{}' AND Quote_Type = '{}'".format(user_ctry,quote_type))

    #exc_rate_query = SqlHelper.GetList("SELECT TOP 1 * FROM CT_EXCHANGE_RATE  WHERE FROM_CURRENCY = '{}' AND TO_CURRENCY = '{}' AND LanguageKey ='{}' ORDER BY [Date] Desc".format(from_curr,to_curr))
    limit_amnt_USD=0

    if query:
        limit_curr = query.Currency
        if limit_curr != lc_USD:  #Added by Ishika
        # if limit_curr!='USD': #Commented by Ishika
            exc_rate_query = SqlHelper.GetList("SELECT TOP 1 * FROM CT_EXCHANGE_RATE  WHERE FROM_CURRENCY = '{}' AND TO_CURRENCY = '{}' AND LanguageKey ='{}' ORDER BY [Date] Desc".format(limit_curr,'USD',lv_LanguageKey)) #Modified by Srinivasan Dorairaj
            if exc_rate_query:
                for er_qry in exc_rate_query:
                    us_ex_rate = er_qry.RATE
            limit_amnt_USD = query.Limit * round(us_ex_rate,2)
            exc_rate_query2 = SqlHelper.GetList("SELECT TOP 1 * FROM CT_EXCHANGE_RATE  WHERE FROM_CURRENCY = '{}' AND TO_CURRENCY = '{}' AND LanguageKey ='{}' ORDER BY [Date] Desc".format('USD',quote_curr,lv_LanguageKey)) #Modified by Srinivasan Dorairaj
            if exc_rate_query2 and limit_amnt_USD!=0:
                for er_qry2 in exc_rate_query2:
                    qc_ex_rate = er_qry2.RATE
            limit_amnt_qcurr = limit_amnt_USD * round(qc_ex_rate,2)
        else:
            exc_rate_query3 = SqlHelper.GetList("SELECT TOP 1 * FROM CT_EXCHANGE_RATE  WHERE FROM_CURRENCY = '{}' AND TO_CURRENCY = '{}' AND LanguageKey ='{}' ORDER BY [Date] Desc".format('USD',quote_curr,lv_LanguageKey)) #Modified by Srinivasan Dorairaj
            if exc_rate_query3:
                for er_qry3 in exc_rate_query3:
                    qc_ex_rate2 = er_qry3.RATE
            limit_amnt_qcurr = query.Limit * round(qc_ex_rate2,2)
        limit_amount = UserPersonalizationHelper.ToUserFormat(limit_amnt_qcurr)
        # Trace.Write("QLM: Limit Amount:"+str(limit_amount))
        #if query.Quote_Type  == str(quote_type) and float(amount) > float(limit_amnt_qcurr):
        if query.Quote_Type  == quote_type and float(amount) > float(limit_amnt_qcurr):
            #limAmount = str(quote_curr)+" "+str(limit_amount)
            limAmount = quote_curr+" "+limit_amount
            lc_message = GM_TRANSLATIONS.GetText('000011', lv_LanguageKey, limAmount, query.Quote_Type, '', '','')  # Added by Ishika
            #message = "Amount: '{} {}' value has exceeded for the quote type: {}".format(quote_curr,limit_amount,query.Quote_Type)
            message = lc_message    #Added by Ishika
            # Trace.Write("QLM: Limit Message:"+str(message))
            exitmsg = context.Quote.Messages
            if exitmsg.Count > 0:
                for msge in exitmsg:
                    # if "value has exceeded for the quote type" in str(msge.Content):   #Commented by Ishika
                    if lc_is_String_in_message in msge.Content:   #Added by Ishika
                        context.Quote.DeleteMessage(msge.Id)
            context.Quote.AddMessage(message,MessageLevel.Error,True)