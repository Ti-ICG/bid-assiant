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
    pass


class SchemeSchemas(BaseScheme, InDBMixin):
    catalog_url: bytes = File(...)
    file_path_url: bytes = File(...)
    scheme_name: str
    create_time: datetime
    update_time: datetime


class CreateScheme(BaseScheme):
    scheme_name: str
    catalog_url: bytes = File(...)
    file_path_url: bytes = File(...)


class UpdateScheme(BaseScheme):
    pass


class DownloadScheme(BaseScheme):
    url: bytes = File(...)


class DetailScheme(BaseScheme):
    requirement_id: int
    requirement_content: str
    framework_id: int
    framework_content: str
    indicator_id: int
    indicator_content: str
    file_url: str


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
    
    requirement_content: str
    tmp_requirement_content: str


class RequirementAnalysisSchemas(BaseRequirementAnalysis, InDBMixin):
    scheme_id: int
    create_time: datetime
    update_time: datetime


class CreateRequirementAnalysis(BaseRequirementAnalysis):
    scheme_id: int


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
    
    framework_content: str
    tmp_framework_content: str


class SystemFrameworkSchemas(BaseSystemFramework, InDBMixin):
    scheme_id: int
    create_time: datetime
    update_time: datetime


class CreateSystemFramework(BaseSystemFramework):
    scheme_id: int


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
    
    indicator_content: str
    tmp_indicator_content: str


class ResponseIndicatorSchemas(BaseResponseIndicator, InDBMixin):
    scheme_id: int
    create_time: datetime
    update_time: datetime


class CreateResponseIndicator(BaseResponseIndicator):
    scheme_id: int


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
    index: str
    title: str

    # is_flag :bool


class BidCatalogSchemas(BaseBidCatalog, InDBMixin):
    id: str
    parent_id: str
    level: int
    scheme_id: int
    create_time: datetime
    update_time: datetime


class CreateBidCatalog(BaseBidCatalog):
    id: str
    parent_id: str
    level: int
    scheme_id: int


class UpdateBidCatalog(BaseBidCatalog):
    pass


#  Bid_catalog_content
class BaseBidCatalogContent(BaseModel):
    catalog_id: str
    content: str


class BidCatalogContentSchemas(BaseBidCatalogContent, InDBMixin):
    create_time: datetime
    update_time: datetime


class CreateBidCatalogContent(BaseBidCatalogContent):
    pass


class UpdateBidCatalogContent(BaseBidCatalogContent):
    pass


#  Catalog_prompt
class BaseCatalogPrompt(BaseModel):
    catalog_id: str


class CatalogPromptSchemas(BaseCatalogPrompt, InDBMixin):
    create_time: datetime
    update_time: datetime


class CreateCatalogPrompt(BaseCatalogPrompt):
    content: str


class UpdateCatalogPrompt(BaseCatalogPrompt):
    content: str


#  Chat
class Chat(BaseModel):
    scheme_id: int
    title: str
