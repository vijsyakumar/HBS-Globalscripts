import GM_TRANSLATIONS
import datetime

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)

cf_name = Param.Name
response = {}
#Log.Info("cf_name---->"+str(cf_name))
if str(cf_name) != "":
    try:
        data = SqlHelper.GetFirst("Select Tooltip_Description from CT_Tooltip Where Custom_Fields_Name='{}' and LANGUAGEKEY = '{}'".format(cf_name,lv_LanguageKey))
        #Log.Info("data.Tooltip_Description---->"+str(data.Tooltip_Description))
        response[cf_name] = data.Tooltip_Description
    except:
        pass
ApiResponse = ApiResponseFactory.JsonResponse(response)