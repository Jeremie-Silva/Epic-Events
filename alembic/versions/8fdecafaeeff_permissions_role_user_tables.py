"""permissions_role_user tables

Revision ID: 8fdecafaeeff
Revises: 5df43ce87515
Create Date: 2024-03-31 14:36:36.405364

"""
from typing import Sequence, Union
from sqlalchemy.dialects import postgresql
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fdecafaeeff'
down_revision: Union[str, None] = '5df43ce87515'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('role',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_role_name'), 'role', ['name'], unique=False)
    op.create_table('permission',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('scope', sa.Enum('me', 'linked', 'all', name='scope'), nullable=False),
        sa.Column('action', sa.Enum('read', 'create', 'update', 'delete', name='action'), nullable=False),
        sa.Column('entity', sa.Enum('role', 'permission', 'user', 'customer', 'contract', 'event', name='entity'), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_name'), 'user', ['name'], unique=False)
    op.add_column('customer', sa.Column('salesman_id', sa.Integer(), nullable=True))
    op.create_foreign_key('foreign_key_for_customer_and_user', 'customer', 'user', ['salesman_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint('foreign_key_for_customer_and_user', 'customer', type_='foreignkey')
    op.drop_column('customer', 'salesman_id')
    op.drop_index(op.f('ix_user_name'), table_name='user')
    op.drop_table('user')
    op.drop_table('permission')
    op.drop_index(op.f('ix_role_name'), table_name='role')
    op.drop_table('role')

    postgresql.ENUM('me', 'linked', 'all', name='scope').drop(
        op.get_bind(), checkfirst=True
    )
    postgresql.ENUM('read', 'create', 'update', 'delete', name='action').drop(
        op.get_bind(), checkfirst=True
    )
    postgresql.ENUM('role', 'permission', 'user', 'customer', 'contract', 'event', name='entity').drop(
        op.get_bind(), checkfirst=True
    )
