#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#Fetching the producttype of the line items
#Fetching the name of Quote Type
#if Quote type is parts only and product type is labor then showing error message#
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 08/08/2022    Sumandrita Moitra	 0 			-Initial Version
# 09/30/2022	Dhruv Bhatnagar		 21			-Replaced Hardcodings
#												-Incorporated Translation
# 12/13/2022    Sumandrita Moitra    28         - added "Third Party" in condition
# 12/23/2022    Sumandrita           29         - Write-in parent in condition for parts only quote
# 12/27/2022    Sumandrita           30          -removed hon material from condition
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
context.Quote.GetCustomField("CF_Producttype_Control").Value = False
Trace.Write("Value" +str(context.Quote.GetCustomField("CF_Producttype_Control").Value))

qtype = context.Quote.GetCustomField('CF_Quote_Type').Value
for i in context.Quote.GetAllItems():
    
    part_no = i.PartNumber
    prd_type = i["QI_Product_Type"]
    p_id = i.Id
    if qtype == str(quote_type_value) and prd_type != str(lc_hon_hard) and prd_type != str(lc_hon_soft) and prd_type != str(lc_third_party) and prd_type != str(lc_Writein): #"Third Party" and Write-in parent added in condition by     Sumandrita
        #msg = 'The Product Type "'+str(prd_type)+'" is not allowed for Quote Type "Parts Only" '
        #context.Quote.DeleteItem(p_id)
        msg = GM_TRANSLATIONS.GetText('000010', lv_LanguageKey,str(prd_type), str(quote_type_value), '', '', '')
        exitmsgs = context.Quote.Messages
        if exitmsgs.Count > 0:
            for msges in exitmsgs:
                #if  "is not allowed for Quote Type" in str(msges.Content):
                lv_msg_txt = GM_TRANSLATIONS.GetText('000022', lv_LanguageKey, '', '', '', '', '')
                if  lv_msg_txt in str(msges.Content):
                    context.Quote.DeleteMessage(msges.Id)
        context.Quote.AddMessage(msg,MessageLevel.Error,True)
        context.Quote.GetCustomField("CF_Producttype_Control").Value = True
        Trace.Write("Value" +str(context.Quote.GetCustomField("CF_Producttype_Control").Value))