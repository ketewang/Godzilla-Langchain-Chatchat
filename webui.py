import streamlit as st
from webui_pages.utils import *
from streamlit_option_menu import option_menu
from webui_pages.dialogue.dialogue import dialogue_page, chat_box
from webui_pages.knowledge_base.knowledge_base import knowledge_base_page
import os
import sys
from configs import VERSION
from server.utils import api_address
from webui_pages.login.login import authenticator


api = ApiRequest(base_url=api_address())



if __name__ == "__main__":

    is_lite = "lite" in sys.argv

    if "authentication_status" in st.session_state and st.session_state["authentication_status"] == True:
        st.set_page_config(
            "Godzilla-AI-Chat WebUI",
            os.path.join("img", "chatchat_icon_blue_square_v2.png"),
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'http://www.godzilla.tech',
                'About': f"""欢迎使用 Godzilla-AI-Chat Web {VERSION}！"""
            }
        )
        pages = {
            "对话": {
                "icon": "chat",
                "func": dialogue_page,
            },
            "知识库管理": {
                "icon": "hdd-stack",
                "func": knowledge_base_page,
            },
        }

        with st.sidebar:
            st.image(
                os.path.join(
                    "img",
                    "logo-godzilla-horizontal-white.png"
                ),
                use_column_width=True
            )
            st.caption(
                f"""<p align="right">当前版本：{VERSION}</p>""",
                unsafe_allow_html=True,
            )
            st.write(f'Welcome *{st.session_state["username"]}*')
            authenticator.logout('退出系统', 'sidebar')
            options = list(pages)
            icons = [x["icon"] for x in pages.values()]

            default_index = 0
            selected_page = option_menu(
                "",
                options=options,
                icons=icons,
                # menu_icon="chat-quote",
                default_index=default_index,
            )
            if "logout" in st.session_state and st.session_state['logout'] == True:
                st.success('成功登出系统')

        if selected_page in pages:
            pages[selected_page]["func"](api=api, is_lite=is_lite)



    else:
        with st.sidebar:
            st.image(
                os.path.join(
                    "img",
                    "logo-godzilla-horizontal-white.png"
                ),
                use_column_width=True
            )
            st.caption(
                f"""<p align="right">当前版本：{VERSION}</p>""",
                unsafe_allow_html=True,
            )
        name,status,username = authenticator.login(api=api,form_name='用户登录',location='sidebar')
        if status == True:
            st.success('登录成功')
        elif status == False:
            st.error('登录失败')
        try:
            if authenticator.register_user('用户注册','sidebar', preauthorization=False):
                st.success('User registered successfully')
        except Exception as e:
            st.error(e)




