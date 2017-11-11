import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr

from webservices import docs

from .base import db

class AuditBase(object):
    __table_args__ = {"schema": "auditsearch"}


# endpoint: audit-primary-category
class PrimaryCategory(AuditBase, db.Model):
    __tablename__ = 'finding_vw'

    primary_category_id = db.Column(db.Integer, index=True, primary_key=True, doc=docs.PRIMARY_CATEGORY_ID)
    primary_category_name = db.Column(db.String, doc=docs.PRIMARY_CATEGORY_NAME)
    tier = db.Column(db.Integer, doc=docs.AUDIT_TIER)


# endpoint: audit-category
class CategoryRelation(AuditBase, db.Model):
    __tablename__ = 'finding_rel_vw'

    primary_category_id = db.Column(db.Integer, index=True, primary_key=True, doc=docs.PRIMARY_CATEGORY_ID)
    sub_category_id = db.Column(db.Integer, index=True, primary_key=True, doc=docs.SUB_CATEGORY_ID)
    sub_category_name = db.Column(db.String, index=True, primary_key=True, doc=docs.SUB_CATEGORY_NAME)


# endpoint: audit-category
class Category(PrimaryCategory):
    @declared_attr
    def sub_category_list(self):
        return sa.orm.relationship(
            CategoryRelation,
            primaryjoin=sa.orm.foreign(CategoryRelation.primary_category_id) == self.primary_category_id,
            uselist=True,
        )

# endpoint audit-case
class AuditCaseSubCategory(db.Model):
    __tablename__ = 'ofec_audit_case_sub_category_rel_mv'
    # add the correction description of each field in the docs.py
    audit_case_id = db.Column(db.Integer, primary_key=True, doc=docs.AUDIT_CASE_ID)
    primary_category_id = db.Column(db.Integer, primary_key=True, doc=docs.PRIMARY_CATEGORY_ID)
    sub_category_id = db.Column(db.Integer, primary_key=True, doc=docs.SUB_CATEGORY_ID)
    sub_category_name = db.Column(db.String, primary_key=True, doc=docs.SUB_CATEGORY_NAME)


# endpoint audit-case
class AuditCategoryRelation(db.Model):
    __tablename__ = 'ofec_audit_case_category_rel_mv'
    # add the correction description of each field in the docs.py
    audit_case_id = db.Column(db.Integer, primary_key=True, doc=docs.AUDIT_CASE_ID)
    primary_category_id = db.Column(db.Integer, primary_key=True, doc=docs.PRIMARY_CATEGORY_ID)
    primary_category_name = db.Column(db.String, primary_key=True, doc=docs.PRIMARY_CATEGORY_NAME)
    sub_category_list = db.relationship(
        'AuditCaseSubCategory',
        primaryjoin='''and_(
            foreign(AuditCategoryRelation.audit_case_id) == AuditCaseSubCategory.audit_case_id,
            AuditCategoryRelation.primary_category_id == AuditCaseSubCategory.primary_category_id
        )''',
        uselist=True,
        lazy='joined'
    )

    
# endpoint audit-case
class AuditCase(db.Model):
    __tablename__ = 'ofec_audit_case_mv'

    audit_case_id = db.Column(db.Integer, index=True, primary_key=True, doc=docs.AUDIT_CASE_ID)
    cycle = db.Column(db.Integer, doc=docs.CYCLE)
    committee_id = db.Column(db.String, doc=docs.COMMITTEE_ID)
    committee_name = db.Column(db.String, doc=docs.COMMITTEE_NAME)
    committee_designation = db.Column(db.String, doc=docs.DESIGNATION)
    committee_type = db.Column(db.String, doc=docs.COMMITTEE_TYPE)
    committee_description = db.Column(db.String, doc=docs.COMMITTEE_DESCRIPTION)
    far_release_date = db.Column(db.Date, doc=docs.FAR_RELEASE_DATE)
    link_to_report = db.Column(db.String, doc=docs.LINK_TO_REPORT)
    audit_id = db.Column(db.Integer, doc=docs.AUDIT_ID)
    candidate_id = db.Column(db.String, doc=docs.CANDIDATE_ID)
    candidate_name = db.Column(db.String, doc=docs.CANDIDATE_NAME)
    primary_category_list = db.relationship(
        AuditCategoryRelation,
        primaryjoin='''and_(
            foreign(AuditCategoryRelation.audit_case_id) == AuditCase.audit_case_id,
        )''',
        uselist=True,
        lazy='joined'
    )

# endpoint audit-case/search/<primary_category_id><sub_category_id>
class AuditCaseSearchByCategoryId(db.Model):
    __tablename__ = 'ofec_audit_case_arg_category_mv'

    primary_category_id = db.Column(db.Integer, primary_key=True, doc=docs.PRIMARY_CATEGORY_ID)
    sub_category_id = db.Column(db.Integer, primary_key=True, doc=docs.SUB_CATEGORY_ID)
    audit_case_id = db.Column(db.Integer, index=True, primary_key=True, doc=docs.AUDIT_CASE_ID)
    cycle = db.Column(db.Integer, doc=docs.CYCLE)
    committee_id = db.Column(db.String, doc=docs.COMMITTEE_ID)
    committee_name = db.Column(db.String, doc=docs.COMMITTEE_NAME)
    committee_designation = db.Column(db.String, doc=docs.DESIGNATION)
    committee_type = db.Column(db.String, doc=docs.COMMITTEE_TYPE)
    committee_description = db.Column(db.String, doc=docs.COMMITTEE_DESCRIPTION)
    far_release_date = db.Column(db.Date, doc=docs.FAR_RELEASE_DATE)
    link_to_report = db.Column(db.String, doc=docs.LINK_TO_REPORT)
    audit_id = db.Column(db.Integer, doc=docs.AUDIT_ID)
    candidate_id = db.Column(db.String, doc=docs.CANDIDATE_ID)
    candidate_name = db.Column(db.String, doc=docs.CANDIDATE_NAME)
    primary_category_list = db.relationship(
        AuditCategoryRelation,
        primaryjoin='''and_(
            foreign(AuditCategoryRelation.audit_case_id) == AuditCaseSearchByCategoryId.audit_case_id,
        )''',
        uselist=True,
        lazy='joined'
    )