"""foreign key addresses for task

Revision ID: 4e8cd0eb8fc6
Revises: bc19fb88e62e
Create Date: 2019-05-03 19:06:31.369621

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '4e8cd0eb8fc6'
down_revision = 'bc19fb88e62e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address1', sa.String(length=64), nullable=True),
    sa.Column('address2', sa.String(length=64), nullable=True),
    sa.Column('town', sa.String(length=64), nullable=True),
    sa.Column('county', sa.String(length=64), nullable=True),
    sa.Column('country', sa.String(length=64), nullable=True),
    sa.Column('postcode', sa.String(length=7), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('saved_locations', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'saved_locations', 'address', ['address_id'], ['id'])
    op.drop_column('saved_locations', 'country')
    op.drop_column('saved_locations', 'address1')
    op.drop_column('saved_locations', 'address2')
    op.drop_column('saved_locations', 'county')
    op.drop_column('saved_locations', 'postcode')
    op.drop_column('saved_locations', 'town')
    op.add_column('task', sa.Column('dropoffAddress_id', sa.Integer(), nullable=True))
    op.add_column('task', sa.Column('pickupAddress_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'task', 'address', ['pickupAddress_id'], ['id'])
    op.create_foreign_key(None, 'task', 'address', ['dropoffAddress_id'], ['id'])
    op.add_column('user', sa.Column('homeAddress_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'address', ['homeAddress_id'], ['id'])
    op.drop_column('user', 'country')
    op.drop_column('user', 'address1')
    op.drop_column('user', 'address2')
    op.drop_column('user', 'county')
    op.drop_column('user', 'postcode')
    op.drop_column('user', 'town')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('town', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('postcode', sa.VARCHAR(length=7), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('county', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('address2', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('address1', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('country', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'homeAddress_id')
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'pickupAddress_id')
    op.drop_column('task', 'dropoffAddress_id')
    op.add_column('saved_locations', sa.Column('town', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.add_column('saved_locations', sa.Column('postcode', sa.VARCHAR(length=7), autoincrement=False, nullable=True))
    op.add_column('saved_locations', sa.Column('county', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.add_column('saved_locations', sa.Column('address2', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.add_column('saved_locations', sa.Column('address1', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.add_column('saved_locations', sa.Column('country', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'saved_locations', type_='foreignkey')
    op.drop_column('saved_locations', 'address_id')
    op.drop_table('address')
    # ### end Alembic commands ###
