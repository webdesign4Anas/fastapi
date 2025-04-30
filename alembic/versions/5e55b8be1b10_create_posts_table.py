"""create posts table

Revision ID: 5e55b8be1b10
Revises: 
Create Date: 2025-04-29 18:17:24.371785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e55b8be1b10'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.INTEGER(),primary_key=True,nullable=False),sa.Column('title',sa.String(),nullable=False))
    pass
                  
    
    

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
