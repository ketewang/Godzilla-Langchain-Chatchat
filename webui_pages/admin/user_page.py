import streamlit as st
from webui_pages.utils import *
import pandas as pd






def user_management_page(api: ApiRequest, is_lite: bool = False):
    if 'token' in st.session_state:
        api.setToken(st.session_state['token'])

    tab1, tab2 = st.tabs([":male-office-worker: 用户", "其他"])

    with tab1:
        st.header("用户")

        response1 = api.system_search_users("e")
        print(response1)
        if response1 is not None:
            resp1 = json.load(response1)
            print(resp1)
            if resp1['code'] == 200:
                users = resp1['data']
                df2 = pd.DataFrame(users)
                st.data_editor(df2)






        urls = []
        response = api.system_urls()
        if response is not None:
            resp = json.load(response)
            if resp['code'] == 200:
                urls = resp['data']


        for item in urls:
            item['enable'] = True
        print(urls)


        df = pd.DataFrame(urls)


        edited_df = st.data_editor(
            df,
            column_config={
                "enable": st.column_config.CheckboxColumn(
                    "grant",
                    help="Grant your **functions** ",
                    default=False,
                )
            },
            disabled=["name", "url"],
            hide_index=True,
        )

    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)







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