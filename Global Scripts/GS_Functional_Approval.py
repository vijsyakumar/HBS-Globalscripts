# -----------------------------------------------------------------------------
#            Change History Log
# -----------------------------------------------------------------------------
# Description:
# This script is used for functional approval
# -----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
# -----------------------------------------------------------------------------
# 07/22/2022    Krishna Chaitanya          0             -Initial Version
# 10/17/2022    Ishika Bhattacharya        30            -Replaced Hardcodings
#                                                        -Incorporated Translation
# 11/04/2022	Srinivasan Dorairaj		   34			 -Script and SQL Translation changes
# 11/05/2022    ishika bhattacharya        35           - added language key in queries and replaced harcodings
# 12/12/2022    Aditi Sharma               36           -Restricted the CSPA matrix to only 3 rows CXCPQ-33177
# 12/29/2022    Aditi Sharma               39           -Removed Language key filter from FUNC Approval query
# 12/30/2022    Aditi Sharma               42           -Restricted the CSPA matrix to only 2 rows instead of 3 rows CXCPQ-33177
# 01/13/2023    Aditi Sharma               46           -Corrected the condition for Parts Only
# -----------------------------------------------------------------------------

import GM_TRANSLATIONS  # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')  # Modified by Srinivasan Dorairaj
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  # Modified by Srinivasan Dorairaj
    lc_parts_only = GM_TRANSLATIONS.GetText('000019', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
    quote_id = context.Quote.Id
    quote_table = context.Quote.QuoteTables['Functional_Approval_R1'] #changes started by Dhruv - 01.23.2023
    quote_table.Rows.Clear()
    count = 0

    custom_table = SqlHelper.GetList("SELECT * FROM CT_QUOTE_FUNC_APPROVAL WHERE QuoteId = '"+ str(quote_id)+"' and Required  = 'true'")  # CXCPQ-35483 start & end  # Modified by Srinivasan Dorairaj #Modified by Aditi for Language Key removal 29th Dec 2022 #modified by srijaydhurga 2 jan 2023
    for customrow in custom_table:
        quote_id_table = customrow.QuoteId
        if str(quote_id) == str(quote_id_table):
            count += 1
            newRow = quote_table.AddNewRow()
            newRow['S_No'] = count
            newRow['Quote_ID'] = customrow.QuoteId
            newRow['Type_of_Approval'] = customrow.Type_of_Approval
            newRow['Required'] = customrow.Required
            newRow['Approval_Status'] = customrow.Approval_Status

    quote_table = context.Quote.QuoteTables['Approval_Matrix']
    quote_table.Rows.Clear()
    quote_type = context.Quote.GetCustomField("CF_Quote_Type").Value

    # Begin of comment by Dhruv
    '''try:
	query = SqlHelper.GetFirst("SELECT * FROM CT_QUOTE_LOOKUP_ATTRIBUTES WHERE Quote_Type = '"+str(quote_type)+"' ")

    except:
    query = SqlHelper.GetFirst("SELECT * FROM CT_QUOTE_LOOKUP_ATTRIBUTES WHERE CpqTableEntryId = '"+str(quote_type)+"' ")

    if query:'''
    # End of comment by Dhruv
    if quote_type:
        # if query.Quote_Type != "Parts Only": #Commented by Dhruv
        # if quote_type != "Parts Only":		  #Inserted by Dhruv  "Commented by Ishika
        if quote_type != lc_parts_only:  # Added by Ishika
            Trace.Write("ffffffff")
            custom_table = SqlHelper.GetList(
                "SELECT * FROM CT_APPROVAL_MATRIX WHERE Quote_Type != '" + lc_parts_only + "' AND LanguageKey='" + lv_LanguageKey + "' ")
            for customrow in custom_table:
                newRow = quote_table.AddNewRow()
                newRow['Sales_Price_Discount_variance'] = str(customrow.Sales_Price)
                #Translation changes started by Dhruv - 01.23.2023
                newRow['_20_'] = Translation.Get(str(customrow.Greater_than_20))
                newRow['_12_20_'] = Translation.Get(str(customrow.Greater_than_12_and_less_than_20))
                newRow['_9_12_'] = Translation.Get(str(customrow.Greater_than_9_and_less_than_12))
                newRow['_6_9_'] = Translation.Get(str(customrow.Greater_than_6_and_less_than_9))
                newRow['_3_6_'] = Translation.Get(str(customrow.Greater_than_3_and_less_than_6))
                newRow['_0_3_'] = Translation.Get(str(customrow.Greater_than_0_and_less_than_3))
                newRow['_0_'] = Translation.Get(str(customrow.Less_than_0_or_eql_to_0))
                #Translation changes ended by Dhruv - 01.23.2023

        else:
            # if query.Quote_Type == "Parts Only":	#Commented by Dhruv #Inserted by Dhruv
            # if quote_type == "Parts Only":	#Inserted by Dhruv         "Commented by Ishika
            if quote_type == lc_parts_only:  # Added by Ishika #Changed the condition from != to == by Aditi 13th Jan
                Trace.Write("gggggggg")
                custom_table = SqlHelper.GetList(
                    "SELECT * FROM CT_APPROVAL_MATRIX WHERE Quote_Type = '" + lc_parts_only + "' AND LanguageKey='" + lv_LanguageKey + "' ")
                for customrow in custom_table:
                    newRow = quote_table.AddNewRow()
                    #Translation changes started by Dhruv - 01.23.2023
                    newRow['Sales_Price_Discount_variance'] = str(customrow.Sales_Price)
                    newRow['_20_'] = Translation.Get(str(customrow.Greater_than_20))
                    newRow['_12_20_'] = Translation.Get(str(customrow.Greater_than_12_and_less_than_20))
                    newRow['_9_12_'] = Translation.Get(str(customrow.Greater_than_9_and_less_than_12))
                    newRow['_6_9_'] = Translation.Get(str(customrow.Greater_than_6_and_less_than_9))
                    newRow['_3_6_'] = Translation.Get(str(customrow.Greater_than_3_and_less_than_6))
                    newRow['_0_3_'] = Translation.Get(str(customrow.Greater_than_0_and_less_than_3))
                    newRow['_0_'] = Translation.Get(str(customrow.Less_than_0_or_eql_to_0))
					#Translation changes ended by Dhruv - 01.23.2023
    quote_table = context.Quote.QuoteTables['CSPA_Matrix']
    quote_table.Rows.Clear()
    #custom_table = SqlHelper.GetList("SELECT * FROM CT_Approval_CSPA_Matrix")
    custom_table = SqlHelper.GetList("SELECT * FROM CT_Approval_CSPA_Matrix where LanguageKey = '{}'".format(lv_LanguageKey))  #Added by ishika
    cspa_row_count = 0 #Added by Aditi 12th Dec 2022
    for customrow in custom_table:
        if cspa_row_count < 2: #Added by Aditi 12th Dec 2022 #Modified by Aditi 30th Dec
            newRow = quote_table.AddNewRow()
            newRow['Sales_Price_GM'] = str(customrow.Sales_Price_GM)
            #Translation changes started by Dhruv - 01.23.2023
            newRow['_0_12_4_'] = Translation.Get(str(customrow.Greater_than_eql_0_to_less_than_12_4))
            newRow['_12_4_20_4_'] = Translation.Get(str(customrow.Greater_than_eql_12_4_to_less_than_20_4))
            newRow['_20_'] = Translation.Get(str(customrow.Greater_than_eql_20))
            #Translation changes ended by Dhruv - 01.23.2023
            cspa_row_count+=1 #Added by Aditi 12th Dec 2022

    quote_table = context.Quote.QuoteTables['CSPA_RQ_SEA']
    quote_table.Rows.Clear()
    # custom_table = SqlHelper.GetList("SELECT * FROM CT_APPROVAL_BUY_HON_MPA_CSPA_RQ_SEA") #Commented by ishika
    custom_table = SqlHelper.GetList("SELECT * FROM CT_APPROVAL_BUY_HON_MPA_CSPA_RQ_SEA where LanguageKey = '{}'".format(lv_LanguageKey)) #Added by ishika
    for customrow in custom_table:
        newRow = quote_table.AddNewRow()
        newRow['SalesPrice_DV'] = str(customrow.Sales_Price_DV)
        #Translation changes started by Dhruv - 01.23.2023
        newRow['_3_'] = Translation.Get(str(customrow.Greater_than_3))
        newRow['_1_3_'] = Translation.Get(str(customrow.Greater_than_1_to_less_than_eql_3))
        newRow['_0_1_'] = Translation.Get(str(customrow.Greater_than_0_to_less_than_eql_1))
        #Translation changes ended by Dhruv - 01.23.2023