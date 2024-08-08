from datetime import datetime
from typing import Optional, TypeVar

from fastapi import File
from pydantic import BaseModel, constr

from thcloud.models import BaseModel as DBModel

ModelType = TypeVar("ModelType", bound=DBModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class InDBMixin(BaseModel):
    id: int

    class Config:
        orm_mode = True


#  方案
class BaseScheme(BaseModel):
    scheme_name: str


class SchemeSchemas(BaseScheme, InDBMixin):
    create_time: datetime
    update_time: datetime


class CreateScheme(BaseScheme):
    catalog_url: bytes = File(...)
    file_path_url: bytes = File(...)


class UpdateScheme(BaseScheme):
    pass


#  用户
# class BaseUser(BaseModel):
#     scheme_name : str
#     openid: str

# class UserSchemas(BaseUser,InDBMixin):
#     create_time: datetime
#     update_time: datetime


# class CreateUser(BaseUser):
#     password : str

# class UpdateUser(BaseUser):
#     password : str
#     pass


#  Requirement_analysis
class BaseRequirementAnalysis(BaseModel):
    scheme_id: int
    requirement_content: str


class RequirementAnalysisSchemas(BaseRequirementAnalysis, InDBMixin):
    create_time: datetime
    update_time: datetime


class CreateRequirementAnalysis(BaseRequirementAnalysis):
    pass


class UpdateRequirementAnalysis(BaseRequirementAnalysis):
    tmp_requirement_content: str


#  Requirement_analysis_detail
class BaseRequirementAnalysisDetail(BaseModel):
    requirement_analysis_id: int
    item_name: str
    item_number: str
    buliding_content: str
    system_function: str
    technical_requirement: str
    technical_review: str


class RequirementAnalysisDetailSchemas(BaseRequirementAnalysisDetail, InDBMixin):
    create_time: datetime
    update_time: datetime


class CreateRequirementAnalysisDetail(BaseRequirementAnalysisDetail):
    pass


class UpdateRequirementAnalysisDetail(BaseRequirementAnalysisDetail):
    pass


#  System_framework
class BaseSystemFramework(BaseModel):
    scheme_id: int
    framework_content: str


class SystemFrameworkSchemas(BaseSystemFramework, InDBMixin):
    create_time: datetime
    update_time: datetime


class CreateSystemFramework(BaseSystemFramework):
    pass


class UpdateSystemFramework(BaseSystemFramework):
    tmp_framework_content: str  # 临时框架内容（草稿）


#  System_framework_detail
class BaseSystemFrameworkDetail(BaseModel):
    system_framework_id: int
    parent_id: int
    content: str
    level: int


class SystemFrameworkDetailSchemas(BaseSystemFrameworkDetail, InDBMixin):
    create_time: datetime
    update_time: datetime


class CreateSystemFrameworkDetail(BaseSystemFrameworkDetail):
    pass


class UpdateSystemFrameworkDetail(BaseSystemFrameworkDetail):
    pass


#  Response_indicator
class BaseResponseIndicator(BaseModel):
    scheme_id: int
    indicator_content: str


class ResponseIndicatorSchemas(BaseResponseIndicator, InDBMixin):
    create_time: datetime
    update_time: datetime


class CreateResponseIndicator(BaseResponseIndicator):
    pass


class UpdateResponseIndicator(BaseResponseIndicator):
    tmp_indicator_content: str


#  Response_indicator_detail
class BaseResponseIndicatorDetail(BaseModel):
    response_indicator_id: int
    indicator_name: str
    indicator_category: str


class ResponseIndicatorDetailSchemas(BaseResponseIndicatorDetail, InDBMixin):
    create_time: datetime
    update_time: datetime


class CreateResponseIndicatorDetail(BaseResponseIndicatorDetail):
    pass


class UpdateResponseIndicatorDetail(BaseResponseIndicatorDetail):
    pass


#  Bid_catalog
class BaseBidCatalog(BaseModel):
    pass


class BidCatalogSchemas(BaseBidCatalog, InDBMixin):
    create_time: datetime
    update_time: datetime


class CreateBidCatalog(BaseBidCatalog):
    id: str
    parent_id: str
    title: str
    level: int
    scheme_id: int
    pass


class UpdateBidCatalog(BaseBidCatalog):
    title: str


#  Bid_catalog_content
class BaseBidCatalogContent(BaseModel):
    catalog_id: str
    index: str
    content: str


class BidCatalogContentSchemas(BaseBidCatalogContent, InDBMixin):
    create_time: datetime
    update_time: datetime


class CreateBidCatalogContent(BaseBidCatalogContent):
    pass


class UpdateBidCatalogContent(BaseBidCatalogContent):
    pass


#  Chat
class KbChat(BaseModel):
    scheme_id: int
    query: str


class ChatChat(BaseModel):
    content: str
