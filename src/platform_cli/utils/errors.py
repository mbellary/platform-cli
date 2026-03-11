from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CLIError(Exception):
    message: str
    exit_code: int = 1

    def __str__(self) -> str:
        return self.message


class ConfigLoadError(CLIError):
    exit_code = 2


class AuthError(CLIError):
    exit_code = 3


class TransportError(CLIError):
    exit_code = 4


class ServerError(CLIError):
    exit_code = 5


class ValidationError(CLIError):
    exit_code = 6
