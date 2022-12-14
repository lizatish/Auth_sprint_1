"""rollback

Revision ID: 806a2fde8ecd
Revises: 75a3381de0a0
Create Date: 2022-11-04 22:16:41.624513

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '806a2fde8ecd'
down_revision = '75a3381de0a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('accounthistory', 'label')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounthistory', sa.Column('label', postgresql.ENUM('STANDARD', 'PRIVILEGED', 'ADMIN', 'TEST', name='roletype'), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
