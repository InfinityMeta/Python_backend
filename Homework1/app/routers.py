from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

import contracts
from storage import STORAGE_ADVERTS, STORAGE_USERS

HTTP_200_OK = status.HTTP_200_OK
HTTP_404_NOT_FOUND = status.HTTP_404_NOT_FOUND
HTTP_400_BAD_REQUEST = status.HTTP_400_BAD_REQUEST
HTTP_403_FORBIDDEN = status.HTTP_403_FORBIDDEN

router = APIRouter()


@router.get("/")
def read_root():
    """
    Returns "Hello world!" message.

    Returns:
        str: Hello world!
    """
    return {"message": "Hello world!"}


@router.get("/users/{user_id}")
async def read_user_info(user_id: int):
    """
    Returns JSON data about user by user ID.

    Args:
        user_id (int): ID of user

    Returns:
        dict: JSON response about user
    """
    if user_id not in STORAGE_USERS:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content=None)
    return JSONResponse(status_code=HTTP_200_OK, content=STORAGE_USERS[user_id].dict())


@router.get("/adverts/{advert_id}/text")
async def read_advert_text(advert_id: int, skip_l: int = 0, skip_r: int = 0):
    """
    Returns JSON response with advert text by advert ID.

    Args:
        advert_id (int): ID of advert
        skip_left (int): number of symbols to skip in advert text from left
        skip_right (int): number of symbols to skip in advert text from right

    Returns:
        dict: JSON response including advert ID, cut advert text
    """

    if advert_id not in STORAGE_ADVERTS:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content=None)

    advert = STORAGE_ADVERTS[advert_id].copy()
    text_len = len(advert.text)
    if skip_l > text_len or skip_r > text_len or skip_l > text_len - skip_r:
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content=None)

    advert.text = advert.text[skip_l:text_len - skip_r]
    return JSONResponse(status_code=HTTP_200_OK, content={"text": advert.text})


@router.put("/adverts/{advert.id}/publish")
async def publish_advert(advert: contracts.Advert):
    """
    Change publication status of advert if moderation is OK.

    Args:
        advert (contracts.Advert): data about advert

    Returns:
        dict: information about advert with updated publication status
    """

    advert_dict = advert.dict()
    if advert.moder_com is None:
        advert_dict.update("published", True)
        return JSONResponse(status_code=HTTP_200_OK, content=advert_dict)
    return JSONResponse(status_code=HTTP_403_FORBIDDEN, content=None)
