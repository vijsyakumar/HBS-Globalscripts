#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script remove the Product Upload container from quote cart items
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 8/2/2022      Anil                   0         -initial version
#
# 10/14/2022	Abhilash		       1		 -Replaced Hardcodings
#												 -Incorporated Translation
# 11/04/2022	Dhruv				   3		 -Transacrtion type
#												  check implemented
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_prodsys_Id = GM_TRANSLATIONS.GetText('000073', lv_LanguageKey, '', '', '', '', '')
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  #Modified by Dhruv
    lv_ItemId = 0 
    lv_uploadProductExist = False
    lt_products = context.Quote.GetAllItems()
    for ls_products in lt_products:
        
        #if ls_products.ProductSystemId == "Product_Upload_cpq":
        if ls_products.ProductSystemId == lc_prodsys_Id:
            lv_uploadProductExist = True
            lv_ItemId = ls_products.Id
            break
    if lv_uploadProductExist == True:
        context.Quote.DeleteItem(lv_ItemId)