"""added phone column to user table

Revision ID: 39ae7df46a24
Revises: c795e88da42d
Create Date: 2023-04-11 14:31:17.394856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39ae7df46a24'
down_revision = 'c795e88da42d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.execute("DELETE FROM user")
    op.drop_table('_alembic_tmp_user')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone', sa.String(length=20), nullable=False))
        batch_op.drop_column('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=30), nullable=False))
        batch_op.drop_column('phone')

    op.create_table('_alembic_tmp_user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=25), nullable=False),
    sa.Column('password', sa.TEXT(), nullable=False),
    sa.Column('fullname', sa.VARCHAR(length=25), nullable=False),
    sa.Column('phone', sa.VARCHAR(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###