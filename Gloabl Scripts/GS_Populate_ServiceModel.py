#24495 Service material Population script.
import clr
from System.Net import HttpWebRequest
clr.AddReference("System.Xml")
import sys
serv_mat =context.Quote.QuoteTables["QT_SERVICE_MATERIALS"]
qte_Sumry =context.Quote.QuoteTables["QT_Quote_Summary"]
Country = context.Quote.GetCustomField("CF_Country").Value

def matidsel():
    sltn_fam = context.Quote.GetCustomField('CF_Solution Family').Value
    slct_qry = "SELECT * FROM CT_SM_MAP WHERE Solution_Family like '%{}%'".format(sltn_fam)
    query = SqlHelper.GetList(slct_qry)
    if query.Count>0:
        return query
    else:
        return False

def popaction():
    serv_cost = {"First Party Material":0.0,"Third Party":0.0,"Labor":0.0,"Subcontractor":0.0,"Travel Expenses":0.0,"Extra Charges":0.0,"Contingency":0.0,"Pricing Adjustments":0.0,"Honeywell Hardware":0.0,"Honeywell Software":0.0,"Honeywell Labor":0.0}
    serv_price = {"First Party Material":0.0,"Third Party":0.0,"Labor":0.0,"Subcontractor":0.0,"Travel Expenses":0.0,"Extra Charges":0.0,"Contingency":0.0,"Pricing Adjustments":0.0,"Honeywell Hardware":0.0,"Honeywell Software":0.0,"Honeywell Labor":0.0}
    hr_rq = 0
    toappl = {}
    for crow in qte_Sumry.Rows:
        #Trace.Write("crow--->"+str(crow["Product_Type_Rows"]))
        serv_price[str(crow["Product_Type_Rows"])] =  float(crow["Sell_Price"])
        serv_cost[str(crow["Product_Type_Rows"])] = float(crow["Cost"])
        #if str(crow["Product_Type_Rows"]).lower() == "labor":
            #hr_rq += crow["Hours"]
        #if str(crow["Product_Type_Rows"]).lower() == "first party material":
            
    Trace.Write("serv_cost--->"+str(serv_cost))
    Trace.Write("serv_price--->"+str(serv_price))
    first_party_price = serv_price["Honeywell Hardware"]+serv_price["Honeywell Software"]
    first_party_cost = serv_cost["Honeywell Hardware"]+serv_cost["Honeywell Software"]
    hrdwr_price = first_party_price+serv_price["Third Party"]
    hrdwr_cost = first_party_cost+serv_cost["Third Party"]
    lbr_price = serv_price["Third Party"]+serv_price["Subcontractor"]+serv_price["Travel Expenses"]+serv_price["Extra Charges"]+serv_price["Contingency"]+serv_price["Pricing Adjustments"]
    lbr_cost = serv_cost["Third Party"]+serv_cost["Subcontractor"]+serv_cost["Travel Expenses"]+serv_cost["Extra Charges"]+serv_cost["Contingency"]+serv_cost["Pricing Adjustments"]
    ext_mat_cst = serv_cost["Third Party"]
    int_mat_cst = first_party_cost
    tot_cst = serv_cost["Honeywell Labor"] - serv_cost["Subcontractor"]
    subcnt_cst = serv_cost["Subcontractor"]
    Trvl_othr_Exp = serv_cost["Travel Expenses"]
    tot_pln_cst = ext_mat_cst+int_mat_cst+tot_cst+subcnt_cst+Trvl_othr_Exp
    #Trace.Write("cst--->"+str(lbr["Cost"]))
    QI_hours = 0.0
    for qitem in context.Quote.GetAllItems():
        if 'Labor' in qitem.ProductTypeName:
            QI_hours += qitem['QI_hours']
    t_toalsaleprice = 0.0
    t_qtecost = 0.0
    m_toalsaleprice = 0.0
    m_qtecost = 0.0
    l_toalsaleprice = 0.0
    l_qtecost = 0.0
    s_toalsaleprice = 0.0
    s_qtecost = 0.0
    e_toalsaleprice = 0.0
    e_qtecost = 0.0
    for qitem in context.Quote.GetAllItems():
        if qitem["QI_RECORD_TYPE"]:
            if qitem["QI_RECORD_TYPE"].upper() == "T":
                Trace.Write("qitem.PartNumber--->"+str(qitem.PartNumber))
                #Log.Info("QI_Final_Sell_Price--->"+str(qitem["QI_Final_Sell_Price"]))
                t_toalsaleprice += qitem["QI_Final_Sell_Price"]
                t_qtecost += qitem["QI_TOTAL_QUOTE_COST"]
                #Trace.Write("t_toalsaleprice--->"+str(t_toalsaleprice))
                #Trace.Write("t_qtecost--->"+str(t_qtecost))
            if qitem["QI_RECORD_TYPE"].upper() == "M":
                m_toalsaleprice += qitem["QI_Final_Sell_Price"]
                m_qtecost += qitem["QI_TOTAL_QUOTE_COST"]
                #Trace.Write("m_toalsaleprice--->"+str(m_toalsaleprice))
                #Trace.Write("m_qtecost--->"+str(m_qtecost))
            if "labor" in qitem['QI_Product_Type'].lower():
                l_toalsaleprice += qitem["QI_Final_Sell_Price"]
                l_qtecost += qitem["QI_TOTAL_QUOTE_COST"]
                #Trace.Write("l_toalsaleprice--->"+str(l_toalsaleprice))
                #Trace.Write("l_qtecost--->"+str(l_qtecost))
            if qitem["QI_RECORD_TYPE"].upper() == "S":
                s_toalsaleprice += qitem["QI_Final_Sell_Price"]
                s_qtecost += qitem["QI_TOTAL_QUOTE_COST"]
                #Trace.Write("s_toalsaleprice--->"+str(s_toalsaleprice))
                #Trace.Write("s_qtecost--->"+str(s_qtecost))
            if qitem["QI_RECORD_TYPE"].upper() == "" and  qitem.ProductSystemId != "Write-in_Products_cpq" and qitem.ProductSystemId != "RQ_Mandatory_Charges_cpq":
                Trace.Write("qitem.Description--->"+str(qitem.Description))
                Trace.Write("qitem.ProductSystemId--->"+str(qitem.ProductSystemId))
                e_toalsaleprice += qitem["QI_Final_Sell_Price"]
                e_qtecost += qitem["QI_TOTAL_QUOTE_COST"]
            #Trace.Write("e_toalsaleprice--->"+str(e_toalsaleprice))
            #Trace.Write("e_qtecost--->"+str(e_qtecost))
    e_toalsaleprice = e_toalsaleprice - l_toalsaleprice
    e_qtecost = e_qtecost - l_qtecost
    if Country != "US":
        lbr = serv_mat.Rows[0]
        lbr["COST"] = float(t_qtecost+m_qtecost+l_qtecost+s_qtecost+e_qtecost)
        lbr["SALES_PRICE"] = float(t_toalsaleprice+m_toalsaleprice+l_toalsaleprice+s_toalsaleprice+e_toalsaleprice)
        lbr["ATS_HOURS_QS"] = QI_hours
        lbr["EXT_MATL_QS"] = t_qtecost#ext_mat_cst
        lbr["INT_MATL_QS"] = m_qtecost
        #if tot_cst > 0:
        lbr["LABOR_QS"] = l_qtecost
        lbr["SUBCONTRACT_QS"] = s_qtecost
        lbr["T_AND_E_QS"] = e_qtecost
        lbr["Planed_Exp_Cost"] = float(t_qtecost+m_qtecost+l_qtecost+s_qtecost+e_qtecost)
        if str(matidsel()) != "False":
            lbr["MAT_ID"] = str(matidsel()[0].Material_ID)
            lbr["DESCRIPTION"] = str(matidsel()[0].Description)
    else:
        lbr = serv_mat.Rows[0]
        lbr["COST"] = float(l_qtecost+s_qtecost)
        lbr["SALES_PRICE"] = float(l_toalsaleprice+s_toalsaleprice)#lbr_price
        lbr["ATS_HOURS_QS"] = QI_hours
        lbr["EXT_MATL_QS"] = t_qtecost#ext_mat_cst
        lbr["INT_MATL_QS"] = m_qtecost#int_mat_cst
        #if tot_cst > 0:
        lbr["LABOR_QS"] = l_qtecost#tot_cst
        lbr["SUBCONTRACT_QS"] = s_qtecost#subcnt_cst
        lbr["T_AND_E_QS"] = e_qtecost
        lbr["Planed_Exp_Cost"] = float(t_qtecost+m_qtecost+l_qtecost+s_qtecost+e_qtecost)
        #commented by Aditi as throwing error - 30/9/22
        hrd = serv_mat.Rows[1]
        hrd["COST"] = float(m_qtecost+t_qtecost+e_qtecost)
        hrd["SALES_PRICE"] = float(t_toalsaleprice+m_toalsaleprice+e_toalsaleprice)
        if str(matidsel()) != "False":
            lbr["MAT_ID"] = str(matidsel()[0].Material_ID)
            lbr["DESCRIPTION"] = str(matidsel()[0].Description)
        
        if str(matidsel()) != "False":
            hrd["MAT_ID"] = str(matidsel()[1].Material_ID)
            hrd["DESCRIPTION"] = str(matidsel()[1].Description)
        #comment end
        
    Trace.Write("cst--->"+str(lbr["COST"]))

try:
    if serv_mat.Rows.Count == 0:
        if Country == "US":
            for i in range(0,2):
                Trace.Write(i)
                row = serv_mat.AddNewRow()
                if i == 1:
                    row["ItemId"] = 20
                    if str(matidsel()) != "False":
                        row["MAT_ID"] = str(matidsel()[1].Material_ID)
                        row["DESCRIPTION"] = str(matidsel()[1].Description)
                    row["MAT_TYPE"] = "HARDWARE"
                    row["Qty"] = 1

                else:
                    row["ItemId"] = 10
                    if str(matidsel()) != "False":
                        row["MAT_ID"] = str(matidsel()[0].Material_ID)
                        row["DESCRIPTION"] = str(matidsel()[0].Description)
                    row["MAT_TYPE"] = "LABOR"
                    row["Qty"] = 1
        else:
            row = serv_mat.AddNewRow()
            row["ItemId"] = 10
            if str(matidsel()) != "False":
                row["MAT_ID"] = str(matidsel()[0].Material_ID)
                row["DESCRIPTION"] = str(matidsel()[0].Description)
            row["MAT_TYPE"] = "LABOR"
            row["Qty"] = 1
        popaction();
    else:
        popaction();
except Exception as e:
    Log.Error("Error--->:"+str(sys.exc_info()[1]))
    Log.Error("Error Line No--->:"+str(sys.exc_info()[-1].tb_lineno))
    Log.Error("Error Detail--->:"+str(e))
"""finSummTable =context.Quote.QuoteTables["QT_Booking_Service"]
finSummTable_cost =context.Quote.Totals.Cost
finSummTable_price =context.Quote.Totals.NetPrice
if finSummTable.Rows.Count>0:
    for tot in finSummTable.Rows:
        tot["Price"] = finSummTable_price
        tot["Cost"] = finSummTable_cost
else:
    row = finSummTable.AddNewRow()"""