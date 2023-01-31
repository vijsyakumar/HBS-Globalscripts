def strtoint(val):
    try:
        return float(val)
    except:
        return 0
HvacCnt = Product.GetContainerByName("AR_HVAC_ASSET")
if HvacCnt.Rows.Count > 0:
    for row in HvacCnt.Rows:
        row["TRAD_SVC_TIME_TTL"] =  str(strtoint(row["ACTUAL_QTY"]) * strtoint(row["TRAD_SVC_TIME_QTY"]))
        row["SVC_TIME_FORGE_IMPACt_TTL"] = str(strtoint(row["ACTUAL_QTY"]) * strtoint(row["SVC_TIME_FORGE_IMPACT"]))
        row["TTL_BMS_POINTS_QTY"] = str(strtoint(row["ACTUAL_QTY"]) * strtoint(row["BMS_POINT"]))
        row["SUM_DP_QTY"] = str(strtoint(row["ACTUAL_QTY"]) * strtoint(row["ADV_DATA_POINT"]))
        row["NUM_DP_ASSET_EO"] = str(strtoint(row["EO_POINTS_READING"]) + strtoint(row["EO_POINTS"]))
        row["SUM_DP_ASSET_EO"] = str(strtoint(row["ACTUAL_QTY"]) * strtoint(strtoint(row["EO_POINTS_READING"]) + strtoint(row["EO_POINTS"])))
        row["NUM_DP_EO"] = str(strtoint(row["ACTUAL_QTY"]) * strtoint(row["EO_POINTS_READING"]))