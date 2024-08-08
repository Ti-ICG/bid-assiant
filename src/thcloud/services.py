"""Service"""

from typing import Generic, List

from sqlalchemy.orm import Session

from thcloud.dao import (
    BaseDAO,
    BidCatalogContentDAO,
    BidCatalogDAO,
    CatalogPromptDAO,
    RequirementAnalysisDAO,
    RequirementAnalysisDetailDAO,
    ResponseIndicatorDAO,
    ResponseIndicatorDetailDAO,
    SchemeDAO,
    SystemFrameworkDAO,
    SystemFrameworkDetailDAO,
)
from thcloud.models import (
    Bid_catalog,
    Bid_catalog_content,
    Catalog_prompt,
    Requirement_analysis,
    Requirement_analysis_detail,
    Response_indicator,
    Response_indicator_detail,
    Scheme,
    System_framework,
    System_framework_detail,
)
from thcloud.schemas import CreateSchema, ModelType, UpdateSchema


class BaseService(Generic[ModelType, CreateSchema, UpdateSchema]):
    dao: BaseDAO

    def get(self, session: Session, offset=0, limit=10) -> List[ModelType]:
        """"""
        return self.dao.get(session, offset=offset, limit=limit)
        
    def get_all_by_id(self, session: Session, pk: int) -> List[ModelType]:
        """"""
        return self.dao.get_all_by_id(session, pk)

    def get_by_scheme_id(self, session: Session, pk: int) -> List[ModelType]:
        """"""
        return self.dao.get_by_scheme_id(session, pk)

    def get_detail(self, session: Session, pk: int) -> ModelType:
        return self.dao.get_detail(session, pk)

    def total(self, session: Session) -> int:
        return self.dao.count(session)

    def get_by_id(self, session: Session, pk: int) -> ModelType:
        """Get by id"""
        return self.dao.get_by_id(session, pk)

    def create(self, session: Session, obj_in: CreateSchema) -> ModelType:
        """Create a object"""
        return self.dao.create(session, obj_in)

    def patch(self, session: Session, pk: int, obj_in: UpdateSchema) -> ModelType:
        """Update"""
        return self.dao.patch(session, pk, obj_in)

    def delete(self, session: Session, pk: int) -> None:
        """Delete a object"""
        return self.dao.delete(session, pk)


class SchemeService(BaseService[Scheme, CreateSchema, UpdateSchema]):
    dao = SchemeDAO()


class RequirementAnalysisService(
    BaseService[Requirement_analysis, CreateSchema, UpdateSchema]
):
    dao = RequirementAnalysisDAO()


class RequirementAnalysisDetailService(
    BaseService[Requirement_analysis_detail, CreateSchema, UpdateSchema]
):
    dao = RequirementAnalysisDetailDAO()


class SystemFrameworkService(BaseService[System_framework, CreateSchema, UpdateSchema]):
    dao = SystemFrameworkDAO()


class SystemFrameworkDetailService(BaseService[System_framework_detail, CreateSchema, UpdateSchema]):
    dao = SystemFrameworkDetailDAO()


class ResponseIndicatorService(
    BaseService[Response_indicator, CreateSchema, UpdateSchema]
):
    dao = ResponseIndicatorDAO()


class ResponseIndicatorDetailService(
    BaseService[Response_indicator_detail, CreateSchema, UpdateSchema]
):
    dao = ResponseIndicatorDetailDAO()


class BidCatalogService(BaseService[Bid_catalog, CreateSchema, UpdateSchema]):
    dao = BidCatalogDAO()


class BidCatalogContentService(
    BaseService[Bid_catalog_content, CreateSchema, UpdateSchema]
):
    dao = BidCatalogContentDAO()


class CatalogPromptService(BaseService[Catalog_prompt, CreateSchema, UpdateSchema]):
    dao = CatalogPromptDAO()
