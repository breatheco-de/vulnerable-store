"""empty message

Revision ID: 1fa6bba580d3
Revises: 62ad32a79fd5
Create Date: 2024-09-27 15:37:26.255496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fa6bba580d3'
down_revision = '62ad32a79fd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vulnerability',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=100), nullable=False),
    sa.Column('file_path', sa.String(length=255), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vulnerability')
    # ### end Alembic commands ###
