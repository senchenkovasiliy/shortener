import logging
from typing import Any
from fastapi import HTTPException, Depends, APIRouter, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from redis import exceptions as dbExceptions  
from backend.app.api.dependencies import get_shortener
from backend.app.config import settings
from backend.app.core.shortener import Shortener
from backend.app.models.url import UrlIn, UrlOut
from backend.app.utils import validate_url

# defaulrt logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# routing
router = APIRouter()

# jinja templates
templates = Jinja2Templates(directory="frontend/templates")


# Show in display error
def display_error_response(request: Request, msg: Any, status_code: int) -> Any:
    return templates.TemplateResponse(f"errors/{status_code}.html",
                                       {"request": request, "detail": [{"msg": msg}]},
                                       status_code=status_code)


# parsing a request body
@router.post("/create", 
             status_code=status.HTTP_201_CREATED, 
                        response_model=UrlOut)
def create_short_url(body: UrlIn, shortener: Shortener = Depends(get_shortener)) -> Any:
    # start condition validated
    try:
        validate_url(body.url)
    except ValueError as value_err:
        logger.error(value_err)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=[{"msg": str(value_err)}])
    # star5t shoring
    try:
        short_key = shortener.long_to_short(body.url)
    except dbExceptions.ConnectionError as conn_err:
        logger.error(conn_err)
        user_msg = "Database Connection couldn't be established. Try again later!"
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=[{"msg": user_msg}])
    except KeyError as key_err:
        logger.error(key_err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(key_err))
    
    # formation fu8ll short url
    short_url = f"{settings.MINI_URL}{short_key}"
    logger.info(f"Generated short url: {short_url}")
    url_out = {"short_url": short_url, "url": body.url}
    return url_out


# redirction
@router.get("/{short_key}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
def redirect(request: Request, short_key: str, shortener: Shortener = Depends(get_shortener)) -> Any:
    # trying to shorting
    try:
        long_url = shortener.short_to_long(short_key)
    except dbExceptions.ConnectionError as conn_err:
        logger.error(conn_err)
        user_msg = "Database Connection couldn't be established. Try again later!"
        return display_error_response(request, user_msg, status.HTTP_503_SERVICE_UNAVAILABLE)
    except KeyError as key_err_msg:
        logger.error(key_err_msg)
        return display_error_response(request, key_err_msg, status.HTTP_404_NOT_FOUND)
    
    # redirection
    logger.info(f"Generated long url: {long_url}")
    return RedirectResponse(url=long_url)
