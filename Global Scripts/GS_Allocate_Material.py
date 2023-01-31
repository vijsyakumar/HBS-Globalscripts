import GM_TRANSLATIONS
from Scripting.Quote import MessageLevel
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') 
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type :
    lc_sub_con = GM_TRANSLATIONS.GetText('000026', lv_LanguageKey, '', '', '', '', '') 
    lc_allocate_to_material = GM_TRANSLATIONS.GetText('000216', lv_LanguageKey, '', '', '', '', '') 
    context.Quote.GetCustomField("CF_Allocation").Value = ""
    context.Quote.GetCustomField("CF_Travel_Allocation").Value = ""
    context.Quote.GetCustomField("CF_Extra_Allocation").Value = ""
    context.Quote.GetCustomField("CF_Contingency_Allocation").Value = ""
    context.Quote.GetCustomField("CF_CSPA_Error").Value = ""
    all_items = context.Quote.GetAllItems()
    allocation_Value = ""
    total_value_count = 0
    total_value_count_Travel = 0
    labor_table_list = []
    table_total_list = []
    material_table_list = []
    sellP = 0
    remain_sellP = 0
    remain_sellP_Travel = 0
    remain_sellP_Extra = 0
    newsellP = 0
    material_allocation = 0
    total_Material_Sellp = 0
    mat_SellPrice_Travel = 0
    Mat_SellP_Travel = 0
    total_value_contingency = 0
    total_value_count_Contingency = 0
    sellP_Contingecy = 0
    remain_sellP_Contingency = 0
    mat_SellPrice_Contingency = 0
    Material_Sellp_Contingency = 0
    Mat_SellP_Contingency = 0
    lc_travel_expense = GM_TRANSLATIONS.GetText('000085', lv_LanguageKey, '', '', '', '', '')
    other_expenses = context.Quote.GetCustomField('Other Expenses').Value
    lc_extra_charges = GM_TRANSLATIONS.GetText('000121', lv_LanguageKey, '', '', '', '', '')
    lc_other_costs = GM_TRANSLATIONS.GetText('000215', lv_LanguageKey, '', '', '', '', '') 
    final_table_other_expenses = context.Quote.QuoteTables["Travel_Expenses"]
    #final_table_other_expenses.Rows.Clear()
    abc = 0
    Material_Sellp_Travel =0 
    total_value_Extra = 0
    total_value_count_Extra = 0
    sellP_Extra = 0
    remain_sellP_Extra = 0
    mat_SellPrice_Extra = 0
    Material_Sellp_Extra = 0
    Mat_SellP_Extra = 0
    lc_contingency = GM_TRANSLATIONS.GetText('000100', lv_LanguageKey, '', '', '', '', '')   
    contingency =  context.Quote.GetCustomField('Contingency').Value
    subcontractor_item  =  context.Quote.GetCustomField('Sub Contractor').Value
    final_table_extra_charges = context.Quote.QuoteTables["QT_SUBCON"]
    #final_table_extra_charges.Rows.Clear()
    material_quote_table=context.Quote.QuoteTables['QT_Materials']
   
    extra_charges_item = context.Quote.GetCustomField('Extra Charges').Value
    
    final_table_labor = context.Quote.QuoteTables["QT_LABOR_PT"]
    qi_product_type = [i['QI_Product_Type'] for i in all_items]
#SUBCONTRACTOR
    if lc_sub_con in qi_product_type:
        if subcontractor_item == lc_allocate_to_material:
            if context.Quote.GetCustomField("CF_Allocation").Value != "Yes SubCon" and (context.Quote.GetCustomField("CF_Travel_Allocation").Value == "Yes OtherCost" or context.Quote.GetCustomField("CF_Extra_Allocation").Value == "Yes ExtraCharges" or context.Quote.GetCustomField("CF_Contingency_Allocation").Value == "Contingency" ):
                for i in all_items:
                    if lc_sub_con in i['QI_Product_Type']:
                        sell_price = i['QI_Unit_Sell_Price']
                        quantity = i.Quantity
                        total_value = sell_price * quantity
                        total_value_count += i.NetPrice
                sellP = total_value_count
                remain_sellP = sellP
                for item in all_items :
                    if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0  :
                        mat_SellPrice = item.NetPrice
                        Material_Sellp += item.NetPrice
                Mat_SellP1 = Material_Sellp
                for item in all_items :
                    if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0  :
                        propotionate_value = item.NetPrice / Mat_SellP
                        material_allocation = round((propotionate_value * sellP),2)
                        remain_sellP = round((remain_sellP - material_allocation),2)
                        value = remain_sellP
                        for r in material_quote_table.Rows :
                            if r['PART_'] == item.PartNumber:
                                Trace.Write("sellPrice row " + str(item.PartNumber) +str(r['SELL_PRICE']))
                                r['TOTAL'] = r['TOTAL'] + material_allocation
                                r['SELL_PRICE'] = r['TOTAL'] / item.Quantity
                                Trace.Write("Allocation SellP" + str(item.PartNumber) +str(r['SELL_PRICE']))
                

                       
                Trace.Write("Remain" +str(remain_sellP))
                if remain_sellP > 0 :
                    '''Trace.Write("Remain sell price last" +str(remain_sellP))
                    msg = 'All materials are CSPA/GSA so other costs cannot be allocated to material'
                    exitmsgs = context.Quote.Messages
                    if exitmsgs.Count > 0:
                        for msges in exitmsgs:
                            #if  "is not allowed for Quote Type" in str(msges.Content):
                            lv_msg_txt = 'All materials are CSPA/GSA so other costs cannot be allocated to material'
                            if  lv_msg_txt in str(msges.Content):
                                context.Quote.DeleteMessage(msges.Id)
                    context.Quote.AddMessage(msg,MessageLevel.Warning,False)'''
                    context.Quote.GetCustomField("CF_CSPA_Error").Value = "True"
                
            else:
                Trace.Write("else subcon.....")
                material_quote_table.Rows.Clear()
                Trace.Write("Yes 1")
                for i in all_items:
                    if lc_sub_con in i['QI_Product_Type']:
                        Trace.Write("Yes 2")
                        sell_price = i['QI_Unit_Sell_Price']
                        quantity = i.Quantity
                        total_value = sell_price * quantity
                        total_value_count += total_value
                        Trace.Write("Total SubCon" +str(total_value_count))
                sellP = total_value_count
                remain_sellP = sellP
                for item in all_items :
                    if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0  :
                        Trace.Write("Yes")
                        mat_SellPrice = item.NetPrice
                        total_Material_Sellp += item.NetPrice
                Mat_SellP = total_Material_Sellp
                
                for item in all_items :
                    if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0  :
                        Trace.Write("Total Material SellPrice " +str(total_Material_Sellp))
                        propotionate_value = item.NetPrice / Mat_SellP
                        material_allocation = round((propotionate_value * sellP),2)
                        Trace.Write("Mat Allocation " +str(material_allocation))
                        remain_sellP = round((remain_sellP - material_allocation),2)
                        value = remain_sellP
                        Trace.Write("Value " +str(value))
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
                        newRow['TOTAL'] = newsellP
                        newRow['SELL_PRICE'] = newsellP / item.Quantity
                    elif  (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] != 0 :
                        if allocation_Value != "Done":
                            material_quote_table=context.Quote.QuoteTables['QT_Materials']
                            
                            newRow = material_quote_table.AddNewRow()
                            newRow['PART_'] = item.PartNumber
                            Trace.Write("Part " +str(newRow['PART_']))
                            newRow['DESCRIPTION'] = item.Description
                            Trace.Write("Description")
                            newRow['QTY'] = item.Quantity
                            newRow['SELL_PRICE'] = item.NetPrice/ newRow['QTY']
                            Trace.Write ("Sell Price allocated " +str(item.PartNumber) +str(newsellP)) 
                            newRow['TOTAL'] = item.NetPrice
                allocation_Value == "Done"
                context.Quote.GetCustomField("CF_Allocation").Value = "Yes Subcon"
                Trace.Write("Remain" +str(remain_sellP))
                if remain_sellP > 0 :
                    '''Trace.Write("Remain sell price last" +str(remain_sellP))
                    msg = 'All materials are CSPA/GSA so other costs cannot be allocated to material'
                    exitmsgs = context.Quote.Messages
                    if exitmsgs.Count > 0:
                        for msges in exitmsgs:
                            #if  "is not allowed for Quote Type" in str(msges.Content):
                            lv_msg_txt = 'All materials are CSPA/GSA so other costs cannot be allocated to material'
                            if  lv_msg_txt in str(msges.Content):
                                context.Quote.DeleteMessage(msges.Id)
                    context.Quote.AddMessage(msg,MessageLevel.Warning,False)'''
                    context.Quote.GetCustomField("CF_CSPA_Error").Value = "True"

    #TRAVEL_EXPENSES.............................................................................................                
    if lc_travel_expense in qi_product_type:
        if other_expenses == lc_allocate_to_material:
            if context.Quote.GetCustomField("CF_Travel_Allocation").Value != "Yes OtherCost" and (context.Quote.GetCustomField("CF_Allocation").Value == "Yes Subcon" or context.Quote.GetCustomField("CF_Extra_Allocation").Value == "Yes ExtraCharges" or context.Quote.GetCustomField("CF_Contingency_Allocation").Value == "Contingency" ):

               
                Trace.Write("if Tarvel....")
                for i in context.Quote.GetAllItems():
                    if i['QI_Product_Type'] == 'Travel Expenses':
                        Trace.Write("Yes Travel")
                        sell_price = i['QI_Unit_Sell_Price']
                        quantity = i.Quantity
                        total_value = sell_price * quantity
                        total_value_count_Travel += i.NetPrice
                        Trace.Write("Total Travel" +str(total_value_count_Travel))
                sellP = total_value_count_Travel
                remain_sellP_Travel = sellP
                for item in context.Quote.GetAllItems() :
                    if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0  :
                        Trace.Write("Yes")
                        mat_SellPrice_Travel = item.NetPrice
                        Material_Sellp_Travel += item.NetPrice
                Mat_SellP_Travel = Material_Sellp_Travel
                for item in all_items :
                    if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0  :
                        Trace.Write("Total Material SellPrice " +str(Material_Sellp_Travel))
                        propotionate_value = item.NetPrice / Mat_SellP_Travel
                        Trace.Write("else Prop Value" +str(propotionate_value))
                        material_allocation = round((propotionate_value * sellP),2)
                        Trace.Write("Mat Allocation " +str(material_allocation))
                        remain_sellP_Travel = round((remain_sellP_Travel - material_allocation),2)

                        value1 = remain_sellP_Travel
                        Trace.Write("Value " +str(value1))
                        Trace.Write("SellP" +str(sellP))
                        for r in material_quote_table.Rows :
                            if r['PART_'] == item.PartNumber:
                                Trace.Write("sellPrice row " + str(item.PartNumber) +str(r['SELL_PRICE']))
                                r['TOTAL'] = r['TOTAL'] + material_allocation
                                r['SELL_PRICE'] = r['TOTAL']/ r['QTY']
                                Trace.Write("Allocation SellP" + str(item.PartNumber) +str(r['SELL_PRICE']))

                Trace.Write("Remain" +str(remain_sellP_Travel))
                if remain_sellP_Travel > 0 :
                    '''Trace.Write("Remain sell price last" +str(remain_sellP))
                    msg = 'All materials are CSPA/GSA so other costs cannot be allocated to material'
                    exitmsgs = context.Quote.Messages
                    if exitmsgs.Count > 0:
                        for msges in exitmsgs:
                            #if  "is not allowed for Quote Type" in str(msges.Content):
                            lv_msg_txt = 'All materials are CSPA/GSA so other costs cannot be allocated to material'
                            if  lv_msg_txt in str(msges.Content):
                                context.Quote.DeleteMessage(msges.Id)
                    context.Quote.AddMessage(msg,MessageLevel.Warning,False)'''
                    context.Quote.GetCustomField("CF_CSPA_Error").Value = "True"

            else:
                Trace.Write("Else travel...")
                material_quote_table.Rows.Clear()
                Trace.Write("Yes 1")
                for i in all_items:
                    if lc_travel_expense in i['QI_Product_Type']:
                        Trace.Write("Yes 2")
                        sell_price = i['QI_Unit_Sell_Price']
                        quantity = i.Quantity
                        total_value = sell_price * quantity
                        total_value_count_Travel += i.NetPrice
                        Trace.Write("Total SubCon" +str(total_value_count_Travel))
                sellP_Travel = total_value_count_Travel
                remain_sellP = sellP_Travel
                for item in context.Quote.GetAllItems() :
                    if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0  :
                        Trace.Write("Yes")
                        mat_SellPrice_Travel = item.NetPrice
                        Material_Sellp_Travel += item.NetPrice
                Mat_SellP_Travel = Material_Sellp_Travel

                for item in all_items :
                    if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0  :
                        Trace.Write("Total Material SellPrice " +str(Mat_SellP_Travel))
                        propotionate_value = item.NetPrice / Mat_SellP_Travel
                        material_allocation = round((propotionate_value * sellP_Travel),2)
                        Trace.Write("Mat Allocation " +str(material_allocation))
                        remain_sellP = round((remain_sellP - material_allocation),2)
                        value = remain_sellP
                        Trace.Write("Value " +str(value))
                        Trace.Write("SellP" +str(sellP))
                        newsellP = item.NetPrice + material_allocation
                        Trace.Write("Allocation SellP" + str(item.PartNumber) +str(newsellP))

                        material_quote_table=context.Quote.QuoteTables['QT_Materials']

                        newRow = material_quote_table.AddNewRow()
                        newRow['PART_'] = item.PartNumber
                        Trace.Write("Part " +str(newRow['PART_']))
                        newRow['DESCRIPTION'] = item.Description
                        Trace.Write("Description")
                        newRow['QTY'] = item.Quantity
                        newRow['SELL_PRICE'] = newsellP / newRow['QTY']
                        Trace.Write ("Sell Price allocated " +str(item.PartNumber) +str(newsellP)) 
                        newRow['TOTAL'] = newsellP 
                    elif (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] != 0 :
                        Trace.Write("Part no" +str(item.PartNumber))
                        material_quote_table = context.Quote.QuoteTables['QT_Materials']
                        if allocation_Value != "Done" :
                            newRow = material_quote_table.AddNewRow()
                            newRow['PART_'] = item.PartNumber
                            Trace.Write("ROW Name " +str(newRow['PART_']))
                            Trace.Write("Part " +str(newRow['PART_']))
                            newRow['DESCRIPTION'] = item.Description
                            Trace.Write("Description")
                            newRow['QTY'] = item.Quantity
                            newRow['SELL_PRICE'] = item.NetPrice/ newRow['QTY']
                            Trace.Write ("Sell Price allocated " +str(item.PartNumber) +str(newsellP)) 
                            newRow['TOTAL'] = item.NetPrice
                allocation_Value == "Done"
                context.Quote.GetCustomField("CF_Travel_Allocation").Value = "Yes OtherCost"
                Trace.Write("Remain" +str(remain_sellP))
                if remain_sellP > 0 :
                    '''Trace.Write("Remain sell price last" +str(remain_sellP))
                    msg = 'All materials are CSPA/GSA so other costs cannot be allocated to material'
                    exitmsgs = context.Quote.Messages
                    if exitmsgs.Count > 0:
                        for msges in exitmsgs:
                            #if  "is not allowed for Quote Type" in str(msges.Content):
                            lv_msg_txt = 'All materials are CSPA/GSA so other costs cannot be allocated to material'
                            if  lv_msg_txt in str(msges.Content):
                                context.Quote.DeleteMessage(msges.Id)
                    context.Quote.AddMessage(msg,MessageLevel.Warning,False)'''
                    context.Quote.GetCustomField("CF_CSPA_Error").Value = "True"
                    
    #EXTRA_CHARGES..............................................................................................
    if lc_extra_charges in qi_product_type:
        if extra_charges_item == lc_allocate_to_material:          
            
            if context.Quote.GetCustomField("CF_Extra_Allocation").Value != "Yes ExtraCharges" and (context.Quote.GetCustomField("CF_Travel_Allocation").Value == "Yes OtherCost" or context.Quote.GetCustomField("CF_Allocation").Value == "Yes Subcon" or context.Quote.GetCustomField("CF_Contingency_Allocation").Value == "Contingency" ):

               
                Trace.Write("if ExtraCharges....")
                for i in context.Quote.GetAllItems():
                    if i['QI_Product_Type'] == 'Extra Charges':
                        
                        sell_price = i['QI_Unit_Sell_Price']
                        quantity = i.Quantity
                        total_value_Extra = sell_price * quantity
                        total_value_count_Extra += i.NetPrice
                        
                sellP_Extra = total_value_count_Extra
                remain_sellP_Extra = sellP_Extra
                for item in context.Quote.GetAllItems() :
                    if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0  :
                        
                        mat_SellPrice_Extra = item.NetPrice
                        Material_Sellp_Extra += item.NetPrice
                Mat_SellP_Extra = Material_Sellp_Extra
                for item in all_items :
                    if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0  :
                        Trace.Write("Total Material SellPrice " +str(Material_Sellp_Extra))
                        propotionate_value = item.NetPrice / Mat_SellP_Extra
                        material_allocation = round((propotionate_value * sellP_Extra),2) 
                        remain_sellP_Extra = round((remain_sellP_Extra - material_allocation),2)
                        value1 = remain_sellP_Extra
                        for r in material_quote_table.Rows :
                            if r['PART_'] == item.PartNumber:
                                Trace.Write("sellPrice row " + str(item.PartNumber) +str(r['SELL_PRICE']))
                                r['TOTAL'] = r['TOTAL'] + material_allocation
                                r['SELL_PRICE'] = r['TOTAL'] / r['QTY']
                                Trace.Write("Allocation SellP" + str(item.PartNumber) +str(r['SELL_PRICE']))
                   

                Trace.Write("Remain" +str(remain_sellP_Extra))
                if remain_sellP_Extra > 0 :
                    Trace.Write("Remain sell price last" +str(remain_sellP_Extra))
                    msg = 'All materials are CSPA/GSA so other costs cannot be allocated to material'
                    exitmsgs = context.Quote.Messages
                    if exitmsgs.Count > 0:
                        '''for msges in exitmsgs:
                            #if  "is not allowed for Quote Type" in str(msges.Content):
                            lv_msg_txt = 'All materials are CSPA/GSA so other costs cannot be allocated to material'
                            if  lv_msg_txt in str(msges.Content):
                                context.Quote.DeleteMessage(msges.Id)
                    context.Quote.AddMessage(msg,MessageLevel.Warning,False)'''
                    context.Quote.GetCustomField("CF_CSPA_Error").Value = "True"

            else:
                material_quote_table.Rows.Clear()
                for i in context.Quote.GetAllItems():
                    if i['QI_Product_Type'] == 'Extra Charges':
                        Trace.Write("Yes Extra Charges")
                        sell_price = i['QI_Unit_Sell_Price']
                        quantity = i.Quantity
                        total_value = sell_price * quantity
                        total_value_count_Extra += i.NetPrice
                        Trace.Write("Total extra charges" +str(total_value_count_Extra))
                sellP_Extra = total_value_count_Extra
                remain_sellP_Extra = sellP_Extra
                for item in context.Quote.GetAllItems() :
                    if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0  :
                        Trace.Write("Yes")
                        mat_SellPrice_Extra = item.NetPrice
                        Material_Sellp_Extra += item.NetPrice
                Mat_SellP_Extra = Material_Sellp_Extra
                for item in all_items :
                    if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0  :
                        Trace.Write("Total Material SellPrice " +str(Material_Sellp_Extra))
                        propotionate_value = item.NetPrice / Mat_SellP_Extra
                        Trace.Write("else Prop Value" +str(propotionate_value))
                        material_allocation = round((propotionate_value * sellP_Extra),2)
                        Trace.Write("Mat Allocation " +str(material_allocation))
                        remain_sellP_Extra = round((remain_sellP_Extra - material_allocation),2)
                        value = remain_sellP_Extra
                        Trace.Write("Value " +str(value))
                        Trace.Write("SellP" +str(sellP))
                        newsellP = item.NetPrice + material_allocation
                        Trace.Write("Allocation SellP" + str(item.PartNumber) +str(newsellP))

                        material_quote_table=context.Quote.QuoteTables['QT_Materials']

                        newRow = material_quote_table.AddNewRow()
                        newRow['PART_'] = item.PartNumber
                        Trace.Write("Part " +str(newRow['PART_']))
                        newRow['DESCRIPTION'] = item.Description
                        Trace.Write("Description")
                        newRow['QTY'] = item.Quantity
                        newRow['SELL_PRICE'] = newsellP / newRow['QTY']
                        Trace.Write ("Sell Price allocated " +str(item.PartNumber) +str(newsellP)) 
                        newRow['TOTAL'] = newsellP
                    elif  (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] != 0 :
                        
                        if allocation_Value != "Done" :
                            Trace.Write("Yes" +str(item.PartNumber))
                            material_quote_table=context.Quote.QuoteTables['QT_Materials']
                            newRow = material_quote_table.AddNewRow()
                            newRow['PART_'] = item.PartNumber
                            Trace.Write("ROW Name " +str(newRow['PART_']))
                            Trace.Write("Part " +str(newRow['PART_']))
                            newRow['DESCRIPTION'] = item.Description
                            Trace.Write("Description")
                            newRow['QTY'] = item.Quantity
                            newRow['SELL_PRICE'] = item.NetPrice/ newRow['QTY']
                            Trace.Write ("Sell Price allocated " +str(item.PartNumber) +str(newsellP)) 
                            newRow['TOTAL'] = item.NetPrice
                allocation_Value == "Done"
                context.Quote.GetCustomField("CF_Extra_Allocation").Value = "Yes ExtraCharges"
                Trace.Write("Remain" +str(remain_sellP_Extra))
                if remain_sellP_Extra > 0 :
                    '''Trace.Write("Remain sell price last" +str(remain_sellP_Extra))
                    msg = 'All materials are CSPA/GSA so other costs cannot be allocated to material'
                    exitmsgs = context.Quote.Messages
                    if exitmsgs.Count > 0:
                        for msges in exitmsgs:
                            #if  "is not allowed for Quote Type" in str(msges.Content):
                            lv_msg_txt = 'All materials are CSPA/GSA so other costs cannot be allocated to material'
                            if  lv_msg_txt in str(msges.Content):
                                context.Quote.DeleteMessage(msges.Id)
                    context.Quote.AddMessage(msg,MessageLevel.Warning,False)'''
                    context.Quote.GetCustomField("CF_CSPA_Error").Value = "True"

    #CONTINGENCY,...................................................................

    if lc_contingency in qi_product_type :
        Trace.Write("test")
        if contingency == lc_allocate_to_material:
            if context.Quote.GetCustomField("CF_Contingency_Allocation").Value != "Yes Contingency"  and (context.Quote.GetCustomField("CF_Travel_Allocation").Value == "Yes OtherCost" or context.Quote.GetCustomField("CF_Allocation").Value == "Yes Subcon" or context.Quote.GetCustomField("CF_Extra_Allocation").Value == "ExtraCharges" ):

               
                Trace.Write("if Contingency....")
                for i in context.Quote.GetAllItems():
                    if i['QI_Product_Type'] == 'Contingency':
                        Trace.Write("Yes Contingency")
                        sell_price = i['QI_Unit_Sell_Price']
                        quantity = i.Quantity
                        total_value_contingency = sell_price * quantity
                        total_value_count_Contingency += i.NetPrice
                        Trace.Write("Total Contingency" +str(total_value_count_Contingency))
                sellP_Contingecy = total_value_count_Contingency
                remain_sellP_Contingency = sellP_Contingecy
                for item in context.Quote.GetAllItems() :
                    if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0  :
                        Trace.Write("Yes")
                        mat_SellPrice_Contingency = item.NetPrice
                        Material_Sellp_Contingency += item.NetPrice
                Mat_SellP_Contingency = Material_Sellp_Contingency
                for item in all_items :
                    if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0  :
                        Trace.Write("Total Material SellPrice " +str(Mat_SellP_Contingency))
                        propotionate_value = item.NetPrice / Mat_SellP_Contingency
                        Trace.Write("else Prop Value" +str(propotionate_value))
                        material_allocation = round((propotionate_value * sellP_Contingecy),2)
                        Trace.Write("Mat Allocation " +str(material_allocation))
                        remain_sellP_Contingency = round((remain_sellP_Contingency - material_allocation),2)

                        value1 = remain_sellP_Contingency
                        for r in material_quote_table.Rows :
                            if r['PART_'] == item.PartNumber:
                                Trace.Write("sellPrice row " + str(item.PartNumber) +str(r['SELL_PRICE']))
                                r['TOTAL'] = r['TOTAL'] + material_allocation 
                                r['SELL_PRICE'] = r['TOTAL']  /  r['QTY']
                                Trace.Write("Allocation SellP" + str(item.PartNumber) +str(r['SELL_PRICE']))
                    
                Trace.Write("Remain" +str(remain_sellP_Contingency))
                if remain_sellP_Contingency > 0 :
                    '''msg = 'All materials are CSPA/GSA so other costs cannot be allocated to material'
                    exitmsgs = context.Quote.Messages
                    if exitmsgs.Count > 0:
                        for msges in exitmsgs:
                            #if  "is not allowed for Quote Type" in str(msges.Content):
                            lv_msg_txt = 'All materials are CSPA/GSA so other costs cannot be allocated to material'
                            if  lv_msg_txt in str(msges.Content):
                                context.Quote.DeleteMessage(msges.Id)
                    context.Quote.AddMessage(msg,MessageLevel.Warning,False)'''
                    context.Quote.GetCustomField("CF_CSPA_Error").Value = "True"

            else:
                material_quote_table.Rows.Clear()
                for i in context.Quote.GetAllItems():
                    if i['QI_Product_Type'] == 'Contingency':
                        Trace.Write("Yes Contingency")
                        sell_price = i['QI_Unit_Sell_Price']
                        quantity = i.Quantity
                        total_value_contingency = sell_price * quantity
                        total_value_count_Contingency += i.NetPrice
                        Trace.Write("Total extra charges" +str(total_value_count_Contingency))
                sellP_contingency = total_value_count_Contingency
                remain_sellP_Contingency = sellP_contingency
                for item in context.Quote.GetAllItems() :
                    if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0  :
                        mat_SellPrice_Contingency = item.NetPrice
                        Material_Sellp_Contingency += item.NetPrice
                Mat_SellP_Contingency = Material_Sellp_Contingency
                for item in all_items :
                    if (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] == 0  :
                        Trace.Write("Total Material SellPrice " +str(Material_Sellp_Contingency))
                        propotionate_value = item.NetPrice / Mat_SellP_Contingency
                        material_allocation = round((propotionate_value * sellP_contingency),2)
                        remain_sellP_Contingency = round((remain_sellP_Contingency - material_allocation),2)
                        value = remain_sellP_Contingency
                        newsellP = item.NetPrice + material_allocation
                        material_quote_table=context.Quote.QuoteTables['QT_Materials']
                        newRow = material_quote_table.AddNewRow()
                        newRow['PART_'] = item.PartNumber
                        newRow['DESCRIPTION'] = item.Description
                        newRow['QTY'] = item.Quantity
                        newRow['SELL_PRICE'] = newsellP / newRow['QTY']
                        newRow['TOTAL'] = newsellP
                    elif  (item['QI_Product_Type'] == "Honeywell Hardware" or item['QI_Product_Type'] == "Third Party") and item['QI_SpecialPriceV'] != 0 :
                        if allocation_Value != "Done":
                            material_quote_table=context.Quote.QuoteTables['QT_Materials']
                            newRow = material_quote_table.AddNewRow()
                            newRow['PART_'] = item.PartNumber
                            newRow['DESCRIPTION'] = item.Description
                            newRow['QTY'] = item.Quantity
                            newRow['SELL_PRICE'] = item.NetPrice/ newRow['QTY']
                            newRow['TOTAL'] = item.NetPrice
                allocation_Value == "Done"
                context.Quote.GetCustomField("CF_Contingency_Allocation").Value = "Yes Contingency"
                Trace.Write("Remain" +str(remain_sellP_Contingency))
                if remain_sellP_Contingency > 0 :
                    '''msg = 'All materials are CSPA/GSA so other costs cannot be allocated to material'
                    exitmsgs = context.Quote.Messages
                    if exitmsgs.Count > 0:
                        for msges in exitmsgs:
                            lv_msg_txt = 'All materials are CSPA/GSA so other costs cannot be allocated to material'
                            if  lv_msg_txt in str(msges.Content):
                                context.Quote.DeleteMessage(msges.Id)
                    context.Quote.AddMessage(msg,MessageLevel.Warning,False)'''
                    context.Quote.GetCustomField("CF_CSPA_Error").Value = "True"