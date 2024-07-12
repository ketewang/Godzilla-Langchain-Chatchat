import json

import jwt
import bcrypt
import streamlit as st
from datetime import datetime, timedelta
import extra_streamlit_components as stx

from webui_pages.login.streamlit_authenticator.hasher import Hasher
from webui_pages.login.streamlit_authenticator.validator import Validator
from webui_pages.login.streamlit_authenticator.utils import generate_random_pw

from webui_pages.login.streamlit_authenticator.exceptions import CredentialsError, ForgotError, RegisterError, ResetError, UpdateError
from webui_pages.utils import *
from server.auth.role_previledge import role_options
import yaml
from yaml.loader import SafeLoader



api = ApiRequest(base_url=api_address())

class Authenticate:
    """
    This class will create login, logout, register user, reset password, forgot password, 
    forgot username, and modify user details widgets.
    """
    def __init__(self, credentials: dict, cookie_name: str, key: str, cookie_expiry_days: float=30.0, 
        preauthorized: list=None, validator: Validator=None):
        """
        Create a new instance of "Authenticate".

        Parameters
        ----------
        credentials: dict
            The dictionary of usernames, names, passwords, and emails.
        cookie_name: str
            The name of the JWT cookie stored on the client's browser for passwordless reauthentication.
        key: str
            The key to be used for hashing the signature of the JWT cookie.
        cookie_expiry_days: float
            The number of days before the cookie expires on the client's browser.
        preauthorized: list
            The list of emails of unregistered users authorized to register.
        validator: Validator
            A Validator object that checks the validity of the username, name, and email fields.
        """
        self.credentials = credentials
        self.credentials['usernames'] = {key.lower(): value for key, value in credentials['usernames'].items()}
        self.cookie_name = cookie_name
        self.key = key
        self.cookie_expiry_days = cookie_expiry_days
        self.preauthorized = preauthorized
        self.cookie_manager = stx.CookieManager()
        self.validator = validator if validator is not None else Validator()

        if 'name' not in st.session_state:
            st.session_state['name'] = None
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
        if 'username' not in st.session_state:
            st.session_state['username'] = None
        if 'logout' not in st.session_state:
            st.session_state['logout'] = None

    def _token_encode(self) -> str:
        """
        Encodes the contents of the reauthentication cookie.

        Returns
        -------
        str
            The JWT cookie for passwordless reauthentication.
        """
        return jwt.encode({'name':st.session_state['name'],
            'username':st.session_state['username'],
            'exp_date':self.exp_date}, self.key, algorithm='HS256')

    def _token_decode(self) -> str:
        """
        Decodes the contents of the reauthentication cookie.

        Returns
        -------
        str
            The decoded JWT cookie for passwordless reauthentication.
        """
        try:
            return jwt.decode(self.token, self.key, algorithms=['HS256'])
        except:
            return False

    def _set_exp_date(self) -> str:
        """
        Creates the reauthentication cookie's expiry date.

        Returns
        -------
        str
            The JWT cookie's expiry timestamp in Unix epoch.
        """
        return (datetime.utcnow() + timedelta(days=self.cookie_expiry_days)).timestamp()

    # def _check_pw(self) -> bool:
    #     """
    #     Checks the validity of the entered password.
    #
    #     Returns
    #     -------
    #     bool
    #         The validity of the entered password by comparing it to the hashed password on disk.
    #     """
    #     return bcrypt.checkpw(self.password.encode(),
    #         self.credentials['usernames'][self.username]['password'].encode())

    def _check_cookie(self):
        """
        Checks the validity of the reauthentication cookie.
        """
        self.token = self.cookie_manager.get(self.cookie_name)
        if self.token is not None:
            self.token = self._token_decode()
            if self.token is not False:
                if not st.session_state['logout']:
                    if self.token['exp_date'] > datetime.utcnow().timestamp():
                        if 'name' and 'username' in self.token:
                            st.session_state['name'] = self.token['name']
                            st.session_state['username'] = self.token['username']
                            st.session_state['authentication_status'] = True
    
    def _check_credentials(self,inplace: bool=True) -> bool:
        """
        Checks the validity of the entered credentials.

        Parameters
        ----------
        inplace: bool
            Inplace setting, True: authentication status will be stored in session state, 
            False: authentication status will be returned as bool.
        Returns
        -------
        bool
            Validity of entered credentials.
        """

        response = api.system_login(self.username, Hasher.hash(self.password))
        if response is not None:
            resp = json.load(response)
            if resp['code'] == 200:
                data = resp['data']
                #print(data)
                #st.session_state['name'] = self.credentials['usernames'][self.username]['name']
                self.exp_date = self._set_exp_date()
                self.token = self._token_encode()
                self.cookie_manager.set(self.cookie_name, self.token,
                                        expires_at=datetime.now() + timedelta(days=self.cookie_expiry_days))
                st.session_state['authentication_status'] = True
                st.session_state['name'] = data['name']
                st.session_state['logout'] = None
                st.session_state['token'] = data['token']
                st.session_state['role'] = data['role']
                print(f"get token:{data['token']} role:{data['role']}")
                return True

        st.session_state['authentication_status'] = False
        return False


        # if self.username in self.credentials['usernames']:
        #     try:
        #         if self._check_pw():
        #             if inplace:
        #                 st.session_state['name'] = self.credentials['usernames'][self.username]['name']
        #                 self.exp_date = self._set_exp_date()
        #                 self.token = self._token_encode()
        #                 self.cookie_manager.set(self.cookie_name, self.token,
        #                     expires_at=datetime.now() + timedelta(days=self.cookie_expiry_days))
        #                 st.session_state['authentication_status'] = True
        #                 st.session_state['logout'] = None
        #             else:
        #                 return True
        #         else:
        #             if inplace:
        #                 st.session_state['authentication_status'] = False
        #             else:
        #                 return False
        #     except Exception as e:
        #         print(e)
        # else:
        #     if inplace:
        #         st.session_state['authentication_status'] = False
        #     else:
        #         return False

    def login(self, form_name: str, location: str='main') -> tuple:
        """
        Creates a login widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the login form.
        location: str
            The location of the login form i.e. main or sidebar.
        Returns
        -------
        str
            Name of the authenticated user.
        bool
            The status of authentication, None: no credentials entered, 
            False: incorrect credentials, True: correct credentials.
        str
            Username of the authenticated user.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")

        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
        if 'name' not in st.session_state:
            st.session_state['name'] = None
        if 'username' not in st.session_state:
            st.session_state['username'] = None

        if st.session_state['authentication_status'] == None or st.session_state['authentication_status'] == False:
            self._check_cookie()
            if not st.session_state['authentication_status']:
                if location == 'main':
                    login_form = st.form('Login')
                elif location == 'sidebar':
                    login_form = st.sidebar.form('Login')
                    # st.sidebar.title(f'用户:blue[{form_name}]')
                    # login_username_text_input = st.sidebar.text_input(
                    #     "username",
                    #     "",
                    #     key="login-username",
                    # )
                    # login_password_text_input = st.sidebar.text_input(
                    #     "password",
                    #     "",
                    #     key="login-password",
                    #     type="password"
                    # )

                login_form.subheader(form_name)
                self.username = login_form.text_input('Username')
                st.session_state['username'] = self.username
                self.password = login_form.text_input('Password', type='password')
                if login_form.form_submit_button('Login',use_container_width=True,type="primary"):
                    self._check_credentials()

        return st.session_state['name'], st.session_state['authentication_status'], st.session_state['username']

    def logout(self, button_name: str, location: str='main', key: str=None):
        """
        Creates a logout button.

        Parameters
        ----------
        button_name: str
            The rendered name of the logout button.
        location: str
            The location of the logout button i.e. main or sidebar.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            if st.button(button_name, key):
                self.cookie_manager.delete(self.cookie_name)
                st.session_state['logout'] = True
                st.session_state['name'] = None
                st.session_state['username'] = None
                st.session_state['authentication_status'] = None
                st.session_state['token'] = None
                st.session_state['role'] = None
        elif location == 'sidebar':
            if st.sidebar.button(button_name, key):
                self.cookie_manager.delete(self.cookie_name)
                st.session_state['logout'] = True
                st.session_state['name'] = None
                st.session_state['username'] = None
                st.session_state['authentication_status'] = None
                st.session_state['token'] = None
                st.session_state['role'] = None

    def _update_password(self, username: str, password: str):
        """
        Updates credentials dictionary with user's reset hashed password.

        Parameters
        ----------
        username: str
            The username of the user to update the password for.
        password: str
            The updated plain text password.
        """
        self.credentials['usernames'][username]['password'] = Hasher.hash(password)

    def reset_password(self,username: str, form_name: str, location: str='main') -> bool:
        """
        Creates a password reset widget.

        Parameters
        ----------
        username: str
            The username of the user to reset the password for.
        form_name: str
            The rendered name of the password reset form.
        location: str
            The location of the password reset form i.e. main or sidebar.
        Returns
        -------
        str
            The status of resetting the password.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            reset_password_form = st.form('Reset password')
        elif location == 'sidebar':
            reset_password_form = st.sidebar.form('Reset password')
        
        reset_password_form.subheader(form_name)
        self.username = username.lower()
        self.password = reset_password_form.text_input('Current password', type='password')
        new_password = reset_password_form.text_input('New password', type='password')
        new_password_repeat = reset_password_form.text_input('Repeat password', type='password')

        if reset_password_form.form_submit_button('Reset'):
            if self._check_credentials(inplace=False):
                if len(new_password) > 0:
                    if new_password == new_password_repeat:
                        if self.password != new_password: 
                            self._update_password(self.username, new_password)
                            return True
                        else:
                            raise ResetError('New and current passwords are the same')
                    else:
                        raise ResetError('Passwords do not match')
                else:
                    raise ResetError('No new password provided')
            else:
                raise CredentialsError('password')
    
    def _register_credentials(self, username: str, name: str, password: str, email: str, preauthorization: bool,role:str):
        """
        Adds to credentials dictionary the new user's information.

        Parameters
        ----------
        username: str
            The username of the new user.
        name: str
            The name of the new user.
        password: str
            The password of the new user.
        email: str
            The email of the new user.
        preauthorization: bool
            The preauthorization requirement, True: user must be preauthorized to register, 
            False: any user can register.
        role:str
            role of the user
        """
        if not self.validator.validate_username(username):
            raise RegisterError('Username is not valid')
        if not self.validator.validate_name(name):
            raise RegisterError('Name is not valid')
        if not self.validator.validate_email(email):
            raise RegisterError('Email is not valid')
        if role is None or role == '':
            raise RegisterError('role is not valid')

        if 'token' in st.session_state:
            api.setToken(st.session_state['token'])

        response = api.user_register(username, Hasher.hash(password),name,email,role)
        if response is not None:
            resp = json.load(response)
            if 'code' in resp and resp['code'] == 200:
                st.session_state['logout'] = None
                self.credentials['usernames'][username] = {'name': name,
                                                           'password': Hasher.hash(password), 'email': email, 'role': role}
                if preauthorization:
                    self.preauthorized['emails'].remove(email)
            else:
                raise RegisterError(f'用户注册失败 {resp}')
        else:
            raise RegisterError(f'用户注册失败 response为None')







    def register_user(self, form_name: str, location: str='main', preauthorization=True) -> bool:
        """
        Creates a register new user widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the register new user form.
        location: str
            The location of the register new user form i.e. main or sidebar.
        preauthorization: bool
            The preauthorization requirement, True: user must be preauthorized to register, 
            False: any user can register.
        Returns
        -------
        bool
            The status of registering the new user, True: user registered successfully.
        """
        if preauthorization:
            if not self.preauthorized:
                raise ValueError("preauthorization argument must not be None")
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            register_user_form = st.form('Register user')
        elif location == 'sidebar':
            register_user_form = st.sidebar.form('Register user')

        register_user_form.subheader(form_name)
        cols = register_user_form.columns(2)
        role_choice = cols[1].selectbox(
            ':male-technologist: Role',
            role_options,
            index=0)
        new_username = cols[0].text_input(':bust_in_silhouette: Username').lower()
        new_name = cols[0].text_input(':man: Name')
        new_email = cols[1].text_input(':e-mail: Email')
        new_password = cols[0].text_input(':key: Password', type='password')
        new_password_repeat = cols[0].text_input(':key: Repeat password', type='password')

        if register_user_form.form_submit_button('创建账户',use_container_width=True,type="primary"):
            if len(new_email) and len(new_username) and len(new_name) and len(new_password) > 0:
                if new_username not in self.credentials['usernames']:
                    if new_password == new_password_repeat:
                        if preauthorization:
                            if new_email in self.preauthorized['emails']:
                                self._register_credentials(new_username, new_name, new_password, new_email, preauthorization,role_choice)
                                return True
                            else:
                                raise RegisterError('User not preauthorized to register')
                        else:
                            self._register_credentials(new_username, new_name, new_password, new_email, preauthorization,role_choice)
                            return True
                    else:
                        raise RegisterError('Passwords do not match')
                else:
                    raise RegisterError('Username already taken')
            else:
                raise RegisterError('Please enter an email, username, name, and password')

    def _set_random_password(self, username: str) -> str:
        """
        Updates credentials dictionary with user's hashed random password.

        Parameters
        ----------
        username: str
            Username of user to set random password for.
        Returns
        -------
        str
            New plain text password that should be transferred to user securely.
        """
        self.random_password = generate_random_pw()
        self.credentials['usernames'][username]['password'] = Hasher.hash(self.random_password)
        return self.random_password

    def forgot_password(self, form_name: str, location: str='main') -> tuple:
        """
        Creates a forgot password widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the forgot password form.
        location: str
            The location of the forgot password form i.e. main or sidebar.
        Returns
        -------
        str
            Username associated with forgotten password.
        str
            Email associated with forgotten password.
        str
            New plain text password that should be transferred to user securely.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            forgot_password_form = st.form('Forgot password')
        elif location == 'sidebar':
            forgot_password_form = st.sidebar.form('Forgot password')

        forgot_password_form.subheader(form_name)
        username = forgot_password_form.text_input('Username').lower()

        if forgot_password_form.form_submit_button('Submit'):
            if len(username) > 0:
                if username in self.credentials['usernames']:
                    return username, self.credentials['usernames'][username]['email'], self._set_random_password(username)
                else:
                    return False, None, None
            else:
                raise ForgotError('Username not provided')
        return None, None, None

    def _get_username(self, key: str, value: str) -> str:
        """
        Retrieves username based on a provided entry.

        Parameters
        ----------
        key: str
            Name of the credential to query i.e. "email".
        value: str
            Value of the queried credential i.e. "jsmith@gmail.com".
        Returns
        -------
        str
            Username associated with given key, value pair i.e. "jsmith".
        """
        for username, entries in self.credentials['usernames'].items():
            if entries[key] == value:
                return username
        return False

    def forgot_username(self, form_name: str, location: str='main') -> tuple:
        """
        Creates a forgot username widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the forgot username form.
        location: str
            The location of the forgot username form i.e. main or sidebar.
        Returns
        -------
        str
            Forgotten username that should be transferred to user securely.
        str
            Email associated with forgotten username.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            forgot_username_form = st.form('Forgot username')
        elif location == 'sidebar':
            forgot_username_form = st.sidebar.form('Forgot username')

        forgot_username_form.subheader(form_name)
        email = forgot_username_form.text_input('Email')

        if forgot_username_form.form_submit_button('Submit'):
            if len(email) > 0:
                return self._get_username('email', email), email
            else:
                raise ForgotError('Email not provided')
        return None, email

    def _update_entry(self, username: str, key: str, value: str):
        """
        Updates credentials dictionary with user's updated entry.

        Parameters
        ----------
        username: str
            The username of the user to update the entry for.
        key: str
            The updated entry key i.e. "email".
        value: str
            The updated entry value i.e. "jsmith@gmail.com".
        """
        self.credentials['usernames'][username][key] = value

    def update_user_details(self, username: str, form_name: str, location: str='main') -> bool:
        """
        Creates a update user details widget.

        Parameters
        ----------
        username: str
            The username of the user to update user details for.
        form_name: str
            The rendered name of the update user details form.
        location: str
            The location of the update user details form i.e. main or sidebar.
        Returns
        -------
        str
            The status of updating user details.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            update_user_details_form = st.form('Update user details')
        elif location == 'sidebar':
            update_user_details_form = st.sidebar.form('Update user details')
        
        update_user_details_form.subheader(form_name)
        self.username = username.lower()
        field = update_user_details_form.selectbox('Field', ['Name', 'Email']).lower()
        new_value = update_user_details_form.text_input('New value')

        if update_user_details_form.form_submit_button('Update'):
            if len(new_value) > 0:
                if new_value != self.credentials['usernames'][self.username][field]:
                    self._update_entry(self.username, field, new_value)
                    if field == 'name':
                            st.session_state['name'] = new_value
                            self.exp_date = self._set_exp_date()
                            self.token = self._token_encode()
                            self.cookie_manager.set(self.cookie_name, self.token,
                            expires_at=datetime.now() + timedelta(days=self.cookie_expiry_days))
                    return True
                else:
                    raise UpdateError('New and current values are the same')
            if len(new_value) == 0:
                raise UpdateError('New value not provided')


with open('configs/login_config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


if __name__ == '__main__':
    password = "1233323是的发送到发送33"
    ff =Hasher.hash(password)
    print(ff)