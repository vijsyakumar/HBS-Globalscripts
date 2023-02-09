#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is for changing the status
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 09/09/2022    Anil Poply                 0             -Initial Version
# 10/19/2022    Ishika Bhattacharya        2             -Replaced Hardcodings
#                                                        -Incorporated Translation
# 11/05/2022	Dhruv Bhatnagar			   3			 -Tranlation corrections
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
lc_status_preparing = GM_TRANSLATIONS.GetText('000018', lv_LanguageKey, '', '', '', '', '')   # Added by Ishika
lc_status_pending_orderConfirm = GM_TRANSLATIONS.GetText('000142', lv_LanguageKey, '', '', '', '', '')   # Added by Ishika
lc_message = GM_TRANSLATIONS.GetText('000002', lv_LanguageKey, '', '', '', '', '')   # Added by Ishika

def data_update(param):
    try:
        if Param.Status:
            if Param.Status == 1:
                #context.Quote.ChangeStatus('Pending Order Confirmation')   # Commented by Ishika
                context.Quote.ChangeStatus(lc_status_pending_orderConfirm)   # Added by Ishika
            if Param.Status == 2:
                #context.Quote.ChangeStatus('Preparing')  # Commented by Ishika
                context.Quote.ChangeStatus(lc_status_preparing)   # Added by Ishika
        else:
            # return "Please provide valid QuoteNumber"   # Commented by Ishika
            return lc_message   # Added by Ishika
    except Exception as ex:
        return ex.message

if len(Param)>0:
    data = data_update(Param)
    ApiResponse = ApiResponseFactory.JsonResponse(data)