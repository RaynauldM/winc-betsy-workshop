# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line

from models import Product, User, Transactions, User_product_ownership
from peewee import fn


def search(term):
    returnList = []
    for product in Product.select():
        if term.lower() in product.name.lower():
            returnList.append(product)
    if returnList:
        for item in returnList:
            print(item.name)
    else:
        print("no matches found")


def list_user_products(user_id):
    ...


def list_products_per_tag(tag_id):
    ...


def add_product_to_catalog(user_id, product):
    ...


def update_stock(product_id, new_quantity):
    ...


def purchase_product(product_id, buyer_id, quantity):
    ...


def remove_product(product_id):
    ...


def populate_test_database():
    User.create(
        name="Andre van Duin",
        address="Huizendorp 12",
        billing_info="1234_3444_2333_7898",
    )
    User.create(
        name="Herbert Andrews", address="Lantinga 2", billing_info="1233_3555_2233_1878"
    )

    User.create(
        name="Piet Tom", address="Glazenweg 488", billing_info="3233_3544_6766_7577"
    )

    Product.create(
        name="Playstation",
        description="gameconsole for younger generations and old alike",
        price_per_unit=499.99,
        quantity_in_stock=300,
        tag="gaming",
    )

    Product.create(
        name="Spoon",
        description="Mostly used for eating purposes",
        price_per_unit=4.90,
        quantity_in_stock=1000,
        tag="eating",
    )
