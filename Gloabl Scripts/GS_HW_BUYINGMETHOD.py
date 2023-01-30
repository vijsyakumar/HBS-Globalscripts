# -----------------------------------------------------------------------------
#			Change History Log
# -----------------------------------------------------------------------------
# Description:
# This script is used to calculate the exchange rate
# -----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
# -----------------------------------------------------------------------------
# 12/23/2022    Karthik Raj     0         -initial version
# 01/21/2023    Aditi Sharma              -made corrections related to CSPA discount and price
# 01/28/2023    Aditi Sharma              -added method for write-in special price and roll up
# -----------------------------------------------------------------------------
import GM_TRANSLATIONS
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
quote = context.Quote
b_mtd = quote.GetCustomField('CF_Buying_Method').Value
solpar = False
for bp in context.Quote.GetInvolvedParties():
    Trace.Write("---->"+str(bp.PartnerFunctionKey))
    if str(bp.PartnerFunctionKey) == "SP" and bp.Name[0] in ['S','C']:
        solpar = True
CF_Country = quote.GetCustomField('CF_Country').Value


def calc_write_in():
    lc_p_systemID = GM_TRANSLATIONS.GetText('000128', lv_LanguageKey, '', '', '', '', '')
   
    for rf_item in context.Quote.GetAllItems():
        #checking parent item or not
        p_systemid = rf_item.ProductSystemId
        #if p_systemid == 'Write-in_Products_cpq':   #Commented by Ishika
        if p_systemid == lc_p_systemID:				#Added by Ishika
            #Trace.Write("rfid" +str(rf_item.Id))
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
            lv_special_price = 0
            lv_special_discountP = 0
            lv_special_discountAmnt = 0
            
            #getting child items associated with Main items
            for child_item in context.Quote.GetItemByItemId(rf_item.Id).AsMainItem.GetChildItems():
                #Trace.Write(child_item.PartNumber)
                if child_item['QI_List_Price']!=None:
                    if child_item["QI_SpecialPriceP"]!=None and child_item["QI_SpecialPriceP"]!='' and child_item["QI_SpecialPriceP"]!='0':
                        Log.Write("HWEXC-14")
                        child_item["QI_CSPA_DiscountAmount"] = (float(child_item["QI_SpecialPriceP"]) * float(child_item["QI_List_Price"])) / 100
                        child_item["QI_SpecialPriceV"] = float(child_item["QI_List_Price"]) - float(child_item["QI_CSPA_DiscountAmount"])
                        child_item["QI_Recommended_Unit_Sell_Price"] = float(child_item["QI_List_Price"]) - float(child_item["QI_CSPA_DiscountAmount"])
                        child_item["QI_Recommended_Sell_Price"] = child_item["QI_Recommended_Unit_Sell_Price"] * child_item.Quantity
                        child_item["QI_Unit_Sell_Price"] = child_item['QI_Recommended_Unit_Sell_Price']
                        child_item.NetPrice = child_item['QI_Recommended_Sell_Price']
                        lv_special_price+=float(child_item["QI_SpecialPriceV"])
                        lv_special_discountAmnt+=float(child_item["QI_CSPA_DiscountAmount"])
                    elif child_item["QI_SpecialPriceP"]=='0':
                        child_item["QI_CSPA_DiscountAmount"] = 0
                        child_item["QI_SpecialPriceV"] = 0
                    lv_quantity += child_item.Quantity
                    lv_list_price += child_item['QI_List_Price']
                    lv_tot_price += child_item['QI_List_Price_Total']
                    lv_rec_Unit += child_item['QI_Recommended_Unit_Sell_Price']
                    lv_rec_sell += child_item['QI_Recommended_Sell_Price']
                    lv_unit_cost += child_item['QI_Unit_Cost_Base_Currency']
                    if child_item.DiscountPercent > 0:
                        child_item.DiscountAmount = (float(child_item['QI_Recommended_Unit_Sell_Price']) * float(child_item.DiscountPercent)/100)# * float(child_item.Quantity)
                        lv_disc_amt = lv_disc_amt + (child_item.DiscountAmount * float(child_item.Quantity))
                        lv_disc_perc += child_item.DiscountPercent
                        lv_count = lv_count + 1
                    lv_unit_sell += child_item['QI_Unit_Sell_Price']
                    if child_item['QI_Unit_Sell_Price']:
                        child_item.NetPrice = float(child_item['QI_Unit_Sell_Price']) * float(child_item.Quantity)
                        lv_net_price += child_item.NetPrice
                        child_item['QI_Final_Sell_Price'] = child_item.NetPrice
                    if child_item['QI_Total_Cost']:
                        lv_tot_cost += child_item['QI_Total_Cost']
                        child_item['QI_TOTAL_QUOTE_COST'] = float(child_item['QI_Total_Cost']) + float(child_item['QI_Warranty_Amt']) + float(child_item['QI_INFLATION_AMOUNT']) + float(child_item['QI_FREIGHT_AMOUNT']) + float(child_item['QI_CUSTOMS_AMOUNT'])
                        lv_tot_quot_cost += child_item['QI_TOTAL_QUOTE_COST']
                        lv_mar_amt += child_item['QI_MARGIN_AMOUNT']
                        lv_mar_perc += child_item['QI_MARGIN_PERCENTAGE']

            for rf_item1 in context.Quote.GetAllItems():
                #p_systemid = rf_item1.ProductSystemId
                if rf_item1.ProductSystemId == "Write-in_Products_cpq" and rf_item1.Id == rf_item.Id:
                    rf_item1['QI_PROD_CATEGORY'] = str("Write-Ins")
                    rf_item1.Quantity = float(1)
                    rf_item1['QI_Product_Type'] = str("Write-In")
                    rf_item1['QI_List_Price'] = float(lv_list_price)
                    rf_item1['QI_List_Price_Total'] = float(lv_tot_price)
                    rf_item1['QI_Unit_Sell_Price'] = float(lv_net_price)
                    rf_item1.NetPrice = float(lv_net_price)
                    rf_item1['QI_Final_Sell_Price'] = float(lv_net_price)
                    rf_item1['QI_Recommended_Unit_Sell_Price'] = float(lv_rec_sell)
                    rf_item1['QI_Recommended_Sell_Price'] = float(lv_rec_sell)
                    lv_special_discountP = (float(lv_special_price)/float(lv_list_price))*100
                    rf_item1["QI_SpecialPriceV"] = lv_special_price
                    rf_item1["QI_SpecialPriceP"] = str(lv_special_discountP)
                    rf_item1["QI_CSPA_DiscountAmount"] = lv_special_discountAmnt
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
                    rf_item1['QI_MARGIN_AMOUNT'] = lv_mar_amt
                    if lv_count > 0:
                        rf_item1['QI_MARGIN_PERCENTAGE'] = lv_mar_perc / float(lv_count)


def assigndisc(qryexec):
    for dat in qryexec:
        if dat.Country_Code == CF_Country:
            d_per = dat.DiscountPercent
            break
        else:
            d_per = dat.DiscountPercent
            break
    Trace.Write("d_per---->"+str(d_per))
    Log.Write("HWBuyingMethod--Special Discount Percent: "+str(d_per))
    #qitem.DiscountPercent = float(d_per)*100
    qitem["QI_SpecialPriceP"] = str(float(d_per)*100)
    #33908 start
    if qitem['QI_Product_Type'].upper() == "THIRD PARTY" or qitem['QI_Product_Type'].upper() == "HONEYWELL LABOR" or qitem['QI_Product_Type'].upper() == "LABOR" or qitem['QI_Product_Type'].upper() == "HONEYWELL HARDWARE" or qitem['QI_Product_Type'].upper() == "HONEYWELL SOFTWARE":
        qitem["QI_CSPA_DiscountAmount"] = (float(qitem["QI_SpecialPriceP"]) * float(qitem["QI_List_Price"])) / 100
        #Trace.Write("CSPA-DA: "+str(qitem["QI_CSPA_DiscountAmount"]))
        #Trace.Write("CSPA-DA2: "+str(qitem["QI_List_Price"]))
        qitem["QI_SpecialPriceV"] = float(qitem["QI_List_Price"]) - float(qitem["QI_CSPA_DiscountAmount"])
        Log.Write("HWBuyingMethod--Special Discount Amount: "+str(qitem["QI_CSPA_DiscountAmount"]))
        qitem["QI_Recommended_Unit_Sell_Price"] = qitem["QI_SpecialPriceV"]
        qitem["QI_Recommended_Sell_Price"] = qitem["QI_Recommended_Unit_Sell_Price"] * qitem.Quantity
        qitem["QI_Unit_Sell_Price"] = qitem['QI_Recommended_Unit_Sell_Price']
        qitem.NetPrice = qitem['QI_Recommended_Sell_Price']
    if qitem['QI_Product_Type'].upper() == "THIRD PARTY":
        qitem['QI_Recommended_Unit_Sell_Price'] = qitem["QI_SpecialPriceV"] #Added by Aditi 24Jan2023
        #Trace.Write("TPH: "+str(i["QI_SpecialPriceV"]))
        qitem["QI_Recommended_Sell_Price"] = qitem['QI_Recommended_Unit_Sell_Price'] * (qitem.Quantity)
        qitem["QI_Unit_Sell_Price"] = qitem['QI_Recommended_Unit_Sell_Price']
        qitem.NetPrice = qitem['QI_Recommended_Sell_Price']#33908 end

if solpar and b_mtd.lower() == "buy honeywell hon to hon":
    Log.Write("HWBuyingMethod--ScriptExecution")
    for qitem in context.Quote.GetAllItems():
        #Trace.Write("query-11---->"+str(query))
        if qitem['QI_Product_Type'].upper() == "HONEYWELL HARDWARE" or qitem['QI_Product_Type'].upper() == "HONEYWELL SOFTWARE":
            sale_Cat = qitem['QI_SALES_CATEGORY']
            query ="SELECT * FROM CT_HW_BuyingMethod WHERE Sales_Category IN (SELECT CODE FROM SALES_CATEGORY WHERE DESCRIPTION = '{}') and (Country_Code = '{}' or Country_Code = 'Global')".format(sale_Cat,CF_Country)
            Trace.Write("query-11---->"+str(query))
            qryexec = SqlHelper.GetList(query)
            if qryexec.Count > 0:
                Trace.Write("query-1231---->"+str(query))
                assigndisc(qryexec)
            else:
                qitem["QI_SpecialPriceP"] = str(0)
                qitem["QI_CSPA_DiscountAmount"] = str(0)
                qitem["QI_SpecialPriceV"] = str(0)
        elif qitem['QI_Product_Type'].upper() == "HONEYWELL LABOR" or qitem['QI_Product_Type'].upper() == "LABOR":
            sale_Cat = qitem['QI_SALES_CATEGORY']
            query ="SELECT * FROM CT_HW_BuyingMethod WHERE Sales_Category = 'LP' and (Country_Code = '{}' or Country_Code = 'Global')".format(CF_Country)
            Trace.Write("query----->"+str(query))
            qryexec = SqlHelper.GetList(query)
            if qryexec.Count > 0:
                assigndisc(qryexec)
            #Log.Write("HWBuyingMethod--Sales Category: "+str(qitem.PartNumber)+" "+str(sale_Cat))
            else:
                qitem["QI_SpecialPriceP"] = str(0)
                qitem["QI_CSPA_DiscountAmount"] = str(0)
                qitem["QI_SpecialPriceV"] = str(0)
        elif qitem['QI_Product_Type'].upper() == "THIRD PARTY":
            sale_Cat = qitem['QI_SALES_CATEGORY']
            query ="SELECT * FROM CT_HW_BuyingMethod WHERE Sales_Category = 'THP' and (Country_Code = '{}' or Country_Code = 'Global')".format(CF_Country)
            Trace.Write("query----->"+str(query))
            qryexec = SqlHelper.GetList(query)
            if qryexec.Count > 0:
                assigndisc(qryexec)
                calc_write_in()
            else:
                qitem["QI_SpecialPriceP"] = str(0)
                qitem["QI_CSPA_DiscountAmount"] = str(0)
                qitem["QI_SpecialPriceV"] = str(0)
                calc_write_in()
                