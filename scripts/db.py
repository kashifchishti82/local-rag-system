from alembic.config import Config
from alembic import command
import os
import sys

def init_db():
    """Initialize the database with initial schema."""
    from rag_system.db import init_db
    init_db()

def create_migration(message: str):
    """Create a new database migration."""
    alembic_cfg = Config("alembic.ini")
    command.revision(alembic_cfg, message=message, autogenerate=True)

def upgrade_db():
    """Upgrade the database to the latest version."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

def downgrade_db(revision: str = "-1"):
    """Downgrade the database to a previous version."""
    alembic_cfg = Config("alembic.ini")
    command.downgrade(alembic_cfg, revision)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Database management commands')
    subparsers = parser.add_subparsers(dest='command')
    
    init_parser = subparsers.add_parser('init', help='Initialize the database')
    migrate_parser = subparsers.add_parser('migrate', help='Create a new migration')
    migrate_parser.add_argument('message', help='Migration message')
    upgrade_parser = subparsers.add_parser('upgrade', help='Upgrade to latest version')
    downgrade_parser = subparsers.add_parser('downgrade', help='Downgrade to previous version')
    downgrade_parser.add_argument('--revision', default='-1', help='Revision to downgrade to')
    
    args = parser.parse_args()
    
    if args.command == 'init':
        init_db()
    elif args.command == 'migrate':
        create_migration(args.message)
    elif args.command == 'upgrade':
        upgrade_db()
    elif args.command == 'downgrade':
        downgrade_db(args.revision)
    else:
        parser.print_help()
