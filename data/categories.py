import sqlalchemy
import sqlalchemy.orm as orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
    
    
class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'category'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, 
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    
    
class Association(SqlAlchemyBase):
    __tablename__ = 'job_to_category'
    
    job = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('jobs.id'), primary_key=True)
    category = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('category.id'))