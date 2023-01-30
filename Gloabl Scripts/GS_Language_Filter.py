country = context.Quote.GetCustomField("CF_Country").Value
cf_name = Param.Name
response = {}
#Log.Info("cf_name---->"+str(cf_name))
if str(cf_name) != "":
    try:
        data = SqlHelper.GetList("Select LANGUAGE from CT_Language_Data Where COUNTRY='{}' and LANGUAGE = '{}'".format(country , cf_name))
        #Log.Info("data.Tooltip_Description---->"+str(data.Tooltip_Description))
        if data:
            response[cf_name] = True
        else:
            response[cf_name] = False
    except:
        pass
ApiResponse = ApiResponseFactory.JsonResponse(response)