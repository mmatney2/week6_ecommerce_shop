"""empty message

Revision ID: 5b5c23621157
Revises: 53eb068c0bf9
Create Date: 2022-05-17 00:53:02.613967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b5c23621157'
down_revision = '53eb068c0bf9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('product_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'cart', 'product', ['product_id'], ['product_id'])
    op.add_column('product', sa.Column('product_id', sa.Integer(), nullable=False))
    op.drop_column('product', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('product', 'product_id')
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.drop_column('cart', 'product_id')
    # ### end Alembic commands ###
