#context.Quote.ChangeStatus('Order Confirmation Pending')
#context.Quote.ChangeStatus('Customer Accepted')
Log.Info("=== CA_ORD_FALED_COUNT Action Start===== ")
order_failed_str = context.Quote.GetCustomField('CF_ORD_FAILED_COUNT').Value

order_failed_count= 0
Log.Info("=== CA_ORD_FALED_COUNT Action order_failed_count ===== ",str(order_failed_count))
if(order_failed_str is None or len(order_failed_str) == 0 ):
    order_failed_count+= 1
else:
    order_failed_count = int(context.Quote.GetCustomField('CF_ORD_FAILED_COUNT').Value)
    order_failed_count+= 1

context.Quote.GetCustomField('CF_ORD_FAILED_COUNT').Value = str(order_failed_count)
Log.Info("=== Order Confirmation Pending ===== ",str(context.Quote.GetCustomField('CF_ORD_FAILED_COUNT').Value))
Log.Info("=== CA_ORD_FALED_COUNT Action End===== ")