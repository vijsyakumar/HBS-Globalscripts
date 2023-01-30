A = Product.GetContainerByName('AR_RQ_MandatoryCharges')
newrow = A.AddNewRow()
newrow["ManProductsChoices"] = "Consumables"
newrow["Man_Category"] = "Extra Charges"
newrow["Man_ProductType"] = "Consumables"

row = A.AddNewRow()
row["ManProductsChoices"] = "Travel"
row["Man_Category"] = "Extra Charges"
row["Man_ProductType"] = "Travel"

row1 = A.AddNewRow()
row1["ManProductsChoices"] = "Environmental"
row1["Man_Category"] = "Extra Charges"
row1["Man_ProductType"] = "Environmental"

row2 = A.AddNewRow()
row2["ManProductsChoices"] = "Administrative Charges"
row2["Man_Category"] = "Extra Charges"
row2["Man_ProductType"] = "Administrative Charges"



