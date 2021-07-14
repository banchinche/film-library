"""empty message

Revision ID: c0d0298bdc53
Revises: 66dc7254b738
Create Date: 2021-07-14 11:58:47.840673

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c0d0298bdc53'
down_revision = '66dc7254b738'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Director',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('created', postgresql.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Genre',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('created', postgresql.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('User',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=False),
    sa.Column('password', sa.VARCHAR(), nullable=False),
    sa.Column('is_admin', sa.BOOLEAN(), nullable=False),
    sa.Column('created', postgresql.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('Movie',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), nullable=False),
    sa.Column('rate', sa.SMALLINT(), nullable=False),
    sa.Column('year', sa.SMALLINT(), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('poster', sa.VARCHAR(length=255), nullable=False),
    sa.Column('director_id', sa.INTEGER(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('created', postgresql.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['director_id'], ['Director.id'], ondelete='SET null'),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('MovieGenre',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('movie_id', sa.INTEGER(), nullable=False),
    sa.Column('genre_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['genre_id'], ['Genre.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['movie_id'], ['Movie.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('MovieGenre')
    op.drop_table('Movie')
    op.drop_table('User')
    op.drop_table('Genre')
    op.drop_table('Director')
    # ### end Alembic commands ###
