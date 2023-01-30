count = 0 
count = Product.GetContainerByName('AR_CON_ASSET_FIRE_M').Rows.Count
if count == 0:
    Product.GetContainerByName('AR_CON_ASSET_FIRE_M').AddNewRow()
count = 0 
count = Product.GetContainerByName('AR_CON_ASSET_HVAC_M').Rows.Count
if count == 0:
    Product.GetContainerByName('AR_CON_ASSET_HVAC_M').AddNewRow()