"""empty message

Revision ID: 9e86ec416866
Revises: 
Create Date: 2021-03-10 19:35:39.883577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e86ec416866'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cron_jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('enable', sa.Boolean(), nullable=True),
    sa.Column('technology', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cron_jobs_id'), 'cron_jobs', ['id'], unique=False)
    op.create_table('arguments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('value', sa.String(length=256), nullable=True),
    sa.Column('cron_job_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cron_job_id'], ['cron_jobs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_arguments_id'), 'arguments', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_arguments_id'), table_name='arguments')
    op.drop_table('arguments')
    op.drop_index(op.f('ix_cron_jobs_id'), table_name='cron_jobs')
    op.drop_table('cron_jobs')
    # ### end Alembic commands ###
