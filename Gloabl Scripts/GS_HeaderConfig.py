#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#Carries Header Configuration
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 7/18/2022     Anbarasan           0           -initial version
# 04/11/2022	Dhruv Bhatnagar 	8	        -Replaced Hardcodings
#												-Incorporated Translation
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS                   												 #Added by Dhruv
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)   								 #Added by Dhruv
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
FireCnt = Product.GetContainerByName("AR_FIRE_ASSET")
FirePnt = Product.Attributes.GetByName("AR_TOTAL_FIRE_ASSETS")

FireCount = 0
qtycount = 0
BMScount = 0
Anzcount = 0
RWcount = 0
if HvacCnt.Rows.Count > 0:
	#Trace.Write("-------->1")
	for row in HvacCnt.Rows:
		#Trace.Write("-------->2")
		qtycount = round(qtycount + strtoint(row["ACTUAL_QTY"]))
		BMScount = round(BMScount + (strtoint(row["ACTUAL_QTY"]) * strtoint(row["BMS_POINT"])))
		Anzcount = round(Anzcount + (strtoint(row["ACTUAL_QTY"]) * strtoint(row["ADV_DATA_POINT"])))
		aa = strtoint(row["EO_POINTS"]) + strtoint(row["EO_POINTS_READING"])
		RWcount = round(RWcount + (strtoint(row["ACTUAL_QTY"]) * aa))
	AssetPnt.AssignValue(str(qtycount))
	BMSPnt.AssignValue(str(BMScount))
	AnalysePnt.AssignValue(str(Anzcount))
	RWPnt.AssignValue(str(RWcount))
if FireCnt.Rows.Count > 0:
    for row in FireCnt.Rows:
        FireCount = round(FireCount + strtoint(row["ACTUAL_QTY"]))
	FirePnt.AssignValue(str(FireCount))
