import streamlit as st
from webui_pages.utils import *
import pandas as pd






def user_management_page(api: ApiRequest, is_lite: bool = False):
    if 'token' in st.session_state:
        api.setToken(st.session_state['token'])

    urls =[]
    response = api.system_urls()
    if response is not None:
        resp = json.load(response)
        if resp['code'] == 200:
            urls = resp['data']
            print(urls)

    df = pd.DataFrame(urls)
    edited_df = st.data_editor(df)


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