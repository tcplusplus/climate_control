import abc
import asyncio
import logging

class CronBase:
    """
    Cron jobs that regularly run while the service is idle
    """
    def __init__(self) -> None:
        self.running = False

    def stop(self) -> None:
        """
        Stop the cron job
        """
        self.running = False

    async def run(self) -> None:
        """
        Run the cron job for all variants
        """
        self.running = True
        while self.running:
            if self.should_run():
                try:
                    await self.run_once()
                except Exception as error:  # pylint: disable=broad-except
                    logging.error('Cron job %s failed with error: %r', self.__class__.__name__, error)
            await asyncio.sleep(0.1)
        self.running = False

    @abc.abstractmethod
    def should_run(self) -> bool:
        """
        Check if the cron job should run
        """

    @abc.abstractmethod
    async def run_once(self) -> None:
        """
        Run the cron job once if should_run is True
        """