from typing import Optional

from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App
from fastapi import status, APIRouter, Query, Request, Response
from fastapi.responses import RedirectResponse
import jwt

from config import settings

from ..utils.strings import generate_oauth2_state


# --- init OAuth2 app for Auth0
oauth = OAuth()
oauth.register(
    name="auth0",
    audience=settings.AUTH0_AUDIENCE,
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    authorize_prompt=None,
    authorize_url=f"https://{settings.AUTH0_DOMAIN}/authorize",
    authorize_token_url=f"https://{settings.AUTH0_DOMAIN}/authorize",
    token_endpoint=f"https://{settings.AUTH0_DOMAIN}/oauth/token",
    client_kwargs={"scope": "openid profile email"},
    jwks_uri=f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json",
)
auth0: StarletteOAuth2App = oauth.auth0


router = APIRouter()


@router.get("/", response_class=RedirectResponse)
async def oauth2_login(request: Request):
    state = generate_oauth2_state()
    request.session["state"] = state
    return await auth0.authorize_redirect(
        request,
        redirect_uri=settings.AUTH0_CALLBACK_URL,
        state=state,
    )


@router.get("/callback")
async def oauth2_callback(
    request: Request, state: Optional[str] = Query(), error: Optional[str] = Query(None)
):
    """Send request to Auth0 to generate access token"""
    if error:
        return RedirectResponse(url="/", status_code=status.HTTP_200_OK)

    try:
        assert state and state == request.session.get("state", "")
    except AssertionError:
        return Response("Invalid state", status_code=status.HTTP_400_BAD_REQUEST)

    response = await auth0.authorize_access_token(request)
    user_info = response["userinfo"]
    id_token_decoded = jwt.decode(response["id_token"], options={"verify_signature": False})
    return {"it": "works!"}
