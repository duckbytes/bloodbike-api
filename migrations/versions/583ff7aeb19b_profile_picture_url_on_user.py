"""profile_picture_url on User

Revision ID: 583ff7aeb19b
Revises: 9144baa0b1fc
Create Date: 2020-09-17 14:05:39.911436

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '583ff7aeb19b'
down_revision = '9144baa0b1fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('session_collaborators')
    op.drop_index('ix_session_time_created', table_name='session')
    op.drop_index('ix_session_time_modified', table_name='session')
    op.drop_table('session')
    op.add_column('user', sa.Column('profile_picture_url', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'profile_picture_url')
    op.create_table('session',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('session_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('uuid', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('flagged_for_deletion', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('time_created', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('time_modified', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('coordinator_uuid', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['coordinator_uuid'], ['user.uuid'], name='session_coordinator_uuid_fkey'),
    sa.PrimaryKeyConstraint('id', name='session_pkey'),
    sa.UniqueConstraint('uuid', name='session_uuid_key'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_session_time_modified', 'session', ['time_modified'], unique=False)
    op.create_index('ix_session_time_created', 'session', ['time_created'], unique=False)
    op.create_table('session_collaborators',
    sa.Column('session_uuid', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('user_uuid', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['session_uuid'], ['session.uuid'], name='session_collaborators_session_uuid_fkey'),
    sa.ForeignKeyConstraint(['user_uuid'], ['user.uuid'], name='session_collaborators_user_uuid_fkey'),
    sa.PrimaryKeyConstraint('session_uuid', 'user_uuid', name='session_collaborators_pkey')
    )
    # ### end Alembic commands ###
