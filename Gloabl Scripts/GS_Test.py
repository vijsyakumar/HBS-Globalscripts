#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#Tax value computed only for testing purpose - it will be fetched from ECC
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 9/28/2022      Sumandrita            0         -initial version
#
# 10/17/2022	Abhilash		       3		 -Replaced Hardcodings
#												 -Incorporated Translation
# 11/04/2022	Dhruv				   4		 -SQL translation,Transacrtion type
#												  check implemented
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS

#Get user launguage from dictionary
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  #Modified by Dhruv
    lc_prod_ty = GM_TRANSLATIONS.GetText('000065', lv_LanguageKey, '', '', '', '', '')

    for item in context.Quote.GetAllItems():
        #if item.ProductTypeName == "Third Party":
        if item.ProductTypeName == lc_prod_ty :
            break