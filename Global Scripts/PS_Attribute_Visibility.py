def hideAttr(product , attr):
    product.Attr(attr).Access = AttributeAccess.Hidden
ValidContainerName = "AR_Product_Upload_Valid"
for attr in Product.Attributes:
    attr.Access = AttributeAccess.Editable
    if attr.DisplayType == "Container":
        container = Product.GetContainerByName(attr.Name)
        if container.Rows.Count == 0:
            attr.Access = AttributeAccess.Hidden

if Product.GetContainerByName(ValidContainerName).Rows.Count == 0:
    hideAttr(Product , "AR_SelectValidParts")
