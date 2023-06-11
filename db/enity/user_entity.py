from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

from db.base_class import Base

user_diet_association = Table('user_diet_association', Base.metadata,
                              Column('user_id', Integer, ForeignKey('users.id')),
                              Column('diet_id', Integer, ForeignKey('diets.id'))
                              )

user_basket_association = Table('user_basket_association', Base.metadata,
                                Column('user_id', Integer, ForeignKey('users.id',ondelete='CASCADE')),
                                Column('basket_id', Integer, ForeignKey('basket.id', ondelete='CASCADE'))
                                )

users_likes = Table('users_likes', Base.metadata,
                    Column('user_id', Integer, ForeignKey('users.id')),
                    Column('product_id', Integer, ForeignKey('products.id')),
                    )


class UserEntity(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    diets = relationship("DietEntity", secondary=user_diet_association)
    baskets = relationship("BasketEntity", secondary=user_basket_association)
    likes = relationship("ProductEntity", secondary=users_likes)
