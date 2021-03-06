"""empty message

Revision ID: fd712803989c
Revises: 
Create Date: 2018-10-18 18:06:46.417895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd712803989c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('axf_mustbuy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=16), nullable=True),
    sa.Column('trackid', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('axf_nav',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=16), nullable=True),
    sa.Column('trackid', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('axf_wheel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=16), nullable=True),
    sa.Column('trackid', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('axf_wheel')
    op.drop_table('axf_nav')
    op.drop_table('axf_mustbuy')
    # ### end Alembic commands ###
