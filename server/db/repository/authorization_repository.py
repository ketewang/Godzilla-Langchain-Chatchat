from server.db.session import with_session
from typing import Dict, List
import uuid
from server.db.models.authorization_model import AuthorizationModel

@with_session
def add_authorization_to_db(session, username: str, password, name, email,
                      authorization_data: Dict = {}):
    """
    新增用户记录
    """

    au = AuthorizationModel(token=uuid.uuid4().hex, username=username, password=password, name=name,
                     email=email,
                     authorization_data=authorization_data)
    session.add(au)
    session.commit()
    return au.id


@with_session
def get_authorization_by_username(session, username) -> AuthorizationModel:
    """
    查询用户记录
    """
    m = session.query(AuthorizationModel).filter_by(username=username).first()
    return m


@with_session
def verify_authorization_by_username_password(session, username,password) -> bool:
    """
    查询用户记录
    """
    m = session.query(AuthorizationModel).filter_by(username=username,password=password).first()

    if m:
        print("验证成功")
        return True
    else:
        print("验证失败")
        return False


@with_session
def reset_password(session, username,password) -> bool:
    """
    查询用户记录
    """
    m = session.query(AuthorizationModel).filter_by(username=username).first()

    if m:
        m.password = password
        session.commit()
        return True
    else:
        return False

@with_session
def refresh_token(session, username) -> bool:
    """
    查询用户记录
    """
    m = session.query(AuthorizationModel).filter_by(username=username).first()

    if m:
        m.token = uuid.uuid4().hex
        session.commit()
        return True
    else:
        return False


if __name__ == '__main__':
    a = uuid.uuid4().hex

    print(a)