#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 09/08/2022    H513910                 0             -Initial Version
# 10/14/2022    Mounika Tarigopula      09       -Replaced Hardcodings
#                                                -Incorporated Translation
# 11/03/2022    Srinivasan Dorairaj     10       - Script Translation changes
#-----------------------------------------------------------------------------
#Begin of change by Mounika
import GM_TRANSLATIONS                   #Inserted by Mounika
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)    #Inserted by Mounika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Added by Srinivasan Dorairaj
lc_flag = GM_TRANSLATIONS.GetText('000048', lv_LanguageKey, '', '', '', '', '')
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Added by Srinivasan Dorairaj
	#context.Quote.GetCustomField("CF_Product_Active").Value= "True"
	context.Quote.GetCustomField("CF_Product_Active").Value = lc_flag                    #end of change by Mounika
	product = None
	for i in context.Quote.GetAllItems():
		lv_part = i.ProductId
		
		if lv_part:
			product = SqlHelper.GetFirst("select PRODUCT_ACTIVE from Products  where Product_ID = '"+str(lv_part)+"'")
			if product.PRODUCT_ACTIVE  == False:
				product_active= str(product.PRODUCT_ACTIVE)
				context.Quote.GetCustomField("CF_Product_Active").Value =str(product_active)
        	
        	
        