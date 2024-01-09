from pydantic import BaseModel, Field
from server.agent.tools_select import tools,tool_names
from langchain.tools import Tool,StructuredTool
from typing import Annotated
from server.agent.tools.tool_register import register_tool,_TOOL_DESCRIPTIONS
import sys
import json
from langchain.agents import tool




#Tool Definitions
@register_tool
def query_data(
        appId: Annotated[str, 'The app ID to be queried, 需要查询的应用ID', True],
        dataPointId: Annotated[str, 'The data point ID to be queried, 需要查询的数据点ID', True],
        startTime: Annotated[str, 'The start time to be queried, 需要查询的数据的起始时间', True],
        endTime: Annotated[str, 'The end time to be queried, 需要查询的数据的结束时间', True],
) -> str:
    """
    查询数据点数据 Get data for dataPointId, 输入分别是应用ID,数据点ID，起始时间，结束时间，返回值为查询的数据
    """
    if not isinstance(dataPointId, str):
        raise TypeError("dataPointId must be a string")
    import requests
    try:

        post_dict = {"appId": appId, "dataPointId": dataPointId,"startTime":startTime,"endTime":endTime}
        header = {
            "Accept": "*/*",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Content-Length": str(sys.getsizeof(post_dict)),
            "Authorization": "xxxx"
        }

        #print(header)
        jsonData = json.dumps(post_dict, ensure_ascii=False)
        resp = requests.post("http://xxxxx/api/collectdata/list",data=jsonData,headers=header)
        resp.raise_for_status()
        resp = resp.json()
        valueList=[]
        if isinstance(resp['data'], dict) and len(resp['data']) > 0:
            #print("data ok")
            if len(resp['data']['collectDataList']) > 0:
                #print("collectDataList >0")
                for item in resp['data']['collectDataList']:
                    valueList.append({'time':item['time'],'value':item['dataValue']})
        #print(valueList)
        ret = valueList
    except:
        import traceback
        ret = "Error encountered while querying dataPoint data!\n" + traceback.format_exc()

    return str(ret)

class Godzilla_Input(BaseModel):
    """
     查询输入的参数
    """
    appId: str = Field()
    dataPointId: str = Field()
    startTime: str = Field()
    endTime: str = Field()
    # appId: str = Field(description = "The app ID to be queried, 应用id")
    # dataPointId: str = Field(description = "The data point ID to be queried, 数据点id")
    # startTime: str = Field(description = "The start time to be queried, 查询起始时间")
    # endTime: str = Field(description = "The end time to be queried, 查询结束时间")


# 1个参数、1个返回值的方法
# tool = Tool.from_function(
#     func=query_data,
#     name="query_data",
#     description= _TOOL_DESCRIPTIONS["query_data"]["description"],
#     args_schema=Godzilla_Input)
# 多个参数返回值的方法
tool = StructuredTool.from_function(
    func=query_data,
    name="query_data",
    description= _TOOL_DESCRIPTIONS["query_data"]["description"],
    args_schema=Godzilla_Input)

tools.append(tool)
tool_names.append(tool.name)