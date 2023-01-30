from Scripting.Quote import MessageLevel
import GM_TRANSLATIONS

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')  
lc_Branch = context.Quote.GetCustomField("CF_Branch/Profit Center").Value
lc_Country = context.Quote.GetCustomField("CF_Country").Value 
lc_opp = GM_TRANSLATIONS.GetText('000024', lv_LanguageKey, '', '', '', '', '')
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:
    context.Quote.GetCustomField('CF_Branch_Restriction').Value = False
    lv_branch = SqlHelper.GetFirst("Select * from CT_PRCTR_MASTER WHERE Branch = '{0}' and OpportunityType = '{1}' and CountryKey = '{2}' and LanguageKey='{3}'".format(lc_Branch,lc_opp,lc_Country,lv_LanguageKey))
    if not lv_branch:
        msg = GM_TRANSLATIONS.GetText('000228', lv_LanguageKey,'', '', '', '', '')
        exitmsgs = context.Quote.Messages
        if exitmsgs.Count > 0:
            for msges in exitmsgs:
                lv_msg_txt = GM_TRANSLATIONS.GetText('000228', lv_LanguageKey, '', '', '', '', '')
                if  lv_msg_txt in str(msges.Content):
                    context.Quote.DeleteMessage(msges.Id)
        context.Quote.AddMessage(msg,MessageLevel.Error,True)
        context.Quote.GetCustomField('CF_Branch_Restriction').Value = True
        Trace.Write(str(context.Quote.GetCustomField('CF_Branch_Restriction').Value))