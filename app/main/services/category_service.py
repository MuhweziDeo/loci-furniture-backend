from app.main.models.category import Category
from .. import db

def find_all_categories():
    return Category.query.all()


def find_category_by_name(name):
    return Category.query.filter_by(name=name).first()


def find_category_by_id(id):
    return Category.query.filter_by(id=id).first()


def create_category(data):
    category = Category(
        name=data['name'],
    )

    db.session.add(category)
    db.session.commit()
    return category


def update_category(category, name):
    category.name = name
    db.session.add(category)
    db.session.commit()
    return category

def delete_category(category):
    db.session.delete(category)
    db.session.commit()
    return category
