import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Category, Recipe


test_engine = create_engine("sqlite:///:memory:", future=True)
TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False, future=True)


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


def test_create_recipe(db):
    recipe = Recipe(title="Test", source_url="http://example.com", ingredients="a", instructions="b")
    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    assert recipe.id is not None
    fetched = db.query(Recipe).first()
    assert fetched.title == "Test"


def test_category_and_link(db):
    category = Category(name="Dinner")
    recipe = Recipe(title="Soup", source_url="http://example.com/soup")
    recipe.categories.append(category)

    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    assert recipe.categories[0].name == "Dinner"
    assert category.recipes[0].title == "Soup"


def test_multiple_categories(db):
    r = Recipe(title="Salad", source_url="http://example.com/salad")
    r.categories.append(Category(name="Quick"))
    r.categories.append(Category(name="Healthy"))

    db.add(r)
    db.commit()
    db.refresh(r)

    assert len(r.categories) == 2
