#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
# GS ENTITY
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 8/30/2022     Sreenivasa              0             -Initial Version
# 11/6/2022    ishika bhattacharya     15             - Commented the Log.info
# 1/11/2023    Srijaydhurga                            cxcpq-31987
#
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS  # Added by ishika
from Scripting.Quote import MessageLevel
reference_quote_no = context.Quote.QuoteNumber
Log.Info('quote creation-- entity-reference_quote_no--'+str(reference_quote_no))
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by krishna
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
ent_aadress1 = ent_aadress2=  ent_city = ent_state = ent_zip = ent_cty =''


def populate_default_entity(entity):
    Log.Info('52----')
    context.Quote.GetCustomField('CF_HW_Default_Entity').Value = str(entity.Id)#CXCPQ=31987 start
    ent_aadress1 = ent_aadress2 =  ent_city = ent_state = ent_zip = ent_cty =''
    if  str(entity.Address1):
        ent_aadress1 =  str(entity.Address1)
    if  str(entity.Address2):
        ent_aadress2 =  str(entity.Address2)
    if str(entity.City):
        ent_city =  str(entity.City)
    if str(entity.State):
        ent_state = str(entity.State)
    if str(entity.ZipCode):
        ent_zip = str(entity.ZipCode)
    if str(entity.Country):
        ent_cty = str(entity.Country)
    context.Quote.GetCustomField('CF_Entity_Address').Value = "{} {} {} {} {} {}".format(ent_aadress1,
                                                                                            ent_aadress2, ent_city,
                                                                                            ent_state,ent_zip,
                                                                                            ent_cty)
    context.Quote.GetCustomField('CF_EntityName').Value = "{}".format(entity.CompanyName)
    context.Quote.GetCustomField('CF_Entity_Address1').Value = "{} {}".format(ent_aadress1,ent_aadress2) 
    context.Quote.GetCustomField('CF_Entity_Address2').Value = "{} {} {} {} ".format(ent_city,ent_state,ent_zip,ent_cty) #CXCPQ=31987 end


    
            
            
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  # Added by ishika
    Log.Info("**** GS_ENTITY ****")#                                                  Commented by Isha
    if context.Quote.GetCustomField('CF_HW_Default_Entity').Value is None or context.Quote.GetCustomField('CF_HW_Default_Entity').Value == "":
        Log.Info('empty-call-')
        profict_center = context.Quote.GetCustomField('CF_Branch/Profit Center').Value
        opp_type = context.Quote.GetCustomField('CF_Opportunity_Type').Value



        entity_profit_center = SqlHelper.GetFirst( "SELECT * FROM CT_PRCTR_MASTER WHERE Branch = '{}' and OpportunityType = '{}' and LanguageKey = '{}' ".format(profict_center, opp_type, lv_LanguageKey))

        if (entity_profit_center):
        
            entity = SqlHelper.GetFirst( "SELECT * FROM TAB_HW_DEFAULT_ENTITY WHERE Id = '{}' and LanguageKey = '{}'".format(entity_profit_center.Location_ID, lv_LanguageKey))  #Added by ishika
        if (entity):
            populate_default_entity(entity)
        #populate_default_entity()
    else:
        entityvalue = context.Quote.GetCustomField('CF_HW_Default_Entity').AttributeValue

        Log.Info("**** GS_ENTITY entityvalue****--->",entityvalue)#CXCPQ-31987 start
        entity = SqlHelper.GetFirst("SELECT * FROM TAB_HW_DEFAULT_ENTITY WHERE CompanyName = '{0}' and city='{1}' and state = '{2}' and LanguageKey = '{3}' ".format(entityvalue.split(',')[0],entityvalue.split(',')[1], entityvalue.split(',')[2], lv_LanguageKey))
        if  str(entity.Address1):
            ent_aadress1 =  str(entity.Address1)
        if  str(entity.Address2):
            ent_aadress2 =  str(entity.Address2)
        if str(entity.City):
            ent_city =  str(entity.City)
        if str(entity.State):
            ent_state = str(entity.State)
        if str(entity.ZipCode):
            ent_zip = str(entity.ZipCode)
        if str(entity.Country):
            ent_cty = str(entity.Country)
        context.Quote.GetCustomField('CF_Entity_Address').Value = str(ent_aadress1)+" "+str(ent_aadress2)+", "+ str(ent_city)+", "+str(ent_state)+", "+str(ent_zip)+", "+str(ent_cty)

        context.Quote.GetCustomField('CF_EntityName').Value = "{}".format(entityvalue.split(',')[0])
        context.Quote.GetCustomField('CF_Entity_Address1').Value = "{} {}".format(ent_aadress1,ent_aadress2) 
        context.Quote.GetCustomField('CF_Entity_Address2').Value = "{} {} {} {} ".format(ent_city,ent_state,ent_zip,ent_cty) #CXCPQ-31987 end    
        
