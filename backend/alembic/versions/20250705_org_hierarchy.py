"""
Revision ID: org_hierarchy
Revises: 
Create Date: 2025-07-05
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'org_hierarchy'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'organization_nodes',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('type', sa.Enum('department', 'project', name='organizationnodetype'), nullable=False),
        sa.Column('parent_id', sa.Integer, sa.ForeignKey('organization_nodes.id'), nullable=True),
        sa.Column('description', sa.String, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )
    op.add_column('data_quality_checks', sa.Column('project_id', sa.Integer, sa.ForeignKey('organization_nodes.id'), nullable=True))
    op.drop_column('data_quality_checks', 'organization')

def downgrade():
    op.add_column('data_quality_checks', sa.Column('organization', sa.String, nullable=True))
    op.drop_column('data_quality_checks', 'project_id')
    op.drop_table('organization_nodes')
