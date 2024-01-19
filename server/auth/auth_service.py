from server.db.repository import add_authorization_to_db,verify_authorization_by_username_password,query_users_from_db,update_name_email
from server.utils import BaseResponse
from fastapi import Body
from httpx import codes
from configs import logger, log_verbose
from server.cache.cache_service import cache
from server.auth.role_previledge import role_privileges,all_urls

import uuid

user_token_prefix = "user_token_"

def user_login(username: str = Body("", max_length=64, description="用户名"),
               password: str = Body("", max_length=256, description="密码")):
    '''
        用户登录，用户名密码验证 verify_authorization_by_username_password
    '''
    #print(f"user_login username: {username} password: {password}")
    try:
        res,db_data = verify_authorization_by_username_password(username,password)
        if res:
            token, role = refreshTokenData(username, db_data)
            logger.info(f"user_login 登录成功 username: {username}")
            data = {'name': db_data['name'],
                    'token': token,
                    'role': role,
                    }
            return BaseResponse(code=codes.OK,msg=f"登录成功 username:{username} role:{role}",data=data)
        else:
            logger.warn(f"验证失败，user_login登录失败 username:{username}")
            return BaseResponse(code=codes.FORBIDDEN, msg=f"验证失败，登录失败 username:{username}")
    except Exception as e:
        msg = f"用户登录出错： {e}"
        logger.error(f'{e.__class__.__name__}: {msg}',
                     exc_info=e if log_verbose else None)
        return BaseResponse(code=codes.INTERNAL_SERVER_ERROR, msg=msg)

def refreshTokenData(username: str, db_data) -> (str,str):

    user_token_key = f"{user_token_prefix}{username}"
    if cache.cache.has(user_token_key):
        token = cache.cache.get(user_token_key)
    else:
        token = uuid.uuid4().hex

    cache.cache.set(user_token_key, token)
    # 设置url权限
    authorization_data = db_data['authorization_data']
    my_privilege_urls = {}
    role = None
    if 'role' in authorization_data:
        role = authorization_data['role']
        privilege_names = role_privileges[role]
        for name in privilege_names:
            my_privilege_urls[all_urls[name]] = "granted"
    db_data['my_privilege_urls'] = my_privilege_urls
    cache.cache.set(token, db_data)
    logger.info(f"刷新token成功 username: {db_data['username']} cache:{token} role:{role} db_data:{db_data}")
    return token,role


def user_register(username: str = Body("", max_length=64, description="用户名"),
                   password: str = Body("", max_length=256, description="密码"),
                   name: str = Body("", max_length=64, description="姓名"),
                   email: str = Body("", max_length=64, description="email"),
                   role: str = Body("", max_length=64, description="role")
                   ):
    '''
        用户注册
    '''
    try:
        authorization_data = {}
        if role is not None:
            authorization_data['role'] = role
        add_authorization_to_db(username,password,name,email,authorization_data)
        return BaseResponse(code=codes.OK, msg=f"用户注册ok username:{username} name:{name} email:{email} role:{role}")
    except Exception as e:
        msg = f"用户注册出错： {e}"
        logger.error(f'{e.__class__.__name__}: {msg}',
                     exc_info=e if log_verbose else None)
        return BaseResponse(code=codes.INTERNAL_SERVER_ERROR, msg=msg)



def search_users(keyword: str = Body("", max_length=64, description="关键字"),
                 foo: str = Body("", max_length=64, description=""),
                 ):
    try:
        users = query_users_from_db(keyword)
        return BaseResponse(code=codes.OK, msg=f"查询用户 ok",data=users)
    except Exception as e:
        msg = f"查询用户出错： {e}"
        logger.error(f'{e.__class__.__name__}: {msg}',
                     exc_info=e if log_verbose else None)
        return BaseResponse(code=codes.INTERNAL_SERVER_ERROR, msg=msg)


def update_user_info(username: str = Body("", max_length=64, description="用户名"),
                   name: str = Body("", max_length=64, description="姓名"),
                   email: str = Body("", max_length=64, description="email"),
      authorization_data: dict = Body("", description="authorization_data"),
                     ):
    try:
        res, ret_data = update_name_email(username,name,email,authorization_data)
        if res:
            refreshTokenData(username, ret_data)
            return BaseResponse(code=codes.OK, msg=f"更新用户{username}信息 ok")
        else:
            return BaseResponse(code=codes.NOT_FOUND, msg=f"更新用户{username}信息 fail,用户信息不存在")

    except Exception as e:
        msg = f"更新用户信息出错： {e}"
        logger.error(f'{e.__class__.__name__}: {msg}',
                     exc_info=e if log_verbose else None)
        return BaseResponse(code=codes.INTERNAL_SERVER_ERROR, msg=msg)
