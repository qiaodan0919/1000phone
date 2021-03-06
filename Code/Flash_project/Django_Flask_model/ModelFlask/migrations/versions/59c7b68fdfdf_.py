"""empty message

Revision ID: 59c7b68fdfdf
Revises: 
Create Date: 2018-10-25 20:33:43.490530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59c7b68fdfdf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('s_name', sa.String(length=20), nullable=True),
    sa.Column('s_password', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=16), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('student')
    # ### end Alembic commands ###
