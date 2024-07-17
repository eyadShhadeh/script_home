import logging
import csv
import os
from typing import Generator
from uuid import uuid4

from src.models.user import User

CHUNK_SIZE = int(os.getenv('chunk_size', '10000'))

logger = logging.getLogger(__name__)


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
