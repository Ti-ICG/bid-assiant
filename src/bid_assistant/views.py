import os
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from thcloud.minio_db import bucket
from thcloud.config import settings
from thcloud.dependencies import CommonQueryParams, get_db
from thcloud.models import Bid_catalog
from thcloud.schemas import (
    BidCatalogContentSchemas,
    BidCatalogSchemas,
    CreateBidCatalog,
    CreateBidCatalogContent,
    CreateRequirementAnalysis,
    CreateRequirementAnalysisDetail,
    CreateResponseIndicator,
    CreateResponseIndicatorDetail,
    CreateScheme,
    CreateSystemFramework,
    RequirementAnalysisDetailSchemas,
    RequirementAnalysisSchemas,
    ResponseIndicatorDetailSchemas,
    ResponseIndicatorSchemas,
    SchemeSchemas,
    SystemFrameworkSchemas,
    UpdateBidCatalog,
    UpdateBidCatalogContent,
    UpdateRequirementAnalysis,
    UpdateRequirementAnalysisDetail,
    UpdateResponseIndicator,
    UpdateResponseIndicatorDetail,
    UpdateScheme,
    UpdateSystemFramework,
)
from thcloud.services import (
    BidCatalogContentService,
    BidCatalogService,
    RequirementAnalysisDetailService,
    RequirementAnalysisService,
    ResponseIndicatorDetailService,
    ResponseIndicatorService,
    SchemeService,
    SystemFrameworkService,
)

router = APIRouter()

# ----------------------------------------scheme------------------------------------
scheme_service = SchemeService()


@router.get("/schemes", tags=["Scheme"])
def get(session: Session = Depends(get_db), commons: CommonQueryParams = Depends()):
    return scheme_service.get(session, offset=commons.offset, limit=commons.limit)


@router.get("/schemes/{pk}", tags=["Scheme"])
def get_by_id(pk: int, session: Session = Depends(get_db)):
    return scheme_service.get_by_id(session, pk)


# @router.post("/schemes", response_model=SchemeSchemas, tags=["Scheme"])
# def create(
#     obj_in: CreateScheme,
#     session: Session = Depends(get_db),
# ):

#     return scheme_service.create(session, obj_in)


# 上传文件并存储在Minio
@router.post("/schemes", response_model=SchemeSchemas, tags=["Scheme"])
async def create(
    scheme_name: str,
    catalog: UploadFile = File(...),
    bidfile: UploadFile = File(...),
    session: Session = Depends(get_db),
):

    contents1 = await catalog.read()
    contents2 = await bidfile.read()
    # 使用with open打开目标文件
    with open("file/catalog" + catalog.filename, "wb") as f:
        # 2.3 将获取的fileb文件内容，写入到新文件中
        f.write(contents1)

    with open("file/bid" + bidfile.filename, "wb") as f1:
        # 2.3 将获取的fileb文件内容，写入到新文件中
        f1.write(contents2)

    bucket.upload_file_to_bucket(
        "bidcatalog", catalog.filename, "file/catalog" + catalog.filename
    )

    bucket.upload_file_to_bucket(
        "bidfile", bidfile.filename, "file/bid" + bidfile.filename
    )
    url = "http://" + settings.MINIO.ADDRESS
    createScheme = CreateScheme(
        scheme_name=scheme_name,
        catalog_url=url + "/catalog/" + catalog.filename,
        file_path_url=url + "/bidfile/" + bidfile.filename,
    )

    return scheme_service.create(session, createScheme)


# 从Minio中获取文件
@router.get("/schemes/download", tags=["Scheme"])
def download(bucket_name: str, filename: str):
    response = bucket.get_file_from_bucket(bucket_name, filename)
    return response


@router.patch("/schemes/{pk}", response_model=SchemeSchemas, tags=["Scheme"])
def patch(pk: int, obj_in: UpdateScheme, session: Session = Depends(get_db)):
    return scheme_service.patch(session, pk, obj_in)


@router.delete("/schemes/{pk}", tags=["Scheme"])
def delete(pk: int, session: Session = Depends(get_db)):
    return scheme_service.delete(session, pk)


# ----------------------------------------requirement_analysis------------------------------------------------------------
requirement_analysis_service = RequirementAnalysisService()


@router.get("/requirement_analysis", tags=["requirement_analysis"])
def get(session: Session = Depends(get_db), commons: CommonQueryParams = Depends()):
    return requirement_analysis_service.get(
        session, offset=commons.offset, limit=commons.limit
    )


@router.get("/requirement_analysis/{pk}", tags=["requirement_analysis"])
def get_by_id(pk: int, session: Session = Depends(get_db)):
    return requirement_analysis_service.get_by_id(session, pk)


@router.post(
    "/requirement_analysis",
    response_model=RequirementAnalysisSchemas,
    tags=["requirement_analysis"],
)
def create(
    obj_in: CreateRequirementAnalysis,
    session: Session = Depends(get_db),
):
    return requirement_analysis_service.create(session, obj_in)


@router.patch(
    "/requirement_analysis/{pk}",
    response_model=RequirementAnalysisSchemas,
    tags=["requirement_analysis"],
)
def patch(
    pk: int, obj_in: UpdateRequirementAnalysis, session: Session = Depends(get_db)
):
    return requirement_analysis_service.patch(session, pk, obj_in)


@router.delete("/requirement_analysis/{pk}", tags=["requirement_analysis"])
def delete(pk: int, session: Session = Depends(get_db)):
    return requirement_analysis_service.delete(session, pk)


##----------------------------------------requirement_analysis_detail------------------------------------------------------------
requirement_analysis_detail_service = RequirementAnalysisDetailService()


@router.get("/requirement_analysis_detail", tags=["requirement_analysis_detail"])
def get(session: Session = Depends(get_db), commons: CommonQueryParams = Depends()):
    return requirement_analysis_detail_service.get(
        session, offset=commons.offset, limit=commons.limit
    )


@router.get("/requirement_analysis_detail/{pk}", tags=["requirement_analysis_detail"])
def get_by_id(pk: int, session: Session = Depends(get_db)):
    return requirement_analysis_detail_service.get_by_id(session, pk)


@router.post(
    "/requirement_analysis_detail",
    response_model=RequirementAnalysisDetailSchemas,
    tags=["requirement_analysis_detail"],
)
def create(
    obj_in: CreateRequirementAnalysisDetail,
    session: Session = Depends(get_db),
):
    return requirement_analysis_detail_service.create(session, obj_in)


@router.patch(
    "/requirement_analysis_detail/{pk}",
    response_model=RequirementAnalysisDetailSchemas,
    tags=["requirement_analysis_detail"],
)
def patch(
    pk: int, obj_in: UpdateRequirementAnalysisDetail, session: Session = Depends(get_db)
):
    return requirement_analysis_detail_service.patch(session, pk, obj_in)


@router.delete(
    "/requirement_analysis_detail/{pk}", tags=["requirement_analysis_detail"]
)
def delete(pk: int, session: Session = Depends(get_db)):
    return requirement_analysis_detail_service.delete(session, pk)


# ----------------------------------------system_framework-------------------------
system_framework_service = SystemFrameworkService()


@router.get("/system_framework", tags=["system_framework"])
def get(session: Session = Depends(get_db), commons: CommonQueryParams = Depends()):
    return system_framework_service.get(
        session, offset=commons.offset, limit=commons.limit
    )


@router.get("/system_framework/{pk}", tags=["system_framework"])
def get_by_id(pk: int, session: Session = Depends(get_db)):
    return system_framework_service.get_by_id(session, pk)


@router.post(
    "/system_framework",
    response_model=SystemFrameworkSchemas,
    tags=["system_framework"],
)
def create(
    obj_in: CreateSystemFramework,
    session: Session = Depends(get_db),
):
    return system_framework_service.create(session, obj_in)


@router.patch(
    "/system_framework/{pk}",
    response_model=SystemFrameworkSchemas,
    tags=["system_framework"],
)
def patch(pk: int, obj_in: UpdateSystemFramework, session: Session = Depends(get_db)):
    return system_framework_service.patch(session, pk, obj_in)


@router.delete("/system_framework/{pk}", tags=["system_framework"])
def delete(pk: int, session: Session = Depends(get_db)):
    return system_framework_service.delete(session, pk)


# ----------------------------------------system_framework-----------------------------
# system_framework_detail_service = SystemFrameworkDetailService()
# @router.get('/system_framework_detail', tags=['system_framework_detail'])
# def get(
#         session: Session = Depends(get_db),
#         commons: CommonQueryParams = Depends()
# ):
#     return system_framework_detail_service.get(session, offset=commons.offset, limit=commons.limit)

# @router.get('/system_framework_detail/{pk}', tags=['system_framework_detail'])
# def get_by_id(
#         pk: int,
#         session: Session = Depends(get_db)
# ):
#     return system_framework_detail_service.get_by_id(session, pk)

# @router.post('/system_framework_detail', response_model=SystemFrameworkDetailSchemas,
# tags=['system_framework_detail'])
# def create(
#         obj_in: CreateSystemFrameworkDetail,
#         session: Session = Depends(get_db),
# ):
#     return system_framework_detail_service.create(session, obj_in)

# @router.patch('/system_framework_detail/{pk}', response_model=SystemFrameworkDetailSchemas,
# tags=['system_framework_detail'])
# def patch(
#         pk: int,
#         obj_in: UpdateSystemFrameworkDetail,
#         session: Session = Depends(get_db)
# ):
#     return system_framework_detail_service.patch(session, pk, obj_in)

# @router.delete('/system_framework_detail/{pk}',tags=['system_framework_detail'])
# def delete(
#         pk: int,
#         session: Session = Depends(get_db)
# ):
#     return system_framework_detail_service.delete(session, pk)


# ----------------------------------------Response_indicator------------------------------------
response_indicator_service = ResponseIndicatorService()


@router.get("/response_indicator", tags=["response_indicator"])
def get(session: Session = Depends(get_db), commons: CommonQueryParams = Depends()):
    return response_indicator_service.get(
        session, offset=commons.offset, limit=commons.limit
    )


@router.get("/response_indicator/{pk}", tags=["response_indicator"])
def get_by_id(pk: int, session: Session = Depends(get_db)):
    return response_indicator_service.get_by_id(session, pk)


@router.post(
    "/response_indicator",
    response_model=ResponseIndicatorSchemas,
    tags=["response_indicator"],
)
def create(
    obj_in: CreateResponseIndicator,
    session: Session = Depends(get_db),
):
    return response_indicator_service.create(session, obj_in)


@router.patch(
    "/response_indicator/{pk}",
    response_model=ResponseIndicatorSchemas,
    tags=["response_indicator"],
)
def patch(pk: int, obj_in: UpdateResponseIndicator, session: Session = Depends(get_db)):
    return response_indicator_service.patch(session, pk, obj_in)


@router.delete("/response_indicator/{pk}", tags=["response_indicator"])
def delete(pk: int, session: Session = Depends(get_db)):
    return response_indicator_service.delete(session, pk)


##----------------------------------------Response_indicator_detail--------------------------------
response_indicator_detail_service = ResponseIndicatorDetailService()


@router.get("/response_indicator_detail", tags=["response_indicator_detail"])
def get(session: Session = Depends(get_db), commons: CommonQueryParams = Depends()):
    return response_indicator_detail_service.get(
        session, offset=commons.offset, limit=commons.limit
    )


@router.get("/response_indicator_detail/{pk}", tags=["response_indicator_detail"])
def get_by_id(pk: int, session: Session = Depends(get_db)):
    return response_indicator_detail_service.get_by_id(session, pk)


@router.post(
    "/response_indicator_detail",
    response_model=ResponseIndicatorDetailSchemas,
    tags=["response_indicator_detail"],
)
def create(
    obj_in: CreateResponseIndicatorDetail,
    session: Session = Depends(get_db),
):
    return response_indicator_detail_service.create(session, obj_in)


@router.patch(
    "/response_indicator_detail/{pk}",
    response_model=ResponseIndicatorDetailSchemas,
    tags=["response_indicator_detail"],
)
def patch(
    pk: int, obj_in: UpdateResponseIndicatorDetail, session: Session = Depends(get_db)
):
    return response_indicator_detail_service.patch(session, pk, obj_in)


@router.delete("/response_indicator_detail/{pk}", tags=["response_indicator_detail"])
def delete(pk: int, session: Session = Depends(get_db)):
    return response_indicator_detail_service.delete(session, pk)


##----------------------------------------Bid_Catalog---------------------------------
bid_catalog_service = BidCatalogService()


@router.get("/bid_catalog", tags=["bid_catalog"])
def get(session: Session = Depends(get_db), commons: CommonQueryParams = Depends()):
    return bid_catalog_service.get(session, offset=commons.offset, limit=commons.limit)


@router.get("/bid_catalog/{pk}", tags=["bid_catalog"])
def get_by_id(pk: str, session: Session = Depends(get_db)):
    return bid_catalog_service.get_by_id(session, pk)


@router.post("/bid_catalog", response_model=BidCatalogSchemas, tags=["bid_catalog"])
def create(
    obj_in: CreateBidCatalog,
    session: Session = Depends(get_db),
):
    return bid_catalog_service.create(session, obj_in)


@router.patch(
    "/bid_catalog/{pk}", response_model=BidCatalogSchemas, tags=["bid_catalog"]
)
def patch(pk: str, obj_in: UpdateBidCatalog, session: Session = Depends(get_db)):
    return bid_catalog_service.patch(session, pk, obj_in)


# 父节点删除，子节点一并删除
@router.delete("/bid_catalog/{pk}", tags=["bid_catalog"])
def delete(pk: str, session: Session = Depends(get_db)):
    main_catalog = (
        session.query(Bid_catalog).filter(Bid_catalog.id.like(f"{pk}%")).all()
    )
    if main_catalog is None:
        raise HTTPException(status_code=404, detail="Bid_catalog not found")
    for catalog in main_catalog:
        session.delete(catalog)
    session.commit()


#     return bid_catalog_service.delete(session, pk)

# ----------------------------------------Bid_Catalog_content-----------------
bid_catalog_content_service = BidCatalogContentService()


@router.get("/bid_catalog_content", tags=["bid_catalog_content"])
def get(session: Session = Depends(get_db), commons: CommonQueryParams = Depends()):
    return bid_catalog_content_service.get(
        session, offset=commons.offset, limit=commons.limit
    )


@router.get("/bid_catalog_content/{pk}", tags=["bid_catalog_content"])
def get_by_id(pk: int, session: Session = Depends(get_db)):
    return bid_catalog_content_service.get_by_id(session, pk)


@router.post(
    "/bid_catalog_content",
    response_model=BidCatalogContentSchemas,
    tags=["bid_catalog_content"],
)
def create(
    obj_in: CreateBidCatalogContent,
    session: Session = Depends(get_db),
):
    return bid_catalog_content_service.create(session, obj_in)


@router.patch(
    "/bid_catalog_content/{pk}",
    response_model=BidCatalogContentSchemas,
    tags=["bid_catalog_content"],
)
def patch(pk: int, obj_in: UpdateBidCatalogContent, session: Session = Depends(get_db)):
    return bid_catalog_content_service.patch(session, pk, obj_in)


@router.delete("/bid_catalog_content/{pk}", tags=["bid_catalog_content"])
def delete(pk: int, session: Session = Depends(get_db)):
    return bid_catalog_content_service.delete(session, pk)
