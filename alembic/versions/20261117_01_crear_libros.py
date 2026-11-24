"""crear tabla de libros

Revision ID: 20261117_01
"""

from alembic import op
import sqlalchemy as sa


revision = "20261117_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "libros",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("titulo", sa.String(length=200), nullable=False),
        sa.Column("autor", sa.String(length=150), nullable=False),
        sa.Column("isbn", sa.String(length=20), nullable=True),
        sa.Column("portada_url", sa.String(length=500), nullable=True),
        sa.Column("creado_en", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("isbn"),
    )
    op.create_index("ix_libros_titulo", "libros", ["titulo"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_libros_titulo", table_name="libros")
    op.drop_table("libros")
