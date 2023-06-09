"""empty message

Revision ID: c54a2a5f28b9
Revises: 6c546e2d32fe
Create Date: 2023-04-12 01:43:09.763909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c54a2a5f28b9'
down_revision = '6c546e2d32fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.create_foreign_key('reservation_table_fk', 'table', ['table_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.drop_constraint('reservation_table_fk', type_='foreignkey')

    # ### end Alembic commands ###
