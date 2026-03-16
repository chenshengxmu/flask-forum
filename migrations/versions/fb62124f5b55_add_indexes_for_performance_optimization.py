"""Add indexes for performance optimization

Revision ID: fb62124f5b55
Revises: 0c0f2ef770e3
Create Date: 2026-03-16 20:39:39.586369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb62124f5b55'
down_revision = '0c0f2ef770e3'
branch_labels = None
depends_on = None


def upgrade():
    # Add indexes on foreign keys for better join performance
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.create_index('ix_posts_author_id', ['author_id'], unique=False)
        batch_op.create_index('ix_posts_category_id_created_at', ['category_id', 'created_at'], unique=False)

    with op.batch_alter_table('replies', schema=None) as batch_op:
        batch_op.create_index('ix_replies_author_id', ['author_id'], unique=False)
        batch_op.create_index('ix_replies_post_id_created_at', ['post_id', 'created_at'], unique=False)


def downgrade():
    # Remove indexes
    with op.batch_alter_table('replies', schema=None) as batch_op:
        batch_op.drop_index('ix_replies_post_id_created_at')
        batch_op.drop_index('ix_replies_author_id')

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_index('ix_posts_category_id_created_at')
        batch_op.drop_index('ix_posts_author_id')
