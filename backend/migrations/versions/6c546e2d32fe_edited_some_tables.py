"""edited some tables

Revision ID: 6c546e2d32fe
Revises: 39ae7df46a24
Create Date: 2023-04-11 21:44:26.227290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c546e2d32fe'
down_revision = '39ae7df46a24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('table_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('reservation_table_fk', 'table', ['table_id'], ['id'])
        batch_op.create_foreign_key('reservation_table_fk', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.drop_constraint('reservation_table_fk', type_='foreignkey')
        batch_op.drop_constraint('reservation_table_fk', type_='foreignkey')
        batch_op.drop_column('user_id')
        batch_op.drop_column('table_id')

    # ### end Alembic commands ###
