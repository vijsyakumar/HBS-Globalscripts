for i in context.Quote.GetAllItems():
    if i.ProductSystemId == "RQ_Mandatory_Charges_cpq":
        i['QI_MARGIN_AMOUNT'] = float(0)
        i['QI_MARGIN_PERCENTAGE'] = float(0)
        i['QI_WTW_Margin'] = float(0)
        for child_item in context.Quote.GetItemByItemId(i.Id).AsMainItem.GetChildItems():
            child_item['QI_MARGIN_AMOUNT'] = float(0)
            child_item['QI_MARGIN_PERCENTAGE'] = float(0)
            child_item['QI_WTW_Margin'] = float(0)
    if i.Description == "Adhoc Product":
        i.Description = i['QI_Description']
        #i.PartNumber = i['QI_Description']
    if i.Description == "WriteIn" or i.Description == "Write-In":
        i.Description = i['QI_Description']
        i.PartNumber = i['QI_Description']
        #i['QI_Exchange_Rate'] = float(0)
        i['QI_WTW_COST'] = float(0)
        i['QI_UNIT_WTW_COST'] = float(0)
        i['QI_WTW_Margin'] = float(0)
        i['QI_MARGIN_AMOUNT'] = float(0)
        i['QI_MARGIN_PERCENTAGE'] = float(0)