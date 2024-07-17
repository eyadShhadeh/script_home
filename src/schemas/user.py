from sqlalchemy import Table, Column, SmallInteger, String, DateTime
from src.util.db import metadata
from datetime import datetime
from uuid import UUID


users = Table(
    'users',
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("first_name", String(50)),
    Column("last_name", String(50), nullable=False),
    Column("address", String(50)),
    Column("age", SmallInteger, nullable=False),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('updated_at', DateTime),
)
