"""create posts users  foriegnkey

Revision ID: 2ebd7f30f22a
Revises: b32f5847a401
Create Date: 2025-04-30 11:47:39.126167

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ebd7f30f22a'
down_revision: Union[str, None] = 'b32f5847a401'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key("posts-users-fk",source_table="posts",referent_table="users",local_cols=["owner_id"],remote_cols=["id"],ondelete="cascade")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("posts-users-fk",table_name="posts")
    op.drop_column("posts",column_name="owner_id")
    pass
