import json
import logging
import os

import httpx
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from preprocessing_docx import preprocessing_lib
from thcloud.config import settings
from thcloud.dependencies import CommonQueryParams, get_db
from thcloud.minio_db import bucket
from thcloud.models import Bid_catalog, Catalog_prompt, Bid_catalog_content
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
    CreateSystemFrameworkDetail,
    DetailScheme,
    DownloadScheme,
    RequirementAnalysisDetailSchemas,
    RequirementAnalysisSchemas,
    ResponseIndicatorDetailSchemas,
    ResponseIndicatorSchemas,
    SchemeSchemas,
    SystemFrameworkDetailSchemas,
    SystemFrameworkSchemas,
    UpdateBidCatalog,
    UpdateBidCatalogContent,
    UpdateRequirementAnalysis,
    UpdateRequirementAnalysisDetail,
    UpdateResponseIndicator,
    UpdateResponseIndicatorDetail,
    UpdateScheme,
    UpdateSystemFramework,
    UpdateSystemFrameworkDetail,
    Chat, CatalogPromptSchemas, CreateCatalogPrompt, UpdateCatalogPrompt,
)
from thcloud.services import (
    BidCatalogContentService,
    BidCatalogService,
    RequirementAnalysisDetailService,
    RequirementAnalysisService,
    ResponseIndicatorDetailService,
    ResponseIndicatorService,
    SchemeService,
    SystemFrameworkDetailService,
    SystemFrameworkService, CatalogPromptService,
)

router = APIRouter()

# ----------------------------------------scheme------------------------------------
scheme_service = SchemeService()


@router.get("/schemes", tags=["Scheme"])
def get(session: Session = Depends(get_db), commons: CommonQueryParams = Depends()):
    return scheme_service.get(session, offset=commons.offset, limit=commons.limit)


@router.get("/schemes/{pk}", response_model=SchemeSchemas, tags=["Scheme"])
def get_by_id(pk: int, session: Session = Depends(get_db)):
    return scheme_service.get_by_id(session, pk)


@router.get("/schemes/detail/{pk}", response_model=DetailScheme, tags=["Scheme"])
def get_detail(pk: int, session: Session = Depends(get_db)):
    return scheme_service.get_detail(session, pk)


# 上传文件并存储在Minio
@router.post("/schemes", response_model=SchemeSchemas, tags=["Scheme"])
async def create(
    scheme_name: str,
    catalog: UploadFile = File(...),
    bidfile: UploadFile = File(...),
    session: Session = Depends(get_db),
):
    # 读取文件  返回bytes
    catalog_contents = await catalog.read()
    bidfile_contents = await bidfile.read()
    bucket.upload_object("bidcatalog", catalog.filename, catalog_contents)
    bucket.upload_object("bidfile", bidfile.filename, bidfile_contents)
    url = "http://" + settings.MINIO.ADDRESS
    createScheme = CreateScheme(
        scheme_name=scheme_name,
        catalog_url=url + "/catalog/" + catalog.filename,
        file_path_url=url + "/bidfile/" + bidfile.filename,
    )

    scheme = scheme_service.create(session, createScheme)

    # 调用需求解析接口
    confidence = 0.65
    match_text = "技术内容"
    bid_path = f".tmp/{scheme.id}/{bidfile.filename}"
    os.makedirs(os.path.dirname(bid_path), exist_ok=True)
    with open(bid_path, "wb") as file:
        file.write(bidfile_contents)
    out_path = f".tmp/{scheme.id}/out/"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    preprocessing_lib.preprocess_docx(bid_path, out_path, confidence, match_text)

    kb_name = get_kb_name(scheme.id)
    kb_create(kb_name)
    await kb_upload_docs(kb_name, out_path)

    return scheme


# 从Minio中获取文件
@router.get("/schemes/download/", response_model=DownloadScheme, tags=["Scheme"])
def download(bucket_name: str, filename: str):
    # 获取下载url
    url = bucket.presigned_get_file(bucket_name, filename)
    return {"url": url}


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


@router.get(
    "/requirement_analysis/{pk}",
    response_model=RequirementAnalysisSchemas,
    tags=["requirement_analysis"],
)
def get_by_id(pk: int, session: Session = Depends(get_db)):
    return requirement_analysis_service.get_by_id(session, pk)


@router.get(
    "/scheme/requirement_analysis/{scheme_pk}",
    response_model=RequirementAnalysisSchemas,
    tags=["scheme_requirement_analysis"],
)
def get_by_scheme_id(scheme_pk: int, session: Session = Depends(get_db)):
    return requirement_analysis_service.get_by_scheme_id(session, scheme_pk)


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

@router.patch(
    "/scheme/requirement_analysis/{scheme_pk}",
    response_model=RequirementAnalysisSchemas,
    tags=["scheme_requirement_analysis"],
)
def patch_by_scheme_id(
    scheme_pk: int,
    obj_in: UpdateRequirementAnalysis,
    session: Session = Depends(get_db),
):
    return requirement_analysis_service.patch_by_scheme_id(session, scheme_pk, obj_in)


@router.delete("/requirement_analysis/{pk}", tags=["requirement_analysis"])
def delete(pk: int, session: Session = Depends(get_db)):
    return requirement_analysis_service.delete(session, pk)


@router.delete(
    "/scheme/requirement_analysis/{scheme_pk}", tags=["scheme_requirement_analysis"]
)
def delete_by_scheme_id(scheme_pk: int, session: Session = Depends(get_db)):
    return requirement_analysis_service.delete_by_scheme_id(session, scheme_pk)


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


@router.get(
    "/system_framework/{pk}",
    response_model=SystemFrameworkSchemas,
    tags=["system_framework"],
)
def get_by_id(pk: int, session: Session = Depends(get_db)):
    return system_framework_service.get_by_id(session, pk)

@router.get(
    "/scheme/system_framework/{scheme_pk}",
    response_model=SystemFrameworkSchemas,
    tags=["scheme_system_framework"],
)
def get_by_scheme_id(scheme_pk: int, session: Session = Depends(get_db)):
    return system_framework_service.get_by_scheme_id(session, scheme_pk)


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


@router.patch(
    "/scheme/system_framework/{scheme_pk}",
    response_model=SystemFrameworkSchemas,
    tags=["scheme_system_framework"],
)
def patch_by_scheme_id(
    scheme_pk: int, obj_in: UpdateSystemFramework, session: Session = Depends(get_db)
):
    return system_framework_service.patch_by_scheme_id(session, scheme_pk, obj_in)

@router.delete("/system_framework/{pk}", tags=["system_framework"])
def delete(pk: int, session: Session = Depends(get_db)):
    return system_framework_service.delete(session, pk)


@router.delete("/scheme/system_framework/{scheme_id}", tags=["scheme_system_framework"])
def delete_by_scheme_id(scheme_id: int, session: Session = Depends(get_db)):
    return system_framework_service.delete_by_scheme_id(session, scheme_id)


# ----------------------------------------system_framework_detail-----------------------------
system_framework_detail_service = SystemFrameworkDetailService()
@router.get('/system_framework_detail', tags=['system_framework_detail'])
def get(
        session: Session = Depends(get_db),
        commons: CommonQueryParams = Depends()
):
    return system_framework_detail_service.get(session, offset=commons.offset, limit=commons.limit)

@router.get('/system_framework_detail/{pk}', tags=['system_framework_detail'])
def get_by_id(
        pk: int,
        session: Session = Depends(get_db)
):
    return system_framework_detail_service.get_by_id(session, pk)

@router.post('/system_framework_detail', response_model=SystemFrameworkDetailSchemas,
tags=['system_framework_detail'])
def create(
        obj_in: CreateSystemFrameworkDetail,
        session: Session = Depends(get_db),
):
    return system_framework_detail_service.create(session, obj_in)

@router.patch('/system_framework_detail/{pk}', response_model=SystemFrameworkDetailSchemas,
tags=['system_framework_detail'])
def patch(
        pk: int,
        obj_in: UpdateSystemFrameworkDetail,
        session: Session = Depends(get_db)
):
    return system_framework_detail_service.patch(session, pk, obj_in)

@router.delete('/system_framework_detail/{pk}',tags=['system_framework_detail'])
def delete(
        pk: int,
        session: Session = Depends(get_db)
):
    return system_framework_detail_service.delete(session, pk)


# ----------------------------------------Response_indicator------------------------------------
response_indicator_service = ResponseIndicatorService()


@router.get("/response_indicator", tags=["response_indicator"])
def get(session: Session = Depends(get_db), commons: CommonQueryParams = Depends()):
    return response_indicator_service.get(
        session, offset=commons.offset, limit=commons.limit
    )


@router.get(
    "/response_indicator/{pk}",
    response_model=ResponseIndicatorSchemas,
    tags=["response_indicator"],
)
def get_by_id(pk: int, session: Session = Depends(get_db)):
    return response_indicator_service.get_by_id(session, pk)


@router.get(
    "/scheme/response_indicator/{scheme_pk}",
    response_model=ResponseIndicatorSchemas,
    tags=["scheme_response_indicator"],
)
def get_by_scheme_id(scheme_pk: int, session: Session = Depends(get_db)):
    return response_indicator_service.get_by_scheme_id(session, scheme_pk)


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


@router.patch(
    "/scheme/response_indicator/{scheme_pk}",
    response_model=ResponseIndicatorSchemas,
    tags=["scheme_response_indicator"],
)
def patch_by_scheme_id(
    scheme_pk: int, obj_in: UpdateResponseIndicator, session: Session = Depends(get_db)
):
    return response_indicator_service.patch_by_scheme_id(session, scheme_pk, obj_in)


@router.delete("/response_indicator/{pk}", tags=["response_indicator"])
def delete(pk: int, session: Session = Depends(get_db)):
    return response_indicator_service.delete(session, pk)


@router.delete(
    "/scheme/response_indicator/{scheme_pk}", tags=["scheme_response_indicator"]
)
def delete_by_scheme_id(scheme_pk: int, session: Session = Depends(get_db)):
    return response_indicator_service.delete_by_scheme_id(session, scheme_pk)


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


@router.get("/bid_catalog/{pk}", tags=["bid_catalog"])
def get_all_by_id(pk: int, session: Session = Depends(get_db)):
    result = bid_catalog_service.get_all_by_id(session, pk)
    for i in result:
        i.children = (
            session.query(Bid_catalog).filter(Bid_catalog.parent_id == i.id).all()
        )
    data = []
    for i in result:
        if i.level == 1:
            data.append(i)
    return data


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


@router.get(
    "/bid_catalog_content/{pk}",
    response_model=BidCatalogContentSchemas,
    tags=["bid_catalog_content"],
)
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


# ----------------------------------------Catalog_prompt-----------------
catalog_prompt_Service = CatalogPromptService()


@router.get("/catalog_prompt", tags=["catalog_prompt"])
def get(session: Session = Depends(get_db), commons: CommonQueryParams = Depends()):
    return catalog_prompt_Service.get(
        session, offset=commons.offset, limit=commons.limit
    )


@router.get(
    "/catalog_prompt/{pk}",
    response_model=CatalogPromptSchemas,
    tags=["catalog_prompt"],
)
def get_by_id(pk: int, session: Session = Depends(get_db)):
    return catalog_prompt_Service.get_by_id(session, pk)


@router.post(
    "/catalog_prompt",
    response_model=CatalogPromptSchemas,
    tags=["catalog_prompt"],
)
def create(
    obj_in: CreateCatalogPrompt,
    session: Session = Depends(get_db),
):
    return catalog_prompt_Service.create(session, obj_in)


@router.patch(
    "/catalog_prompt/{pk}",
    response_model=CatalogPromptSchemas,
    tags=["catalog_prompt"],
)
def patch(pk: int, obj_in: UpdateCatalogPrompt, session: Session = Depends(get_db)):
    return catalog_prompt_Service.patch(session, pk, obj_in)


@router.delete("/catalog_prompt/{pk}", tags=["catalog_prompt"])
def delete(pk: int, session: Session = Depends(get_db)):
    return catalog_prompt_Service.delete(session, pk)


# ----------------------------------------Chat-----------------
CHAT_HOST = "http://192.168.200.17:7861"
KB_CREATE_API = CHAT_HOST + "/knowledge_base/create_knowledge_base"
KB_UPLOAD_DOCS_API = CHAT_HOST + "/knowledge_base/upload_docs"
KB_CHAT_API = CHAT_HOST + "/chat/kb_chat"
CHAT_CHAT_API = CHAT_HOST + "/chat/chat/completions"


def get_kb_name(scheme_id: int) -> str:
    return f"bid-assistant/{scheme_id}"


def kb_create(kb_name: str):
    data = {
        "knowledge_base_name": kb_name,
        "vector_store_type": "faiss",
        "kb_info": "",
        "embed_model": "bge-large-zh-v1.5"
    }
    with httpx.Client() as client:
        response = client.post(KB_CREATE_API, json=data)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Create knowledge base failed.")


async def kb_upload_docs(kb_name: str, docs_path: str):
    data = {
        "knowledge_base_name": kb_name,
        "override": True,
        "to_vector_store": True,
        "chunk_size": 750,
        "chunk_overlap": 150,
        "zh_title_enhance": False,
        "docs": "",
        "not_refresh_vs_cache": False
    }
    try:
        async with httpx.AsyncClient() as client:
            files_to_upload = []
            for filename in os.listdir(docs_path):
                file_path = os.path.join(docs_path, filename)
                if os.path.isfile(file_path):
                    files_to_upload.append(("files", open(file_path, "rb")))

            if files_to_upload:
                response = await client.post(KB_UPLOAD_DOCS_API, data=data, files=files_to_upload)
                for _, file in files_to_upload:
                    file.close()

                if response.status_code == 200:
                    failed_files = response.json()['data'].get('failed_files', {})
                    if failed_files:
                        logging.error(f"以下文件上传失败：{failed_files}")
                        raise HTTPException(status_code=500, detail="Upload docs to knowledge base failed.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Create knowledge base failed.")


@router.post("/ai", tags=["ai"])
async def ai(req: Chat, session: Session = Depends(get_db)):
    actions = session.query(Catalog_prompt).filter_by(title=req.title).order_by(Catalog_prompt.sequence).all()
    if actions is None:
        raise HTTPException(status_code=500, detail="Param query error.")
    previous = ""
    for index, action in enumerate(actions):
        if index == len(actions) - 1:
            url = chat_url(action)
            data = chat_data(req, action, True, previous)
            return stream_chat(url, data)
        else:
            if action.type == "DB":
                previous = chat_prompt(req, action, previous)
            else:
                url = chat_url(action)
                data = chat_data(req, action, False, previous)
                previous = direct_chat(url, data)


@router.post("/direct-chat-test", tags=["ai"])
async def direct_chat_test(req: Chat, session: Session = Depends(get_db)):
    actions = session.query(Catalog_prompt).filter_by(title=req.title).order_by(Catalog_prompt.sequence).all()
    if actions is None:
        raise HTTPException(status_code=500, detail="Param query error.")
    previous = ""
    for index, action in enumerate(actions):
        if index == len(actions) - 1:
            url = chat_url(action)
            data = chat_data(req, action, False, previous)
            return direct_chat(url, data)


def chat_url(action: Catalog_prompt) -> str:
    if action.type == "RAG":
        return KB_CHAT_API
    elif action.type == "CTCT":
        return CHAT_CHAT_API
    return ""


def chat_prompt(chat: Chat, action: Catalog_prompt, previous: str, session: Session = Depends(get_db)) -> str:
    prompt = action.prompt
    if "{title}" in prompt:
        prompt = prompt.replace("{title}", chat.title)
    if "{previous}" in prompt:
        prompt = prompt.replace("{previous}", previous)
    if "{tech_analyze}" in prompt:
        requirement_analysis = requirement_analysis_service.get_by_id(session, chat.scheme_id)
        prompt = prompt.replace("{tech_analyze}", requirement_analysis.requirement_content)
    if "{系统接口方案}" in prompt:
        catalog_content = session.query(Bid_catalog_content).filter_by(catalog_id="14", scheme_id=chat.scheme_id).first()
        prompt = prompt.replace("{系统接口方案}", catalog_content.content)
    return prompt


def chat_data(chat: Chat, action: Catalog_prompt, stream: bool, previous: str) -> dict:
    prompt = chat_prompt(chat, action, previous)
    data = {}
    if action.type == "RAG":
        data = {
            "query": prompt,
            "mode": "local_kb",
            "kb_name": get_kb_name(chat.scheme_id),
            "top_k": 3,
            "score_threshold": 1.79,
            "history": [],
            "stream": stream,
            "model": "glm-4-9b-chat-1m",
            "temperature": 0.7,
            "max_tokens": 30000,
            "prompt_name": "default",
            "return_direct": False
        }
    elif action.type == "CTCT":
        data = {
            "messages": [
                {
                    "content": prompt,
                    "role": "system",
                    "name": "string",
                }
            ],
            "model": "glm-4-9b-chat-1m",
            "max_tokens": 2048,
            "n": 0,
            "stream": stream,
            "temperature": 0.7,
        }
    return data


def stream_chat(url: str, data: dict) -> StreamingResponse:
    async def generate():
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", url, json=data) as stream:
                async for chunk in stream.aiter_text():
                    yield chunk
    return StreamingResponse(generate(), media_type="text/event-stream")


def direct_chat(url: str, data: dict) -> str:
    with httpx.Client(timeout=300) as client:
        response = client.post(url, json=data)
        if response.status_code == 200:
            choices = response.json()['choices']
            if choices:
                return choices[0]['message']['content']
    raise HTTPException(status_code=500, detail="Chat failed.")
