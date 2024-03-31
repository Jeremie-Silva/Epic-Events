"""contract table

Revision ID: 7e5a82dbfedb
Revises: 8fdecafaeeff
Create Date: 2024-03-31 14:51:10.824637

"""
from typing import Sequence, Union
from sqlalchemy.dialects import postgresql
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e5a82dbfedb'
down_revision: Union[str, None] = '8fdecafaeeff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('contract',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('salesman_id', sa.Integer(), nullable=False),
        sa.Column('amount_total', sa.Integer(), nullable=True),
        sa.Column('amount_outstanding', sa.Integer(), nullable=True),
        sa.Column('creation_date', sa.DateTime(), nullable=True),
        sa.Column('state', sa.Enum('signed', 'waiting', name='contractstate'), nullable=False),
        sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
        sa.ForeignKeyConstraint(['salesman_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('contract')
    postgresql.ENUM('signed', 'waiting', name='contractstate').drop(
        op.get_bind(), checkfirst=True
    )
