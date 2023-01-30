#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for extra charges calculation
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 09/06/2022    Payal Gupta                0             -Initial Version
# 10/17/2022    Ishika Bhattacharya        33            -Replaced Hardcodings
#                                                        -Incorporated Translation
# 11/04/2022	Srinivasan Dorairaj		   34			 -Script Translation changes
# 12/02/2022    Payal Gupta                35            - Changes as part of enhancement
# 12/03/2022    Payal Gupta                36            - Changes as part of enhancement
# 12/06/2022    Payal Gupta                37            -Fixes for mandatory charges
# 12/28/2022    Payal Gupta                38            - Changes as part of enhancement
# 01/11/2022    Payal Gupta                39            -Changes as part of enhancement
# 01/19/2023    Sumandrita                               -modified allocation calculation
# 01/24/2023    Sumandrita                      - Commented allocate to material part, that part will be addressed in GS_Allocate_Material
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS    # Added by Ishika
from Scripting.Quote import MessageLevel
# Added by Ishika
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Srinivasan Dorairaj
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Modified by Srinivasan Dorairaj
    lc_detail = GM_TRANSLATIONS.GetText('000067', lv_LanguageKey, '', '', '', '', '')
    lc_lumpsum = GM_TRANSLATIONS.GetText('000066', lv_LanguageKey, '', '', '', '', '')
    lc_allocate_to_labor = GM_TRANSLATIONS.GetText('000045', lv_LanguageKey, '', '', '', '', '')
    lc_extra_charges = GM_TRANSLATIONS.GetText('000121', lv_LanguageKey, '', '', '', '', '')
    lc_other_costs = GM_TRANSLATIONS.GetText('000215', lv_LanguageKey, '', '', '', '', '') #Added by Payal
    lc_allocate_to_material = GM_TRANSLATIONS.GetText('000216', lv_LanguageKey, '', '', '', '', '') #Added by Payal
    #lv_msg_txt = GM_TRANSLATIONS.GetText('000229', lv_LanguageKey, '', '', '', '', '')

    all_items = context.Quote.GetAllItems()
    quantity_count = 0
    sell_price_count_mandatory = 0
    sell_price_count = 0
    final_sell_price = 0
    total_count = 0
    total_sell_price = 0
    total_quantity = 0
    final_total = 0
    total_value_count = 0
    discount_amount = 0
    labor_table_list = []
    material_table_list = []
    table_total_list = []
    total_Material_Sellp = 0
    sellP = 0
    material_allocation = 0
    remain_sellP = 0

    ###-----Getting Extra Charges Table-----###

    extra_charges_item =  context.Quote.GetCustomField('Extra Charges').Value
    final_table_extra_charges = context.Quote.QuoteTables["QT_Extra_charges"]
    final_table_extra_charges.Rows.Clear()
    material_quote_table=context.Quote.QuoteTables['QT_Materials']
    material_quote_table.Rows.Clear()
    qi_product_type = [i['QI_Product_Type'] for i in all_items]

    if lc_extra_charges in qi_product_type:
        ###-----When Extra Charges type is Detail-----###

        # if extra_charges_item == 'Detail':       "Commented by Ishika
        if extra_charges_item == lc_detail:         # Added by Ishika
            for i in all_items:
                # if 'Extra Charges' in i['QI_Product_Type']:  "Commented by Ishika
                if lc_extra_charges in i['QI_Product_Type']:    # Added by Ishika
                    final_row = final_table_extra_charges.AddNewRow()
                    final_row["Description"] = i.Description
                    final_row["QTY"] = i.Quantity
                    final_row["LIST_PRICE"] = i['QI_Recommended_Unit_Sell_Price']
                    final_row["DISC_"] = i.DiscountPercent
                    if i['QI_Unit_Sell_Price'] ==0:
                        final_row["SELL_PRICE"] = i.NetPrice
                    else:
                        final_row["SELL_PRICE"] = i['QI_Unit_Sell_Price']
                    final_row["TOTAL"] = final_row["SELL_PRICE"] * final_row["QTY"]

        ###-----When Extra Charges type is Lumpsum-----### #Added by Payal

        if extra_charges_item == lc_lumpsum:
            for i in all_items:
                if lc_extra_charges in i['QI_Product_Type']:
                    '''quantity_count += i.Quantity #Commented by Payal
                    if i['QI_Unit_Sell_Price'] ==0:
                        sell_price_count_mandatory += i.NetPrice
                    else:
                        sell_price_count += i['QI_Unit_Sell_Price']
                    final_sell_price = sell_price_count_mandatory + sell_price_count
                    discount_amount += i.DiscountAmount
                    discount_percent = discount_amount/final_sell_price
                    final_discount = discount_percent * 100'''
                    if i['QI_Unit_Sell_Price'] ==0:
                        total = i.Quantity * i.NetPrice
                    else:
                        total = i.Quantity * i['QI_Unit_Sell_Price']
                    total_count += total
            final_row = final_table_extra_charges.AddNewRow()
            #final_row["DESCRIPTION"] = lc_other_costs #Commented by Payal
            final_row["TOTAL"] = total_count
            '''final_row["QTY"] = quantity_count #Commented by Payal
            final_row["SELL_PRICE"] = final_row["TOTAL"]/final_row["QTY"]
            final_row["DISC_"] = final_discount
            final_discount_amount = final_discount/100
            final_row["LIST_PRICE"] = final_row["SELL_PRICE"]/(1-final_discount_amount)'''

        ###-----When Extra Charges type is Allocate to Material-----### #Added by Payal

        '''if extra_charges_item == lc_allocate_to_material:     # Added by Payal
            for i in all_items:
                if lc_extra_charges in i['QI_Product_Type']:    # Added by Payal
                    if i['QI_Unit_Sell_Price'] ==0:
                        sell_price = i.NetPrice
                    else:
                        sell_price = i['QI_Unit_Sell_Price']
                    quantity = i.Quantity
                    total_value = sell_price * quantity
                    total_value_count += total_value
        sellP = total_value_count
        remain_sellP = sellP
        for item in all_items :
            if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0:
                Trace.Write("Yes")
                mat_SellPrice = item.NetPrice
                total_Material_Sellp += item.NetPrice
        Mat_SellP = total_Material_Sellp
        
        for item in all_items :
            if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0:
                Trace.Write("Total Material SellPrice " +str(total_Material_Sellp))
                propotionate_value = item.NetPrice / Mat_SellP
                material_allocation = round((propotionate_value * sellP),2)
                remain_sellP = round((remain_sellP - material_allocation),2)
                Trace.Write("Mat Allocation " +str(material_allocation))
                Trace.Write("SellP" +str(sellP))
                newsellP = item.NetPrice + material_allocation
                Trace.Write("Allocation SellP" +str(item['QI_Product_Type']) +str(newsellP))
                material_quote_table=context.Quote.QuoteTables['QT_Materials']
                
                newRow = material_quote_table.AddNewRow()
                newRow['PART_'] = item.PartNumber
                Trace.Write("Part " +str(newRow['PART_']))
                newRow['DESCRIPTION'] = item.Description
                Trace.Write("Description")
                newRow['QTY'] = item.Quantity
                newRow['SELL_PRICE'] = newsellP
                Trace.Write ("Sell Price allocated " +str(item.PartNumber) +str(newsellP)) 
                newRow['TOTAL'] = newRow['SELL_PRICE'] * newRow['QTY']    
        if remain_sellP > 0 :
            Trace.Write("True")
            msg = 'All materials are CSPA/GSA so other costs cannot be allocated to material' #GM_TRANSLATIONS.GetText('000229', lv_LanguageKey,str(prd_type), str(quote_type_value), '', '', '')
            exitmsgs = context.Quote.Messages
            if exitmsgs.Count > 0:
                for msges in exitmsgs:
                    #if  "is not allowed for Quote Type" in str(msges.Content):
                    lv_msg_txt = 'All materials are CSPA/GSA so other costs cannot be allocated to material' 
                    if  lv_msg_txt in str(msges.Content):
                        context.Quote.DeleteMessage(msges.Id)
            context.Quote.AddMessage(msg,MessageLevel.Error,True)'''
            
        ###-----When Extra Charges type is Allocate to Labor-----###

        # if extra_charges_item == 'Allocate to Labor':     "Commented By Ishika
        if extra_charges_item == lc_allocate_to_labor:       # Added by Ishika
            for i in all_items:
                # if 'Extra Charges' in i['QI_Product_Type']:   "Commented By Ishika
                if lc_extra_charges in i['QI_Product_Type']:    # Added by Ishika
                    if i['QI_Unit_Sell_Price'] ==0:
                        sell_price = i.NetPrice
                    else:
                        sell_price = i['QI_Unit_Sell_Price']
                    quantity = i.Quantity
                    total_value = sell_price * quantity
                    total_value_count += total_value
            quote_table=context.Quote.QuoteTables['QT_LABOR_PT'].Rows
            for j in quote_table:
                labor_table_list.append(j)
            labor_table_first_row = labor_table_list[0]
            labor_sell_price = labor_table_first_row["SELL_PRICE"]
            labor_quantity = labor_table_first_row["QTY"]
            extra_charges_total = total_value_count/labor_sell_price
            labor_table_first_row["QTY"] = labor_quantity + extra_charges_total
            labor_table_first_row["TOTAL"] = labor_table_first_row["QTY"] * labor_sell_price

    ###-----Calculating total for proposal template-----###

    final_table_extra_charges = context.Quote.QuoteTables['QT_Extra_charges'].Rows
    for row in final_table_extra_charges:
        table_total_list.append(row)
    for t in range(len(table_total_list)):
        table_total_row = table_total_list[t]
        table_total = table_total_row["TOTAL"]
        final_total += table_total
    context.Quote.GetCustomField('CF_TOTAL_EXTRA_CHARGES').Value = '%.2f' %final_total