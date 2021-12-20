# Graphene Dataloader Errors Repro

##### A minimal app to reproduce dataloader errors with Graphene

This repo is an attempt to implement [the dataloaders example from the Graphene docs](https://docs.graphene-python.org/en/latest/execution/dataloader/). My finding is that dataloaders _only_ work inside an asyncio event loop with promises manually configured to use `AsyncioScheduler`. Dataloaders seem to fail completely when called synchronously or via gevent's event loop.

Since the Graphene docs don't say anything about asyncio being a requirement, I assume this must either be a bug in Graphene or an error in my implementation (in which case it would be nice to see a working example documented).

```sh
pipenv sync && pipenv shell  # if using pipenv, else `pip install -r requirements.txt`
PYTHONPATH=. python repro/test_dataloaders.py  # FAILS
PYTHONPATH=. python repro/test_dataloaders_gevent.py  # FAILS
PYTHONPATH=. python repro/test_dataloaders_asyncio.py  # WORKS
```
