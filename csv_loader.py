import logging
import csv
import os
from uuid import uuid4, UUID
from sqlalchemy import Table, Column, SmallInteger, String, MetaData, insert, DateTime
import sqlalchemy as sa
from pydantic import BaseModel
from typing import Generator, Tuple
from datetime import datetime

CHUNK_SIZE = int(os.getenv('chunk_size', '10000'))

logger = logging.getLogger(__name__)


def get_db_url() -> str:
    return 'postgresql://%s:%s@%s:%s/%s' % (
        os.getenv('PGUSER', 'postgres'),
        os.getenv('PGPASSWORD', 'password'),
        os.getenv('PGHOST', 'si-tech-db'),
        os.getenv('PGPORT', '5432'),
        os.getenv('PGDATABASE', 'postgres'),
    )


engine = sa.create_engine(get_db_url(), echo=False,
                          echo_pool=True, pool_size=10, max_overflow=16)
metadata = MetaData()
metadata.bind = engine

users = Table(
    "user",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("first_name", String(50)),
    Column("last_name", String(50), nullable=False),
    Column("address", String(50)),
    Column("age", SmallInteger, nullable=False),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('updated_at', DateTime),

)


class User(BaseModel):
    user_id: UUID = uuid4()
    first_name: str
    last_name: str
    address: str
    age: int


def file_reader(path: str = "./test_data.csv") -> Generator:
    """
    Generator reads rows from a path in given path or takes default local path.

    Yields:
        Generator: File rows data
    """
    logger.info(f'Processing csv file in: {path}')
    try:
        with open(path, encoding=str) as content:
            for row in csv.DictReader(content):
                yield row
    except Exception:
        logger.warning(
            'Failed to process the CSV file', exc_info=True)


def data_loader():
    """
    Load data incoming from file into its model and data chunk for easier insertion.
    """
    buffer = []
    for row in file_reader():
        # adding model parsing layer for data-type validation
        user = User(
            user_id=uuid4(),
            first_name=row["first name"],
            last_name=row["last name"],
            address=row["address"],
            age=row["age"]
        )
        buffer.append(user)
        buffer = chunk_persist(buffer=buffer)

    if len(buffer) != 0:
        chunk_persist(buffer, True)


def chunk_persist(buffer: list, is_final: bool = False):
    """Insert data to db when it reaches the desired chunk size.

    Args:
        buffer (list): data objects list.
        is_final (bool, optional): Flag for the data remnant. Defaults to False.
    """
    if len(buffer) == CHUNK_SIZE or is_final:
        persist_user(buffer)
        buffer.clear()


def persist_user(persisted_users: Tuple[User, ...]) -> None:
    """Persist user data into the data base.

    Args:
        persisted_users (Tuple[User, ...]): Inserted data
    """
    user_values = []
    for user in persisted_users:
        user_values.append(
            {
                'id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'address': user.address,
                'age': user.age,
            }
        )

    insert_stmt = insert(users).values(user_values)
    insert_stmt.on_conflict_do_update(
        index_elements=[
            users.c.id,
            users.c.first_name,
            users.c.last_name,
        ],
        set_=dict(
            address=insert_stmt.excluded.address,
            age=insert_stmt.excluded.age,
        ),
    ).execute()


if __name__ == '__main__':
    data_loader()
