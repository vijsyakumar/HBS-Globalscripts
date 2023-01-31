#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script defines the custom fields that is
#mapped to the proposal template to show the text for proposal validity and tax
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 09/21/2022    Sunil S                    0             -Initial Version
# 10/20/2022    Ishika Bhattacharya        3             -Replaced Hardcodings
#                                                        -Incorporated Translation
# 10/21/2022    Payal Gupta                4             - Incorporated changes for include
#														   exclude Use Tax
# 11/03/2022    Aditi Sharma               5             -Replaced lc_op_type with lc_trans_type
#                                                         to remove dependency on multiple opp types
#-----------------------------------------------------------------------------


import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)   # Added by Ishika
#lc_op_type = GM_TRANSLATIONS.GetText('000024', lv_LanguageKey, '', '', '', '', '') #commented by Aditi 3rd Nov 2022
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #added by Aditi 3rd Nov 2022

#if (context.Quote.GetCustomField('CF_Opportunity_Type').Value) == lc_op_type: #Added by Ishika  #commented by Aditi 3rd Nov 2022
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type: #added by Aditi 3rd Nov 2022
    lc_include_tax = GM_TRANSLATIONS.GetText('000113', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
    lc_exclude_tax = GM_TRANSLATIONS.GetText('000114', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
    #lc_US = GM_TRANSLATIONS.GetText('000056', lv_LanguageKey, '', '', '', '', '')   # Commented by Payal
    lc_US_message = GM_TRANSLATIONS.GetText('000155', lv_LanguageKey, '', '', '', '', '')   # Added by Ishika
    lc_US_message_include = GM_TRANSLATIONS.GetText('000165', lv_LanguageKey, '', '', '', '', '')   # Added by Payal


    Tax_item  =  context.Quote.GetCustomField('Tax').Value
    Use_Tax = context.Quote.GetCustomField('CF_Use_Tax').Value # Added by Payal
    #Country_item = context.Quote.GetCustomField('CF_Country').Value # Commented by Payal
    #if Tax_item == 'Include Tax':   #Commented by Ishika
    if Tax_item == lc_include_tax:  #Added by Ishika
        lc_IncludeTax_message = GM_TRANSLATIONS.GetText('000153', lv_LanguageKey, context.Quote.GetCustomField('CF_TotalTax').Value, '', '', '', '')  # Added by Ishika

        # context.Quote.GetCustomField('CF_Tax_include_statement').Value = "Sales tax @ the rate" + context.Quote.GetCustomField('CF_TotalTax').Value + "% is  included in the price and will be charged at actuals." #Commented by Ishika
        context.Quote.GetCustomField('CF_Tax_include_statement').Value = lc_IncludeTax_message  #Added by Ishika

        #Trace.Write("pass")
    #if Tax_item == 'Exclude Tax':  #Commented by Ishika
    if Tax_item == lc_exclude_tax:  #Added by Ishika
        lc_ExcludeTax_message = GM_TRANSLATIONS.GetText('000154', lv_LanguageKey, context.Quote.GetCustomField('CF_TotalTax').Value, '', '', '', '')  # Added by Ishika

        # context.Quote.GetCustomField('CF_Tax_include_statement').Value = "Sales tax @ the rate" + context.Quote.GetCustomField('CF_TotalTax').Value + "% is not included in the price and will be charged at actuals."  #Commented by Ishika
        context.Quote.GetCustomField('CF_Tax_include_statement').Value = lc_ExcludeTax_message #Added by Ishika

    #if Country_item == 'US':  #Commented by Ishika
    if Use_Tax == lc_exclude_tax: #Added by Payal
        #context.Quote.GetCustomField('CF_US_Include_statement').Value = "Use tax is not included in the quoted price and shall be charged at actuals"  #Commented by Ishika
        context.Quote.GetCustomField('CF_US_Include_statement').Value = lc_US_message  #Added by Ishika

    if Use_Tax == lc_include_tax : #Added by Payal
        context.Quote.GetCustomField('CF_US_Include_statement').Value = lc_US_message_include  #Added by Payal

