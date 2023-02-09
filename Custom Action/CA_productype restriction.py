#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#Fetching the producttype of the line items
#Fetching the name of Quote Type
#if Quote type is parts only and product type is labor then showing error message#and restricting the workflow to move forward
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 08/03/2022    Sumandrita Moitra	 0 			-Initial Version
# 10/19/2022	Ishika Bhattacharya  19			-Replaced Hardcodings
#												-Incorporated Translation
# 11/05/2022	Dhruv Bhatnagar		 20			-Tranlation corrections
#-----------------------------------------------------------------------------
#Imports
from Scripting.Quote import MessageLevel
import GM_TRANSLATIONS

#quote_type_value = "Parts Only"
#product_type = "First Party Material"

#Get user launguage from dictionary
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)

quote_type_value = GM_TRANSLATIONS.GetText('000019', lv_LanguageKey, '', '', '', '', '')
lc_hon_hard = GM_TRANSLATIONS.GetText('000027', lv_LanguageKey, '', '', '', '', '')
lc_hon_soft = GM_TRANSLATIONS.GetText('000124', lv_LanguageKey, '', '', '', '', '')
lc_hon_mat = GM_TRANSLATIONS.GetText('000131', lv_LanguageKey, '', '', '', '', '')
lc_third_party = GM_TRANSLATIONS.GetText('000065', lv_LanguageKey, '', '', '', '', '')
lc_Writein = GM_TRANSLATIONS.GetText('000175', lv_LanguageKey, '', '', '', '', '')

lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
lc_True = GM_TRANSLATIONS.GetText('000048', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Modified by Dhruv

    qtype = context.Quote.GetCustomField('CF_Quote_Type').Value
    for i in context.Quote.GetAllItems():
        part_no = i.PartNumber
        prd_type = i["QI_Product_Type"]
        mand_val = i["QI_Mand_Charges_Validation"]
        if qtype == str(quote_type_value) and prd_type != str(lc_hon_hard) and prd_type != str(lc_hon_soft) and prd_type != str(lc_hon_mat) and prd_type != str(lc_third_party) and prd_type != str(lc_Writein) and i.ProductSystemId != "RQ_Mandatory_Charges_cpq" and mand_val != "True": #"Third Party" and Write-in parent added in condition by     Sumandrita :
            #msg = 'The Product Type "'+str(prd_type)+'" is not allowed for Quote Type "Parts Only" '
            msg = GM_TRANSLATIONS.GetText('000010', lv_LanguageKey, str(prd_type), str(quote_type_value), '', '', '')
            exitmsgs = context.Quote.Messages
            if exitmsgs.Count > 0:
                for msges in exitmsgs:
                    #if  "is not allowed for Quote Type" in str(msges.Content):
                    lv_msg_txt = GM_TRANSLATIONS.GetText('000022', lv_LanguageKey, '', '', '', '', '')
                    if  lv_msg_txt in str(msges.Content):
                        context.Quote.DeleteMessage(msges.Id)
            context.Quote.AddMessage(msg,MessageLevel.Warning,lc_True) #Modified by Dhruv
            #context.Quote.ChangeStatus('Preparing')
            context.Quote.ChangeStatus(GM_TRANSLATIONS.GetText('000018', lv_LanguageKey, '', '', '', '', ''))