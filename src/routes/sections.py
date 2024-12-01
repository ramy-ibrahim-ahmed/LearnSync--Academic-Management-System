import fastapi

router = fastapi.APIRouter()


@router.get("/sections/{id}")
async def read_section():
    pass


@router.get("/sections/{id}/content-blocks")
async def read_section_content_blocks():
    pass


@router.get("/content-blocks/{id}")
async def read_content_block():
    pass
