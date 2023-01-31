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
# 01/02/2023    Aditi Sharma                        -Changes to default country as opportunity country if account country is None
# 01/30/2023    Sumandrita                         -Added condition to populate labor category break-up CXCPQ-38244 by Sumandrita
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
    lc_prodType_writein = GM_TRANSLATIONS.GetText('000175', lv_LanguageKey, '', '', '', '', '')

    quote_org = context.Quote.GetCustomField('CF_Sales_Org').Value    #Inserted by Dhruv
    for i in context.Quote.GetAllItems():
        if i.ProductTypeName != lc_prodType_writein :
            i['QI_Product_Type'] = i.ProductTypeName
        lv_part = i.PartNumber
        #lv_sub = SqlHelper.GetFirst("Select * from CT_MATERIALS_CDE_VALIDATION WHERE Part_no  = '"+str(lv_part)+"'")   #Commented by Dhruv
        lv_head = SqlHelper.GetFirst("Select * from CT_PRODUCT_HEADER WHERE PARTNUMBER = '{}' ".format(lv_part) )     #Inserted by Srinivasan Dorairaj
        #lv_sales = SqlHelper.GetFirst("Select * from CT_PRODUCT_SALES WHERE PARTNUMBER = '{}' and SALESORG = '{}' and LanguageKey = '{}'".format(lv_part,quote_org,lv_LanguageKey))   #Inserted by Srinivasan Dorairaj
        
        lv_sales = SqlHelper.GetFirst("Select * from CT_PRODUCT_SALES WHERE PARTNUMBER = '{}' and SALESORG = '{}' ".format(lv_part,quote_org))   #Inserted by Dhruv
        #Begin of change by Dhruv
        '''if lv_sub:
            i.DescriptionLong  = lv_sub.Description
            i['QI_UOM'] = str(lv_sub.UOM)
            i['QI_MFG_CODE'] = str(lv_sub.Vendor_Number)
            i['QI_PROD_CATEGORY'] = str(lv_sub.Sales_Category)'''
        #if lv_head:
        #   i.DescriptionLong  = lv_head.Description
        #   i['QI_UOM'] = str(lv_sub.UOM)
        if lv_sales:
            # Added by ishika
            if lv_sales.VENDOR_NUMBER:
                i['QI_MFG_CODE'] = str(lv_sales.VENDOR_NUMBER)
            if lv_sales.SALES_CATEGORY:
                i['QI_SALES_CATEGORY'] = str(lv_sales.SALES_CATEGORY)
            #------------------------#
        #i['QI_PROD_CATEGORY'] = str(lv_sales.SALES_CATEGORY_DESC)
        if i['QI_Product_Type'] == lc_prodType_FP or i['QI_Product_Type'] == lc_prodType_HH:
            if lv_head and lv_head.SOLUTION_FAMILY:
                sm_text = SqlHelper.GetFirst("SELECT * FROM CT_SM_TEXT WHERE ID = '{}' and LanguageKey='{}'".format(lv_head.SOLUTION_FAMILY,lv_LanguageKey))
                if sm_text:
                    lv_head.SOLUTION_FAMILY = str(sm_text.Text)
                i['QI_PROD_CATEGORY'] = lv_head.SOLUTION_FAMILY
                i['QI_Category'] = lv_head.SOLUTION_FAMILY #Added for CXCPQ-38244 by Sumandrita
            else:
                i['QI_PROD_CATEGORY'] = lc_prodcat_UA
                i['QI_Category'] = lc_prodcat_UA #Added for CXCPQ-38244 by Sumandrita
        elif i['QI_Product_Type'] == lc_prodType_TPH or i['QI_Product_Type'] == lc_prodType_TP or i['QI_Product_Type'] == lc_prodType_Adhoc :
            i['QI_PROD_CATEGORY'] = lc_prodcat_TP
            i['QI_Category'] = lc_prodcat_TP #Added for CXCPQ-38244 by Sumandrita
        elif lv_sales and lv_sales.VENDOR_TYPE != lc_vendor_type_HW  and lv_sales.VENDOR_TYPE != '' :
            i['QI_PROD_CATEGORY'] = lc_prodcat_TP
            i['QI_Category'] = lc_prodcat_TP #Added for CXCPQ-38244 by Sumandrita
        elif i['QI_Product_Type'] == lc_prodType_HL or i['QI_Product_Type'] == lc_prodType_LB:
            part = i.PartNumber
            #Change starts by Sumandrita
            productId = i.ProductId
            directory = SqlHelper.GetFirst("select * from directory where PRODUCT_ID = '{}'".format(i.ProductId))
            cat_id = directory.DIRECTORY_CD
            dir_name = SqlHelper.GetFirst("select * from directory_defn where DIRECTORY_CD = '{}'".format(cat_id))
            i['QI_PROD_CATEGORY'] = dir_name.DIR_NAME
            #end by Sumandrita
            #Added condition to populate labor category break-up CXCPQ-38244 by Sumandrita
            labour_summary = SqlHelper.GetFirst("select * from CT_Activity_Type where Ser_Material = '{}'".format(part))
            if labour_summary:
                i['QI_Category'] = labour_summary.Category
            #end
                
        #else:
            #i['QI_PROD_CATEGORY'] = lc_prodcat_TP
            

        #End of change by Dhruv
        lv_branch = context.Quote.GetCustomField("CF_Branch/Profit Center").Value
        lv_opp_typ = context.Quote.GetCustomField("CF_Opportunity_Type").Value
        bp_country = context.Quote.GetCustomField("CF_Country").Value
        if lv_branch and lv_opp_typ and bp_country:
            lv_sub = SqlHelper.GetFirst("Select * from CT_PRCTR_MASTER WHERE Branch = '{0}' and OpportunityType = '{1}' and CountryKey = '{2}' and LanguageKey='{3}'".format(lv_branch,lv_opp_typ,bp_country,lv_LanguageKey))
            if lv_sub:
                if i['CFI_SUB_LOCATION'] is None:
                    i['CFI_SUB_LOCATION'] = lv_sub.BranchID
                    
                if i['QI_Branch'] is None:
                    i['QI_Branch'] = str(lv_sub.Branch_Name)
        #CXCPQ-36051 end
                            

    #if context.Quote.StatusName == "Preparing":         #Begin of change by Mounika
    #Log.Info('116---->')
    if context.Quote.StatusName == lc_prep:
        for i in context.Quote.GetAllItems():
            #Log.Info('116--QI_Product_Type-->'+str(i['QI_Product_Type'])+'--CATEGORY----'+str(i['QI_PROD_CATEGORY']))
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