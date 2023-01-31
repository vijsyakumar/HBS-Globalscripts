#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#checks wether inclusions and exclusions/scope of work table have atleast one value and based on that assigns value to the respective custom field
#-----------------------------------------------------------------------------
# Date			  Name				    Version	  Comments(Changes done)
#-----------------------------------------------------------------------------
# 12/27/2022      Ishika Bhattacharya   0         -initial version
# 12/28/2022	  Ishika Bhattacharya 	1	      -Replaced Hardcodings
#										          -Incorporated Translation
# 12/29/2022      Ishika Bhattacharya   2         -added check for scope of work 
# 12/29/2022      Ishika Bhattacharya   3         -reverted above change
#-----------------------------------------------------------------------------
from Scripting.Quote import MessageLevel
import GM_TRANSLATIONS      
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)

#lc_op_type = GM_TRANSLATIONS.GetText('000024', lv_LanguageKey, '', '', '', '', '')
#if (context.Quote.GetCustomField('CF_Opportunity_Type').Value) == lc_op_type : 
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') 
lc_QT_Inclusions = GM_TRANSLATIONS.GetText('000219', lv_LanguageKey, '', '', '', '', '') 
lc_Inclusions = GM_TRANSLATIONS.GetText('000220', lv_LanguageKey, '', '', '', '', '') 
lc_Custom_Inclusions = GM_TRANSLATIONS.GetText('000221', lv_LanguageKey, '', '', '', '', '') 
lc_Yes = GM_TRANSLATIONS.GetText('000054', lv_LanguageKey, '', '', '', '', '') 
lc_No = GM_TRANSLATIONS.GetText('000198', lv_LanguageKey, '', '', '', '', '') 
lc_Exclusions = GM_TRANSLATIONS.GetText('000222', lv_LanguageKey, '', '', '', '', '') 
lc_Custom_Exclusions = GM_TRANSLATIONS.GetText('000223', lv_LanguageKey, '', '', '', '', '') 
# lc_SOW = GM_TRANSLATIONS.GetText('000224', lv_LanguageKey, '', '', '', '', '') 

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : 

    def inclusion_exclusion_SOW(quoteTable, column_name):
        get_inclusions_exclusions_SOW =  0
        quote_table = context.Quote.QuoteTables[quoteTable]
        for rows in quote_table.Rows:
            Trace.Write(rows[column_name])
            if rows[column_name]:
                get_inclusions_exclusions_SOW += 1
                return get_inclusions_exclusions_SOW


    # INCLUSIONS
    std_inclusion = inclusion_exclusion_SOW(lc_QT_Inclusions, lc_Inclusions)
    custom_inclusion = inclusion_exclusion_SOW(lc_Custom_Inclusions, lc_Custom_Inclusions)

    if std_inclusion or custom_inclusion:
        #context.Quote.GetCustomField('CF_isInclusion').Value = 'Yes'
        context.Quote.GetCustomField('CF_isInclusion').Value = lc_Yes
    else:
        #Trace.Write('isInclusion:{}'.format('No'))
        context.Quote.GetCustomField('CF_isInclusion').Value = lc_No


    # EXCLUSIONS
    std_exclusion = inclusion_exclusion_SOW(lc_Exclusions, lc_Exclusions)
    custom_exclusion = inclusion_exclusion_SOW(lc_Custom_Exclusions, lc_Custom_Exclusions)

    if std_exclusion or custom_exclusion:
        #Trace.Write('isExclusion:{}'.format('Yes'))
        context.Quote.GetCustomField('CF_isExclusion').Value = lc_Yes
    else:
        #Trace.Write('isExclusion:{}'.format('No'))
        context.Quote.GetCustomField('CF_isExclusion').Value = lc_No

    # CHECK WETHER EITHER OF INCLUSIONS OF EXCLUSIONS IS PRESENT
    if context.Quote.GetCustomField('CF_isExclusion').Value == lc_Yes or context.Quote.GetCustomField('CF_isInclusion').Value == lc_Yes:
        context.Quote.GetCustomField('CF_isInclusion_or_isExclusion').Value = lc_Yes
    else:
        context.Quote.GetCustomField('CF_isInclusion_or_isExclusion').Value = lc_No

    # SCOPE OF WORK
    '''scope_of_work = inclusion_exclusion_SOW(lc_SOW, lc_SOW)
    if scope_of_work:
        context.Quote.GetCustomField('CF_isScopeOfWork').Value = lc_Yes
    else:
        #Trace.Write('isExclusion:{}'.format('No'))
        context.Quote.GetCustomField('CF_isScopeOfWork').Value = lc_No'''