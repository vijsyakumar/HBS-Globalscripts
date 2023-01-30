#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#Tax value computed only for testing purpose - it will be fetched from ECC
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 10/15/2022    Sumandrita            0         -initial version
#
# 10/17/2022	Abhilash		      4		    -Replaced Hardcodings
#												-Incorporated Translation
# 11/04/2022	Dhruv				  5	        -SQL translation,Transacrtion type
#												 check implemented
# 01/19/2023    Aditi                           -Removed all rounding
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS

#Get user launguage from dictionary
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  #Modified by Dhruv
    lc_yes = GM_TRANSLATIONS.GetText('000054', lv_LanguageKey, '', '', '', '', '')
    lc_kwd = GM_TRANSLATIONS.GetText('000115', lv_LanguageKey, '', '', '', '', '')
    lc_omr = GM_TRANSLATIONS.GetText('000116', lv_LanguageKey, '', '', '', '', '')

    total_tax_act = context.Quote.GetCustomField('CF_TotalTax').Value
    currency = context.Quote.GetCustomField('CF_Quote_Currency').Value
    #if currency != "KWD" and currency != "OMR" and total_tax_act:
    if currency != lc_kwd and currency != lc_omr and total_tax_act:
        #Trace.Write("Yes")
        Trace.Write(lc_yes)
        #total_tax = round(float(total_tax_act),2)
        total_tax = float(total_tax_act)
        context.Quote.GetCustomField('CF_TotalTax').Value = total_tax
