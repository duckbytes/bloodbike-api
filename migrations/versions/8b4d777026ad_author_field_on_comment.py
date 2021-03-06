"""author field on comment

Revision ID: 8b4d777026ad
Revises: 095c1d831199
Create Date: 2020-04-15 19:39:07.133494

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8b4d777026ad'
down_revision = '095c1d831199'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('author', postgresql.UUID(as_uuid=True), nullable=True))
    op.drop_constraint('comment_author_uuid_fkey', 'comment', type_='foreignkey')
    op.create_foreign_key(None, 'comment', 'user', ['author'], ['uuid'])
    op.drop_column('comment', 'author_uuid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('author_uuid', postgresql.UUID(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.create_foreign_key('comment_author_uuid_fkey', 'comment', 'user', ['author_uuid'], ['uuid'])
    op.drop_column('comment', 'author')
    # ### end Alembic commands ###
