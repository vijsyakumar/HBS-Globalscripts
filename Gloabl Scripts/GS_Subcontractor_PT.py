#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script define Values for subcontractor table present in Proposal Template Based on the vales selected for Sub Contractor field in the Commercial Tab
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 9/14/2022     Sunil                  0         -initial version
#
# 10/17/2022	Abhilash		      11		 -Replaced Hardcodings
#												 -Incorporated Translation
# 11/04/2022	Dhruv				  17		 -SQL translation,Transacrtion type
#												  check implemented
# 12/03/2022    Payal Gupta           18         -Changes as part of enhancement
# 01/24/2023    Sumandrita                      - Commented allocate to material part, that part will be addressed in GS_Allocate_Material
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS
from Scripting.Quote import MessageLevel
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_sub_con = GM_TRANSLATIONS.GetText('000026', lv_LanguageKey, '', '', '', '', '') # Added by Dhruv
lc_sub_item1 =  GM_TRANSLATIONS.GetText('000066', lv_LanguageKey, '', '', '', '', '')
lc_sub_item2 =  GM_TRANSLATIONS.GetText('000067', lv_LanguageKey, '', '', '', '', '')
lc_sub_item3 =  GM_TRANSLATIONS.GetText('000045', lv_LanguageKey, '', '', '', '', '')
lc_allocate_to_material = GM_TRANSLATIONS.GetText('000216', lv_LanguageKey, '', '', '', '', '') #Added by Payal

all_items = context.Quote.GetAllItems()
list_price_count = 0
quantity_count = 0
total_count = 0
sell_price_count = 0
table_total = 0
final_total = 0
discount_amount = 0
disc_div = 0
total_disc = 0
total_value_count = 0
labor_table_list = []
table_total_list = []
material_table_list = []
sellP = 0
remain_sellP = 0

material_allocation = 0
total_Material_Sellp = 0

###-----Getting Subcontractor Table-----###

subcontractor_item  =  context.Quote.GetCustomField('Sub Contractor').Value
final_table_extra_charges = context.Quote.QuoteTables["QT_SUBCON"]
final_table_extra_charges.Rows.Clear()
material_quote_table=context.Quote.QuoteTables['QT_Materials']
material_quote_table.Rows.Clear()

###-----Getting Labor Table-----###

final_table_labor = context.Quote.QuoteTables["QT_LABOR_PT"]


qi_product_type = [i['QI_Product_Type'] for i in all_items]

if lc_sub_con in qi_product_type:

    ###-----When Subcontractor type is Lumpsum-----###
    if subcontractor_item == lc_sub_item1:
        for i in all_items:
            if lc_sub_con in i['QI_Product_Type']:		# Modified by Dhruv
                quantity_count += i.Quantity
                sell_price_count += i['QI_Unit_Sell_Price']
                discount_amount += i.DiscountAmount
                discount_percent = discount_amount/sell_price_count
                final_discount = discount_percent * 100
                total = i.Quantity * i['QI_Unit_Sell_Price']
                total_count += total
        final_row = final_table_extra_charges.AddNewRow()
        final_row["Description"] = lc_sub_con			# Modified by Dhruv
        final_row["TOTAL"] = total_count
        final_row["QTY"] = quantity_count
        final_row["SELL_PRICE"] = final_row["TOTAL"]/final_row["QTY"]
        final_row["DISC_"] = final_discount
        final_discount_amount = final_discount/100
        final_row["LIST_PRICE"] = final_row["SELL_PRICE"]/(1-final_discount_amount)

    ###-----When Subcontractor type is Detail-----###

    if subcontractor_item == lc_sub_item2 :
        for i in all_items:
            if lc_sub_con in i['QI_Product_Type']:
                final_row = final_table_extra_charges.AddNewRow()
                final_row["Description"] = i.Description
                final_row["QTY"] = i.Quantity
                final_row["LIST_PRICE"] = i['QI_Recommended_Unit_Sell_Price']
                final_row["DISC_"] = i.DiscountPercent
                final_row["SELL_PRICE"] = i['QI_Unit_Sell_Price']
                total = i['QI_Unit_Sell_Price'] * i.Quantity
                final_row["TOTAL"] = total

    ###-----When Subcontractor type is Allocate to Labor-----###

    if subcontractor_item == lc_sub_item3 :
        for i in all_items:
            if lc_sub_con in i['QI_Product_Type']:			# Modified by Dhruv
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
        sub_con_total = total_value_count/labor_sell_price
        labor_table_first_row["QTY"] = labor_quantity + sub_con_total 
        labor_table_first_row["TOTAL"] = labor_table_first_row["QTY"] * labor_sell_price

    ###-----When Subcontractor type is Allocate to Material-----### #Added by Payal

    '''if subcontractor_item == lc_allocate_to_material:
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
            msg = 'All materials are CSPA/GSA so other costs cannot be allocated to material'
            exitmsgs = context.Quote.Messages
            if exitmsgs.Count > 0:
                for msges in exitmsgs:
                    #if  "is not allowed for Quote Type" in str(msges.Content):
                    lv_msg_txt = 'All materials are CSPA/GSA so other costs cannot be allocated to material'
                    if  lv_msg_txt in str(msges.Content):
                        context.Quote.DeleteMessage(msges.Id)
            context.Quote.AddMessage(msg,MessageLevel.Warning,True)'''
                



###-----Calculating total for proposal template-----###

final_table_sub_con = context.Quote.QuoteTables["QT_SUBCON"].Rows
for row in final_table_sub_con:
    table_total_list.append(row)
for t in range(len(table_total_list)):
    table_total_row = table_total_list[t]
    table_total = table_total_row["TOTAL"]
    final_total += table_total
context.Quote.GetCustomField('CF_TOTAL_SUBCON').Value = '%.2f' %final_total

