count = 0 
count = Product.GetContainerByName('AR_HVAC_COMPREHENSIVE_COVERAGE_DETAILS').Rows.Count
if count == 0:
    Product.GetContainerByName('AR_HVAC_COMPREHENSIVE_COVERAGE_DETAILS').AddNewRow()
    count = 0 

count = Product.GetContainerByName('AR_HVAC_SOFTWARE_ASSURANCE_DETAILS').Rows.Count
if count == 0:
    Product.GetContainerByName('AR_HVAC_SOFTWARE_ASSURANCE_DETAILS').AddNewRow()
    count = 0 

count = Product.GetContainerByName('AR_HVAC_HVAC_CONTROLS_PM_TASKING_DETAILS').Rows.Count    
if count == 0:
    Product.GetContainerByName('AR_HVAC_HVAC_CONTROLS_PM_TASKING_DETAILS').AddNewRow()
    count = 0
    
count = Product.GetContainerByName('AR_HVAC_FORGE_DIGITIZED_MAINTENANCE_DETAILS').Rows.Count    
if count == 0:
    Product.GetContainerByName('AR_HVAC_FORGE_DIGITIZED_MAINTENANCE_DETAILS').AddNewRow()
    count = 0
    
count = Product.GetContainerByName('AR_HVAC_FORGE_MOBILIZATION_DETAILS').Rows.Count
if count == 0:
    Product.GetContainerByName('AR_HVAC_FORGE_MOBILIZATION_DETAILS').AddNewRow()
    count = 0
    
count = Product.GetContainerByName('AR_ENERGY_OPTIMIZATION_DETAILS').Rows.Count
if count == 0:
    Product.GetContainerByName('AR_ENERGY_OPTIMIZATION_DETAILS').AddNewRow()
    count = 0  
    
count = Product.GetContainerByName('AR_Emergency_Service').Rows.Count
if count == 0:
    Product.GetContainerByName('AR_Emergency_Service').AddNewRow()
    count = 0    
    
count = Product.GetContainerByName('AR_Q_FIRE_SOFT_ASSURANCE').Rows.Count
if count == 0:
    Product.GetContainerByName('AR_Q_FIRE_SOFT_ASSURANCE').AddNewRow()
    count = 0    
    
count = Product.GetContainerByName('AR_Q_FIRE_SERVICES').Rows.Count
if count == 0:
    Product.GetContainerByName('AR_Q_FIRE_SERVICES').AddNewRow()
    count = 0  
    
count = Product.GetContainerByName('AR_Cyber_Details').Rows.Count
if count == 0:
    Product.GetContainerByName('AR_Cyber_Details').AddNewRow()
    count = 0  
    
count = Product.GetContainerByName('AR_Honeywell_Threat_Defense_Platform').Rows.Count
if count == 0:
    Product.GetContainerByName('AR_Honeywell_Threat_Defense_Platform').AddNewRow()
    count = 0  
    