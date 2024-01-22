from server.db.session import with_session
from typing import Dict, List
import uuid
from server.db.models.authorization_model import AuthorizationModel
from configs import logger, log_verbose
from sqlalchemy import desc,or_,and_

@with_session
def delete_authorization(session,usernames: list):
    """
     删除用户记录
    """
    if len(usernames) == 0:
        logger.warn(f"没有提供删除的username")
        return 0
    print(f"删除 usernames:{usernames}")
    del_count = 0

    for username in usernames:
        del_count += session.query(AuthorizationModel).filter(AuthorizationModel.username == username).delete()
    session.commit()
    logger.info(f"删除用户记录成功 删除数目:{del_count}")
    return del_count

@with_session
def add_authorization_to_db(session, username: str, password, name, email,
                      authorization_data: Dict = {}):
    """
    新增用户记录
    """

    au = AuthorizationModel(username=username, password=password, name=name,
                     email=email,
                     authorization_data=authorization_data)
    session.add(au)
    session.commit()
    logger.info(f"新增用户记录成功 username:{username} name:{name} email:{email} authorization_data:{authorization_data}")
    return au.id


@with_session
def get_authorization_by_username(session, username) -> AuthorizationModel:
    """
    查询用户记录
    """
    m = session.query(AuthorizationModel).filter_by(username=username).first()
    return m


@with_session
def update_name_email(session, username:str,name:str,email:str,authorization_data:dict):
    """
    修改姓名，邮箱，权限
    """
    m = session.query(AuthorizationModel).filter_by(username=username).first()

    if m:
        m.name = name
        m.email = email
        if authorization_data is None:
            m.authorization_data = {}
        else:
            m.authorization_data = authorization_data
        session.commit()
        ret_data = {
            "username": m.username,
            "name": m.name,
            "email": m.email,
            "authorization_data": m.authorization_data,
            "create_time": m.create_time,
        }


        logger.info(f"update_name_email 修改姓名、邮箱与权限成功 username: {username}")
        return True,ret_data
    else:
        logger.warn(f"update_name_email 修改姓名、邮箱与权限失败 username: {username}")
        return False,None



@with_session
def query_users_from_db(session,keyword: str=None):
    """
        查询用户
    """
    if keyword is not None and keyword != '':
        #print(f"keyword:{keyword}")
        list = session.query(AuthorizationModel).filter(or_(AuthorizationModel.username.like(f"%{keyword}%"),AuthorizationModel.name.like(f"%{keyword}%"),AuthorizationModel.email.like(f"%{keyword}%"))).order_by(AuthorizationModel.username).all()
    else:
        list = session.query(AuthorizationModel).order_by(AuthorizationModel.username).all()

    ret = []
    if list is not None:
        for authorization in list:
            ret.append({
                "username": authorization.username,
                "name": authorization.name,
                "email": authorization.email,
                "authorization_data": authorization.authorization_data,
                "create_time": authorization.create_time,
            })
    return ret


@with_session
def verify_authorization_by_username_password(session, username,password) -> (bool,dict):
    """
    查询用户记录
    """
    m = session.query(AuthorizationModel).filter_by(username=username,password=password).first()

    if m:
        logger.info(f"verify_authorization_by_username_password 验证成功 username: {username}")
        data = {
            "username": m.username,
            "name": m.name,
            "email": m.email,
            "authorization_data": m.authorization_data,
            "create_time": m.create_time,
        }
        return True,data
    else:
        logger.warn(f"verify_authorization_by_username_password 验证失败 username: {username}")
        return False,None


@with_session
def reset_password(session, username,password) -> bool:
    """
    重置密码
    """
    m = session.query(AuthorizationModel).filter_by(username=username).first()

    if m:
        m.password = password
        session.commit()
        logger.info(f"reset_password 重置密码成功 username: {username}")
        return True
    else:
        logger.warn(f"reset_password 重置密码失败 username: {username}")
        return False

# @with_session
# def refresh_token(session, username) -> bool:
#     """
#     刷新token
#     """
#     m = session.query(AuthorizationModel).filter_by(username=username).first()
#
#     if m:
#         m.token = uuid.uuid4().hex
#         session.commit()
#         return True
#     else:
#         return False


if __name__ == '__main__':
    a = uuid.uuid4().hex

    print(a)