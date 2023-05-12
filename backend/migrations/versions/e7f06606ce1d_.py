"""empty message

Revision ID: e7f06606ce1d
Revises: a1471670cc8c
Create Date: 2023-04-12 01:50:04.607043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7f06606ce1d'
down_revision = 'a1471670cc8c'
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