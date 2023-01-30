#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 10/06/2022    Shweta Kandwal        0             -Initial Version
# 10/14/2022    Mounika Tarigopula    4           -Replaced Hardcodings
#                                                -Incorporated Translation
# 11/03/2022	Srinivasan Dorairaj	  5			 -Script Translation changes
#-----------------------------------------------------------------------------
#Begin of change by Mounika
import GM_TRANSLATIONS                   #Inserted by Mounika
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)    #Inserted by Mounika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Added by Srinivasan Dorairaj
lc_val = GM_TRANSLATIONS.GetText('000054', lv_LanguageKey, '', '', '', '', '')
lc_log = GM_TRANSLATIONS.GetText('000088', lv_LanguageKey, '', '', '', '', '')    #end of change by Mounika
#if context.Quote.GetCustomField('CF_Primary_Quote') == "Yes":
if context.Quote.GetCustomField('CF_Primary_Quote') == lc_val:
	context.Quote.GetCustomField('CF_PrimaryKey').Value = 0
else:
    context.Quote.GetCustomField('CF_PrimaryKey').Value = 1
#Log.Write(" +++ Primary Quote +++ ")               #commented by Mounika
Log.Write(lc_log)                                   #Inserted by Mounika

#if context.Quote.GetCustomField('CF_Primary_Quote').Value = False