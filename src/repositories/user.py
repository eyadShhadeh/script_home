from src.models.user import User
from typing import Tuple


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
