"""add few columns to posts table

Revision ID: 432f3cd8891f
Revises: 2ebd7f30f22a
Create Date: 2025-04-30 11:56:52.601776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '432f3cd8891f'
down_revision: Union[str, None] = '2ebd7f30f22a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column("published",sa.Boolean(),nullable=False,server_default="True"),)
    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("now()")))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts",column_name="published")
    op.drop_column("posts",column_name="created_at")
    pass
