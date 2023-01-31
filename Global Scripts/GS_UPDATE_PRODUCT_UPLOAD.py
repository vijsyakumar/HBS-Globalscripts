#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#This Script Updates Products added via Upload
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 08/28/2022	Ashutosh K Mishra	0			-Initial Creation
# 11/04/2022	Dhruv Bhatnagar		23			-Replaced Hardcodings
#												-Incorporated Translation
# 11/07/2022    Aditi Sharma        24          -Added calculation for total list price
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS			#Added by Dhruv
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)	#Added by Dhruv
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') # Added by Dhruv
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Added by Dhruv
    lc_prodsys_Id = GM_TRANSLATIONS.GetText('000073', lv_LanguageKey, '', '', '', '', '')#Added by Dhruv
    reference_quote_no = context.Quote.QuoteNumber
    rf_quote = QuoteHelper.Get(reference_quote_no)

    def get_valid_items(rf_quote,item_id):
        #adding upload products into list
        validchildItemsList = []
        try:
            rf_main_item = rf_quote.GetItemByItemId(item_id).AsMainItem
            mainProduct = rf_main_item.Edit()
            ValContainer = mainProduct.GetContainerByName("AR_Product_Upload_Valid")
            if ValContainer.Rows.Count >0:
                for Val in ValContainer.Rows:
                    temp_childItemsList = []
                    if Val.IsSelected == True:
                        temp_childItemsList.append(str(Val['Part Number']))
                        temp_childItemsList.append(str(Val['Quantity']))
                        #temp_childItemsList.append(str(Val['Description (English)']))
                        #temp_childItemsList.append(str(Val['Cost']))
                        #temp_childItemsList.append(str(Val['Currency']))
                        #temp_childItemsList.append(str(Val['Unit List Price']))
                        #temp_childItemsList.append(str(Val['Discount']))
                        validchildItemsList.append(temp_childItemsList)
            
            return validchildItemsList
        except:
            return "Null"

    
    def get_invalid_items(rf_quote,item_id):
        #adding upload products into list
        InvalidchildItemsList = []
        try:
            rf_main_item = rf_quote.GetItemByItemId(item_id).AsMainItem
            mainProduct = rf_main_item.Edit()
            
            InvalContainer = mainProduct.GetContainerByName("AR_Product_Upload_Invalid")
            if InvalContainer.Rows.Count >0:
                for Inval in InvalContainer.Rows:
                    temp_childItemsList = []
                    if Inval.IsSelected == True:
                        temp_childItemsList.append(str('Adhoc'))
                        temp_childItemsList.append(str(Inval['Quantity']))
                        temp_childItemsList.append(str(Inval['Description (English)']))
                        temp_childItemsList.append(str(Inval['Cost']))
                        temp_childItemsList.append(str(Inval['Currency']))
                        temp_childItemsList.append(str(Inval['Unit List Price']))
                        temp_childItemsList.append(str(Inval['Part Number']))
                        temp_childItemsList.append(str(Inval.RowIndex))
                        InvalidchildItemsList.append(temp_childItemsList)
            return InvalidchildItemsList
        except:
            return "Null"
    
    ValidchildItems = []
    InvalidchildItems = []
    for rf_item in context.Quote.GetAllItems():
        #checking parent item or not
        p_systemid = rf_item.ProductSystemId
        if "." not in rf_item.RolledUpQuoteItem and p_systemid == lc_prodsys_Id:	#Modified by Dhruv
            #Trace.Write(rf_item.Id)
            ValidchildItems = get_valid_items(rf_quote,rf_item.Id)
            InvalidchildItems = get_invalid_items(rf_quote,rf_item.Id)

	"""lv_row = 0
    for rf_item1 in context.Quote.GetAllItems():
        for c_item_list in ValidchildItems:
            #Trace.Write(c_item_list[1])
            #Trace.Write(rf_item1.Quantity)
            if rf_item1.PartNumber == c_item_list[0] and int(rf_item1.Quantity) == int(c_item_list[1]):
                #child_item['QI_PROD_CATEGORY'] = str(c_item_list[1])
                if c_item_list[2]:
                    rf_item1.Description = str(c_item_list[2])
                if c_item_list[3]:
                    rf_item1['QI_List_Price'] = float(c_item_list[5])
                    rf_item1['QI_List_Price_Total'] = float(c_item_list[5]) * rf_item1.Quantity #Added by Aditi 7th Nov
                    rf_item1['QI_Unit_Sell_Price'] = float(c_item_list[5])
                    rf_item1['QI_UnitCost'] = float(c_item_list[3])
                    rf_item1['QI_Unit_Cost_Base_Currency'] = float(c_item_list[3])
                    rf_item1['QI_Recommended_Unit_Sell_Price'] = float(c_item_list[5])
                    rf_item1["QI_Recommended_Sell_Price"] = rf_item1['QI_Recommended_Unit_Sell_Price'] * (rf_item1.Quantity)
                    rf_item1['QI_Unit_Sell_Price'] = rf_item1['QI_Recommended_Unit_Sell_Price'] - rf_item1.DiscountAmount
                    rf_item1.NetPrice = rf_item1['QI_Unit_Sell_Price'] * (rf_item1.Quantity)
                    rf_item1['QI_Total_Cost'] = rf_item1['QI_UnitCost'] * (rf_item1.Quantity)
                    rf_item1['QI_TOTAL_QUOTE_COST'] = rf_item1['QI_Total_Cost']
                rf_item1['QI_WTW_Margin'] = 0
                rf_item1['QI_WTW_COST'] = 0
                rf_item1['QI_UNIT_WTW_COST'] = 0
                
                ValidchildItems.remove(c_item_list)"""

                
    for c_item_list in InvalidchildItems:
        
        InvalProd = rf_quote.AddItem(312,int(c_item_list[1]))
        
        if c_item_list[2]:
            InvalProd.Description = str(c_item_list[2])
            InvalProd['QI_Description'] = str(c_item_list[2])
        elif c_item_list[2] == "" and c_item_list[6]:
            InvalProd.Description = str(c_item_list[6])
            InvalProd['QI_Description'] = str(c_item_list[6])
            
        if c_item_list[3]:
            Log.Write("Upload :" +str(c_item_list[5]))
            InvalProd['QI_List_Price'] = float(c_item_list[5])
            InvalProd['QI_List_Price_Total'] = float(c_item_list[5]) * InvalProd.Quantity
            InvalProd['QI_Unit_Sell_Price'] = float(c_item_list[5])
            #InvalProd['QI_UnitCost'] = float(c_item_list[3])
            InvalProd['QI_Unit_Cost_Base_Currency'] = float(c_item_list[3])
            InvalProd['QI_TransferCost'] = float(c_item_list[3])* InvalProd['QI_Exchange_Rate']
            InvalProd['QI_Recommended_Unit_Sell_Price'] = float(c_item_list[5])
            InvalProd["QI_Recommended_Sell_Price"] = InvalProd['QI_Recommended_Unit_Sell_Price'] * (InvalProd.Quantity)
            InvalProd['QI_Unit_Sell_Price'] = InvalProd['QI_Recommended_Unit_Sell_Price'] - InvalProd.DiscountAmount
            InvalProd.NetPrice = InvalProd['QI_Unit_Sell_Price'] * (InvalProd.Quantity)
            InvalProd['QI_Total_Cost'] = InvalProd['QI_TransferCost'] * (InvalProd.Quantity)
            InvalProd['QI_TOTAL_QUOTE_COST'] = InvalProd['QI_Total_Cost']
            
        InvalProd['QI_WTW_Margin'] = 0
        InvalProd['QI_WTW_COST'] = 0
        InvalProd['QI_UNIT_WTW_COST'] = 0
        
        #InvalidchildItems.remove(c_item_list)
                

                #child_item['QI_PROD_CATEGORY'] = str(c_item_list[1])    #rf_item1['QI_Sell_Price_Discount_amount'] = float(c_item_list[6])
                #child_item['QI_DiscountP'] = c_item_list[5]
                #child_item['QI_Product_Type'] = c_item_list[6]