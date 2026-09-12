"""Append-only JSON histories with an on-disk index and bounded export buffers."""

import json
from collections.abc import Iterator, Mapping, Sequence
from contextlib import suppress
from pathlib import Path
from struct import Struct
from tempfile import TemporaryFile
from types import TracebackType
from typing import Self, TextIO, cast, overload

_ENTRY = Struct("<QQ")
_COPY_BYTES = 65536


class JsonArchive[T](Sequence[T]):
    """Single-owner history; indexing loads one item and iteration loads one at a time.

    Encoded data and fixed-size index entries both stay on disk. Values read back
    have JSON types, so tuples become lists. The writer owns neither physics nor
    a growing in-memory offset table. Closing deletes both temporary files.
    """

    def __init__(self, directory: Path | None = None) -> None:
        self._data = TemporaryFile(mode="w+b", dir=directory)
        try:
            self._index = TemporaryFile(mode="w+b", dir=directory)
        except BaseException:
            self._data.close()
            raise
        self._count = 0

    @property
    def closed(self) -> bool:
        return self._data.closed

    def __len__(self) -> int:
        return self._count

    def append(self, value: T) -> None:
        self._data.seek(0, 2)
        start = self._data.tell()
        index_start = self._count * _ENTRY.size
        try:
            for piece in json.JSONEncoder().iterencode(value):
                self._data.write(piece.encode("utf-8"))
            size = self._data.tell() - start
            self._index.seek(index_start)
            self._index.write(_ENTRY.pack(start, size))
        except BaseException:
            # A failed encode must not publish a partial item or corrupt its prefix.
            with suppress(OSError):
                self._data.truncate(start)
                self._index.truncate(index_start)
            raise
        self._count += 1

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> list[T]: ...

    def __getitem__(self, index: int | slice) -> T | list[T]:
        if isinstance(index, slice):
            return [self[position] for position in range(*index.indices(self._count))]
        position = index + self._count if index < 0 else index
        if not 0 <= position < self._count:
            raise IndexError("archive index out of range")
        self._index.seek(position * _ENTRY.size)
        start, size = _ENTRY.unpack(self._index.read(_ENTRY.size))
        self._data.seek(start)
        return cast(T, json.loads(self._data.read(size)))

    def json_chunks(self) -> Iterator[str]:
        """Export existing bytes without decoding any complete history item."""
        yield "["
        for position in range(self._count):
            if position:
                yield ", "
            self._index.seek(position * _ENTRY.size)
            start, remaining = _ENTRY.unpack(self._index.read(_ENTRY.size))
            while remaining:
                self._data.seek(start)
                chunk = self._data.read(min(remaining, _COPY_BYTES))
                if not chunk:
                    raise OSError("archive data ended before its indexed item")
                remaining -= len(chunk)
                start += len(chunk)
                # JSONEncoder's default ensure_ascii keeps every byte ASCII.
                yield chunk.decode("ascii")
        yield "]"

    def close(self) -> None:
        try:
            self._data.close()
        finally:
            self._index.close()

    def __enter__(self) -> Self:
        if self.closed:
            raise ValueError("archive is closed")
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()


def _json_chunks(value: object) -> Iterator[str]:
    if isinstance(value, JsonArchive):
        yield from value.json_chunks()
    elif isinstance(value, Mapping):
        yield "{"
        for index, (key, item) in enumerate(value.items()):
            if index:
                yield ", "
            # JSON object keys in all run/observer/recording schemas are strings.
            if not isinstance(key, str):
                raise TypeError("archive JSON object keys must be strings")
            yield json.dumps(key)
            yield ": "
            yield from _json_chunks(item)
        yield "}"
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        yield "["
        for index, item in enumerate(value):
            if index:
                yield ", "
            yield from _json_chunks(item)
        yield "]"
    else:
        yield from json.JSONEncoder().iterencode(value)


def write_json(stream: TextIO, value: object, *, escape_html: bool = False) -> None:
    """Stream ordinary data and nested archives using the ordinary JSON encoding."""
    for chunk in _json_chunks(value):
        stream.write(chunk.replace("<", "\\u003c") if escape_html else chunk)
