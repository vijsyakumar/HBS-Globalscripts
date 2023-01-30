#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script provide approval requests
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 7/4/2022      Payal Gupta           0         -initial version
# 10/14/2022	MarripudiKrishna 	  23	    -Replaced Hardcodings
#				Chaitanya						-Incorporated Translation
#
#-----------------------------------------------------------------------------
from Scripting.Quote import MessageLevel
import GM_TRANSLATIONS      #Added by krishna

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)          #Added by krishna

lc_op_type = GM_TRANSLATIONS.GetText('000024', lv_LanguageKey, '', '', '', '', '')
if (context.Quote.GetCustomField('CF_Opportunity_Type').Value) == lc_op_type : 

    primary_quote = context.Quote.GetCustomField('CF_Primary_Quote').Value
    proposal_type = context.Quote.GetCustomField('CF_Proposal_Type').Value
    status = context.Quote.StatusName
    #Log.Info("status---->"+str(status))

    lc_ready_for_app = GM_TRANSLATIONS.GetText('000044', lv_LanguageKey, '', '', '', '', '')         #Added by krishna
    lc_approved_status = GM_TRANSLATIONS.GetText('000071', lv_LanguageKey, '', '', '', '', '')
    lc_budgetary = GM_TRANSLATIONS.GetText('000072', lv_LanguageKey, '', '', '', '', '')
    lc_yes = GM_TRANSLATIONS.GetText('000054', lv_LanguageKey, '', '', '', '', '')
    lc_firm = GM_TRANSLATIONS.GetText('000060', lv_LanguageKey, '', '', '', '', '')
    lc_true = GM_TRANSLATIONS.GetText('000048', lv_LanguageKey, '', '', '', '', '')
    lc_msg = GM_TRANSLATIONS.GetText('000003', lv_LanguageKey, '', '', '', '', '')
    lc_message2 = GM_TRANSLATIONS.GetText('000004', lv_LanguageKey, '', '', '', '', '')
    lc_message3 = GM_TRANSLATIONS.GetText('000005', lv_LanguageKey, '', '', '', '', '')

    #if status == 'Ready For Approval':                 #commented by krishna
    if status == lc_ready_for_app:      #Added by krishna
        if primary_quote == '':
            #message1 = 'Please mark the quote as primary before submitting for SEA approval'                #commented by krishna
            message1 = lc_msg                 #Added by krishna
            exitmsg1 = context.Quote.Messages
            if exitmsg1.Count > 0:
                for msgs1 in exitmsg1:
                    if message1 in str(msgs1.Content):
                        context.Quote.DeleteMessage(msgs1.Id)
            #Log.Info("message1---->"+str(message1))
            context.Quote.AddMessage(message1,MessageLevel.Warning,True)

    #if status == 'Ready For Approval':             #commented by krishna
    if status == lc_ready_for_app:                          #Added by krishna
        #if proposal_type == 'Budgetary':      #commented by krishna
        if proposal_type == lc_budgetary:          #Added by krishna
            #message2 = 'Budgetary quote can not submitted for SEA approval, please change the proposal type before submitting for approval'       #commented by krishna
            message2 = lc_message2                       #Added by krishna
            exitmsg2 = context.Quote.Messages
            if exitmsg2.Count > 0:
                for msgs2 in exitmsg2:
                    if message2 in str(msgs2.Content):
                        context.Quote.DeleteMessage(msgs2.Id)
            context.Quote.AddMessage(message2,MessageLevel.Warning,True)

    sea_approval = ''
    quote_table=context.Quote.QuoteTables['Functional_Approval_R1'].Rows #Updated by Dhruv  for translation
    for customrow in quote_table:
        status_value = customrow['Approval_Status']
        required_value = customrow['Required']
        typeof_value= customrow['Type_of_Approval'].lower()
        #if status_value == 'Approved':              #commented by krishna
        if status_value == lc_approved_status:             #Added by krishna
            #sea_approval = 'Approved'                 #commented by krishna
            sea_approval = lc_approved_status                 #Added by krishna
        else:
            #if status == 'Ready For Approval':
            if status == lc_ready_for_app and required_value == True : #checking if the functional approval is required or not. Added by Sumandrita
                #msg = 'Please obtain functional approval for the opportunity before submitting the quote for SEA approval'     #commented by krishna
                if typeof_value!="honeywell t & c" and typeof_value!="opportunity credit check" and typeof_value!="payment terms" : # added by sanket
                    msg = lc_message3                          #Added by krishna
                    exitmsgs = context.Quote.Messages
                    if exitmsgs.Count > 0:
                        for msges in exitmsgs:
                            if msg in str(msges.Content):
                                context.Quote.DeleteMessage(msges.Id)
                    context.Quote.AddMessage(msg,MessageLevel.Warning,True)

    #if (primary_quote == "Yes") and (proposal_type == "Firm") and (sea_approval == 'Approved'):        #commented by krishna
        #context.Quote.GetCustomField('CF_SEA_APPROVAL_FLAG').Value = 'True'       #commented by krishna
        
    if (primary_quote == lc_yes) and (proposal_type == lc_firm) and (sea_approval == lc_approved_status):        #Added by krishna
        context.Quote.GetCustomField('CF_SEA_APPROVAL_FLAG').Value = lc_true      #Added by krishna