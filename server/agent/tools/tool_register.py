import inspect
import sys
import traceback
from copy import deepcopy
from pprint import pformat
from types import GenericAlias
from typing import get_origin, Annotated
import json

_TOOL_HOOKS = {}
_TOOL_DESCRIPTIONS = {}



def register_tool(func: callable):
    tool_name = func.__name__
    tool_description = inspect.getdoc(func).strip()
    python_params = inspect.signature(func).parameters
    #tool_params = {'type': 'object','properties': {}}
    tool_params = {}
    properties = {}
    # required_params = []
    for name, param in python_params.items():
        annotation = param.annotation
        if annotation is inspect.Parameter.empty:
            raise TypeError(f"Parameter `{name}` missing type annotation")
        if get_origin(annotation) != Annotated:
            raise TypeError(f"Annotation type for `{name}` must be typing.Annotated")

        typ, (description, required) = annotation.__origin__, annotation.__metadata__
        typ: str = str(typ) if isinstance(typ, GenericAlias) else typ.__name__
        if not isinstance(description, str):
            raise TypeError(f"Description for `{name}` must be a string")
        if not isinstance(required, bool):
            raise TypeError(f"Required for `{name}` must be a bool")
        tool_params[name]={'type': typ, 'description':description,'required':required }
        # tool_params.append({
        #     "name": name,
        #     "description": description,
        #     "type": typ,
        #     "required": required
        # })
        # properties[name]={'type': typ, 'description':description }
    #     if required:
    #         required_params.append(name)
    #
    # tool_params['properties'] = properties
    tool_def = {
        "name": tool_name,
        "description": tool_description,
        "parameters": tool_params,
        # "required": required_params
    }

    print("[registered tool] " + pformat(tool_def))
    _TOOL_HOOKS[tool_name] = func
    _TOOL_DESCRIPTIONS[tool_name] = tool_def

    return func

# {'name': 'calculate',
#   'description': 'Useful for when you need to answer questions about simple calculations',
#   'parameters': {'type': 'object', 'properties': {'query': {'type': 'string', 'description': 'The formula to be calculated'}}},
#   'required': ['query']}


def dispatch_tool(tool_name: str, tool_params: dict) -> str:
    if tool_name not in _TOOL_HOOKS:
        return f"Tool `{tool_name}` not found. Please use a provided tool."
    tool_call = _TOOL_HOOKS[tool_name]
    try:
        ret = tool_call(**tool_params)
    except:
        ret = traceback.format_exc()
    return str(ret)


def get_tools() -> dict:
    return deepcopy(_TOOL_DESCRIPTIONS)







if __name__ == "__main__":
    #print(get_tools())
    pass
    #查询下 应用id 为b17398d8b0974b1dab73e7414aa7b036,数据点id为003fba6e57bf4ddbb2f0abbb73cd8716的数据，开始时间 为2023-11-28 10:00:00，结束时间为2023-11-28 22:00:00
    print(dispatch_tool("query_data",{"appId": "b17398d8b0974b1dab73e7414aa7b036","dataPointId": "003fba6e57bf4ddbb2f0abbb73cd8716","startTime":"2023-11-28 13:13:15","endTime": "2023-11-28 23:13:15"
                                      }))



