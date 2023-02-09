product = SqlHelper.GetFirst("select p.product_ID from Products p join product_versions pv on p.Product_ID = pv.Product_ID where System_ID = 'Write-in_Products_cpq' and pv.Is_Active = 1")
if product is not None:
    activePID = product.product_ID
    rURL = '/configurator.aspx?pid=' + str(activePID) + '&cid=3102'
    context.WorkflowContext.RedirectToURL = rURL