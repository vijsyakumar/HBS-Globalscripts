#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#SIN Number
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 11/22/2022    Payal Gupta    0          -Initial Version
#
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)

lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type :

    lc_prodType_HL = GM_TRANSLATIONS.GetText('000118', lv_LanguageKey, '', '', '', '', '')
    lc_prodType_LB = GM_TRANSLATIONS.GetText('000040', lv_LanguageKey, '', '', '', '', '')

    for i in context.Quote.GetAllItems():
#--------Assigning SIN number to materials--------#

        part_number = i.PartNumber
        table_entry = SqlHelper.GetFirst("Select * from CT_CSPA_TAB WHERE PartNumber = '{}' ".format(part_number))
        if table_entry:
            if table_entry.SIN:
                i['QI_Sin_Number'] = str(table_entry.SIN)

#--------Assigning SIN number to Labor products--------#

        buying_method = context.Quote.GetCustomField('CF_Buying_Method').Value

        if i['QI_Product_Type'] == lc_prodType_HL or i['QI_Product_Type'] == lc_prodType_LB:
            if 'GSA: 03' in buying_method:
                i['QI_Sin_Number'] = '561210FAC'
            elif 'GSA: 84' in buying_method:
                i['QI_Sin_Number'] = '334290'
