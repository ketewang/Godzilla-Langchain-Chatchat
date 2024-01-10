from server.db.repository import add_authorization_to_db,verify_authorization_by_username_password
from server.utils import BaseResponse



def user_login(username:str,password:str) -> BaseResponse:
    '''
        用户登录，用户名密码验证 verify_authorization_by_username_password
    '''
    print(f"user_login username {username}")
    if verify_authorization_by_username_password(username,password):
        return BaseResponse(code=200,msg=f"{username}登录成功")

    return BaseResponse(code=501,msg=f"验证失败，{username}登录失败")


if __name__ == '__main__':
    ret=user_login("a","b")
    print(ret)
