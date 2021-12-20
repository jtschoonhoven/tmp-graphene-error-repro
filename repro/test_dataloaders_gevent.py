"""
This script fails with "GraphQLError: 'Promise' object has no attribute 'best_friend_id'"
It also raises an AssertionError on "assert self.is_tick_used"

CMD:
    PYTHONPATH=. pipenv run python repro/test_dataloaders_gevent.py
"""
from gevent import monkey

monkey.patch_all()

import json
from promise import promise
from promise.schedulers.gevent import GeventScheduler
from repro.schema import schema, friends_query, user_loader

promise.set_default_scheduler(GeventScheduler())


if __name__ == '__main__':
    result = schema.execute(friends_query)
    if result.errors:
        raise result.errors[0]
    print(json.dumps(result.data))
    print(user_loader.call_count)
