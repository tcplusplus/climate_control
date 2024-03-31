import asyncio
import logging

from climate_control import ClimateControl
from cronbase import CronBase
import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from crons.collect_climate_cron import CollectClimateCron
from webhandlerbase import WebHandlerBase
from webhandlers.climate_handler import ClimateHandler


class ClimateControlService(FastAPI):
    def __init__(self, port: int) -> None:
        super().__init__()
        self.running = False
        self.port = port
        self.climate_control = ClimateControl()
        server_config = uvicorn.Config(self, host='0.0.0.0', port=port, log_level="info")
        self.__crons: list[CronBase] = []
        self.server = uvicorn.Server(server_config)
        self.add_webhandler('/climate', ClimateHandler(self.climate_control))
        self.add_cron(CollectClimateCron(self.climate_control))
        self.allow_cors()

    def start(self) -> None:
        """
        Start the server
        """
        self.running = True
        try:
            asyncio.run(self.__run_async())
        except Exception as error:  # pylint: disable=broad-except
            logging.error('Error during start: %r', error)

    async def main(self) -> None:
        """
        An infinite loop checking for incoming events from buttons and responding to it
        """
        try:
            while self.running:
                await asyncio.sleep(0.1)
            self.server.should_exit = True
        except Exception as error:  # pylint: disable=broad-except
            logging.error('Error during main: %r', error)

    async def __run_async(self) -> None:
        try:
            jobs = []
            for cron in self.__crons:
                jobs.append(cron.run())
            jobs += [self.main()]
            main_thread = asyncio.gather(*jobs)
            await self.server.serve()
            main_thread.done()
        except Exception as error:  # pylint: disable=broad-except
            logging.error('Error during __run_async: %r', error)

    def allow_cors(self) -> None:
        """
        Allow CORS requests
        usefull to enable for local development
        """
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # pylint: disable=too-complex
    def add_webhandler(self, path: str, handler: WebHandlerBase) -> None:
        """
        Add a webhandler to the server
        :param path: The path to the handler
        :param handler: The handler
        """
        try:
            if handler.get:                             # type: ignore
                self.add_api_route(path,
                                   handler.get,  # type: ignore
                                   methods=['GET'])
        except: # pylint: disable=bare-except
            pass
        try:
            if handler.post:                            # type: ignore
                self.add_api_route(path,
                                   handler.post,        # type: ignore
                                   methods=['POST'])
        except: # pylint: disable=bare-except
            pass
        try:
            if handler.put:                             # type: ignore
                self.add_api_route(path,
                                   handler.put,         # type: ignore
                                   methods=['PUT'])
        except: # pylint: disable=bare-except
            pass
        try:
            if handler.delete:                          # type: ignore
                self.add_api_route(path,
                                   handler.delete,      # type: ignore
                                   methods=['DELETE'])
        except: # pylint: disable=bare-except
            pass

    @property
    def crons(self) -> list[CronBase]:
        """
        Get all cron jobs
        """
        return self.__crons

    def add_cron(self, cron: CronBase) -> None:
        """
        Add a cron job
        """
        if self.running:
            raise RuntimeError('Cannot add cron job while server is running')
        self.__crons.append(cron)

if __name__ == '__main__':
    app = ClimateControlService(port=8000)
    app.start()