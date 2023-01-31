"""
ContEntSel = Product.GetContainerByName("AR_ENTITLEMENT_SEL")

lv_solutionfamliy = ""
a = Product.Attributes.GetByName('AR_BPS_SOLUTION_FAMILY').SelectedValues

if a:
    for i in a:
        if lv_solutionfamliy != "":
            lv_solutionfamliy = lv_solutionfamliy + ',' + "'" + i.ValueCode + "'"
        else:
            lv_solutionfamliy = "'" + i.ValueCode + "'" 

list_ent = SqlHelper.GetList("SELECT * from CT_SOL_FAM_ENT_MAPPING where SOLUTION_FAMILY IN ("+lv_solutionfamliy+")")

for j in list_ent:
    row = ContEntSel.AddNewRow()
    row["SOLUTION_FAMILY"]     = j.SOLUTION_FAMILY
    row["ENTITLEMENT_DETAILS"]        = j.ENTITLEMENT
    row.SetColumnValue("ENTITLEMENT_INPUT", "*Required")
""""""
ContEntSel = Product.GetContainerByName("AR_ENTITLEMENT_SEL")

lv_solutionfamliy = ""
a = Product.Attributes.GetByName('AR_BPS_SOLUTION_FAMILY').SelectedValues

if a:
    for i in a:
        if lv_solutionfamliy != "":
            lv_solutionfamliy = lv_solutionfamliy + ',' + "'" + i.ValueCode + "'"
        else:
            lv_solutionfamliy = "'" + i.ValueCode + "'" 

list_ent = SqlHelper.GetList("SELECT * from CT_SOL_FAM_ENT_MAPPING where SOLUTION_FAMILY IN ("+lv_solutionfamliy+")")

for j in list_ent:
    row = ContEntSel.AddNewRow()
    row["SOLUTION_FAMILY"]     = j.SOLUTION_FAMILY
    row["ENTITLEMENT_DETAILS"]        = j.ENTITLEMENT
    row.SetColumnValue("ENTITLEMENT_INPUT", "*Required")
"""