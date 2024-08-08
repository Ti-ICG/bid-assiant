"""Models"""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship


class CustomBase:
    """https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/mixins.html"""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {"mysql_engine": "InnoDB", "mysql_collate": "utf8mb4_general_ci"}

    # id = Column(Integer, primary_key=True, autoincrement=True)


BaseModel = declarative_base(cls=CustomBase)


class Scheme(BaseModel):
    """scheme table"""  # 方案表

    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 方案id
    scheme_name = Column(String(100), nullable=False)  # 方案名
    catalog_url = Column(String(100), nullable=False)  # 目录文件url
    file_path_url = Column(String(100), nullable=False)  # 标书文件 url
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    update_time = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    requirement_analysis = relationship(
        "Requirement_analysis", cascade="all, delete-orphan", backref="schemes"
    )
    system_framework = relationship(
        "System_framework", cascade="all, delete-orphan", backref="schemes"
    )
    Response_indicator = relationship(
        "Response_indicator", cascade="all, delete-orphan", backref="schemes"
    )
    Bid_catalog = relationship(
        "Bid_catalog", cascade="all, delete-orphan", backref="schemes"
    )


class User(BaseModel):
    """users table"""  # 用户表

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 用户id
    user_name = Column(String(100), nullable=False)  # 用户名
    user_pwd = Column(String(100), nullable=False)  # 密码
    openid = Column(String(100))  # openid
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    update_time = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )


class Requirement_analysis(BaseModel):
    """requirement_analysis table"""  # 需求解析表

    __tablename__ = "requirement_analysis"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 需求id
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)  # 所属方案id
    requirement_content = Column(Text, nullable=True)  # 需求内容
    tmp_requirement_content = Column(Text, nullable=True)  # 临时保存内容
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    update_time = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    detail = relationship(
        "Requirement_analysis_detail",
        cascade="all, delete-orphan",
        backref="requirement_analysis",
    )


class Requirement_analysis_detail(BaseModel):
    """requirement_analysis_detail table"""  # 需求解析详情表

    __tablename__ = "requirement_analysis_detail"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 详情id
    requirement_analysis_id = Column(
        Integer, ForeignKey("requirement_analysis.id")
    )  # 所属需求id
    item_name = Column(String(100), nullable=True)  # 项目名称
    item_number = Column(String(100), nullable=True)  # 项目编号
    buliding_content = Column(Text, nullable=True)  # 建设内容
    system_function = Column(Text, nullable=True)  # 系统功能
    technical_requirement = Column(Text, nullable=True)  # 技术要求
    technical_review = Column(Text, nullable=True)  # 技术评审办法
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    update_time = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )


class System_framework(BaseModel):
    """system_framework table"""  # 系统框架表

    __tablename__ = "system_framework"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 系统框架id
    scheme_id = Column(Integer, ForeignKey("schemes.id"))  # 所属方案id
    framework_content = Column(Text, nullable=True)  # 系统框架内容
    tmp_framework_content = Column(Text, nullable=True)  # 临时框架内容（草稿）
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    update_time = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    detail = relationship(
        "System_framework_detail",
        cascade="all, delete-orphan",
        backref="system_framework",
    )


class System_framework_detail(BaseModel):
    """system_framework_detail table"""  # 系统框架详情表

    __tablename__ = "system_framework_detail"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 详情id
    system_framework_id = Column(
        Integer, ForeignKey("system_framework.id")
    )  # 所属系统框架id
    parent_id = Column(Integer, nullable=True)  # 父节点id
    content = Column(String(100), nullable=False)  # 框架详细内容
    level = Column(Integer, nullable=False)  # 框架层级
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    update_time = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )


class Response_indicator(BaseModel):
    """response_indicators table"""  # 响应指标表

    __tablename__ = "response_indicators"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 指标id
    scheme_id = Column(Integer, ForeignKey("schemes.id"))  # 所属方案id
    indicator_content = Column(Text, nullable=True)  # 相应指标内容
    tmp_indicator_content = Column(Text, nullable=True)  # 临时响应指标内容
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    update_time = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    detail = relationship(
        "Response_indicator_detail",
        cascade="all, delete-orphan",
        backref="response_indicators",
    )


class Response_indicator_detail(BaseModel):
    """response_indicator_detail table"""  # 响应指标详情表

    __tablename__ = "response_indicator_detail"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 详情指标id
    response_indicator_id = Column(
        Integer, ForeignKey("response_indicators.id")
    )  # 所属指标id
    indicator_name = Column(String(100), nullable=True)  # 指标名称
    indicator_category = Column(String(20), nullable=True)  # 指标类型
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    update_time = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )


class Bid_catalog(BaseModel):
    """bid_catalog table"""  # 标书目录表

    __tablename__ = "bid_catalog"

    id = Column(String(10), primary_key=True)  # 目录id
    parent_id = Column(String(10), nullable=True)  # 父节点id
    index = Column(String(20), nullable=True)  # 章节编号
    title = Column(String(50), nullable=False)  # 章节标题
    level = Column(Integer, nullable=False)  # 章节层级
    # is_flag = Column(Boolean, nullable=False)               #是否是叶子节点
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)  # 所属标书
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    update_time = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    detail = relationship(
        "Bid_catalog_content", cascade="all, delete-orphan", backref="bid_catalog"
    )


class Bid_catalog_content(BaseModel):
    """bid_catalog_content table"""  # 标书目录内容表

    __tablename__ = "bid_catalog_content"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 标书目录内容id
    catalog_id = Column(String(10), ForeignKey("bid_catalog.id"))  # 所属目录id
    content = Column(Text, nullable=True)  # 目录具体内容
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    update_time = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
