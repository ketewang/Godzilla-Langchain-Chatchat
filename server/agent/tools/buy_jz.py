from pydantic import BaseModel, Field
from server.agent.tools_select import tools,tool_names
from langchain.tools import Tool
from typing import Annotated
from server.agent.tools.tool_register import register_tool,_TOOL_DESCRIPTIONS



@register_tool
def buy_jz(quantity: Annotated[str, '输入买的是饺子的数量，单位为斤', True])-> str:
    """
    当你需要买一份饺子时候可以使用这个工具,输入为饺子的数量,返回值为买了多少饺子成功
    """
    return f"成功购买{quantity}斤饺子"


class Buy_jzInput(BaseModel):
    quantity: str = Field()


tool = Tool.from_function(
    func=buy_jz,
    name="buy_jz",
    description= _TOOL_DESCRIPTIONS["buy_jz"]["description"],
    args_schema=Buy_jzInput)


tools.append(tool)
tool_names.append(tool.name)

