"""empty message

Revision ID: 002_auth0_user
Revises: 001_init
Create Date: 2024-10-19 09:57:26.515121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002_auth0_user'
down_revision: Union[str, None] = '001_init'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 前処理
    pre_upgrade()

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth_auth0_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sub', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('nickname', sa.String(length=50), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_auth_auth0_users_sub'), 'auth_auth0_users', ['sub'], unique=True)
    # ### end Alembic commands ###

    # 後処理
    post_upgrade()


def downgrade() -> None:
    # 前処理
    pre_downgrade()

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_auth_auth0_users_sub'), table_name='auth_auth0_users')
    op.drop_table('auth_auth0_users')
    # ### end Alembic commands ###

    # 後処理
    post_downgrade()

def pre_upgrade():
    # スキーマ更新前に実行する必要がある処理
    pass


def post_upgrade():
    # スキーマ更新後に実行する必要がある処理
    pass


def pre_downgrade():
    # スキーマ更新前に実行する必要がある処理
    pass


def post_downgrade():
    # スキーマ更新後に実行する必要がある処理
    pass
