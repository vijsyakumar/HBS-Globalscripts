#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#Sets the item type as Optional or Base to the quote line item custom field
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 10/28/2022      Ishika Bhattacharya   0         -initial version
# 10/28/2022	  Ishika Bhattacharya 	1	      -Replaced Hardcodings
#										          -Incorporated Translation
#
#-----------------------------------------------------------------------------


# Sets the item type as Optional or Base to the quote line item custom field based on
# whether the 'IsOptional' standard field of each item returns True or False

import GM_TRANSLATIONS

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_Base = GM_TRANSLATIONS.GetText('000173', lv_LanguageKey, '', '', '', '', '')
lc_Optional = GM_TRANSLATIONS.GetText('000174', lv_LanguageKey, '', '', '', '', '')

for i in context.Quote.GetAllItems():
    if i.IsOptional == False:
        # i['QI_ItemType_Value'] = "Base"
        i['QI_ItemType_Value'] = lc_Base
    else:
        #i['QI_ItemType_Value'] = "Optional"
        i['QI_ItemType_Value'] = lc_Optional
    # added by ishika 7 Nov
    i['QI_MaterialsSalesCategory_Description'] = i['QI_SALES_CATEGORY']
