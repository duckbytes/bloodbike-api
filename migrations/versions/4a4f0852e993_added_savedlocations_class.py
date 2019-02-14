"""Added SavedLocations class

Revision ID: 4a4f0852e993
Revises: fd42174a8393
Create Date: 2019-01-10 22:51:15.911403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a4f0852e993'
down_revision = 'fd42174a8393'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('saved_locations',
    sa.Column('address1', sa.String(length=64), nullable=True),
    sa.Column('address2', sa.String(length=64), nullable=True),
    sa.Column('town', sa.String(length=64), nullable=True),
    sa.Column('county', sa.String(length=64), nullable=True),
    sa.Column('country', sa.String(length=64), nullable=True),
    sa.Column('postcode', sa.String(length=7), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('notes', sa.String(length=10000), nullable=True),
    sa.Column('contact', sa.String(length=64), nullable=True),
    sa.Column('phoneNumber', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_saved_locations_timestamp'), 'saved_locations', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_saved_locations_timestamp'), table_name='saved_locations')
    op.drop_table('saved_locations')
    # ### end Alembic commands ###