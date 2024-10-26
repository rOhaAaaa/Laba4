"""Add brand column to access_points

Revision ID: 6597ecd33220
Revises: f18fae1197bc
Create Date: 2024-10-26 19:18:41.863823

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6597ecd33220'
down_revision = 'f18fae1197bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('access_points', schema=None) as batch_op:
        batch_op.add_column(sa.Column('brand', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('model', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('serial_number', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('office_id', sa.Integer(), nullable=True))
        
        # Задайте ім'я унікальному обмеженню
        batch_op.create_unique_constraint('uq_access_points_serial_number', ['serial_number'])
        
        # Задайте ім'я зовнішньому ключу
        batch_op.create_foreign_key('fk_access_points_office_id', 'offices', ['office_id'], ['office_id'])
        
        batch_op.drop_column('model_name')
        batch_op.drop_column('bandwidth')

    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('access_points', schema=None) as batch_op:
        
        
        # Зніміть обмеження за іменем
        batch_op.drop_constraint('fk_access_points_office_id', type_='foreignkey')
        batch_op.drop_constraint('uq_access_points_serial_number', type_='unique')
        
        batch_op.drop_column('office_id')
        batch_op.drop_column('serial_number')
        batch_op.drop_column('model')
        batch_op.drop_column('brand')

    # ### end Alembic commands ###