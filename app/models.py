from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class RecipeCategory(Base):
    __tablename__ = "recipe_categories"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    recipe = relationship("Recipe", back_populates="category_links")
    category = relationship("Category", back_populates="recipe_links")

    __table_args__ = (UniqueConstraint("recipe_id", "category_id", name="uq_recipe_category_link"),)


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    source_url = Column(String(500), nullable=False)
    ingredients = Column(Text)
    instructions = Column(Text)
    prep_time_minutes = Column(Integer)
    cook_time_minutes = Column(Integer)
    servings = Column(String(50))
    image_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    categories = relationship(
        "Category",
        secondary="recipe_categories",
        back_populates="recipes",
    )
    category_links = relationship(
        "RecipeCategory",
        back_populates="recipe",
        cascade="all, delete-orphan",
    )


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    color = Column(String(20))

    recipes = relationship(
        "Recipe",
        secondary="recipe_categories",
        back_populates="categories",
    )
    recipe_links = relationship(
        "RecipeCategory",
        back_populates="category",
        cascade="all, delete-orphan",
    )
