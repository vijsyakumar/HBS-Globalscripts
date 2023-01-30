A = Product.GetContainerByName('AR_FIRE_ASSET')
total_1 = Product.GetContainerByName('AR_FIRE_ASSET').Rows.Count
flag = False
if total_1 > 0:
    for i in Product.GetContainerByName('AR_FIRE_ASSET').Rows:
        c = i.Product.GetContainerByName('AR_CON_ASSET_FIRE_M').Rows[0]
        if c:
            if c["ASSET_TYPE"]!= "":
                flag = True
        
total_1 = Product.GetContainerByName('AR_FIRE_ASSET').Rows.Count

if total_1 > 0 and flag == True:

    col = Product.GetContainerByName('AR_FIRE_ASSET').Rows[total_1-1]
    c = col.Product.GetContainerByName('AR_CON_ASSET_FIRE_M').Rows
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

        total_1 = Product.GetContainerByName('AR_FIRE_ASSET').Rows.Count
        i = 0
        while (i < total_1):
            total_2 = Product.GetContainerByName('AR_FIRE_ASSET').Rows.Count
            cal1 = Product.GetContainerByName('AR_FIRE_ASSET').Rows[i]
            j = 0
            while( j < total_2):
                cal2 = Product.GetContainerByName('AR_FIRE_ASSET').Rows[j]
                if cal2["ASSET_TYPE"] == cal1["ASSET_TYPE"] and (i != j):
                    cal1["SOURCE"] = "Local"
                    cal1["ACTUAL_QTY"] = str(cal2["ACTUAL_QTY"])
                    A.DeleteRow(j)
                    total_2 = Product.GetContainerByName('AR_FIRE_ASSET').Rows.Count
                    if j > total_2:
                        break
                j = j + 1
            total_1 = Product.GetContainerByName('AR_FIRE_ASSET').Rows.Count
            if i > total_1:
                break
            i = i + 1

    A = Product.GetContainerByName('AR_FIRE_ASSET')
    for i in A.Rows:
        asset_data = SqlHelper.GetFirst("SELECT * from CT_ASSETS where SOLUTION_FAMILY ='FIRE' AND ASSET_TYPE = '"+str(i["ASSET_TYPE"])+"'")   
        i["PRODUCT_ID"] = str(asset_data.PRODUCT_ID)
        i["YEARLY_SVC_FREQ"] = str(asset_data.YEARLY_SVC_FREQ)

def strtoint(val):
	try:
		return float(val)
	except:
		return 0
FirePnt = Product.Attributes.GetByName("AR_TOTAL_FIRE_ASSETS")
FireCnt = Product.GetContainerByName("AR_FIRE_ASSET")
FireCount = 0
if FireCnt.Rows.Count > 0:
	for row in FireCnt.Rows:
		FireCount = round(FireCount + strtoint(row["ACTUAL_QTY"]))
	FirePnt.AssignValue(str(FireCount))
