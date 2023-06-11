from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

from db.base_class import Base

basket_product_association = Table('basket_product_association', Base.metadata,
                                   Column('basket_id', Integer, ForeignKey('basket.id', ondelete='CASCADE')),
                                   Column('product_id', Integer, ForeignKey('products.id', ondelete='CASCADE')),
                                   )


class BasketEntity(Base):
    __tablename__ = 'basket'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    products = relationship("ProductEntity", secondary=basket_product_association)
