"""empty message

Revision ID: 161e79ab949c
Revises: 012a7ab65ce0
Create Date: 2016-08-10 15:11:53.837050

"""

# revision identifiers, used by Alembic.
revision = '161e79ab949c'
down_revision = '012a7ab65ce0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friendship',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('actioning_user_id', sa.Integer(), nullable=True),
    sa.Column('recieving_user_id', sa.Integer(), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['actioning_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['recieving_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('actioning_user_id', 'recieving_user_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('friendship')
    ### end Alembic commands ###
