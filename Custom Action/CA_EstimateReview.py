#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
# Description:
# This script is used for estimating review
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 10/3/2022     Sreenivasa Mucharla        0             -Initial Version
# 10/19/2022    Ishika Bhattacharya        11            -Replaced Hardcodings
#                                                        -Incorporated Translation
# 10/20/2022    Sreenivasa Mucharla        11            -Labor report structure changes
# 11/05/2022	Dhruv Bhatnagar			   30			 -Tranlation corrections
# 11/29/2022    ishika bhattacharya        41            -logic mofidication as per new change
# 11/29/2022    ishika bhattacharya        44            -replaced total cost by unit list price for quote details table
# 12/9/2022     ishika bhattacharya        46            -reverted back the above change
# 12/13/2022    ishika bhattacharya        47            -replaced total cost by total quote cost
# 1/12/2023     ishika bhattacharya        58            -added logic for mandatory charges product and modified the logic for others as well
# 1/14/2023     ishika bhattacharya        61            -added logic if mandatory charge total quote cost is 0 dont show in report
# 1/17/2023     ishika bhattacharya        66            -removed str() function from line 119, 108, 126
# 1/20/2023     ishika bhattacharya        68            -added zero division error validation check
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
lc_Yes = GM_TRANSLATIONS.GetText('000054', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
lc_NO = GM_TRANSLATIONS.GetText('000140', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
lc_discount_variance_perc = GM_TRANSLATIONS.GetText('000138', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
lc_highest_approval_req = GM_TRANSLATIONS.GetText('000139', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
lc_L1 = GM_TRANSLATIONS.GetText('000141', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
lc_NT = GM_TRANSLATIONS.GetText('000033', lv_LanguageKey, '', '', '', '', '')       #NORMAL TIME
lc_OT = GM_TRANSLATIONS.GetText('000034', lv_LanguageKey, '', '', '', '', '')       #OVERTIME
lc_PT = GM_TRANSLATIONS.GetText('000035', lv_LanguageKey, '', '', '', '', '')       #PREMIUM TIME
lc_nt = GM_TRANSLATIONS.GetText('000036', lv_LanguageKey, '', '', '', '', '')       #Normal Time
lc_ot = GM_TRANSLATIONS.GetText('000037', lv_LanguageKey, '', '', '', '', '')       #Overtime
lc_pt = GM_TRANSLATIONS.GetText('000038', lv_LanguageKey, '', '', '', '', '')       # premium Time
lc_others = GM_TRANSLATIONS.GetText('000130', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
lc_Write_In = GM_TRANSLATIONS.GetText('000175', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
lc_mandatory_charges = GM_TRANSLATIONS.GetText('000213', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
hourstypelist = [lc_NT,lc_OT,lc_PT,lc_nt,lc_ot,lc_pt]


if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type :
    ScriptExecutor.Execute('GS_TotalCost_Doc')
    totalcost = context.Quote.GetCustomField('CF_TotalCost_QuoteSummary').Value

    quote_table = context.Quote.QuoteTables['Quote_Summary_Doc']
    quote_table.Rows.Clear()

    getAllItems = context.Quote.GetAllItems()
    product_details = {}

    flag = 0
    
    for item in getAllItems:
        if item.ProductSystemId == "RQ_Mandatory_Charges_cpq" and item.ParentItemId == 0:
            for child_item in context.Quote.GetItemByItemId(item.Id).AsMainItem.GetChildItems():
                if child_item['QI_TOTAL_QUOTE_COST']:
                    flag += 1
                    break

    for item in getAllItems:
        if item.ProductTypeName != lc_Write_In and item.ProductTypeName != lc_mandatory_charges:
            if item.ProductTypeName not in product_details.keys():
                product_details[item.ProductTypeName] = {}
                product_details[item.ProductTypeName]['Total_Quote_Cost'] = item['QI_TOTAL_QUOTE_COST']
                product_details[item.ProductTypeName]['isBold'] = True
                product_details[item.ProductTypeName]['child'] =[]
                if float(totalcost):
                    product_details[item.ProductTypeName]['child'].append({'Part_number': item.PartNumber,'totalQuotecost': item['QI_TOTAL_QUOTE_COST'],'per_of_tot_cost': round((item['QI_TOTAL_QUOTE_COST']/float(totalcost))*100,2),'isBold': False})
                else:
                    product_details[item.ProductTypeName]['child'].append({'Part_number': item.PartNumber,'totalQuotecost': item['QI_TOTAL_QUOTE_COST'],'per_of_tot_cost': 0,'isBold': False})
            else:
                product_details[item.ProductTypeName]['Total_Quote_Cost'] += item['QI_TOTAL_QUOTE_COST']
                if float(totalcost):
                    product_details[item.ProductTypeName]['child'].append({'Part_number': item.PartNumber,'totalQuotecost': item['QI_TOTAL_QUOTE_COST'],'per_of_tot_cost': round((item['QI_TOTAL_QUOTE_COST']/float(totalcost))*100,2),'isBold': False})
                else:
                    product_details[item.ProductTypeName]['child'].append({'Part_number': item.PartNumber,'totalQuotecost': item['QI_TOTAL_QUOTE_COST'],'per_of_tot_cost': 0,'isBold': False})

        elif item.ProductSystemId == "RQ_Mandatory_Charges_cpq" and item.ParentItemId == 0:
            if flag:
                product_details[item.ProductTypeName] = {}
                product_details[item.ProductTypeName]['Total_Quote_Cost'] = item['QI_TOTAL_QUOTE_COST']
                product_details[item.ProductTypeName]['isBold'] = True
                product_details[item.ProductTypeName]['child'] =[]
                for child_item in context.Quote.GetItemByItemId(item.Id).AsMainItem.GetChildItems():
                    if child_item['QI_TOTAL_QUOTE_COST']:
                        product_details[item.ProductTypeName]['child'].append({'Part_number': child_item.PartNumber,'totalQuotecost': child_item['QI_TOTAL_QUOTE_COST'],'per_of_tot_cost': 0,'isBold': False})

        elif item.ProductTypeName == lc_Write_In and item.ParentItemId == 0:
            if item.ProductTypeName not in product_details.keys():
                product_details[item.ProductTypeName] = {}
                product_details[item.ProductTypeName]['Total_Quote_Cost'] = item['QI_TOTAL_QUOTE_COST']
                product_details[item.ProductTypeName]['isBold'] = True
                product_details[item.ProductTypeName]['items'] =[]
                if float(totalcost):
                    product_details[item.ProductTypeName]['items'].append({'Part_number': item.PartNumber,'totalQuotecost': item['QI_TOTAL_QUOTE_COST'],'per_of_tot_cost': round((item['QI_TOTAL_QUOTE_COST']/float(totalcost))*100,2),'isBold': True, 'child':[]})
                else:
                    product_details[item.ProductTypeName]['items'].append({'Part_number': item.PartNumber,'totalQuotecost': item['QI_TOTAL_QUOTE_COST'],'per_of_tot_cost': 0,'isBold': True, 'child':[]})
                for child_item in context.Quote.GetItemByItemId(item.Id).AsMainItem.GetChildItems():
                    if float(totalcost):
                        product_details[item.ProductTypeName]['items'][-1]['child'].append({'Part_number': child_item.PartNumber,'totalQuotecost': child_item['QI_TOTAL_QUOTE_COST'],'per_of_tot_cost': round((child_item['QI_TOTAL_QUOTE_COST']/float(totalcost))*100,2),'isBold': False})
                    else:
                        product_details[item.ProductTypeName]['items'][-1]['child'].append({'Part_number': child_item.PartNumber,'totalQuotecost': child_item['QI_TOTAL_QUOTE_COST'],'per_of_tot_cost': 0,'isBold': False})
            else:
                product_details[item.ProductTypeName]['Total_Quote_Cost'] += item['QI_TOTAL_QUOTE_COST']
                if float(totalcost):
                    product_details[item.ProductTypeName]['items'].append({'Part_number': item.PartNumber,'totalQuotecost': item['QI_TOTAL_QUOTE_COST'],'per_of_tot_cost': round((item['QI_TOTAL_QUOTE_COST']/float(totalcost))*100,2),'isBold': True, 'child':[]})
                else:
                    product_details[item.ProductTypeName]['items'].append({'Part_number': item.PartNumber,'totalQuotecost': item['QI_TOTAL_QUOTE_COST'],'per_of_tot_cost': 0,'isBold': True, 'child':[]})
                for child_item in context.Quote.GetItemByItemId(item.Id).AsMainItem.GetChildItems():
                    if float(totalcost):
                        product_details[item.ProductTypeName]['items'][-1]['child'].append({'Part_number': child_item.PartNumber,'totalQuotecost': child_item['QI_TOTAL_QUOTE_COST'],'per_of_tot_cost': round((child_item['QI_TOTAL_QUOTE_COST']/float(totalcost))*100,2),'isBold': False})
                    else:
                        product_details[item.ProductTypeName]['items'][-1]['child'].append({'Part_number': child_item.PartNumber,'totalQuotecost': child_item['QI_TOTAL_QUOTE_COST'],'per_of_tot_cost': 0,'isBold': False})

    for key, value in product_details.items():

        if key != lc_Write_In:
            row = quote_table.AddNewRow()
            row['isBold'] = value['isBold']
            row['ProductType'] = str(key)
            row['Cost'] = value['Total_Quote_Cost']
            for ele in value['child']:
                row = quote_table.AddNewRow()
                row['isBold'] = ele['isBold']
                row['ProductType'] = '  '+ ele['Part_number']
                row['Cost'] = ele['totalQuotecost']
                row['PerTotalCost'] = ele['per_of_tot_cost']
        elif key == lc_Write_In:
            row = quote_table.AddNewRow()
            row['isBold'] = value['isBold']
            row['ProductType'] = str(key)
            row['Cost'] = value['Total_Quote_Cost']
            for ele in value['items']:
                row = quote_table.AddNewRow()
                row['isBold'] = ele['isBold']
                row['ProductType'] = '  '+ ele['Part_number']
                row['Cost'] = ele['totalQuotecost']
                row['PerTotalCost'] = ele['per_of_tot_cost']
                for items in ele['child']:

                    row = quote_table.AddNewRow()
                    row['isBold'] = items['isBold']
                    row['ProductType'] = '    '+ items['Part_number']
                    row['Cost'] = items['totalQuotecost']
                    row['PerTotalCost'] = items['per_of_tot_cost']


    summary_doc_Table = context.Quote.QuoteTables['Quote_Summary_Details_Doc']
    summary_doc_Table.Rows.Clear()
    quote_table1 = context.Quote.QuoteTables['QT_Quote_Summary']
    for rows in quote_table1.Rows:
        if rows['Product_Type_Rows'] == 'Extra Charges' or rows['Product_Type_Rows'] == 'Travel Expenses':
            if rows['Cost']:
                newRow = summary_doc_Table.AddNewRow()
                newRow['Product_Type_Rows'] = rows['Product_Type_Rows']
                newRow['Cost'] = rows['Cost']
                newRow['Cost_Percentage'] = rows['Costper']
        else:
            newRow = summary_doc_Table.AddNewRow()
            newRow['Product_Type_Rows'] = rows['Product_Type_Rows']
            newRow['Cost'] = rows['Cost']
            newRow['Cost_Percentage'] = rows['Costper']

try:
    if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Modified by Dhruv
        quote_table_financial = context.Quote.QuoteTables['Financial_Summary'].Rows
        for rowi in quote_table_financial:
            #if rowi['Summary'] == "Discount Variance %":    #Commented by Ishika
            if rowi['Summary'] == lc_discount_variance_perc: #Added by Ishika
                context.Quote.GetCustomField('CF_DiscountVariance_Document').Value = str(rowi['Quote_Currency'])
            #if rowi['Summary'] == "Highest Approval Level Required":        #Commented by Ishika
            if rowi['Summary'] == lc_highest_approval_req:                  #Added by Ishika
                #if str(rowi['Quote_Currency']) == 'L1':     #Commented by Ishika
                context.Quote.GetCustomField('CFH_Approval_Level').Value = str(rowi['Quote_Currency'])  #added by ishika 21 nov
                if str(rowi['Quote_Currency']) == lc_L1:     #Added by Ishika
                    #context.Quote.GetCustomField('CFH_Aprover_Doc').Value = "Yes"   #Commented by Ishika
                    context.Quote.GetCustomField('CFH_Aprover_Doc').Value = lc_Yes   #Added by Ishika
                else:
                    #context.Quote.GetCustomField('CFH_Aprover_Doc').Value = "NO   #Commented by Ishika
                    context.Quote.GetCustomField('CFH_Aprover_Doc').Value = lc_NO   #Added by Ishika
except Exception as ex:
    '''Trace.Write("====Estimate Report changes Exception2 ===="+str(ex))'''

try:

    Log.Info("=== CA_EstimateReview Labor/Supplier Details ====")
    lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)    #Added by Ishika
    lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
    lc_Others = GM_TRANSLATIONS.GetText('000130', lv_LanguageKey, '', '', '', '', '')  # Added by Dhruv
    
    if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Modified by Dhruv
        lc_Labor = GM_TRANSLATIONS.GetText('000040', lv_LanguageKey, '', '', '', '', '')   #Added by Ishika
        lc_Honeywell_Labor = GM_TRANSLATIONS.GetText('000118', lv_LanguageKey, '', '', '', '', '')
        
        CF_Profit_Center_ID = context.Quote.GetCustomField('CF_Profit_Center_ID').Value
        CF_Opportunity_Type = context.Quote.GetCustomField('CF_Opportunity_Type').Value
        toal_labor_cost =0
        total_labor_hours = 0
        total_labor_sell_price = 0
        for cu_item in context.Quote.GetAllItems():
            Log.Info("CF_Profit_Center_IDN is::",str(cu_item['CFI_SUB_LOCATION']))
            if cu_item.ProductTypeName == lc_Labor or cu_item.ProductTypeName == lc_Honeywell_Labor:    #Added by Ishika
                toal_labor_cost += cu_item['QI_Total_Cost']
                #toal_labor_cost += cu_item['QI_TOTAL_QUOTE_COST']
                total_labor_hours += cu_item['QI_hours']
                total_labor_sell_price += cu_item.NetPrice
                QI_SAP_Activity_Type = cu_item['QI_SAP_Activity_Type']
                query = SqlHelper.GetFirst("SELECT SERVICE_Material_Description FROM CT_Activity_Type WHERE SAP_Activity_Type = '"+str(QI_SAP_Activity_Type)+"' AND LanguageKey = '"+str(lv_LanguageKey)+"'")	#Modified by Dhruv
                if query:
                    cu_item['QI_SAP_Activity_Type_Desc'] = query.SERVICE_Material_Description
                    Log.Info("QI_SAP_Activity_Type_Desc is::",str(cu_item['QI_SAP_Activity_Type_Desc']))
                    query_location = SqlHelper.GetFirst("SELECT Location_ID FROM CT_PRCTR_MASTER WHERE BranchID = '"+str(CF_Profit_Center_ID)+"' AND LanguageKey = '"+str(lv_LanguageKey)+"' ")	#Modified by Dhruv
                    if(query_location):
                        Log.Info("query_location.Location_ID is::",str(query_location.Location_ID))
                        entity = SqlHelper.GetFirst("SELECT * FROM TAB_HW_DEFAULT_ENTITY WHERE Id = '{0}' AND LanguageKey ='{1}'  ".format(query_location.Location_ID,lv_LanguageKey))	#Modified by Dhruv
                        cu_item['CI_LABOR_LOCATION'] = CF_Profit_Center_ID+" - "+str(entity.Address1)+" "+ str(entity.Address2)+", "+ str(entity.City)+", "+str(entity.State)+", "+str(entity.ZipCode)+", "+str(entity.Country)+" - "+CF_Opportunity_Type
                        Log.Info("CI_LABOR_LOCATION is::",str(cu_item['CI_LABOR_LOCATION']))
                for i in range(len(hourstypelist)):
                    if(hourstypelist[i] in cu_item.ProductName):
                        cu_item['QI_Hours_Type'] = hourstypelist[i]
            query_vendor_type = SqlHelper.GetFirst("SELECT VENDOR_TYPE FROM CT_PRODUCT_SALES WHERE PARTNUMBER = '"+str(cu_item.PartNumber)+"'")	#Modified by Dhruv
            Log.Info("===query_vendor_type executed =====")
            if query_vendor_type:
                Log.Info("===query_vendor_type.VENDOR_TYPE =====",str(query_vendor_type.VENDOR_TYPE))
                cu_item['QI_Vendor_Type'] = query_vendor_type.VENDOR_TYPE
                Log.Info("===Vendor Type =====",str(cu_item['QI_Vendor_Type']))
            else:
                cu_item['QI_Vendor_Type'] = lc_Others				#Modified by Ishika
                
            query_supplier = SqlHelper.GetFirst("SELECT SupplierDescription FROM CT_TP_H WHERE PartNumber = '"+str(cu_item.PartNumber)+"'")	#Modified by Dhruv
            Log.Info("===query_supplier executed =====")
            if query_supplier:
               Log.Info("===query_supplier.SupplierDescription =====",str(query_supplier.SupplierDescription))
               cu_item['QI_Supplier_Desc'] = query_supplier.SupplierDescription
               Log.Info("===Supplier Desc =====",str(cu_item['QI_Supplier_Desc']))
        context.Quote.GetCustomField('CF_Total_Labor_Cost').Value = str(toal_labor_cost)
        context.Quote.GetCustomField('CF_Total_Labor_Hours').Value = str(total_labor_hours)
        context.Quote.GetCustomField('CF_Total_Labor_Sell_Price').Value = str(total_labor_sell_price)            
except Exception as ex:
    Trace.Write(":: For Labor Report changes Exception ::"+str(ex))
    '''Log.Info(":: For Labor Report changes Exception ::",str(ex))'''