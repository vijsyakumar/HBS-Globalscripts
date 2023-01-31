#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#SF Quote Status Sync
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 09/10/2022    Shweta Kandwal    	   0            -Initial Version
# 04/11/2022    Dhruv Bhatnagar        2            -Script translation changes
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS       #Added by Dhruv
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)          #Added by Dhruv
lc_approved_status = GM_TRANSLATIONS.GetText('000071', lv_LanguageKey, '', '', '', '', '')#Added by Dhruv
Quote_Statuses = context.Quote.GetCustomField('CF_SF_QUOTE_STATUS').Value

#context.Quote.ChangeStatus('Approved')	#Commented by Dhruv
context.Quote.ChangeStatus(lc_approved_status)	#Added by Dhruv