"""
DB schema for automx2 version 2020.0
Created: 2020-01-17 22:30:05.748651
"""
from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision = 'f62e64b43d2f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ldapserver',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('port', sa.Integer(), nullable=False),
    sa.Column('use_ssl', sa.Boolean(), nullable=False),
    sa.Column('search_base', sa.String(length=128), nullable=False),
    sa.Column('search_filter', sa.String(length=128), nullable=False),
    sa.Column('attr_uid', sa.String(length=128), nullable=False),
    sa.Column('attr_cn', sa.String(length=128), nullable=True),
    sa.Column('bind_password', sa.String(length=128), nullable=True),
    sa.Column('bind_user', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('provider',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('short_name', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('server',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('port', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=128), nullable=False),
    sa.Column('socket_type', sa.String(length=128), nullable=False),
    sa.Column('user_name', sa.String(length=128), nullable=False),
    sa.Column('authentication', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('domain',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.Column('ldapserver_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ldapserver_id'], ['ldapserver.id'], ),
    sa.ForeignKeyConstraint(['provider_id'], ['provider.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('server_domain',
    sa.Column('server_id', sa.Integer(), nullable=False),
    sa.Column('domain_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['domain_id'], ['domain.id'], ),
    sa.ForeignKeyConstraint(['server_id'], ['server.id'], ),
    sa.PrimaryKeyConstraint('server_id', 'domain_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('server_domain')
    op.drop_table('domain')
    op.drop_table('server')
    op.drop_table('provider')
    op.drop_table('ldapserver')
    # ### end Alembic commands ###