#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#Based on the conditions we are enabling the Request For Approval action button
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 9/25/2022     MarripudiKrishna       0         -initial version
#
# 10/17/2022	Abhilash		       3		 -Replaced Hardcodings
#												 -Incorporated Translation
# 11/04/2022	Dhruv				   4		 -SQL translation,Transacrtion type
#												  check implemented
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS

#Get user launguage from dictionary
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  #Modified by Dhruv

    lc_approval = GM_TRANSLATIONS.GetText('000071', lv_LanguageKey, '', '', '', '', '')
    lc_not_approval = GM_TRANSLATIONS.GetText('000109', lv_LanguageKey, '', '', '', '', '')
    lc_yes = GM_TRANSLATIONS.GetText('000054', lv_LanguageKey, '', '', '', '', '')
    lc_firm = GM_TRANSLATIONS.GetText('000060', lv_LanguageKey, '', '', '', '', '')
    lc_true = GM_TRANSLATIONS.GetText('000048', lv_LanguageKey, '', '', '', '', '')
    lc_false = GM_TRANSLATIONS.GetText('000068', lv_LanguageKey, '', '', '', '', '')

    #Trace.Write("---checking for request approval")

    primary_quote = context.Quote.GetCustomField('CF_Primary_Quote').Value
    proposal_type = context.Quote.GetCustomField('CF_Proposal_Type').Value

    sea_approval = sea_approval_lev = ''
    #quote_table=context.Quote.QuoteTables['Functional_Approval'].Rows # Code commented by Dhruv
    quote_table=context.Quote.QuoteTables['Functional_Approval_R1'].Rows # Code added by Dhruv 
    for customrow in quote_table:
        status_value = customrow['Approval_Status']
        #if status_value == 'Approved':
        if status_value == lc_approval:
            #Trace.Write("Approved")
            Trace.Write(lc_approval)
            #sea_approval = 'Approved'
            sea_approval = lc_approval
            
        #elif status_value != 'Approved':
        elif status_value != lc_approval: 
            #Trace.Write("Not Approved")
            Trace.Write(lc_not_approval)
            #sea_approval_lev = 'Not Approved'
            sea_approval_lev = lc_not_approval

    #if (primary_quote == "Yes") and (proposal_type == "Firm") and (sea_approval == "Approved") and (sea_approval_lev == ""):
    if (primary_quote == lc_yes) and (proposal_type == lc_firm) and (sea_approval == lc_approval) and (sea_approval_lev == ""):
        #Trace.Write("check-----")
        #context.Quote.GetCustomField('CF_SEA_APPROVAL_FLAG').Value = 'True'
        context.Quote.GetCustomField('CF_SEA_APPROVAL_FLAG').Value = lc_true
    #elif (primary_quote == "Yes") and (proposal_type == "Firm") and (sea_approval == "Approved") and (sea_approval_lev != ""):
    elif (primary_quote == lc_yes) and (proposal_type == lc_firm) and (sea_approval == lc_approval) and (sea_approval_lev != ""):
        #Trace.Write("=====-")
        #context.Quote.GetCustomField('CF_SEA_APPROVAL_FLAG').Value = 'False'
        context.Quote.GetCustomField('CF_SEA_APPROVAL_FLAG').Value = lc_false
        