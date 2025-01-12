"""del testAA

Revision ID: f5149bb47da8
Revises: a62a24a0e035
Create Date: 2018-07-23 16:18:25.539168

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f5149bb47da8'
down_revision = 'a62a24a0e035'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dj_admin_action', 'testAA')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dj_admin_action', sa.Column('testAA', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
