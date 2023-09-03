# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line

from models import (
    Product,
    User,
    Transactions,
    User_product_ownership,
    Tag,
    create_tables,
)


def search(term):
    returnList = []
    for product in Product.select():
        if term.lower() in product.name.lower() or term.lower() in product.description:
            returnList.append(product)
    if returnList:
        for item in returnList:
            print(item.name)
    else:
        print("no matches found")


def list_user_products(user_id):
    user = User.get_or_none(id=user_id)
    if user:
        owned_products = (
            Product.select()
            .join(User_product_ownership)
            .where(User_product_ownership.user == user)
        )
        if owned_products:
            for product in owned_products:
                print(product.name)
        else:
            print("no products found for this user")
    else:
        print("No matching user found")


def list_products_per_tag(tag_id):
    try:
        tag = Tag.get(Tag.id == tag_id)

        found_products = tag.products

        if found_products:
            print(f"Products with tag {tag_id}:")
            for product in found_products:
                print(product.name)
        else:
            print("None found with chosen tag")
    except Tag.DoesNotExist:
        print("Chosen tag not found")


def add_product_to_catalog(user_id, product):
    try:
        user = User.get(User.id == user_id)
        product_to_add = Product.get(Product.name == product)

        User_product_ownership.create(user=user, product=product_to_add)
        print(f"Added '{product}' to the catalog of '{user.name}'")
    except User.DoesNotExist:
        print(f"User with ID {user_id} not found")
    except Product.DoesNotExist:
        print(f"Product '{product}' not found")


def remove_product_from_catalog(user_id, product):
    try:
        user = User.get(User.id == user_id)
        product_to_remove = Product.get(Product.name == product)

        ownership = User_product_ownership.get(
            (User_product_ownership.user == user)
            & (User_product_ownership.product == product_to_remove)
        )

        ownership.delete_instance()

        print(f"'{product}' removed from catalog of '{user.name}'")

    except User.DoesNotExist:
        print(f"user with id '{user_id}' not found")
    except Product.DoesNotExist:
        print(f"'{product}' not found")
    except User_product_ownership.DoesNotExist:
        print("error finding the ownership of the product and user")


def update_stock(product_id, new_quantity):
    try:
        product = Product.get(Product.id == product_id)
        product.quantity_in_stock = new_quantity
        product.save()
        print(f"Updated stock for product '{product.name}' to {new_quantity}.")
    except Product.DoesNotExist:
        print(f"Product with ID {product_id} not found.")


def purchase_product(product_id, buyer_id, quantity):
    try:
        product = Product.get(Product.id == product_id)
        buyer = User.get(User.id == buyer_id)

        if product.quantity_in_stock >= quantity:
            # Calculate the cost
            total_cost = product.price_per_unit * quantity

            Transactions.create(buyer=buyer, product=product, quantity=quantity)

            product.quantity_in_stock -= quantity
            product.save()

            print(f"Purchase successful!")
            print(f"Buyer: {buyer.name}")
            print(f"Product: {product.name}")
            print(f"Quantity: {quantity}")
            print(f"Total Cost: ${total_cost}")
        else:
            print(f"Insufficient stock for product '{product.name}'.")

    except Product.DoesNotExist:
        print(f"Product with ID {product_id} not found.")
    except User.DoesNotExist:
        print(f"Buyer with ID {buyer_id} not found.")


def remove_product(product_id):
    try:
        product = Product.get(Product.id == product_id)
        product_name = product.name

        product.delete_instance()

        print(f"Product '{product_name}' has been removed from the catalog.")
    except Product.DoesNotExist:
        print(f"Product with ID {product_id} not found.")


def populate_test_database():
    User.create(
        name="Henk Klooster",
        address="Huizendorp 1233",
        billing_info="1234_3444_2333_7898",
    )
    User.create(
        name="Herbert Andrews",
        address="Lantinga 22",
        billing_info="1233_3555_2233_1878",
    )

    User.create(
        name="Piet Tom",
        address="Glazenweg 4883",
        billing_info="3233_3544_6766_7577",
    )

    furniture_Tag = Tag.create(name="furniture")
    eating_Tag = Tag.create(name="eating")
    gaming_Tag = Tag.create(name="gaming")

    Product.create(
        name="table",
        description="for eating purposes",
        price_per_unit=299.99,
        quantity_in_stock=300,
        tag=furniture_Tag,
    )

    Product.create(
        name="chair",
        description="Mostly used for eating purposes",
        price_per_unit=4.90,
        quantity_in_stock=1000,
        tag=furniture_Tag,
    )

    Product.create(
        name="playstation",
        description="One of the best console, at least before the psplus pricehike",
        price_per_unit=500.00,
        quantity_in_stock=5,
        tag=gaming_Tag,
    )

    Product.create(
        name="spoon",
        description="mostly used for eating by placing it in the food and then in your mouth",
        price_per_unit=3.55,
        quantity_in_stock=60,
        tag=eating_Tag,
    )


if __name__ == "__main__":
    create_tables()
    populate_test_database()
