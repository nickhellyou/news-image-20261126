#!/usr/bin/env python3
"""news-image-20261126 entry: copy the bundled front page to the output dir.

Stdlib only. The image was drawn at build time by the builder's compose
script; this program only validates and copies it, so two runs write
byte-identical bytes.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
EXPECTED_SHA256 = (
    "bd9946c004d131ba641037886d52224ece04efe2dd99b7aea59617d8a4e28e6a"
)
MAX_BYTES = 1048576
MAX_DIM = 1024
IEND = b"\x00\x00\x00\x00IEND\xaeB`\x82"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    with open(SRC, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit("entry.png is not a PNG")
    if len(data) > MAX_BYTES:
        sys.exit("entry.png exceeds 1 MiB")
    if data[-12:] != IEND:
        sys.exit("entry.png has no IEND trailer")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        sys.exit("entry.png exceeds 1024x1024")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        sys.exit("entry.png sha256 mismatch")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as fh:
        fh.write(data)
    print(f"entry.png: {len(data)} bytes, {width}x{height}, sha256 {digest}")


if __name__ == "__main__":
    main()
