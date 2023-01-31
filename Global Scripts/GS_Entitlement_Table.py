#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#Entitlement and Cost calculation in SC
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 10/14/2022    MarripudiKrishna     0                -Initial Version
# 10/17/2022    Isha Sharma          2                -Replaced Hardcodings
#                                                     -Incorporated Translation
#
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS                                                    #Added by Isha
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)                     #Added by Isha
lc_desc_value = GM_TRANSLATIONS.GetText('000057', lv_LanguageKey, '', '', '', '', '')    #Added by Isha

def cost_calculation(): 
    for i in context.Quote.GetAllItems():
        #if i.Description == 'HVAC Control PM Tasking':                 #Commented by Isha
        if i.Description == lc_desc_value:
            tempdesc = i.Description
            tempdisc = i.DiscountAmount
            tempper = i.DiscountPercent
            tempsellpr = i['QI_Yearly_Sell_Price']
            #Trace.Write(tempdesc)
            #Trace.Write(tempdisc)
            #Trace.Write(tempsellpr)
            #Trace.Write(tempper)
            if i.DiscountPercent:
                #Trace.Write("-- Discount Amount ---")
                i.DiscountAmount =  i['QI_Yearly_Sell_Price']* (i.DiscountPercent/100)
               # Trace.Write(i.DiscountAmount)
               # Trace.Write(i.DiscountPercent)
            if i.DiscountAmount:
                i.DiscountPercent = i.DiscountAmount /i['QI_Yearly_Sell_Price']
               # Trace.Write(i.DiscountAmount)

cost_calculation()

for product in context.Quote.GetAllItems():
        if len(product.RolledUpQuoteItem) == 1:
            #Trace.Write('prod id:{}'.format(product.Id))
            SolFam_DisPercent, SolFam_DisAmt = 0, 0
   
            for sol_family in context.Quote.GetItemByItemId(product.Id).AsMainItem.GetChildItems():
                entl_DisAmt = 0
                entl_DistPer = 0
                
                m = len(sol_family.RolledUpQuoteItem.split('.'))
                # Trace.Write('m:{}'.format(m))
                
                if m == 2:
                    #Trace.Write('sol_family.Id:{}'.format(sol_family.Id))
                    
                    for entitlement in context.Quote.GetItemByItemId(sol_family.Id).AsMainItem.GetChildItems():
                        #Trace.Write('entitlement.Id:{}'.format(entitlement.Id))
                        entl_DisAmt += entitlement.DiscountAmount
                        entl_DistPer += entitlement.DiscountPercent
                
                    
                    sol_family.DiscountAmount= entl_DisAmt
                    SolFam_DisAmt = entl_DisAmt
                    
                    sol_family.DiscountPercent = entl_DistPer
                    SolFam_DisPercent = entl_DistPer
                    
            # Trace.Write('main:{}'.format(product['QI_Yearly_Sell_Price']))
            product.DiscountAmount = SolFam_DisAmt
            product.DiscountPercent = SolFam_DisPercent