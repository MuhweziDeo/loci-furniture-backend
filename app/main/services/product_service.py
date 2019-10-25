from app.main.models.products import Product
from app.main import db 


def get_all_products():
    return Product.query.all()

def create_product(data):
    product = Product(
        name = data['name'],
        image_1 = data['image_1'],
        image_2 = data['image_2'],
        image_3 = data['image_3'],
        category_id = data['category_id'],
        description = data['description'],
        price = data['price']
    )

    db.session.add(product)
    db.session.commit()
    return product

def find_product_by_id(product_id):
    product = Product.query.filter_by(id=product_id).first()
    return product

def update_product(product, data):
    
    if "name" in data:
        product.name = data["name"]
    if "description" in data:
        product.description = data["description"]
    if "price" in data:
        data.price = data["price"]
    if "category_id" in data:
        product.category_id = data["category_id"]   
    if "image_1" in data:
        product.image_1 = data["image_1"]        

    if "image_2" in data:
        product.image_1 = data["image_2"]   

    if "image_3" in data:
        product.image_1 = data["image_3"]       
    
    db.session.add(product)
    db.session.commit()
    return product

def delete_product(product):
    db.session.delete(product)
    db.session.commit()
    return product
