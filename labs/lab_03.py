from asyncio import TaskGroup
from random import random
import asyncio
import logging
from typing import Coroutine, Iterable

logging.basicConfig(level=logging.INFO)


class TaskErrorAlpha(BaseException):

    def __repr__(self) -> str:
        return f"TaskErrorAlpha: {super().__repr__()}"


class TaskErrorBeta(BaseException):

    def __repr__(self) -> str:
        return f"TaskErrorBeta: {super().__repr__()}"


async def my_async_task():

    delay = random()

    if delay < 0.5:
        logging.info(f"delay {delay}")
    elif delay < 0.8:
        raise TaskErrorAlpha(f"error {delay}")
    else:
        raise TaskErrorBeta(f"error {delay}")


async def my_task_group(tasks: Iterable[Coroutine]):

    async with TaskGroup() as tg:
        for task in tasks:
            tg.create_task(task)


async def main():

    try:
        await my_task_group([my_async_task() for _ in range(10)])
    except* TaskErrorAlpha as eg_alpha:
        logging.error(f"catch alpha error {eg_alpha.exceptions}")
    except* TaskErrorBeta as eg_beta:
        logging.error(f"catch beta error {eg_beta.exceptions}")


if __name__ == "__main__":

    asyncio.run(main())
