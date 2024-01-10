from sqlalchemy import Column, Integer, String, DateTime, JSON, func

from server.db.base import Base


class AuthorizationModel(Base):
    """
    用户权限模型
    """
    __tablename__ = 'authorization'
    id = Column(Integer,autoincrement='auto', primary_key=True, comment='流水号')
    username = Column(String(64), unique=True, index=True,nullable=False,comment='用户名')
    password = Column(String(128),nullable=False, comment='密码')
    token = Column(String(128),unique=True,nullable=False, comment='token')
    name = Column(String(128),nullable=True, comment='姓名')
    email = Column(String(128),nullable=True, comment='email')
    # key:编号 value：值
    authentication_data = Column(JSON, default={}, comment='权限')
    create_time = Column(DateTime, default=func.now(), comment='创建时间')

    def __repr__(self):
        return f"<authorization(id='{self.id}', username='{self.username}', password='{self.password}',token='{self.token}', name='{self.name}', email='{self.email}', authentication_data='{self.authentication_data}', create_time='{self.create_time}')>"
