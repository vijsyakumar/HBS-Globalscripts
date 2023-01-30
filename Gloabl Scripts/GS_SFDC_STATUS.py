#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#Based on the conditions we are enabling the Request For Approval action button
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 8/26/2022     AshutoshKumar          0         -initial version
#
# 10/17/2022	Abhilash		       11		 -Replaced Hardcodings
#												 -Incorporated Translation
# 11/04/2022	Dhruv				   12		 -SQL translation,Transacrtion type
#												  check implemented
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  #Modified by Dhruv
    lc_expired = GM_TRANSLATIONS.GetText('000074', lv_LanguageKey, '', '', '', '', '')
    lc_rejected = GM_TRANSLATIONS.GetText('000075', lv_LanguageKey, '', '', '', '', '')
    lc_preparing = GM_TRANSLATIONS.GetText('000018', lv_LanguageKey, '', '', '', '', '')
    #context.Quote.GetCustomField("CF_SFDC_STATUS").Value = "Expired"
    #if context.Quote.StatusName == "Expired":
    if context.Quote.StatusName == lc_expired :
        #context.Quote.GetCustomField("CF_SFDC_STATUS").Value = "Expired"
        context.Quote.GetCustomField("CF_SFDC_STATUS").Value = lc_expired
    #elif context.Quote.StatusName == "Rejected":
    elif context.Quote.StatusName == lc_rejected:
        #context.Quote.GetCustomField("CF_SFDC_STATUS").Value = "Rejected"
        context.Quote.GetCustomField("CF_SFDC_STATUS").Value = lc_rejected
    #elif context.Quote.StatusName == "Preparing":
    elif context.Quote.StatusName == lc_preparing:
        #context.Quote.GetCustomField("CF_SFDC_STATUS").Value = "Preparing"
        context.Quote.GetCustomField("CF_SFDC_STATUS").Value = lc_preparing