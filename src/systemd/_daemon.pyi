from typing import Sequence
from socket import AF_UNSPEC

__version__: str
LISTEN_FDS_START: int

def _is_mq(fd: int, path: str | None = None, /) -> bool: ...
def _is_socket_unix(
    fd: int, type: int = 0, listening: int = -1, path: str | None = None, /
) -> bool: ...
def _is_socket_sockaddr(
    fd: int, address: str, type: int = 0, flowinfo: int = 0, listening: int = -1, /
) -> bool: ...
def _is_socket_inet(
    fd: int,
    family: int = AF_UNSPEC,
    type: int = 0,
    listening: int = -1,
    port: int = 0,
    /,
) -> bool: ...
def _is_socket(
    fd: int, family: int = AF_UNSPEC, type: int = 0, listening: int = -1, /
) -> bool: ...
def _is_fifo(fd: int, path: str | None = None, /) -> bool: ...
def _listen_fds(unset_environment: bool = True) -> int: ...
def _listen_fds_with_names(
    unset_environment: bool = False,
) -> tuple[str | int, ...]: ...
def notify(
    status: str,
    unset_environment: bool = False,
    pid: int = 0,
    fds: Sequence[int] | None = None,
) -> bool: ...
def booted() -> bool: ...

__all__ = ["LISTEN_FDS_START", "notify", "booted"]
