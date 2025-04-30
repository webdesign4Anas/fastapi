"""add content column to posts table

Revision ID: e46ec78ae4d7
Revises: 5e55b8be1b10
Create Date: 2025-04-29 18:59:40.549016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e46ec78ae4d7'
down_revision: Union[str, None] = '5e55b8be1b10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
