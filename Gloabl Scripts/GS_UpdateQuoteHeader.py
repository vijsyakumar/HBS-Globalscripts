#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#Update all the Quote Header fields
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 06/15/2022	Ashutosh K Mishra	0			-Initial Creation
# 11/04/2022	Dhruv				61	        -SQL translation,Transacrtion type
#												 check implemented
#-----------------------------------------------------------------------------
from System.Net import WebRequest
from System.Text import Encoding
from System.Net import WebException
import GM_TRANSLATIONS
#Get user launguage from dictionary
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_quote_ty = GM_TRANSLATIONS.GetText('000058', lv_LanguageKey, '', '', '', '', '')
lc_pro_val = GM_TRANSLATIONS.GetText('000059', lv_LanguageKey, '', '', '', '', '')
lc_pro_ty = GM_TRANSLATIONS.GetText('000060', lv_LanguageKey, '', '', '', '', '')
lc_booked = GM_TRANSLATIONS.GetText('000082', lv_LanguageKey, '', '', '', '', '')
lc_accpeted = GM_TRANSLATIONS.GetText('000050', lv_LanguageKey, '', '', '', '', '')
lc_status_exp = GM_TRANSLATIONS.GetText('000074', lv_LanguageKey, '', '', '', '', '') #Added by Dhruv

system = 'CPQ'
ls_cred = SqlHelper.GetFirst("SELECT * FROM CT_CREDENTIALS WHERE SYSTEM = '"+str(system)+"' ")

def creating_bearer_token():

    data = 'grant_type=password&username='+ls_cred.UserName+'&password='+ls_cred.Password+'&domain='+ls_cred.Domain
    data = Encoding.UTF8.GetBytes(data)
    url = "https://{}/basic/api/token".format(ls_cred.HOST)
    #url = "https://sandbox.webcomcpq.com/basic/api/token"
    request = WebRequest.Create(url)
    request.Method = "POST"

    # Set the ContentType property of the WebRequest.
    request.ContentType = "application/x-www-form-urlencoded"
    request.Accept = 'application/json'
    request.ContentLength = data.Length
    request.GetRequestStream().Write(data, 0, data.Length)

    response = request.GetResponse()
    stream = RestClient.DeserializeJson(StreamReader(response.GetResponseStream()).ReadToEnd())
    bearer_token = stream.access_token
    Trace.Write("token created {}".format(bearer_token))
    return bearer_token

def create_jwt_token():
    url = "https://sandbox.webcomcpq.com/api/rd/v1/core/GenerateJWT"
    url = "https://{}/api/rd/v1/core/GenerateJWT".format(ls_cred.HOST)
    encodedKeys = "Bearer "+str(creating_bearer_token())
    headers = {"Authorization":encodedKeys}
    data = ""
    jwt_resp_token = RestClient.Post(url,data,headers)
    return jwt_resp_token.token

def invoke_Action(quote_Id,action_Id):
    #url = "https://sandbox.webcomcpq.com/api/v1/quotes/6221/actions/2500/invoke"
    url = "https://{}/api/v1/quotes/{}/actions/{}/invoke".format(ls_cred.HOST,quote_Id,action_Id)
    encodedKeys = " Bearer "+str(create_jwt_token())
    headers = {"Authorization":encodedKeys}
    data = ""
    result = RestClient.Post(url,data,headers)
    return result


context.Quote.GetCustomField("CF_Quote Number").Value = context.Quote.QuoteNumber



if context.Quote.GetCustomField("CF_Quote_Type").Value == "":
    #context.Quote.GetCustomField("CF_Quote_Type").Value = "Fixed Price"
    context.Quote.GetCustomField("CF_Quote_Type").Value = lc_quote_ty

    
if context.Quote.GetCustomField("CF_Proposal_Validity").Value == "":
    #context.Quote.GetCustomField("CF_Proposal_Validity").Value = "30"
    context.Quote.GetCustomField("CF_Proposal_Validity").Value = lc_pro_val



if context.Quote.GetCustomField("CF_Proposal_Type").Value == "":
    #context.Quote.GetCustomField("CF_Proposal_Type").Value = "Firm"
    context.Quote.GetCustomField("CF_Proposal_Type").Value = lc_pro_ty
    
    
"""context.Quote.GetCustomField("CFH_MODIFIED_BY").Value = str(User.Name) + " / " + str(User.UserName)

if  len(set(context.Quote.GetInvolvedParties())) > 0:
    for bp in context.Quote.GetInvolvedParties():
        if bp.PartnerFunctionKey == "SP":
            bp_country  = bp.Country
            
            if bp_country:
                context.Quote.GetCustomField("CF_Account_Country").Value = bp_country
                
                lv_user = SqlHelper.GetFirst("Select LANGUAGE from TAB_LANGUAGE_DATA WHERE COUNTRY = '"+str(bp_country)+"'")
                
                if lv_user:
                    context.Quote.GetCustomField("Customer's Language").Value = lv_user.LANGUAGE
                    context.Quote.GetCustomField("CF_Language").Value = lv_user.LANGUAGE"""
                
    
    
"""if context.Quote.StatusName == "Submitted to Customer ":
    lv_praposal = context.Quote.GetCustomField("CF_Proposal_Validity").Value
    
    if lv_praposal:        
        lv_Praposal_date = SqlHelper.GetFirst("SELECT ProposalValidity FROM TAB_Proposal_Valdity WHERE CpqTableEntryId  = '"+str(lv_praposal)+"'")
        
        if lv_Praposal_date:            
            lv_expired_dat = context.Quote.DateCreated.AddDays(lv_Praposal_date.ProposalValidity)
            
            if lv_expired_dat:                
                context.Quote.GetCustomField("Quote Expiration Date").Value = lv_expired_dat"""
                
verify_status = [lc_booked, lc_accpeted]
if context.Quote.StatusName not in verify_status :
    if context.Quote.GetCustomField('Quote Expiration Date').Value:
        expiryDate = UserPersonalizationHelper.CovertToDate(context.Quote.GetCustomField('Quote Expiration Date').Value)
        
        if expiryDate < DateTime.Now:
            context.Quote.ChangeStatus(lc_status_exp) #Modified by Dhruv
            try:
                invoke_Action(context.Quote.Id,2500)
            except Exception as ex:
                Log.Info("Exception Raised for Invoke Action")
