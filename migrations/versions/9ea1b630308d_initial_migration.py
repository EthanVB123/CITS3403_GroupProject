"""Initial migration

Revision ID: 9ea1b630308d
Revises: 19d4eb6cb2fb
Create Date: 2025-05-02 09:36:22.596652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ea1b630308d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'puzzle',
        sa.Column('puzzle_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('num_rows', sa.Integer(), nullable=False),
        sa.Column('num_columns', sa.Integer(), nullable=False),
        sa.Column('row_clues', sa.PickleType(), nullable=False),
        sa.Column('column_clues', sa.PickleType(), nullable=False),
        sa.Column('number_players_solved', sa.Integer(), nullable=False)
    )


def downgrade():
    op.drop_table('puzzle')
