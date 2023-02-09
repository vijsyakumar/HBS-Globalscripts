#script descriptuion:update warning message in quote if tax is not calculated


import GM_TRANSLATIONS
from Scripting.Quote import MessageLevel
Log.Info('25--->')

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')
lc_quotetax = GM_TRANSLATIONS.GetText('000218', lv_LanguageKey, '', '', '', '', '')


def clearmsg():
    exitmsgs = context.Quote.Messages
    if exitmsgs.Count > 0:
        for msges in exitmsgs:
            messagess = lc_quotetax
            if messagess in str(msges.Content):
                Log.Write('msg--id--??--'+str(msges.Id))
                context.Quote.DeleteMessage(msges.Id)
                
clearmsg()
totalTax = context.Quote.GetCustomField('CF_TotalTax').Value
if totalTax is None or totalTax == '':
    context.Quote.AddMessage(lc_quotetax,MessageLevel.Warning,False)
else:
    clearmsg()