#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#Line item update
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 09/06/2022    AshutoshKumar Mishra    0          -Initial Version
# 10/14/2022    Mounika Tarigopula      17         -Replaced Hardcodings
#                                                  -Incorporated Translation
# 10/30/2022    Aditi Sharma            29         -Changed lc_prodType_TPH to 000065
#
# 11/01/2022    Aditi Sharma            31         -Replaced lc_op_type with lc_trans_type
#                                                   to remove dependency on multiple opp types
# 11/02/2022    Sumandrita              32         -Assigning proper category name to catagory column for labor products
#
# 11/03/2022    Srinivasan Dorairaj     35			- Script and SQL Translation changes
# 11/04/2022	Dhruv Bhatnagar			36			- Corrections
#-----------------------------------------------------------------------------
#Begin of change by Mounika
import GM_TRANSLATIONS                   #Inserted by Mounika
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)    #Inserted by Mounika
#lc_op_type = GM_TRANSLATIONS.GetText('000024', lv_LanguageKey, '', '', '', '', '') #commented by Aditi 1st Nov 2022
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #replaced by Aditi 1st Nov 2022 'lc_trans_type'
    lc_sp = GM_TRANSLATIONS.GetText('000023', lv_LanguageKey, '', '', '', '', '')
    lc_prep = GM_TRANSLATIONS.GetText('000018', lv_LanguageKey, '', '', '', '', '')
    lc_EA = GM_TRANSLATIONS.GetText('000025', lv_LanguageKey, '', '', '', '', '')
    lc_prod_cat = GM_TRANSLATIONS.GetText('000026', lv_LanguageKey, '', '', '', '', '')
    lc_prodType_FP = GM_TRANSLATIONS.GetText('000020', lv_LanguageKey, '', '', '', '', '')
    lc_prodType_HH = GM_TRANSLATIONS.GetText('000027', lv_LanguageKey, '', '', '', '', '')
    lc_prodType_TPH = GM_TRANSLATIONS.GetText('000065', lv_LanguageKey, '', '', '', '', '')
    lc_prodType_PU = GM_TRANSLATIONS.GetText('000029', lv_LanguageKey, '', '', '', '', '')
    lc_RecType_S = GM_TRANSLATIONS.GetText('000030', lv_LanguageKey, '', '', '', '', '')
    lc_RecType_T = GM_TRANSLATIONS.GetText('000031', lv_LanguageKey, '', '', '', '', '')
    lc_RecType_M = GM_TRANSLATIONS.GetText('000032', lv_LanguageKey, '', '', '', '', '')
    lc_prodType_Adhoc = GM_TRANSLATIONS.GetText('000111', lv_LanguageKey, '', '', '', '', '')
    lc_prodcat_UA = GM_TRANSLATIONS.GetText('000166', lv_LanguageKey, '', '', '', '', '')
    lc_prodcat_TP = GM_TRANSLATIONS.GetText('000065', lv_LanguageKey, '', '', '', '', '')
    lc_prodType_TP = GM_TRANSLATIONS.GetText('000065', lv_LanguageKey, '', '', '', '', '')
    lc_vendor_type_HW = GM_TRANSLATIONS.GetText('000168', lv_LanguageKey, '', '', '', '', '')
    lc_prodType_HL = GM_TRANSLATIONS.GetText('000118', lv_LanguageKey, '', '', '', '', '')
    lc_prodType_LB = GM_TRANSLATIONS.GetText('000040', lv_LanguageKey, '', '', '', '', '')

    
    if context.Quote.StatusName == lc_prep:
        for i in context.Quote.GetAllItems():
            
            
            if i['QI_UOM'] == "" :
                #i['QI_UOM'] = "EA"
                i['QI_UOM'] = lc_EA
            #if i['QI_PROD_CATEGORY'] == "Subcontractor" :
            if i['QI_PROD_CATEGORY'] == lc_prod_cat :
            # i['QI_RECORD_TYPE'] = "S"
                i['QI_RECORD_TYPE'] = lc_RecType_S
            #Aditi: 6th Oct: Product type will be Honeywell Hardware instead of First party material, so modified the condition
            #if i['QI_Product_Type'] == "First Party Material" or i['QI_Product_Type'] == "Honeywell Hardware":
            if i['QI_Product_Type'] == lc_prodType_FP or i['QI_Product_Type'] == lc_prodType_HH:
                #i['QI_RECORD_TYPE'] = "M"
                i['QI_RECORD_TYPE'] = lc_RecType_M
            #if i['QI_Product_Type'] == Third Party Hardware :
            if i['QI_Product_Type'] == lc_prodType_TPH :
                #i['QI_RECORD_TYPE'] = "T"
                i['QI_RECORD_TYPE'] = lc_RecType_T
            #if i['QI_Product_Type'] == Product Upload :
            if i['QI_Product_Type'] == lc_prodType_PU :
                #i['QI_RECORD_TYPE'] = "T"
                i['QI_RECORD_TYPE'] = lc_RecType_T    #end of change by Mounika