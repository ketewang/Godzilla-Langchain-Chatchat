import yaml
from yaml.loader import SafeLoader
from webui_pages.login.streamlit_authenticator.authenticate_page import Authenticate


with open('configs/login_config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# def login_page(api: ApiRequest, is_lite: bool = False):
#     print("login_page open")
#     authenticator.login('登录', 'main')

#
#
# # name1,authentication_status1,username1 = authenticator.login('登录', 'main')
# #
# # authenticator.logout('Logout')