"""empty message

Revision ID: f55913433061
Revises: 95bfe64bcf0a
Create Date: 2023-07-14 04:09:52.159088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f55913433061'
down_revision = '95bfe64bcf0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('email_address',
               existing_type=sa.VARCHAR(length=150),
               type_=sa.String(length=50),
               existing_nullable=True)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=150),
               type_=sa.String(length=50),
               existing_nullable=True)
        batch_op.alter_column('first_name',
               existing_type=sa.VARCHAR(length=150),
               type_=sa.String(length=50),
               existing_nullable=True)
        batch_op.alter_column('last_name',
               existing_type=sa.VARCHAR(length=150),
               type_=sa.String(length=50),
               existing_nullable=True)
        batch_op.alter_column('role',
               existing_type=sa.VARCHAR(length=150),
               type_=sa.String(length=50),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('role',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=150),
               existing_nullable=True)
        batch_op.alter_column('last_name',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=150),
               existing_nullable=True)
        batch_op.alter_column('first_name',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=150),
               existing_nullable=True)
        batch_op.alter_column('password',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=150),
               existing_nullable=True)
        batch_op.alter_column('email_address',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=150),
               existing_nullable=True)

    # ### end Alembic commands ###