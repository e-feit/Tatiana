"""create plan table

Revision ID: 315181ca5d54
Revises: a6a8325e1f45
Create Date: 2019-03-31 14:58:14.002991

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = '315181ca5d54'
down_revision = 'a6a8325e1f45'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()

    if 'plan' not in tables:
        op.create_table('plan',
        sa.Column('id', sa.Integer(), nullable=False, comment='id строки плана'),
        sa.Column('pin', sa.SmallInteger(), nullable=False, comment='выходной пин'),
        sa.Column('ontime', sa.CHAR(length=255), nullable=False, comment='время включения (hh:mm:ss)'),
        sa.Column('offtime', sa.CHAR(length=255), nullable=False, comment='время выключения (hh:mm:ss)'),
        sa.Column('calendar', sa.CHAR(length=255), nullable=False, comment='1-будни, 2-выхи, 3-ежедневно'),
        sa.PrimaryKeyConstraint('id')
        )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('plan')
    # ### end Alembic commands ###