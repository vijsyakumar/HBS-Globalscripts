lt_selected_sol_family = Product.Attributes.GetByName('AR_BPS_SOLUTION_FAMILY').SelectedValues
Lt_selected_container = Product.GetContainerByName('AR_SELECTED_SOL_FAM')
for items in lt_selected_sol_family:
    lv_sol_fam = items.ValueCode
    Product.GetContainerByName('AR_SELECTED_SOL_FAM').AddNewRow(lv_sol_fam, False)