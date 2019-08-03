#!/usr/bin/env python
"""Barrier WSGI Service.

This script will serve WSGI requests at the bound address and port using the given number of workers.

"""
from typing import Mapping, Union

import click
from flask import Flask
from gunicorn.app.base import BaseApplication

from .app import app


class BarrierApplication(BaseApplication):
    """Bare-bones Gunicorn WSGI Application.

    Parameters
    ----------
    application : Flask
        Barrier app
    settings : Mapping[str, Union[str, int]]
        WSGI Server Options:
        -  bind: [str "HOST:PORT"]
        -  workers: [int NUMBER OF WORKERS]

    """

    def __init__(self, application: Flask, settings: Mapping[str, Union[str, int]] = None):
        self.application = application
        self.settings = settings
        super().__init__()

    def __is_valid_setting(self, key: str, value: Union[str, int]) -> bool:
        """Validate that key is a canonical setting and value is non-null."""
        return key in self.cfg.settings and value is not None

    def load_config(self):
        """Load and validate configuration."""
        validated_options = {key: value for key, value in self.settings.items() if self.__is_valid_setting(key, value)}
        for key, value in validated_options.items():
            self.cfg.set(key.lower(), value)

    def load(self) -> Flask:
        """Load the request handler."""
        return self.application


@click.option("-b", "--bind", default="127.0.0.1:8000")
@click.option("-w", "--workers", default=4)
@click.command()
def main(bind, workers):
    """Run the WSGI service."""
    BarrierApplication(app, locals()).run()


if __name__ == "__main__":
    main()
