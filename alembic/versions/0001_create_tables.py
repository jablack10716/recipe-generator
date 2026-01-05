"""create recipe tables

Revision ID: 0001_create_tables
Revises: 
Create Date: 2026-01-05
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_create_tables"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "recipes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("source_url", sa.String(length=500), nullable=False),
        sa.Column("ingredients", sa.Text()),
        sa.Column("instructions", sa.Text()),
        sa.Column("prep_time_minutes", sa.Integer()),
        sa.Column("cook_time_minutes", sa.Integer()),
        sa.Column("servings", sa.String(length=50)),
        sa.Column("image_url", sa.String(length=500)),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("color", sa.String(length=20)),
        sa.UniqueConstraint("name", name="uq_category_name"),
    )

    op.create_table(
        "recipe_categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("recipe_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["recipe_id"], ["recipes.id"], ),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"], ),
        sa.UniqueConstraint("recipe_id", "category_id", name="uq_recipe_category_link"),
    )

def downgrade():
    op.drop_table("recipe_categories")
    op.drop_table("categories")
    op.drop_table("recipes")
