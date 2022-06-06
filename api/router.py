from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from api.shortener import Shortener
from api.schema import Response, Status

router = APIRouter()
shortener = Shortener()


@router.post("/shorten")
async def shorten(url: str):
    """
    Shorten a url
    """
    if data := shortener.shorten(long_url=url):
        return Response(
            status=Status.OK,
            code=200,
            message="Url shortened successfully",
            data=data
        )

    return Response(
        status=Status.ERROR,
        code=400,
        message="Url could not be shortened"
    )


@router.get("/{hash_value}")
async def expand(hash_value: str):
    """
    Redirect to the original url
    """
    if long_url := shortener.expand(hash_value):
        return RedirectResponse(long_url)

    return Response(
        status=Status.ERROR,
        code=404,
        message="Url could not be expanded"
    )


@router.get("/stats/{hash_value}")
async def stats(hash_value: str):
    """
    Get analytics for a url
    """
    if data := shortener.get_url(hash_value):
        return Response(
            status=Status.OK,
            code=200,
            message="Url analytics retrieved successfully",
            data=data
        )

    return Response(
        status=Status.ERROR,
        code=404,
        message="Url could not be found"
    )
