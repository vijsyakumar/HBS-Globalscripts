#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script define Values for Labor table present in Proposal Template Based
#on the values selected for Labor Type field in the Commercial Tab
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 09/06/2022    Sunil S                  0          -Initial Version
# 10/14/2022    Mounika Tarigopula       21         -Replaced Hardcodings
#                                                   -Incorporated Translation
# 11/04/2022	Srinivasan Dorairaj		 24			-Script Translation changes
# 11/22/2022    Payal Gupta              25         -Added SIN# number
# 12/07/2022    Payal Gupta              26         -Fixes
# 12/28/2022    Payal Gupta              27         - Changes as part of enhancement
#-----------------------------------------------------------------------------
#Begin of change by Mounika
import GM_TRANSLATIONS                   #Inserted by Mounika
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)    #Inserted by Mounika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Srinivasan Dorairaj
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Modified by Srinivasan Dorairaj
    lc_NT = GM_TRANSLATIONS.GetText('000033', lv_LanguageKey, '', '', '', '', '')       #NORMAL TIME
    lc_OT = GM_TRANSLATIONS.GetText('000034', lv_LanguageKey, '', '', '', '', '')       #OVERTIME
    lc_PT = GM_TRANSLATIONS.GetText('000035', lv_LanguageKey, '', '', '', '', '')       #PREMIUM TIME
    lc_nt = GM_TRANSLATIONS.GetText('000036', lv_LanguageKey, '', '', '', '', '')       #Normal Time
    lc_ot = GM_TRANSLATIONS.GetText('000037', lv_LanguageKey, '', '', '', '', '')       #Overtime
    lc_pt = GM_TRANSLATIONS.GetText('000038', lv_LanguageKey, '', '', '', '', '')       # premium Time
    lc_labor_cons = GM_TRANSLATIONS.GetText('000039',lv_LanguageKey, '', '', '', '', '')#Labor consolidated
    lc_labor = GM_TRANSLATIONS.GetText('000040', lv_LanguageKey, '', '', '', '', '')       #Labor
    lc_honeywell_labor = GM_TRANSLATIONS.GetText('000118', lv_LanguageKey, '', '', '', '', '') #Added by Payal
    lc_labor_bo = GM_TRANSLATIONS.GetText('000042', lv_LanguageKey, '', '', '', '', '')#Labor broken out
    all_items = context.Quote.GetAllItems()
    total_count = 0
    quantity_count = 0
    sell_price_count = 0
    final_total = 0
    list_price_count = 0
    discount_amount = 0
    disc_div = 0
    total_disc = final_discount = 0
    table_total_list = []
    #hourstypelist = ['NORMAL TIME','OVERTIME','PREMIUM TIME','Normal Time','Overtime','Premium Time']  #commented by Mounika
    hourstypelist = [lc_NT,lc_OT,lc_PT,lc_nt,lc_ot,lc_pt]                             #Inserted by Mounika
    Labor_item  =  context.Quote.GetCustomField('CF_LaborType').Value
    Labor_table = context.Quote.QuoteTables["QT_LABOR_PT"]
    Labor_table.Rows.Clear()

    qi_product_type = [i['QI_Product_Type'] for i in all_items]

    if lc_labor in qi_product_type or lc_honeywell_labor in qi_product_type:
        #if Labor_item == 'Labor consolidated':                 #commented by Mounika
        if Labor_item == lc_labor_cons:                       #Inserted by Mounika
            for i in all_items:
                #if 'Labor' in i['QI_Product_Type']:            #commented by Mounika
                if lc_labor in i['QI_Product_Type']:          #Inserted by Mounika
                    '''quantity_count += i.Quantity #Commented by Payal
                    sell_price_count += i['QI_Unit_Sell_Price']
                    discount_amount += i.DiscountAmount
                    discount_percent = discount_amount/sell_price_count
                    final_discount = discount_percent * 100'''
                    total = i.Quantity * i['QI_Unit_Sell_Price']
                    total_count += total
            final_row = Labor_table.AddNewRow()
            #final_row["DESCRIPTION"] = 'Labor'              #commented by Mounika 
            #final_row["DESCRIPTION"] = lc_labor              #Inserted by Mounika #Commented by Payal
            final_row["TOTAL"] = total_count
            '''final_row["QTY"] = quantity_count #Commented by Payal
            if final_row["QTY"] > 0:
                final_row["SELL_PRICE"] = final_row["TOTAL"]/final_row["QTY"]
            final_row["DISC_"] = final_discount
            final_discount_amount = final_discount/100
            final_row["LIST_PRICE"] = final_row["SELL_PRICE"]/(1-final_discount_amount)'''

        #if Labor_item == 'Labor broken out':      #commented by Mounika
        if Labor_item == lc_labor_bo:              #Inserted by Mounika
            for i in all_items:
                #if 'Labor' in i['QI_Product_Type']:        #commented by Mounika
                if lc_labor in i['QI_Product_Type']:      #Inserted by Mounika
                    new_row = Labor_table.AddNewRow()
                    new_row["PART_"] = i['QI_SAP_Activity_Type']
                    new_row["DESCRIPTION"] = i.Description
                    new_row["QTY"] = i.Quantity
                    new_row["SIN_"] = i['QI_Sin_Number']
                    new_row["LIST_PRICE"] = i['QI_Recommended_Unit_Sell_Price']
                    new_row["DISC_"] = i.DiscountPercent
                    new_row["SELL_PRICE"] = i['QI_Unit_Sell_Price']
                    total = i['QI_Unit_Sell_Price'] * i.Quantity
                    new_row["TOTAL"] = total
                    for i in range(len(hourstypelist)):
                        if(hourstypelist[i] in new_row["DESCRIPTION"]):
                            new_row["HOURS_TYPE"] = hourstypelist[i]
