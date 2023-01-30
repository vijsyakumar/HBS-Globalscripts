#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script remove the Product Upload container from quote cart items
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 9/25/2022     Shweta                 0         -initial version
#
# 10/14/2022	Abhilash		       1		 -Replaced Hardcodings
#												 -Incorporated Translation
# 11/04/2022	Dhruv				   9		 -SQL translation,Transacrtion type
#												  check implemented
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS

#Get user launguage from dictionary
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_cty_value = GM_TRANSLATIONS.GetText('000056', lv_LanguageKey, '', '', '', '', '')
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  #Modified by Dhruv
    #if context.Quote.GetCustomField('country').Value == "us":
    if context.Quote.GetCustomField('CF_Country').Value == lc_cty_value:

        
        context.Quote.GetCustomField('CF_US Tax 01').Value = context.Quote.GetCustomField('CF_USTax01').AttributeValueCode
        context.Quote.GetCustomField('CF_US Tax 02').Value = context.Quote.GetCustomField('CF_USTax02').AttributeValueCode
    else :
        context.Quote.GetCustomField('CF_US Tax 01').Value = ""
        context.Quote.GetCustomField('CF_US Tax 02').Value = ""