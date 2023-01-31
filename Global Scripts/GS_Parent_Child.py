#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for calculation of list price, sell price, recommended sell price etc for child items
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 08/22/2022    Sreenivasa Mucharla        0             -Initial Version
# 10/18/2022    Ishika Bhattacharya        17            -Replaced Hardcodings
#                                                        -Incorporated Translation
# 01/04/2023    Aditi Sharma               53            -Modified Discount percent assignment for child item
# 01/14/2023   Aditi Sharma                              -Added condition check for Preparing status & transaction type
# 01/30/2023    Sumandrita                               -Introduced "QI_Category" to incorporated changes for CXCPQ-38244
#-----------------------------------------------------------------------------


import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)   # Added by Ishika
lc_op_type = GM_TRANSLATIONS.GetText('000024', lv_LanguageKey, '', '', '', '', '')    # Added by Ishika
quote_status_ID = context.Quote.StatusId #Added by Aditi 14th Jan
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Added by Aditi 14th Jan

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type and quote_status_ID==32:   # Added by Ishika #Modified by Aditi 14th Jan
    lc_p_systemID = GM_TRANSLATIONS.GetText('000128', lv_LanguageKey, '', '', '', '', '') # Added by Ishika
    lc_prd_typ = GM_TRANSLATIONS.GetText('000026', lv_LanguageKey, '', '', '', '', '') # Added by Dhruv
    lc_rec_typ = GM_TRANSLATIONS.GetText('000030', lv_LanguageKey, '', '', '', '', '') # Added by Dhruv
    lc_prd_ele = GM_TRANSLATIONS.GetText('000053', lv_LanguageKey, '', '', '', '', '') # Added by Dhruv
    lc_prd_mec = GM_TRANSLATIONS.GetText('000055', lv_LanguageKey, '', '', '', '', '') # Added by Dhruv
    lc_prodcat_ADM = GM_TRANSLATIONS.GetText('000167', lv_LanguageKey, '', '', '', '', '')
    lc_prodcat_TP = GM_TRANSLATIONS.GetText('000065', lv_LanguageKey, '', '', '', '', '')
    #Product.UpdateQuote()
    reference_quote_no = context.Quote.QuoteNumber
    rf_quote = QuoteHelper.Get(reference_quote_no)
    def get_child_items(rf_quote,item_id):
        #adding child products into list
        childItemsList = []
        try:
            rf_main_item = rf_quote.GetItemByItemId(item_id).AsMainItem
            mainProduct = rf_main_item.Edit()
            accContainer = mainProduct.GetContainerByName("WriteInProduct")
            if accContainer.Rows.Count >0:
                for row in accContainer.Rows:
                    temp_childItemsList = []
                    if row['AR_WriteInProduct']:
                        temp_childItemsList.append(str(row['AR_WriteInProduct']))
                        
                        if lc_prodcat_ADM == str(row['Writein_Category']):
                            temp_childItemsList.append(lc_prodcat_TP)
                        else:
                            temp_childItemsList.append(str(row['Writein_Category']))
                        temp_childItemsList.append(str(row['Description']))
                        #temp_childItemsList.append(str(row['Extended Description']))
                        temp_childItemsList.append(str(row['Price']))
                        temp_childItemsList.append(str(row['cost']))
                        #temp_childItemsList.append(str(row['Discount']))
                        temp_childItemsList.append(str(row['ProductType']))
                        childItemsList.append(temp_childItemsList)
            return childItemsList
        except:
            return "Null"
    
    child_id_List = []
    for rf_item in context.Quote.GetAllItems():
        #checking parent item or not
        p_systemid = rf_item.ProductSystemId
        #if p_systemid == 'Write-in_Products_cpq':   #Commented by Ishika
        if p_systemid == lc_p_systemID:				#Added by Ishika

            #Trace.Write('c')
            childItemsList = get_child_items(rf_quote,rf_item.Id)
            
            Trace.Write("rfid" +str(rf_item.Id))
            
            lv_tot_price = 0
            lv_quantity = 0
            lv_unit_sell = 0
            lv_net_price = 0
            lv_rec_Unit = 0
            lv_rec_sell = 0
            lv_unit_cost = 0
            lv_disc_amt = 0
            lv_disc_perc = 0
            lv_mar_amt = 0
            lv_mar_perc = 0
            lv_tot_quot_cost = 0
            lv_tot_cost = 0
            lv_list_price = 0
            lv_count = 0
            lv_count1 = 0
            lv_war_per = 0
            lv_war_amt = 0
            """lv_count_freight = 0
            lv_frt_per = 0
            lv_frt_amt = 0
            lv_count_custom = 0
            lv_cst_per = 0
            lv_cst_amt = 0
            lv_count_war = 0"""
            #lv_war_per = 0
            #lv_war_amt = 0
            
            #geeting child items associated with Main items
            for child_item in context.Quote.GetItemByItemId(rf_item.Id).AsMainItem.GetChildItems():
                #Trace.Write(child_item.PartNumber)
                for c_item_list in childItemsList:
                    Trace.Write("id" +str(child_item.Id))
                    if child_item.PartNumber == c_item_list[0] and child_item.Id not in child_id_List:
                        child_id_List.append(child_item.Id)
                        child_item['QI_PROD_CATEGORY'] = str(c_item_list[1])
                        child_item['QI_Category'] = str(c_item_list[1]) #Added by Sumandrita for CXCPQ-38244
                        lv_quantity += child_item.Quantity
                        Log.Info("===GS_Parent_Child QI_PROD_CATEGORY==="+str(c_item_list[1]))
                        child_item.Description = str(c_item_list[2])
                        child_item['QI_Product_Type'] = str(c_item_list[5])
                        if c_item_list[3]:

                            child_item['QI_List_Price'] = float(c_item_list[3]) * child_item['QI_Exchange_Rate']
                            lv_list_price += child_item['QI_List_Price']
                            
                            #Trace.Write("list"+ str(child_item['QI_List_Price']))
                            child_item['QI_List_Price_Total'] = (float(c_item_list[3]) * float(child_item.Quantity) ) * child_item['QI_Exchange_Rate']
                            lv_tot_price += child_item['QI_List_Price_Total']
                            
                            child_item['QI_Unit_Sell_Price'] = float(c_item_list[3]) * child_item['QI_Exchange_Rate']
                            #lv_unit_sell += child_item['QI_Unit_Sell_Price']
                            
                            child_item['QI_Recommended_Unit_Sell_Price'] = float(c_item_list[3]) * child_item['QI_Exchange_Rate']
                            lv_rec_Unit += child_item['QI_Recommended_Unit_Sell_Price']
                            
                            child_item["QI_Recommended_Sell_Price"] = (float(child_item['QI_Recommended_Unit_Sell_Price']) * float(child_item.Quantity))
                            lv_rec_sell += child_item['QI_Recommended_Sell_Price']

                        if c_item_list[4]:
                            Trace.Write("Yes Cost")
                            child_item['QI_Unit_Cost_Base_Currency'] = float(c_item_list[4])
                            child_item['QI_TransferCost']= float(c_item_list[4]) * child_item['QI_Exchange_Rate']
                            child_item['QI_Total_Cost'] = child_item['QI_TransferCost'] * (child_item.Quantity)
                            lv_unit_cost += child_item['QI_Unit_Cost_Base_Currency']

                    
                        if child_item.DiscountPercent > 0:
                            child_item.DiscountAmount = (float(child_item['QI_Recommended_Unit_Sell_Price']) * float(child_item.DiscountPercent)/100)# * float(child_item.Quantity)
                            lv_disc_amt = lv_disc_amt + (child_item.DiscountAmount * float(child_item.Quantity))
                            lv_disc_perc += child_item.DiscountPercent
                            lv_count = lv_count + 1
                            
                            Trace.Write("abc" +str(child_item.DiscountAmount))
						 #Commented by Aditi 4th Jan
                        """elif child_item.DiscountAmount == 0 and float(c_item_list[5]) >= 0: #Commented by Aditi 4th Jan
                        #if float(c_item_list[5]) >= 0:
                            Trace.Write("Yes")
                            child_item.DiscountPercent = float(c_item_list[5])
                            lv_disc_perc += child_item.DiscountPercent
                            lv_count = lv_count + 1
                            child_item.DiscountAmount = (float(child_item['QI_Recommended_Unit_Sell_Price']) * float(c_item_list[5])/100)
                            lv_disc_amt += child_item.DiscountAmount"""

                        child_item['QI_WTW_Margin'] = 0
                        child_item['QI_WTW_COST'] = 0
                        child_item['QI_UNIT_WTW_COST'] = 0
                        child_item['QI_WTW_Margin'] = 0
                        child_item['QI_Unit_Sell_Price'] = (child_item['QI_Recommended_Unit_Sell_Price'] - child_item.DiscountAmount)
                        lv_unit_sell += child_item['QI_Unit_Sell_Price']
                        
                        """if child_item['QI_FREIGHT_PERCENT'] > 0:
                            child_item['QI_FREIGHT_AMOUNT'] = (float(child_item['QI_Total_Cost'])*float(child_item['QI_FREIGHT_PERCENT']))/100
                            lv_count_freight = lv_count_freight + 1
                            lv_frt_per += child_item['QI_FREIGHT_PERCENT']
                            lv_frt_amt += child_item['QI_FREIGHT_AMOUNT']
                        
                        if child_item['QI_Warranty_P'] > 0:
                            child_item['QI_Warranty_Amt'] = (float(child_item['QI_Total_Cost'])*float(child_item['QI_Warranty_P']))/100
                            lv_count_war = lv_count_war + 1
                            lv_war_per += child_item['QI_Warranty_P']
                            lv_war_amt += child_item['QI_Warranty_Amt']
                                                        
                            
                        if child_item['QI_CUSTOMS_PERCENT'] > 0:
                            child_item['QI_CUSTOMS_AMOUNT'] = (float(child_item['QI_Total_Cost'])*float(child_item['QI_CUSTOMS_PERCENT']))/100
                            lv_count_custom = lv_count_custom + 1
                            lv_cst_per += child_item['QI_CUSTOMS_PERCENT']
                            lv_cst_amt += child_item['QI_CUSTOMS_AMOUNT']"""

                        if child_item['QI_Unit_Sell_Price']:
                            child_item.NetPrice = float(child_item['QI_Unit_Sell_Price']) * float(child_item.Quantity)
                            lv_net_price += child_item.NetPrice
                            
                            child_item['QI_Final_Sell_Price'] = child_item.NetPrice
                            
                        if child_item['QI_Total_Cost']:
                            lv_tot_cost += child_item['QI_Total_Cost']
                            Log.Write('157--'+str(child_item['QI_Product_Type']))#CXCPQ-33770 start
                            """if (child_item['QI_Product_Type'] == "Third Party" or child_item['QI_PROD_CATEGORY'] == "Adhoc Material") and child_item['QI_Warranty_P'] is None:
                                country = context.Quote.GetCustomField('CF_Country').Value
                                Mat_Type = "Third Party Material"
                                
                                query = SqlHelper.GetFirst("SELECT Warranty_Percent FROM TAB_Warranty_Percentage WHERE Country = '"+str(country)+"' and Mat_Type =  '"+str(Mat_Type)+"' ")
                                if(query is None):
                                    query = SqlHelper.GetFirst("SELECT Warranty_Percent FROM TAB_Warranty_Percentage WHERE Country = 'Default' and Mat_Type =  '"+str(Mat_Type)+"' ")
                                    
                                if query:
                                    lv_count1 = lv_count1 + 1
                                    child_item['QI_Warranty_P'] = query.Warranty_Percent
                                    lv_war_per = lv_war_per + child_item['QI_Warranty_P']
                                    if float(child_item['QI_Total_Cost']) > 0:
                                        child_item['QI_Warranty_Amt'] = (float(child_item['QI_Total_Cost'])*float(query.Warranty_Percent))/100
                                        lv_war_amt = lv_war_amt + child_item['QI_Warranty_Amt']
                                    else:
                                        child_item['QI_Warranty_Amt'] = 0"""

                            if child_item['QI_INFLATION_AMOUNT'] is None:
                                child_item['QI_INFLATION_AMOUNT'] = 0
                            if child_item['QI_FREIGHT_AMOUNT'] is None:
                            	child_item['QI_FREIGHT_AMOUNT'] = 0
                            if child_item['QI_CUSTOMS_AMOUNT'] is None:
                            	child_item['QI_CUSTOMS_AMOUNT'] = 0
                            if child_item['QI_Warranty_Amt'] is None:
                            	child_item['QI_Warranty_Amt'] = 0
                                
                            child_item['QI_TOTAL_QUOTE_COST'] = float(child_item['QI_Total_Cost']) + float(child_item['QI_Warranty_Amt']) + float(child_item['QI_INFLATION_AMOUNT']) + float(child_item['QI_FREIGHT_AMOUNT']) + float(child_item['QI_CUSTOMS_AMOUNT'])#CXCPQ-33770 end
                            lv_tot_quot_cost += child_item['QI_TOTAL_QUOTE_COST']
                        #child_item['QI_TOTAL_QUOTE_COST'] =
                        
                        #Begin of change by Dhruv
                        #if child_item['QI_Product_Type'] == "Subcontractor" :
                            #child_item['QI_RECORD_TYPE'] = "S"
                        #if child_item['QI_PROD_CATEGORY'] == "Third Party" or child_item['QI_PROD_CATEGORY'] == "Subcontractor Mechanical":
                            #child_item['QI_RECORD_TYPE'] = "S"
                        if child_item['QI_Product_Type'] == lc_prd_typ :
                            child_item['QI_RECORD_TYPE'] = lc_rec_typ
                        if child_item['QI_PROD_CATEGORY'] == lc_prd_ele or child_item['QI_PROD_CATEGORY'] == lc_prd_mec:
                            child_item['QI_RECORD_TYPE'] = lc_rec_typ
                        
                        child_item['QI_MARGIN_AMOUNT'] = (float(child_item.NetPrice) - float(child_item['QI_TOTAL_QUOTE_COST']))
                        if child_item['QI_MARGIN_AMOUNT']:
                            child_item['QI_MARGIN_PERCENTAGE'] = (float(child_item['QI_MARGIN_AMOUNT']) / float(child_item.NetPrice)) * 100
                        lv_mar_amt += child_item['QI_MARGIN_AMOUNT']
                        lv_mar_perc += child_item['QI_MARGIN_PERCENTAGE']
                        childItemsList.remove(c_item_list)
                        
                        #End of change by Dhruv
                for rf_item1 in context.Quote.GetAllItems():
                    #p_systemid = rf_item1.ProductSystemId
        
                    if rf_item1.ProductSystemId == "Write-in_Products_cpq" and rf_item1.Id == rf_item.Id:
                        rf_item1['QI_PROD_CATEGORY'] = str("Write-Ins")
                        rf_item1['QI_Category'] = str("Write-Ins") #Added by Sumandrita for CXCPQ-38244
                        rf_item1.Quantity = float(1)
                        rf_item1['QI_Product_Type'] = str("Write-In")
                        rf_item1['QI_List_Price'] = float(lv_tot_price)
                        rf_item1['QI_List_Price_Total'] = float(lv_tot_price)
                        rf_item1['QI_Unit_Sell_Price'] = float(lv_net_price)
                        rf_item1.NetPrice = float(lv_net_price)
                        rf_item1['QI_Final_Sell_Price'] = float(lv_net_price)
                        rf_item1['QI_Recommended_Unit_Sell_Price'] = float(lv_rec_sell)
                        rf_item1['QI_Recommended_Sell_Price'] = float(lv_rec_sell)
                        if rf_item1['QI_Exchange_Rate']:
                            rf_item1['QI_Unit_Cost_Base_Currency'] = float(lv_tot_cost) / rf_item1['QI_Exchange_Rate']
                        rf_item1['QI_TransferCost'] = float(lv_tot_cost)
                        rf_item1['QI_Total_Cost'] = float(lv_tot_cost)
                        rf_item1.DiscountAmount = float(lv_disc_amt)
                        if lv_count > 0:
                            rf_item1.DiscountPercent = float(lv_disc_perc) / float(lv_count)
                        rf_item1['QI_TOTAL_QUOTE_COST'] = float(lv_tot_quot_cost)
                        rf_item1['QI_WTW_Margin'] = 0
                        rf_item1['QI_WTW_COST'] = 0
                        rf_item1['QI_UNIT_WTW_COST'] = 0
                        rf_item1['QI_WTW_Margin'] = 0
                        rf_item1['QI_Warranty_Amt'] = lv_war_amt
                        if lv_war_per and lv_count1 > 0:
                            rf_item1['QI_Warranty_P'] = float(lv_war_per) / float(lv_count1)
                  
                        """rf_item1['QI_FREIGHT_AMOUNT'] = lv_frt_amt
                        if lv_frt_per and lv_count_freight > 0:
                            rf_item1['QI_FREIGHT_PERCENT'] = float(lv_frt_per) / float(lv_count_freight)
                            
                        rf_item1['QI_CUSTOMS_AMOUNT'] = lv_cst_amt
                        if lv_cst_per and lv_count_custom > 0:
                            rf_item1['QI_CUSTOMS_PERCENT'] = float(lv_cst_per) / float(lv_count_custom)"""
                            
                        rf_item1['QI_MARGIN_AMOUNT'] = lv_mar_amt
                        if lv_count > 0:
                            rf_item1['QI_MARGIN_PERCENTAGE'] = lv_mar_perc / float(lv_count)
                            
                        Log.Write("list11111"+ str(lv_list_price))