#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
# Identification of Transaction Type
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 08/09/2022	Anil Poply			0			-Initial Creation
# 11/04/2022	Dhruv Bhatnagar		2			-SQL translation,Transacrtion type
#												 check implemented
# 12/15 		Chirag Taneja		3			Addressing Defect 
#-----------------------------------------------------------------------------

#commented by Chirag 12/15
'''import GM_TRANSLATIONS
#Get user launguage from dictionary
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_lang_des = GM_TRANSLATIONS.GetText('000064', lv_LanguageKey, '', '', '', '', '')

try:
	_LanguageDescription = context.Quote.GetCustomField("CF_Language").AttributeValue
except:
    _LanguageDescription = lc_lang_des



if _LanguageDescription == "":
    _LanguageDescription = lc_lang_des

    
_LanguageKey = SqlHelper.GetFirst("SELECT * FROM CT_MASTER_LANGUAGES WHERE LanguageDescription = '{}'".format(_LanguageDescription))
if _LanguageKey:
    _OpportunityType = context.Quote.GetCustomField("CF_Opportunity_Type").Value
    _TransactionType = SqlHelper.GetFirst("SELECT * FROM CT_TRANSACTION_TYPE WHERE LanguageKey = '{0}' and OpportunityType = '{1}' ".format(_LanguageKey.LanguageKey, _OpportunityType))
    if _TransactionType:
        context.Quote.GetCustomField("CF_TRANSACTION_TYPE").Value = _TransactionType.TransactionType
''' 


_OpportunityType = context.Quote.GetCustomField("CF_Opportunity_Type").Value
_TransactionType = SqlHelper.GetFirst("SELECT * FROM CT_TRANSACTION_TYPE WHERE OpportunityType = '{0}' ".format(_OpportunityType))
if _TransactionType:
    context.Quote.GetCustomField("CF_TRANSACTION_TYPE").Value = _TransactionType.TransactionType
#End of change by Chirag 