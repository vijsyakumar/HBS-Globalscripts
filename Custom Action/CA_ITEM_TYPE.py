'''context.Quote.Totals.Amount = 10
Log.Write('Item Type  Main Executed 123')
#context.Quote.Totals.Amount = 0'''
Log.Write('Item Type  Main Executed ')
lv_total = 0
lt_items = context.Quote.GetAllItems()
for items in lt_items:
    if items.IsOptional == False:
        lv_total += items.ExtendedAmount
context.Quote.Totals.Amount = lv_total