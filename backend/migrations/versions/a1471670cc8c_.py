"""empty message

Revision ID: a1471670cc8c
Revises: c54a2a5f28b9
Create Date: 2023-04-12 01:48:01.411082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1471670cc8c'
down_revision = 'c54a2a5f28b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.create_foreign_key('reservation_table_fk', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.drop_constraint('reservation_table_fk', type_='foreignkey')

    # ### end Alembic commands ###
