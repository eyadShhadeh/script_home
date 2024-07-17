import os


import sqlalchemy as sa
from sqlalchemy import MetaData

pool_size = int(os.getenv('SQLALCHEMY_POOL_SIZE', 10))


def get_db_url():
    return 'postgresql://%s:%s@%s:%s/%s' % (
        os.getenv('PGUSER', 'postgres'),
        os.getenv('PGPASSWORD', 'password'),
        os.getenv('PGHOST', 'home-script-db'),
        os.getenv('PGPORT', '5432'),
        os.getenv('PGDATABASE', 'postgres'),
    )


engine = sa.create_engine(get_db_url(), echo=False,
                          echo_pool=True, pool_size=pool_size, max_overflow=16)

metadata: MetaData = sa.MetaData()
