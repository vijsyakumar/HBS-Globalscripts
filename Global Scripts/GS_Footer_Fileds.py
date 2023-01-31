#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used to get the footer fields values
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 9/8/2022      Neha Chaure              0             -Initial Version
# 10/17/2022    Ishika Bhattacharya      8             -Incorporated Translation
# 11/04/2022	Srinivasan Dorairaj		 9			   -Script Translation changes
# 11/05/2022    ishika bhattacharya      10            - SQL query modification
#-----------------------------------------------------------------------------


import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)   # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Srinivasan Dorairaj
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Modified by Srinivasan Dorairaj

    unique_id = ''
    hw_entity = context.Quote.GetCustomField("CF_HW_Default_Entity")

    #####----- Getting Default entity value and using split function to get unique id -----#####
	#CXCPQ-37626 start
    if context.Quote.GetCustomField("CF_HW_Default_Entity").Value:#CXCPQ-37626 end
        entity = hw_entity.AttributeValue
        split_entity = entity.split(',')
        unique_id = split_entity[0]


    #####----- Getting details from CT_Footer_Table using unique id -----#####

    if unique_id:#CXCPQ-37626 start
       	
        query = SqlHelper.GetFirst("SELECT Fax,Email,Phone,WebSite FROM CT_Footer_Table WHERE Id = '"+str(unique_id)+"' ") ##CXCPQ-37626 end

        if query:
            context.Quote.GetCustomField("CF_Footer_Fax").Value = query.Fax
            context.Quote.GetCustomField("CF_Footer_Email").Value = query.Email
            context.Quote.GetCustomField("CF_Footer_Phone").Value = query.Phone
            context.Quote.GetCustomField("CF_Footer_URL").Value = query.WebSite

