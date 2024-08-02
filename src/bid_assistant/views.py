import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from thcloud.dependencies import CommonQueryParams, get_db
from thcloud.schemas import (ArticleSchema, CreateArticleSchema,
                             UpdateArticleSchema)
from thcloud.services import ArticleService

router = APIRouter()

_service = ArticleService()


CHAT_HOST = "http://192.168.200.17:7861"
UPLOAD_TEMP_DOCS_API = CHAT_HOST + "/knowledge_base/upload_temp_docs"

CHAT_FILE_API = CHAT_HOST + "/chat/file_chat"
CHAT_FILE_DATA = {
    "model_name": "glm-4-9b-chat-1m",
    "max_tokens": 4096,
    "prompt_name": "kb_extend",
    "temperature": 0.15,
    "score_threshold": 1.6,
    "top_k": 1,
    "knowledge_id": "f2123836799e4842b9fa9a366a1b9f34",
    "history": [
        {
            "role": "user",
            "content": "背景：我需要投标一个项目[智能问答系统]，售前工程师已根据招标文件的要求编写了一个标书章节大纲，现在需要将每一个章节的内容完善；\n\n角色：你是一个专业的售前工程师，擅长编写各类投标书；\n\n任务：根据用户给出的章节，结合知识库中的内容和上下文，编写指定章节的内容；\n\n要求：- 使用严谨、专业的语言编写，避免口语化、AI化表达，注意标点符号的使用，确保内容符合招标文件要求，并突出公司优势；\n- 只需要生成章节的内容，禁止生成子章节或不相关的内容；\n- 请按照招标文件中的内容生成对应内容；\n- 如果遇到表格，请以markdown的表格形式展示；\n- 如果没有匹配到知识库中的内容，请以自身能力去编写内容；\n- 如果需要绘制图标，请以mermiad语法绘制；\n\n章节大纲如下：\n```\n符合性审查索引表\n第一章 谈判函\n第二章 商务条款响应偏离表\n第三章 技术指标参数响应偏离表\n第四章 交货清单\n第五章 易损易耗件清单\n第六章 售后服务方案\n6.1 售后服务方案\n6.1.1 服务方式\n6.1.1.1 应急响应服务\n6.1.1.2 在线咨询服务\n6.1.1.3 远程维护服务\n6.1.1.4 本地化技术支持服务\n6.1.1.5 7*24小时电话答询\n6.1.1.6 定期回访巡检服务\n6.1.1.7 紧急恢复服务\n6.1.1.8 用户满意度指标\n6.1.2 现场支持\n6.1.2.1 现场应急响应\n6.1.2.2 现场服务快速响应\n6.1.2.3 健康检查\n6.1.2.4 故障处理\n6.1.3 服务等级\n6.1.4 运维人员安排\n6.1.5 升级服务\n6.1.6 关于运维人员安排的承诺\n第七章 技术方案和所谈判产品技术支持材料\n7.1 项目背景\n7.2 项目需求分析\n7.2.1 功能需求分析\n7.2.1.1 基于大模型的智能问答\n7.2.1.1.1 高效的自然语言理解（NLU）\n7.2.1.1.2 多领域知识融合\n7.2.1.1.3 实时响应与个性化服务\n7.2.1.1.4 自动学习与持续优化\n7.2.1.2 基于语义相似性的文档内容检索\n7.2.1.2.1 理解复杂查询\n7.2.1.2.2 特定检索与个性化检索\n7.2.1.2.3 自然语言处理(NLP)与语义模型\n7.2.1.2.4 系统交互设计\n7.2.1.2.5 性能评估与监控\n7.2.1.3 支持问答与检索的数据处理\n7.2.1.3.1 数据预处理\n7.2.1.3.2 结果排序与展示\n7.2.1.3.3 性能与可扩展性\n7.2.2 技术架构需求分析\n7.2.2.1 前后端分离架构\n7.2.2.2 灵活的计算资源管理\n7.2.2.3 用户友好交互设计\n7.2.3 系统性能需求分析\n7.2.3.1 快速响应时间\n7.2.3.2 高效语义匹配\n7.2.3.3 高质量语义向量与匹配精度\n7.2.3.3.1 定制化训练数据\n7.2.3.3.2 高维度语义向量\n7.2.3.3.3 余弦相似性计算\n7.2.3.3.4 模型优化与调参\n7.2.3.3.5 评估与验证\n7.2.3.4 文档处理能力\n7.2.3.5 用户体验评估\n7.2.3.5.1 问题覆盖率\n7.2.3.5.2 问题匹配度\n7.2.3.5.3 回答事实正确率\n7.2.3.5.4 人工评估满意度\n7.3 流程图描述\n7.3.1 业务流程图\n7.3.1.1 模型训练业务流程图\n7.3.1.2 模型测试业务流程图\n7.3.1.3 问答服务业务流程图\n7.3.1.4 基于语义相似性的文档内容检索业务流程图\n7.3.1.5 支持问答与检索的数据处理业务流程图\n7.3.2 数据流程图\n7.3.2.1 模型训练及测试数据流程图\n7.3.2.2 问答服务数据流程图\n7.3.2.3 基于语义相似性的文档内容检索数据流程图\n7.3.2.4 基于语义相似性的文档内容检索数据流程图\n7.4 系统功能方案\n7.4.1 系统架构设计\n7.4.1.1 总体架构\n7.4.1.2 业务架构\n7.4.1.3 逻辑架构\n7.4.1.4 技术架构\n7.4.1.5 数据架构\n7.4.2 基于大模型的智能问答\n7.4.2.1 系统架构\n7.4.2.2 Web端\n7.4.2.3 后端系统功能\n7.4.2.3.1 模型训练\n7.4.2.3.2 模型测试\n7.4.2.3.3 问答服务\n7.4.2.4 业务处理流程\n7.4.2.5 数据处理流程\n7.4.3 基于语义相似性的文档内容检索\n7.4.3.1 Web端\n7.4.3.2 后端系统功能\n7.4.3.2.1 提取文件语义\n7.4.3.2.2 语义测试\n7.4.3.2.3 文档内容匹配服务\n7.4.3.2.4 问答记录\n7.4.3.3 业务处理流程\n7.4.3.4 数据处理流程\n7.4.4 支持问答与检索的数据处理\n7.4.4.1 问答数据处理\n7.4.4.2 文档数据处理\n7.4.4.3 数据的存储与管理\n7.4.4.4 业务处理流程\n7.4.4.5 数据处理流程\n7.5 系统接口方案\n7.5.1 内部接口\n7.5.2 外部接口\n7.6 系统数据库方案\n7.6.1 E-R图\n7.6.1.1 实体类型\n7.6.1.2 关系\n7.6.2 主要数据库表\n7.7 系统部署方案\n7.7.1 服务器部署方案\n7.7.1.1 服务器\n7.7.1.2 网络设备\n7.7.1.3 安全设备\n7.7.2 网络部署架构\n7.8 项目安全设计\n7.8.1 网络安全\n7.8.1.1 安全通信网络要求\n7.8.1.2 安全区域边界要求\n7.8.1.2.1 边界防护\n7.8.1.2.2 访问控制\n7.8.1.2.3 入侵防范\n7.8.1.2.4 恶意代码防范\n7.8.1.2.5 安全审计\n7.9 关键技术\n7.9.1 大模型参数高效微调技术\n7.9.2 基于智能问答的实时问答引擎技术\n7.9.3 基于大模型的人工智能系统全栈优化技术\n7.9.4 基于语义相似性的文档内容检索技术\n7.9.5 基于对象检测和OCR模型的文档解析技术\n7.10 技术指标响应说明\n7.10.1 功能指标\n7.10.1.1 基于大模型的智能问答\n7.10.1.2 基于语义相似性的文档内容检索\n7.10.1.3 支持问答与检索的数据处理中的问答数据处理\n7.10.2 性能指标\n7.10.3 正偏离指标说明\n7.10.4 负偏离指标说明（提供承诺函）\n7.11 项目管理和实施方案\n7.11.1 实施周期管理\n7.11.1.1 项目关键环节分析\n7.11.1.2 项目人力资源分配\n7.11.1.2.1 项目领导小组\n7.11.1.2.2 项目执行小组\n7.11.1.2.3 程序组\n7.11.1.2.4 测试组\n7.11.1.2.5 运维实施组\n7.11.1.2.6 质量保证小组\n7.11.1.2.7 项目验收小组\n7.11.1.3 项目关键过程管理和控制策略\n7.11.1.4 项目协作管理\n7.11.2 项目风险控制\n7.11.2.1 风险因素分析\n7.11.2.1.1 技术风险\n7.11.2.1.2 管理风险\n7.11.2.1.3 人员风险\n7.11.2.1.4 政策风险\n7.11.2.2 风险评估防范\n7.11.2.3 风险控制措施\n7.11.3 质量控制\n7.11.3.1 质量管理体系\n7.11.3.2 质量管理人员配备\n7.11.3.3 质量计划\n7.11.3.4 设计开发过程质量控制的方法措施\n7.11.3.5 测试过程质量控制\n7.11.3.6 交付和售后服务质量控制\n7.12 项目负责人\n7.12.1 项目负责人说明\n7.12.2 项目负责人证书\n7.12.3 项目负责人累积业绩\n7.13 开发项目团队和人员\n7.13.1 项目人力资源分配方案\n7.14 培训方案\n7.14.1 培训人员\n7.14.2 培训时间地点\n7.14.3 培训组织架构\n7.14.4 培训对象和内容\n7.14.5 培训方式\n7.14.5.1 集中培训\n7.14.5.2 现场培训\n7.14.6 培训流程\n7.14.7 培训课程\n7.14.8 培训考核\n第八章 财务社保数据统计表\n第九章 其他材料\n\n```\n    "
        }
    ],
    "query": "请编写第7.2.1.1.4章自动学习与持续优化内容",
    "stream": True
}

CHAT_CHAT_API = CHAT_HOST + "/chat/chat/completions"
CHAT_CHAT_DATA = {
    "messages": [
        {
            "content": "你是谁",
            "role": "system",
            "name": "string",
        }
    ],
    "model": "glm-4-9b-chat-1m",
    "max_tokens": 2048,
    "n": 0,
    "stream": True,
    "temperature": 0.7,
}


@router.get("/chat/file-chat")
async def chat_file():
    async def generate():
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", CHAT_FILE_API, json=CHAT_FILE_DATA) as stream:
                async for chunk in stream.aiter_text():
                    yield chunk
    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get("/chat/chat")
async def chat_chat():
    async def generate():
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", CHAT_CHAT_API, json=CHAT_CHAT_DATA) as stream:
                async for chunk in stream.aiter_text():
                    yield chunk
    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get('/articles')
def get(
        session: Session = Depends(get_db),
        commons: CommonQueryParams = Depends()
):
    return _service.get(session, offset=commons.offset, limit=commons.limit)


@router.get('/articles/{pk}')
def get_by_id(
        pk: int,
        session: Session = Depends(get_db)
):
    return _service.get_by_id(session, pk)


@router.post('/articles', response_model=ArticleSchema)
def create(
        obj_in: CreateArticleSchema,
        session: Session = Depends(get_db),
):
    return _service.create(session, obj_in)


@router.patch('/articles/{pk}', response_model=ArticleSchema)
def patch(
        pk: int,
        obj_in: UpdateArticleSchema,
        session: Session = Depends(get_db)
):
    return _service.patch(session, pk, obj_in)


@router.delete('/articles/{pk}')
def delete(
        pk: int,
        session: Session = Depends(get_db)
):
    return _service.delete(session, pk)