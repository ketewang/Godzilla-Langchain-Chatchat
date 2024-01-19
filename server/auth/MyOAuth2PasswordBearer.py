from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from server.cache.cache_service import cache
from configs import logger, log_verbose



class MyOAuth2PasswordBearer(OAuth2PasswordBearer):
    '''
    全局添加OAuth2PasswordBearer依赖，则登录接口会陷入死循环，因为登录接口没有OAuth2PasswordBearer的信息
    重写OAuth2PasswordBearer，对于登录接口，或者指定的接口不读取OAuth2PasswordBearer，直接返回空字符串
    '''

    def __init__(self, tokenUrl: str):
        super().__init__(
            tokenUrl=tokenUrl,
            scheme_name=None,
            scopes=None,
            description=None,
            auto_error=True
        )

    async def __call__(self, request: Request) -> Optional[str]:
        path: str = request.get('path')
        logger.info(f"request path:{path}")
        if path.startswith('/auth/login') | path.startswith('/docs'):
            return ""
        authorization: str = request.headers.get("Authorization")
        logger.info(f"request authorization:{authorization}")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="401 UNAUTHORIZED",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        else:
            #todo 验证
            token = authorization.replace("bearer ","")
            logger.info(f"OAuth2 token:{token}")
            if token and cache.cache.has(token):
                #读cache
                db_data = cache.cache.get(token)
                if path in db_data['my_privilege_urls']:
                    logger.info(f"token {token}有效 db_data:{db_data}")
                else:
                    logger.warn(f"token {token}无效 {path}不可访问 db_data:{db_data}")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"401 UNAUTHORIZED {path}不可访问",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
            else:
                logger.info(f"token {token}不存在cache中")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="401 UNAUTHORIZED bad token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            # 这个是我自己封装的校验token的逻辑，大家可以自己替换成自己的
            # with SessionLocal() as db:
            #     if secret.verify_token(db, token):
            #         logger.info("token验证通过")
            #         response = await call_next(request)
            #         return response
            #     else:
            #         raise auth_error
            #
            # pass

        return param


my_oauth2_scheme = MyOAuth2PasswordBearer(tokenUrl='token')