from server.db.session import with_session
from typing import Dict, List
import uuid
from server.db.models.authorization_model import AuthorizationModel
from configs import logger, log_verbose

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
def verify_authorization_by_username_password(session, username,password) -> (bool,str):
    """
    查询用户记录
    """
    m = session.query(AuthorizationModel).filter_by(username=username,password=password).first()

    if m:
        logger.info(f"verify_authorization_by_username_password 验证成功 username: {username}")
        return True,m.name
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