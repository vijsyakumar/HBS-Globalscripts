#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#Based on the Contingency custom field value we are updating the quote items 
#values and quote table values
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 7/4/2022      Payal Gupta           0         -initial version
# 10/17/2022	MarripudiKrishna 	  4	        -Replaced Hardcodings
#				Chaitanya						-Incorporated Translation
##03/11/2022     Srijaydhurga         7         -Script translation changes
# 11/24/2022    Payal Gupta           8         - Added code as per new requirements
# 12/02/2022    Payal Gupta           9         - Added code as per new requirements
# 12/03/2022    Payal Gupta           10        - Added code as per new requirements
# 12/28/2022    Payal Gupta           11        - Changes as part of enhancement
# 01/11/2022    Payal Gupta           12        - Changes as part of enhancement
# 01/24/2023    Sumandrita                      - Commented allocate to material part, that part will be addressed in GS_Allocate_Material
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS                   												 #Added by krishna
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)   								 #Added by krishna
#lc_op_type = GM_TRANSLATIONS.GetText('000024', lv_LanguageKey, '', '', '', '', '')		 #Added by krishna
#if (context.Quote.GetCustomField('CF_Opportunity_Type').Value) == lc_op_type :			 #Added by krishna
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') # Added by Dhurga
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Added by Dhurga

    lc_allocate_labor = GM_TRANSLATIONS.GetText('000045', lv_LanguageKey, '', '', '', '', '')        #Added by krishna
    lc_contingency = GM_TRANSLATIONS.GetText('000100', lv_LanguageKey, '', '', '', '', '')        #Added by krishna
    lc_details = GM_TRANSLATIONS.GetText('000067', lv_LanguageKey, '', '', '', '', '') #Added by Payal
    lc_lumpsum = GM_TRANSLATIONS.GetText('000066', lv_LanguageKey, '', '', '', '', '') #Added by Payal
    lc_allocate_to_material = GM_TRANSLATIONS.GetText('000216', lv_LanguageKey, '', '', '', '', '') #Added by Payal

    all_items = context.Quote.GetAllItems()
    total_value_count = 0
    labor_table_list = []
    table_total_list = []
    material_table_list = []
    final_total = 0
    quantity_count = 0
    total_count = 0
    sell_price_count = 0
    discount_amount = 0
    total_Material_Sellp = 0
    sellP = 0
    material_allocation = 0
    remain_sellP = 0

    ###-----Getting Contingency Value-----###

    contingency =  context.Quote.GetCustomField('Contingency').Value
    final_table_contingency = context.Quote.QuoteTables["Contingency"]
    final_table_contingency.Rows.Clear()
    material_quote_table=context.Quote.QuoteTables['QT_Materials']
    material_quote_table.Rows.Clear()


    qi_product_type = [i['QI_Product_Type'] for i in all_items]

    if lc_contingency in qi_product_type:
        ###-----Contingency type is Allocate to Labor-----###

        #if contingency == 'Allocate to Labor':            #commented by krishna
        if contingency == lc_allocate_labor:                        #Added by krishna
            for i in all_items:
                #if 'Contingency' in i['QI_Product_Type']:  #commented by krishna
                if lc_contingency in i['QI_Product_Type']:  #Added by krishna
                    sell_price = i['QI_Unit_Sell_Price']
                    quantity = i.Quantity
                    total_value = sell_price * quantity
                    total_value_count += total_value
            labor_table=context.Quote.QuoteTables['QT_LABOR_PT'].Rows
            for j in labor_table:
                labor_table_list.append(j)
            labor_table_first_row = labor_table_list[0]
            labor_sell_price = labor_table_first_row["SELL_PRICE"]
            labor_quantity = labor_table_first_row["QTY"]
            contingency_total = total_value_count/labor_sell_price
            labor_table_first_row["QTY"] = labor_quantity + contingency_total
            labor_table_first_row["TOTAL"] = labor_table_first_row["QTY"] * labor_sell_price


        ###-----Contingency type is Detail-----### #Added by Payal

        if contingency == lc_details:
            for i in all_items:
                if lc_contingency in i['QI_Product_Type']:
                    final_row = final_table_contingency.AddNewRow()
                    final_row["DESCRIPTION"] = i.Description
                    final_row["QTY"] = i.Quantity
                    final_row["LIST_PRICE"] = i['QI_Recommended_Unit_Sell_Price']
                    final_row["DISC_"] = i.DiscountPercent
                    final_row["SELL_PRICE"] = i['QI_Unit_Sell_Price']
                    total = i['QI_Unit_Sell_Price'] * i.Quantity
                    final_row["TOTAL"] = total

        ###-----Contingency type is Lumpsum-----### #Added by Payal

        if contingency == lc_lumpsum:
            for i in all_items:
                if lc_contingency in i['QI_Product_Type']:
                    '''quantity_count += i.Quantity #Commented by Payal
                    sell_price_count += i['QI_Unit_Sell_Price']
                    discount_amount += i.DiscountAmount
                    discount_percent = discount_amount/sell_price_count
                    final_discount = discount_percent * 100'''
                    total = i.Quantity * i['QI_Unit_Sell_Price']
                    total_count += total
            final_row = final_table_contingency.AddNewRow()
            #final_row["DESCRIPTION"] = lc_contingency #Commented by Payal
            final_row["TOTAL"] = total_count
            '''final_row["QTY"] = quantity_count #Commented by Payal
            final_row["SELL_PRICE"] = final_row["TOTAL"]/final_row["QTY"]
            final_row["DISC_"] = final_discount
            final_discount_amount = final_discount/100
            final_row["LIST_PRICE"] = final_row["SELL_PRICE"]/(1-final_discount_amount)'''

        ###-----When Contingency type is Allocate to Material-----### #Added by Payal

        '''if contingency == lc_allocate_to_material:
            for i in all_items:
                if lc_contingency in i['QI_Product_Type']:
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
            if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0 :
                Trace.Write("Total Material SellPrice " +str(total_Material_Sellp))
                propotionate_value = item.NetPrice / Mat_SellP
                material_allocation = round((propotionate_value * sellP),2)
                remain_sellP = round((sellP - material_allocation),2)
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
            msg = GM_TRANSLATIONS.GetText('000229', lv_LanguageKey,str(prd_type), str(quote_type_value), '', '', '')
            exitmsgs = context.Quote.Messages
            if exitmsgs.Count > 0:
                for msges in exitmsgs:
                    #if  "is not allowed for Quote Type" in str(msges.Content):
                    lv_msg_txt = GM_TRANSLATIONS.GetText('000229', lv_LanguageKey, '', '', '', '', '')
                    if  lv_msg_txt in str(msges.Content):
                        context.Quote.DeleteMessage(msges.Id)
            context.Quote.AddMessage(msg,MessageLevel.Error,True)'''


    ###-----Calculating total for proposal template-----###

    final_table_contingency = context.Quote.QuoteTables["Contingency"].Rows
    for row in final_table_contingency:
        table_total_list.append(row)
    for t in range(len(table_total_list)):
        table_total_row = table_total_list[t]
        table_total = table_total_row["TOTAL"]
        final_total += table_total
    context.Quote.GetCustomField('CF_TOTAL_CONTINGENCY').Value = '%.2f' %final_total