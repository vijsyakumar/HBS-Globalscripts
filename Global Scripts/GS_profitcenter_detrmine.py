# -----------------------------------------------------------------------------
#            Change History Log
# -----------------------------------------------------------------------------
# Description:
# This script is used to get the profit centre from custom table based on
# country, district and branch
# -----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
# -----------------------------------------------------------------------------
# 09/20/20222    Anil Poply                0             -Initial Version
# 10/18/2022    Ishika Bhattacharya        5             -Incorporated Translation
# 11/03/2022	Srinivasan Dorairaj		   8			 -Script Translation changes
# 11/05/2022    ishika bhattacharya        9             - added language key in query
# 01/13/2023    Aditi Sharma               10            -removed condition for opportunity type check
# -----------------------------------------------------------------------------


import GM_TRANSLATIONS  # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')  # Modified by Srinivasan Dorairaj
#if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  # Modified by Srinivasan Dorairaj #Commented by Aditi
quote_branch = context.Quote.GetCustomField('CF_Branch/Profit Center').Value
quote_district = context.Quote.GetCustomField('CF_District').Value
quote_country = context.Quote.GetCustomField('CF_Country').Value
opp_type = context.Quote.GetCustomField('CF_Opportunity_Type').Value

# fetch Branch ID from table CT_PRCTR_MASTER using country code, district, branch name and opp type

# query_branchID = SqlHelper.GetFirst("SELECT BranchID FROM CT_PRCTR_MASTER WHERE CountryKey = '{}' and District = '{}' and Branch = '{}' and OpportunityType = '{}'".format(quote_country,quote_branch,opp_type))

'''query_branchID = SqlHelper.GetFirst(
"SELECT BranchID FROM CT_PRCTR_MASTER WHERE CountryKey = '{}' and Branch = '{}' and OpportunityType = '{}'".format(
quote_country, quote_branch, opp_type))''' #Commented by ishika
query_branchID = SqlHelper.GetFirst("SELECT BranchID FROM CT_PRCTR_MASTER WHERE CountryKey = '{}' and Branch = '{}' and OpportunityType = '{}' and LanguageKey = '{}'".format(quote_country, quote_branch, opp_type, lv_LanguageKey))  #Added by ishika

# assign branch ID value to profit center ID custom field
if query_branchID:
    context.Quote.GetCustomField("CF_Profit_Center_ID").Value = query_branchID.BranchID