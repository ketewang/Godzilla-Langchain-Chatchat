from server.db.repository import add_authorization_to_db,verify_authorization_by_username_password
from server.utils import BaseResponse
from fastapi import Body
from httpx import codes
from configs import logger, log_verbose

def user_login(username: str = Body("", max_length=64, description="用户名"),
               password: str = Body("", max_length=256, description="密码")):
    '''
        用户登录，用户名密码验证 verify_authorization_by_username_password
    '''
    #print(f"user_login username: {username} password: {password}")
    try:
        ret,name = verify_authorization_by_username_password(username,password)
        if ret:
            logger.info(f"user_login 登录成功 username: {username}")
            return BaseResponse(code=codes.OK,msg=f"登录成功 username:{username}",data=name)
        else:
            logger.warn(f"验证失败，user_login登录失败 username:{username}")
            return BaseResponse(code=codes.FORBIDDEN, msg=f"验证失败，登录失败 username:{username}")
    except Exception as e:
        msg = f"用户登录出错： {e}"
        logger.error(f'{e.__class__.__name__}: {msg}',
                     exc_info=e if log_verbose else None)
        return BaseResponse(code=codes.INTERNAL_SERVER_ERROR, msg=msg)




def user_register(username: str = Body("", max_length=64, description="用户名"),
                   password: str = Body("", max_length=256, description="密码"),
                   name: str = Body("", max_length=64, description="姓名"),
                   email: str = Body("", max_length=64, description="email")
                   ):
    '''
        用户注册
    '''
    try:
        add_authorization_to_db(username,password,name,email)
        return BaseResponse(code=codes.OK, msg=f"用户注册ok username:{username} name:{name} email:{email}")
    except Exception as e:
        msg = f"用户注册出错： {e}"
        logger.error(f'{e.__class__.__name__}: {msg}',
                     exc_info=e if log_verbose else None)
        return BaseResponse(code=codes.INTERNAL_SERVER_ERROR, msg=msg)






