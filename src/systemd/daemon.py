# SPDX-License-Identifier: LGPL-2.1-or-later

import typing as _typing
from socket import AF_UNSPEC as _AF_UNSPEC

from ._daemon import (__version__,
                      booted,
                      notify,
                      _listen_fds,
                      _listen_fds_with_names,
                      _is_fifo,
                      _is_socket,
                      _is_socket_inet,
                      _is_socket_sockaddr,
                      _is_socket_unix,
                      _is_mq,
                      LISTEN_FDS_START)

class _FileObject(_typing.Protocol):
    def fileno(self) -> int:
        ...

def _convert_fileobj(fileobj: _FileObject | int) -> int:
    if isinstance(fileobj, int):
        return fileobj
    else:
        return fileobj.fileno()

def is_fifo(fileobj: _FileObject | int, path: str | None=None) -> bool:
    fd = _convert_fileobj(fileobj)
    return _is_fifo(fd, path)

def is_socket(fileobj: _FileObject |int, family: int=_AF_UNSPEC, type: int=0, listening: int=-1) -> bool:
    fd = _convert_fileobj(fileobj)
    return _is_socket(fd, family, type, listening)

def is_socket_inet(fileobj: _FileObject | int, family: int=_AF_UNSPEC, type: int=0, listening: int=-1, port: int=0) -> bool:
    fd = _convert_fileobj(fileobj)
    return _is_socket_inet(fd, family, type, listening, port)

def is_socket_sockaddr(fileobj: _FileObject | int, address: int, type: int=0, flowinfo: int=0, listening: int=-1) -> bool:
    """Check socket type, address and/or port, flowinfo, listening state.

    Wraps sd_is_socket_inet_sockaddr(3).

    `address` is a systemd-style numerical IPv4 or IPv6 address as used in
    ListenStream=. A port may be included after a colon (":").
    See systemd.socket(5) for details.

    Constants for `family` are defined in the socket module.
    """
    fd = _convert_fileobj(fileobj)
    return _is_socket_sockaddr(fd, address, type, flowinfo, listening)

def is_socket_unix(fileobj: _FileObject | int, type: int=0, listening: int=-1, path: str | None=None) -> bool:
    fd = _convert_fileobj(fileobj)
    return _is_socket_unix(fd, type, listening, path)

def is_mq(fileobj: _FileObject | int, path: str | None=None) -> bool:
    fd = _convert_fileobj(fileobj)
    return _is_mq(fd, path)

def listen_fds(unset_environment: bool=True) -> list[int]:
    """Return a list of socket activated descriptors

    Example::

      (in primary window)
      $ systemd-socket-activate -l 2000 python3 -c \\
          'from systemd.daemon import listen_fds; print(listen_fds())'
      (in another window)
      $ telnet localhost 2000
      (in primary window)
      ...
      Execing python3 (...)
      [3]
    """
    num = _listen_fds(unset_environment)
    return list(range(LISTEN_FDS_START, LISTEN_FDS_START + num))

def listen_fds_with_names(unset_environment: bool=True) -> dict[int, str]:
    """Return a dictionary of socket activated descriptors as {fd: name}

    Example::

      (in primary window)
      $ systemd-socket-activate -l 2000 -l 4000 --fdname=2K:4K python3 -c \\
          'from systemd.daemon import listen_fds_with_names; print(listen_fds_with_names())'
      (in another window)
      $ telnet localhost 2000
      (in primary window)
      ...
      Execing python3 (...)
      [3]
    """
    composite = _listen_fds_with_names(unset_environment)
    retval: dict[int, str] = {}
    for i in range(0, _typing.cast(int, composite[0])):
        retval[i+LISTEN_FDS_START] = _typing.cast(str, composite[1+i])
    return retval
