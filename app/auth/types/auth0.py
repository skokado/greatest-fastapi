from typing import Literal, Optional, TypedDict


class Auth0AccessTokenResponse(TypedDict):
    class Auth0UserInfo(TypedDict):
        sub: str
        aud: str
        iss: str
        iat: int
        exp: int  # expiry time of id token
        email: Optional[str]
        email_verified: bool
        nickname: Optional[str]
        created_at: str
        updated_at: str
        is_active: bool

    access_token: str
    token_type: Literal["Bearer"]
    id_token: str
    scope: str
    expires_in: int  # expiry time in seconds of access token
    expires_at: int  # expiry time in seconds since epoch
    userinfo: Auth0UserInfo
