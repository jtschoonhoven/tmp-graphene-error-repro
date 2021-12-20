"""
This script fails with "GraphQLError: 'Promise' object has no attribute 'best_friend_id'"

CMD:
    PYTHONPATH=. pipenv run python repro/test_dataloaders.py
"""
import json
from repro.schema import schema, friends_query, user_loader


if __name__ == '__main__':
    result = schema.execute(friends_query)
    if result.errors:
        raise result.errors[0]
    print(json.dumps(result.data))
    print(user_loader.call_count)
