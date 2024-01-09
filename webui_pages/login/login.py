import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# with open('../../configs/login_config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)
#
# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )

# name1,authentication_status1,username1 = authenticator.login('登录', 'main')
#
# authenticator.logout('Logout')