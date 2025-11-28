"""empty message

Revision ID: cca7f96d93e9
Revises: 8e367a8c3215
Create Date: 2025-10-20 11:41:29.857771

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cca7f96d93e9"
down_revision: Union[str, Sequence[str], None] = "8e367a8c3215"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TABLE rooms ALTER COLUMN price TYPE INTEGER USING price::integer")


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "rooms",
        "price",
        existing_type=sa.Integer(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
