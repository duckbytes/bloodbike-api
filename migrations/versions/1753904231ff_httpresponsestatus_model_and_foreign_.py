"""HTTPResponseStatus model and foreign key to HTTPResonseStatus on LogEntry

Revision ID: 1753904231ff
Revises: 1e7d54e6cc89
Create Date: 2020-11-05 22:07:59.287571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1753904231ff'
down_revision = '1e7d54e6cc89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('http_response_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('status_description', sa.String(length=64), nullable=True),
    sa.Column('status_type', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('log_entry', sa.Column('http_response_status_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'log_entry', 'http_response_status', ['http_response_status_id'], ['id'])
    op.drop_column('log_entry', 'http_response_code')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('log_entry', sa.Column('http_response_code', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'log_entry', type_='foreignkey')
    op.drop_column('log_entry', 'http_response_status_id')
    op.drop_table('http_response_status')
    # ### end Alembic commands ###
