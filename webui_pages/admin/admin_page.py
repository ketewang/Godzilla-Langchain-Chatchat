import streamlit as st
from webui_pages.utils import *
import pandas as pd
from webui_pages.login.streamlit_authenticator.authenticate_page import authenticator





def user_management_page(api: ApiRequest, is_lite: bool = False):
    if 'token' in st.session_state:
        api.setToken(st.session_state['token'])

    tab1, tab2 = st.tabs([":male-office-worker: 用户管理", ":memo:用户注册"])

    with tab1:
        st.header("用户")

        response1 = api.system_search_users("")
        #print(response1)
        if response1 is not None:
            resp1 = json.load(response1)
            #print(resp1)
            if resp1['code'] == 200:
                users = resp1['data']
                df_users = pd.DataFrame(users)
                edited_user_df =st.data_editor(df_users,
                               disabled=["username","create_time"],
                               on_change=user_onchange,
                               )
                #print(df_users.items)
                #print(edited_user_df)
                for i in range(df_users["username"].size):
                    if df_users.loc[i]["name"] == edited_user_df.loc[i]["name"] and df_users.loc[i]["email"] == edited_user_df.loc[i]["email"]:
                        continue
                    else:
                        logger.info(f"go update edited: {edited_user_df.loc[i]['name']} {edited_user_df.loc[i]['email']}")
                        resp_sub_1 = api.system_update_user_info(edited_user_df.loc[i]['username'],edited_user_df.loc[i]['name'],edited_user_df.loc[i]['email'])
                        if resp_sub_1 is not None:
                            resp_sub_1 = json.load(resp_sub_1)
                            if resp_sub_1['code'] == 200:
                                st.success(resp_sub_1['msg'])
                            else:
                                st.error(resp_sub_1['msg'])

        urls = []
        response = api.system_urls()
        if response is not None:
            resp = json.load(response)
            if resp['code'] == 200:
                urls = resp['data']

        options = st.multiselect(
            '选择权限',
            urls,
            [])

        st.write('You selected:', options)
        #print(urls)


        df = pd.DataFrame(options)
        edited_df = st.data_editor(
            df,
            # column_config={
            #     "enable": st.column_config.CheckboxColumn(
            #         "grant",
            #         help="Grant your **functions** ",
            #         default=False,
            #     )
            # },
            disabled=["name", "url"],
            hide_index=True,
        )

    with tab2:
        try:
            if authenticator.register_user('用户注册', 'main', preauthorization=False):
                st.success('用户注册成功')
        except Exception as e:
            st.error(e)


def user_onchange(** kwargs):
    print("user_onchange")
    print(kwargs)
    pass




    # edited_df = st.data_editor(df)

    # selected_username = edited_df.loc[edited_df["name"].last_valid_index]["username"]
    # st.markdown(f" **{selected_username}** 🎈")
    with st.sidebar:
        pass


if __name__ == "__main__":
    df = pd.DataFrame(
        [
            {"username": "用户a", "name": "kurt", "email": "a#a.com", "is_widget": True},
            {"username": "用户b", "name": "peter", "email": "a#a.com", "is_widget": True},
            {"username": "用户c", "name": "tom", "email": "a#a.com", "is_widget": True},

        ]
    )
    edited_df = st.data_editor(df)

    selected_username = edited_df.loc[edited_df["name"].last_valid_index]["username"]

    pass