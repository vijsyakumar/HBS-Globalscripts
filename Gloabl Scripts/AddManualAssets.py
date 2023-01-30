A = Product.GetContainerByName('AR_HVAC_ASSET')
total_1 = Product.GetContainerByName('AR_HVAC_ASSET').Rows.Count
flag = False
if total_1 > 0:
    for i in Product.GetContainerByName('AR_HVAC_ASSET').Rows:
        c = i.Product.GetContainerByName('AR_CON_ASSET_HVAC_M').Rows[0]
        if c:
            if c["ASSET_TYPE"]!= "":
                flag = True
        
total_1 = Product.GetContainerByName('AR_HVAC_ASSET').Rows.Count

if total_1 > 0 and flag == True:

    col = Product.GetContainerByName('AR_HVAC_ASSET').Rows[total_1-1]
    c = col.Product.GetContainerByName('AR_CON_ASSET_HVAC_M').Rows
    if c:
        index = 1
        for x in c:
            newrow = A.AddNewRow()
            newrow["ASSET_TYPE"] = x["ASSET_TYPE"]
            newrow["SOURCE"]     = "Local"
            newrow["ACTUAL_QTY"]   = str(x["ACTUAL_QTY"])
            if index == 1:
                A.DeleteRow(total_1-1)
            index = index + 1    

        total_1 = Product.GetContainerByName('AR_HVAC_ASSET').Rows.Count
        i = 0
        while (i < total_1):
            total_2 = Product.GetContainerByName('AR_HVAC_ASSET').Rows.Count
            cal1 = Product.GetContainerByName('AR_HVAC_ASSET').Rows[i]
            j = 0
            while( j < total_2):
                cal2 = Product.GetContainerByName('AR_HVAC_ASSET').Rows[j]
                if cal2["ASSET_TYPE"] == cal1["ASSET_TYPE"] and (i != j):
                    cal1["SOURCE"] = "Local"
                    cal1["ACTUAL_QTY"] = str(cal2["ACTUAL_QTY"])
                    A.DeleteRow(j)
                    total_2 = Product.GetContainerByName('AR_HVAC_ASSET').Rows.Count
                    if j > total_2:
                        break
                j = j + 1
            total_1 = Product.GetContainerByName('AR_HVAC_ASSET').Rows.Count
            if i > total_1:
                break
            i = i + 1

A = Product.GetContainerByName('AR_HVAC_ASSET')
for i in A.Rows:
    asset_data = SqlHelper.GetFirst("SELECT * from CT_ASSETS where ASSET_TYPE = '"+str(i["ASSET_TYPE"])+"'")
    if asset_data:
    	i["TRAD_SVC_TIME_QTY"] = str(asset_data.TRAD_SVC_TIME_QTY)
        i["SVC_TIME_FORGE_IMPACT"] = str(asset_data.SVC_TIME_FORGE_IMPACT)
        i["BMS_POINT"] = str(asset_data.BMS_POINT)
        i["ADV_DATA_POINT"] = str(asset_data.ADV_DATA_POINT)
        i["EO_POINTS"] = str(asset_data.EO_POINTS)
        i["EO_POINTS_READING"] = str(asset_data.EO_POINTS_READING)
        i["PRODUCT_ID"] = str(asset_data.PRODUCT_ID)

    def strtoint(val):
        try:
            return float(val)
        except:
            return 0
AssetPnt = Product.Attributes.GetByName("TotalSelectedAssets")
BMSPnt = Product.Attributes.GetByName("TotalBMSPoints")
AnalysePnt = Product.Attributes.GetByName("TotalAnalyzedPoints")
RWPnt = Product.Attributes.GetByName("TotalDataPoints")
HvacCnt = Product.GetContainerByName("AR_HVAC_ASSET")
qtycount = 0
BMScount = 0
Anzcount = 0
RWcount = 0
if HvacCnt.Rows.Count > 0:
    for row in HvacCnt.Rows:
    	qtycount = round(qtycount + strtoint(row["ACTUAL_QTY"]))
    	BMScount = round(BMScount + (strtoint(row["ACTUAL_QTY"]) * strtoint(row["BMS_POINT"])))
    	Anzcount = round(Anzcount + (strtoint(row["ACTUAL_QTY"]) * strtoint(row["ADV_DATA_POINT"])))
    	aa = strtoint(row["EO_POINTS"]) + strtoint(row["EO_POINTS_READING"])
    	RWcount = round(RWcount + (strtoint(row["ACTUAL_QTY"]) * aa))
    	AssetPnt.AssignValue(str(qtycount))
    	BMSPnt.AssignValue(str(BMScount))
    	AnalysePnt.AssignValue(str(Anzcount))
    	RWPnt.AssignValue(str(RWcount))