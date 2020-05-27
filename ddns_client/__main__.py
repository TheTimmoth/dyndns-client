#!/usr/bin/python3

from contextlib import redirect_stdout
from time import strftime

from .ddns_client import DDNSClient
from .io_ import read_file
from .io_ import write_file
from .settings import Settings

_DEFAULT_SETTINGS = {
    "logToFile": False,
    "logPath": "/var/log/ddns",
    "servers": "./servers.json",
}

_SETTINGS_PATH = "./settings.json"


def start_client(settings: Settings):
  DDNSClient(settings["servers"])


def main():
  settingsFile = read_file(_SETTINGS_PATH)
  settings = Settings(settingsFile, _DEFAULT_SETTINGS)

  # Write settings file if it does not exist and exit
  if not settingsFile:
    write_file(_SETTINGS_PATH, str(settings))
    print(
        strftime("%Y-%m-%d %H:%M:%S ") +
        f"Settings file created at {_SETTINGS_PATH}. Please edit settings first."
    )
    print(strftime("%Y-%m-%d %H:%M:%S ") + "Bye")
    exit()

  if settings["logToFile"]:
    f = open(settings["logPath"], mode="a", buffering=1)
    with redirect_stdout(f):
      start_client(settings)
  else:
    start_client(settings)


if __name__ == "__main__":
  main()
