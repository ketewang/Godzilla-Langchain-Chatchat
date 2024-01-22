from configs import (
    DB_ROOT_PATH,
    logger, log_verbose
)

from webui_pages.login.streamlit_authenticator.hasher import Hasher



def create_admin_user(
        admin_user_name: str = 'admin',
        password: str = '1234',
) -> bool:
    """
    初始化超级用户
    insert into  authorization values(0,'admin','xxxxx','name','admin@godzilla.tech','{"role": "System-super-admin"}',datetime('now','localtime'));
    """
    import sqlite3 as sql
    try:
        con = sql.connect(DB_ROOT_PATH)
        con.row_factory = sql.Row
        cur = con.cursor()
        encode_password = Hasher.hash(password)
        sql = "insert into  authorization values(0,'"+admin_user_name+"','"+encode_password+"','name','admin@godzilla.tech','{\"role\": \"System-super-admin\"}',datetime('now','localtime'));"
        print(sql)
        cur.execute(sql)
        con.commit()
        con.close()
        logger.info(f"成功初始化admin账号：{admin_user_name}。password：{password}")
        return True
    except Exception as e:
        logger.error(f"无法初始化admin账号：{DB_ROOT_PATH}。错误信息：{e}")
        return False