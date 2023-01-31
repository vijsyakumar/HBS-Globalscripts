from Scripting.Quote import MessageLevel

import GM_TRANSLATIONS																	#Inserted by Dhruv
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)

lc_quotetax = GM_TRANSLATIONS.GetText('000218', lv_LanguageKey, '', '', '', '', '')
def clearmsg():
    exitmsgs = context.Quote.Messages
    if exitmsgs.Count > 0:
        for msges in exitmsgs:
            messagess = lc_quotetax
            if messagess in str(msges.Content):
                #Log.Write('msg--id--??--'+str(msges.Id))
                context.Quote.DeleteMessage(msges.Id)
get_tax = context.Quote.GetCustomField('CF_TotalTax').Value
if get_tax:
	clearmsg()