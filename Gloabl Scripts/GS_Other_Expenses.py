#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#Other expenses
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 10/12/2022    Payal Gupta             0             -Initial Version
# 10/14/2022    Mounika Tarigopula      3         -Replaced Hardcodings
#                                                -Incorporated Translation
# 11/03/2022	Srinivasan Dorairaj		5		 - Script Translation changes
# 11/15/2022    Payal Gupta             6        - Added code as per new requirements
# 12/03/2022    Payal Gupta             10        - Added code as per new requirements
# 12/28/2022    Payal Gupta             11        - Changes as part of enhancement
# 01/06/2022    Payal Gupta             12        - Changes to solve mandatory charges issue
# 01/11/2022    Payal Gupta             13        -Changes as part of enhancement
# 01/19/2023    Sumandrita                        - Modified allocation calculation
# 01/24/2023    Sumandrita                      - Commented allocate to material part, that part will be addressed in GS_Allocate_Material
#-----------------------------------------------------------------------------
#Begin of change by Mounika
import GM_TRANSLATIONS  #Inserted by Mounika
from Scripting.Quote import MessageLevel
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)    #Inserted by Mounika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')#Added by Srinivasan Dorairaj
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Added by Srinivasan Dorairaj
    lc_allocate_labor = GM_TRANSLATIONS.GetText('000045', lv_LanguageKey, '', '', '', '', '')
    lc_details = GM_TRANSLATIONS.GetText('000067', lv_LanguageKey, '', '', '', '', '') #Added by Payal
    lc_lumpsum = GM_TRANSLATIONS.GetText('000066', lv_LanguageKey, '', '', '', '', '') #Added by Payal
    lc_travel_expense = GM_TRANSLATIONS.GetText('000085', lv_LanguageKey, '', '', '', '', '')
    lc_allocate_to_material = GM_TRANSLATIONS.GetText('000216', lv_LanguageKey, '', '', '', '', '') #Added by Payal
    all_items = context.Quote.GetAllItems()
    total_value_count = 0
    list_price_count = 0
    quantity_count = 0
    total_count = 0
    sell_price_count = 0
    table_total = 0
    final_total = 0
    discount_amount = 0
    disc_div = 0
    total_disc = 0
    labor_table_list = []
    table_total_list = []
    material_table_list = []
    total_Material_Sellp = 0
    sellP = 0
    material_allocation = 0
    remain_sellP = 0
    

	###-----Getting Other Expenses Value-----###

    other_expenses = context.Quote.GetCustomField('Other Expenses').Value
    final_table_other_expenses = context.Quote.QuoteTables["Travel_Expenses"]
    final_table_other_expenses.Rows.Clear()
    material_quote_table=context.Quote.QuoteTables['QT_Materials']
    material_quote_table.Rows.Clear()

    qi_product_type = [i['QI_Product_Type'] for i in all_items]

    if lc_travel_expense in qi_product_type:
        ###-----Other Expenses type is Allocate to Labor-----###
        #if other_expenses == 'Allocate to Labor':                   #commented by Mounika
        if other_expenses == lc_allocate_labor:                      #inserted by mounika
            for i in all_items:
                #if 'Travel Expense' in i['QI_Product_Type']:        #commented by Mounika
                if lc_travel_expense in i['QI_Product_Type']:        #inserted by mounika
                    if i['QI_Unit_Sell_Price'] ==0: #Added by Payal
                        sell_price = i.NetPrice #Added by Payal
                    else: #Added by Payal
                        sell_price = i['QI_Unit_Sell_Price'] #Added by Payal
                    quantity = i.Quantity
                    total_value = sell_price * quantity
                    total_value_count += total_value
                    labor_table=context.Quote.QuoteTables['QT_LABOR_PT'].Rows
            for j in labor_table:
                labor_table_list.append(j)
            labor_table_first_row = labor_table_list[0]
            labor_sell_price = labor_table_first_row["SELL_PRICE"]
            labor_quantity = labor_table_first_row["QTY"]
            other_expenses_total = total_value_count/labor_sell_price
            labor_table_first_row["QTY"] = labor_quantity + other_expenses_total
            labor_table_first_row["TOTAL"] = labor_table_first_row["QTY"] * labor_sell_price

            ###-----Other Expenses type is Details-----###
        if other_expenses == lc_details:
            for i in all_items:
                if lc_travel_expense in i['QI_Product_Type']:
                    final_row = final_table_other_expenses.AddNewRow()
                    final_row["DESCRIPTION"] = i.Description
                    final_row["QTY"] = i.Quantity
                    final_row["LIST_PRICE"] = i['QI_Recommended_Unit_Sell_Price']
                    final_row["DISC_"] = i.DiscountPercent
                    if i['QI_Unit_Sell_Price'] ==0: #Added by Payal
                        final_row["SELL_PRICE"] = i.NetPrice #Added by Payal
                    else: #Added by Payal 
                        final_row["SELL_PRICE"] = i['QI_Unit_Sell_Price'] #Added by Payal
                    final_row["TOTAL"] = final_row["SELL_PRICE"] * final_row["QTY"]

            ###-----Other Expenses type is Lumpsum-----###

        if other_expenses == lc_lumpsum:
            for i in all_items:
                if lc_travel_expense in i['QI_Product_Type']:
                    '''quantity_count += i.Quantity #Commented by Payal
                    sell_price_count += i['QI_Unit_Sell_Price']
                    discount_amount += i.DiscountAmount
                    discount_percent = discount_amount/sell_price_count
                    final_discount = discount_percent * 100'''
                    if i['QI_Unit_Sell_Price'] ==0: #Added by Payal
                        total = i.Quantity * i.NetPrice #Added by Payal
                    else: #Added by Payal
                        total = i.Quantity * i['QI_Unit_Sell_Price'] #Added by Payal
                    total_count += total #Added by Payal
            final_row = final_table_other_expenses.AddNewRow()
            #final_row["DESCRIPTION"] = lc_travel_expense #Commented by Payal
            final_row["TOTAL"] = total_count
            '''final_row["QTY"] = quantity_count #Commented by Payal
            final_row["SELL_PRICE"] = final_row["TOTAL"]/final_row["QTY"]
            final_row["DISC_"] = final_discount
            final_discount_amount = final_discount/100
            final_row["LIST_PRICE"] = final_row["SELL_PRICE"]/(1-final_discount_amount)

            ###-----When Other Expenses type is Allocate to Material-----### #Added by Payal

       if other_expenses == lc_allocate_to_material:
            for i in all_items:
                if lc_travel_expense in i['QI_Product_Type']:
                    if i['QI_Unit_Sell_Price'] ==0: #Added by Payal
                        sell_price = i.NetPrice #Added by Payal
                    else: #Added by Payal
                        sell_price = i['QI_Unit_Sell_Price'] #Added by Payal
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

    final_table_other_expenses = context.Quote.QuoteTables["Travel_Expenses"].Rows
    for row in final_table_other_expenses:
        table_total_list.append(row)
    for t in range(len(table_total_list)):
        table_total_row = table_total_list[t]
        table_total = table_total_row["TOTAL"]
        final_total += table_total
    context.Quote.GetCustomField('CF_TOTAL_OTHER_EXPENSES').Value = '%.2f' %final_total