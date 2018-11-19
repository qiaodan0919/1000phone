"""empty message

Revision ID: 50318271b0f5
Revises: 
Create Date: 2018-10-17 10:50:35.194392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50318271b0f5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=16), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student')
    # ### end Alembic commands ###
