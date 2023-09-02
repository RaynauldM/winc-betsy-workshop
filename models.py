# Models go here
from peewee import (
    Model,
    SqliteDatabase,
    CharField,
    DecimalField,
    IntegerField,
    ForeignKeyField,
    Check,
    OperationalError,
)


db = SqliteDatabase("betsy_database.db")


class Base(Model):
    class Meta:
        database = db


class User(Base):
    name = CharField(
        max_length=50,
        constraints=[Check("length(name) > 0")],
    )
    address = CharField(max_length=50, constraints=[Check("length(address) > 0")])
    billing_info = CharField(
        max_length=50, constraints=[Check("length(billing_info) > 0")]
    )


class Tag(Base):
    name = CharField(
        max_length=50, constraints=[Check("length(name) > 0")], unique=True
    )


class Product(Base):
    name = CharField(max_length=50, constraints=[Check("length(name) > 0")])
    description = CharField(
        max_length=300, constraints=[Check("length(description) > 0")]
    )
    price_per_unit = DecimalField(
        max_digits=10, decimal_places=2, constraints=[Check("price_per_unit >= 0")]
    )
    quantity_in_stock = IntegerField(constraints=[Check("quantity_in_stock >= 0")])
    tag = ForeignKeyField(Tag, backref="products")


class Transactions(Base):
    buyer = ForeignKeyField(User, backref="transactions")
    product = ForeignKeyField(Product)
    quantity = IntegerField(constraints=[Check("quantity > 0")])


class User_product_ownership(Base):
    user = ForeignKeyField(User, backref="owned_products")
    product = ForeignKeyField(Product, backref="owners")


def create_tables():
    print("creating connection")
    db.connect()
    print("conection established")

    try:
        db.create_tables([User, Product, Transactions, User_product_ownership, Tag])
        print("tables created")
    except OperationalError:
        print("tables alreay exist")

    db.close()
