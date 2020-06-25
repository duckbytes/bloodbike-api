"""collaborators field for assigning multiple users to make changes to a session

Revision ID: 92b8d39ea20b
Revises: 78c51adafd4e
Create Date: 2020-06-23 03:54:05.815342

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '92b8d39ea20b'
down_revision = '78c51adafd4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('session_collaborators',
    sa.Column('session_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['session_uuid'], ['session.uuid'], ),
    sa.ForeignKeyConstraint(['user_uuid'], ['user.uuid'], ),
    sa.PrimaryKeyConstraint('session_uuid', 'user_uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('session_collaborators')
    # ### end Alembic commands ###