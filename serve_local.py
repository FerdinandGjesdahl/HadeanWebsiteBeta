#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import os
import socket
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


DEFAULT_PORT = 4173


def find_open_port(start_port: int, host: str) -> int:
    port = start_port
    while True:
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((host, port))
                return port
            except OSError:
                port += 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the Hadean Ventures site locally.")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host interface to bind to. Defaults to 127.0.0.1.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Preferred port to bind to. Defaults to {DEFAULT_PORT}.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    os.chdir(root)

    port = find_open_port(args.port, args.host)
    handler = partial(SimpleHTTPRequestHandler, directory=str(root))
    server = ThreadingHTTPServer((args.host, port), handler)

    print(f"Serving {root.name} at http://{args.host}:{port}")
    if port != args.port:
        print(f"Requested port {args.port} was unavailable, using {port} instead.")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
