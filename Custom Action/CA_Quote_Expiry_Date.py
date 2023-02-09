#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
# Description:
# This script calculates the quotes expiry date and project start and end date in user format
#-----------------------------------------------------------------------------
# Date           Name                        Version      Comments(Changes done)
#-----------------------------------------------------------------------------
# 09/28/2022    Ishika Bhattacharya          0            -Initial Version
# 10/19/2022    Ishika Bhattacharya          2            -Replaced Hardcodings
#                                                         -Incorporated Translation
# 11/05/2022    Aditi Sharma                 3            -Correction for customer accepted condition
# 11/05/2022	Dhruv Bhatnagar			     4			  -Tranlation corrections
# 12/13/2022    Ishika Bhattacharya          5            -added a new method for converting date to user format
# 12/14/2022    Ishika bhattacharya          7            -added conditions to check if start and end date is not none
# 15/12/2022    Ishika Bhattacharya          8            -changed the date format to user settings date format
# 18/01/2023    Ishika Bhattacharya          13           -Changed expiry date format to static DD-MM-YY
# 19/01/2023    Ishika Bhattacharya          14           -Applied more validation checks
#-----------------------------------------------------------------------------
'''
Calulate the quote expiry date, which is "document generation date + quote validity". If the status is Customer Accepted, then use Expiration date field value directly. Else if, Expiration date field is blank, use the same above formula.
'''

import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
lc_status = GM_TRANSLATIONS.GetText('000050', lv_LanguageKey, '', '', '', '', '')   # Added by Ishika

from datetime import date, timedelta, datetime

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Modified by Dhruv
    def getQuoteExpiryDate():
        # EXPIRY DATE
        quote_expiry_date = ''
        document_generation_date = date.today()
        quote_Validity = context.Quote.GetCustomField('CF_Quote_Validity').Value
        if quote_Validity:
            quote_expiry_date = (document_generation_date + timedelta(days=float(quote_Validity))).strftime("%d-%b-%y")

        # QUOTE DATE
        DateCreated = context.Quote.DateCreated
        if DateCreated:
            getDateCreated= str(DateCreated.Day)+"/"+str(DateCreated.Month)+"/"+str(DateCreated.Year)
            QuoteDate = datetime.strptime(getDateCreated, "%d/%m/%Y").strftime("%d-%b-%y")
            context.Quote.GetCustomField('CF_Quote_Date').Value = QuoteDate

        Trace.Write('QUOTE DATE:{}, EXPIRY DATE:{}'.format(context.Quote.GetCustomField('CF_Quote_Date').Value, quote_expiry_date))
        return quote_expiry_date

    status = context.Quote.StatusName
    #if status == 'Customer Accepted':  #Commented by ishika
    if status == lc_status:   #Added by Ishika
        quote_expiry_date = context.Quote.GetCustomField('Quote Expiration Date').Value

        if quote_expiry_date:
            if Product:
                #quote_expiry_date =  str(Product.ParseString('<*CTX( Quote.CustomField(Quote Expiration Date).Format(dd/MM/yy) )*>'))
                get_QuoteEXPDate = datetime.strptime(str(Product.ParseString('<*CTX( Quote.CustomField(Quote Expiration Date).Format(dd/MM/yy) )*>')), "%d/%m/%y").strftime("%d-%b-%y")
                context.Quote.GetCustomField('Quote_Expiry_Date').Value = str(get_QuoteEXPDate) #corrected the variable name quote_expiry_date: Aditi 5th Nov
            else:
                expiry_date = getQuoteExpiryDate()
                context.Quote.GetCustomField('Quote_Expiry_Date').Value = str(expiry_date)

        else:
            expiry_date = getQuoteExpiryDate()
            context.Quote.GetCustomField('Quote_Expiry_Date').Value = str(expiry_date)

    else:
        expiry_date = getQuoteExpiryDate()
        context.Quote.GetCustomField('Quote_Expiry_Date').Value = str(expiry_date)

    def get_date_in_userFormat():
        startDate = context.Quote.GetCustomField('CF_Project Start Date').Value
        endDate = context.Quote.GetCustomField('CF_Project End Date').Value

        if startDate and endDate:
            date_start = UserPersonalizationHelper.CovertToDate(startDate)
            date_end = UserPersonalizationHelper.CovertToDate(endDate)

            xdate_start = UserPersonalizationHelper.ToUserFormat(date_start)
            xdate_end = UserPersonalizationHelper.ToUserFormat(date_end)

            context.Quote.GetCustomField('CF_Project_StartDate').Value = str(xdate_start)
            context.Quote.GetCustomField('CF_Project_EndDate').Value = str(xdate_end)
            Trace.Write('SD:{}, ED:{}'.format(context.Quote.GetCustomField('CF_Project_StartDate').Value,context.Quote.GetCustomField('CF_Project_EndDate').Value))

    get_date_in_userFormat()