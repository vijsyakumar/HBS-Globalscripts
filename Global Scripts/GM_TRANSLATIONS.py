#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#This module provides all functions relevent for translation purposes
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 09/26/2022	Dhruv Bhatnagar		0			Initial Creation
# 09/29/2022	Dhruv Bhatnagar		6			-Added function which returns
#												 User language from dictionary
#-----------------------------------------------------------------------------

#This function returns static/dynamic translation text/messages maintained in
#table CT_TRANSLATIONS for import parameters TranslationID, LanguageKey and dynamic variables(v1-v5)
def GetText(iv_transid,iv_language,iv_v1,iv_v2,iv_v3,iv_v4,iv_v5):
  lv_text = SqlHelper.GetFirst("select Text from CT_TRANSLATIONS WHERE TranslationID = '{}' and LanguageKey = '{}'".format(iv_transid,iv_language))
#  ev_text = str(lv_text.Text)
  ev_text = lv_text.Text
    
  if iv_v1:
    ev_text = ev_text.replace('<V1>',iv_v1)
  if iv_v2:
    ev_text = ev_text.replace('<V2>',iv_v2)
  if iv_v3:
    ev_text = ev_text.replace('<V3>',iv_v3)
  if iv_v4:
    ev_text = ev_text.replace('<V4>',iv_v4)
  if iv_v5:
    ev_text = ev_text.replace('<V5>',iv_v5)
  return ev_text

#Get User language key from dictionary
def GetLanguageKey(iv_user):
  ev_LanguageKey = ''
  lv_Dictionary = iv_user.SelectedDictionary.Name
  ev_LanguageKey = (SqlHelper.GetFirst("select LanguageKey from CT_MASTER_LANGUAGES where LanguageDictionary = '"+str(lv_Dictionary)+"'").LanguageKey)
  return 'EN' #ev_LanguageKey
