"""
This is the only script that seems to work as intended.

CMD:
    PYTHONPATH=. pipenv run python repro/test_dataloaders_asyncio.py
"""
import asyncio
import json
from graphql.execution.execute import ExecutionResult
from promise import promise
from promise.schedulers.asyncio import AsyncioScheduler
from repro.schema import schema, friends_query, user_loader

# Force the promise library to use AsyncioScheduler to enable batching in dataloaders
promise.set_default_scheduler(AsyncioScheduler())


async def get_friends() -> ExecutionResult:
    result = await schema.execute_async(friends_query)
    if result.errors:
        raise result.errors[0]
    print(json.dumps(result.data))
    print(user_loader.call_count)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_friends())
