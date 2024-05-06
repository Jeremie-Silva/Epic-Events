"""events table

Revision ID: 0cf8c6f403b6
Revises: 
Create Date: 2024-05-06 17:26:20.800035

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '0cf8c6f403b6'
down_revision: Union[str, None] = None
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
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('last_update', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_name'), 'user', ['name'], unique=False)
    op.create_table('customer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('salesman_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('phone', sa.String(length=255), nullable=True),
    sa.Column('company_name', sa.String(length=255), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('last_update', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['salesman_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_name'), 'customer', ['name'], unique=True)
    op.create_table('contract',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('salesman_id', sa.Integer(), nullable=False),
    sa.Column('amount_total', sa.Float(), nullable=True),
    sa.Column('amount_outstanding', sa.Float(), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('last_update', sa.DateTime(), nullable=True),
    sa.Column('state', sa.Enum('signed', 'waiting', name='contractstate'), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['salesman_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contract_state'), 'contract', ['state'], unique=False)
    op.create_table('event',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('contract_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('support_contact_id', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('attendees', sa.Integer(), nullable=True),
    sa.Column('notes', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['contract_id'], ['contract.id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['support_contact_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_event_name'), 'event', ['name'], unique=False)
    op.create_index(op.f('ix_event_start_date'), 'event', ['start_date'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_event_start_date'), table_name='event')
    op.drop_index(op.f('ix_event_name'), table_name='event')
    op.drop_table('event')
    op.drop_index(op.f('ix_contract_state'), table_name='contract')
    op.drop_table('contract')
    op.drop_index(op.f('ix_customer_name'), table_name='customer')
    op.drop_table('customer')
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
    postgresql.ENUM('signed', 'waiting', name='contractstate').drop(
        op.get_bind(), checkfirst=True
    )
