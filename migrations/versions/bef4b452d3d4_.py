"""empty message

Revision ID: bef4b452d3d4
Revises: 6de4259760ee
Create Date: 2019-09-11 14:12:59.116700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bef4b452d3d4'
down_revision = '6de4259760ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_likes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_likes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='post_likes_post_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='post_likes_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='post_likes_pkey')
    )
    # ### end Alembic commands ###
