"""empty message

Revision ID: 98ae03ac491a
Revises: 049bbc94efb4
Create Date: 2018-10-19 20:15:21.409468

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '98ae03ac491a'
down_revision = '049bbc94efb4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('axf_user', sa.Column('_u_passwd', sa.String(length=255), nullable=True))
    op.drop_column('axf_user', 'u_passwd')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('axf_user', sa.Column('u_passwd', mysql.VARCHAR(length=255), nullable=True))
    op.drop_column('axf_user', '_u_passwd')
    # ### end Alembic commands ###