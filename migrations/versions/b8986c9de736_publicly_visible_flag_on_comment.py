"""publicly_visible flag on comment

Revision ID: b8986c9de736
Revises: 90adc2e968b8
Create Date: 2020-04-15 20:34:49.493054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8986c9de736'
down_revision = '90adc2e968b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('publicly_visible', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'publicly_visible')
    # ### end Alembic commands ###
