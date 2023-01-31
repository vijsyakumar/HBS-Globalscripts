#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is called from UI and Sets order reason value as true or false
#Used for translation purpose display
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 01/20/2023	Dhruv Bhatnagar		0			-Initial Creation
#
#-----------------------------------------------------------------------------
import datetime
Country_Key = context.Quote.GetCustomField("CF_Country").Value
cf_name = Param.Name
response = {}

if str(cf_name) !=" ":
    try:
        data = SqlHelper.GetFirst("SELECT VALUE FROM CT_ORDER_REASON_BOOKING WHERE VALUE ='{}' and Country_Key ='{}' ".format(cf_name,str(Country_Key)))
        if data:
            response[cf_name] = True
    	else:
            response[cf_name] = False
    except:
        pass
ApiResponse = ApiResponseFactory.JsonResponse(response)