"""empty message

Revision ID: 717ade5947a4
Revises: ca8917817272
Create Date: 2024-03-19 11:10:16.764081

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '717ade5947a4'
down_revision: Union[str, None] = 'ca8917817272'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_token_blacklist_token', table_name='token_blacklist')
    op.drop_table('token_blacklist')
    op.add_column('end_of_call', sa.Column('phone_number', postgresql.JSON(astext_type=sa.Text()), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('end_of_call', 'phone_number')
    op.create_table('token_blacklist',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('expires_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='token_blacklist_pkey')
    )
    op.create_index('ix_token_blacklist_token', 'token_blacklist', ['token'], unique=True)
    # ### end Alembic commands ###
