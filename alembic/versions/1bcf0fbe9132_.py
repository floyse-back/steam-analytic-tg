"""empty message

Revision ID: 1bcf0fbe9132
Revises: 427840400a33
Create Date: 2025-06-25 15:02:47.221636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bcf0fbe9132'
down_revision: Union[str, None] = '427840400a33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wishlist',
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('short_desc', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('game_id')
    )
    op.alter_column('subscribes', 'role_permitions',
               existing_type=sa.INTEGER(),
               nullable=1)
    op.create_foreign_key(None, 'users_to_whishlist', 'wishlist', ['game_id'], ['game_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users_to_whishlist', type_='foreignkey')
    op.alter_column('subscribes', 'role_permitions',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_table('wishlist')
    # ### end Alembic commands ###
