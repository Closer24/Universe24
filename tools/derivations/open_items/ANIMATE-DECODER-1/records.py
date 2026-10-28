"""The decoder's record reader (Animate; staged here until stage 0a gives src/tensor24/decoder/, then moved whole).

One record of the schema is read line by line into its header, its events and its end, with the schema's rules checked
as it reads: the header first and the end last, the major version known (an older minor read unchanged), and the
events in the schema's order (round, kind, site, train). A record that breaks a rule is not read, and the cause is named;
nothing is raised. The standard library alone: nothing of the engine or the runner, and no numpy.
"""

import json

RECORD = "tensor24.record"
MAJOR = 1
KINDS = ("whole", "split", "books", "turnover", "rate")


class Record:
    """A record read: its header, its events in order, and its end."""

    def __init__(self, header, events, end):
        self.header, self.events, self.end = header, events, end

    def of(self, kind):
        return [e for e in self.events if e["kind"] == kind]


def place(e):
    """An event's place in the schema's order."""
    return (e["round"], KINDS.index(e["kind"]), e["site"], e.get("train", 0))


def read(path):
    """The record at path, or None and the cause it is not read."""
    with open(path) as f:
        lines = [json.loads(text) for text in f]
    header, *events, end = lines
    if header.get("kind") != "header" or header.get("record") != RECORD:
        return None, "the first line is no header of the schema"
    if header["version"][0] != MAJOR:
        return None, f"the major version {header['version'][0]} is unknown"
    if end.get("kind") != "end":
        return None, "the record has no end line"
    unknown = sorted({e["kind"] for e in events} - set(KINDS))
    if unknown:
        return None, f"unknown line kinds {unknown}"
    places = [place(e) for e in events]
    if places != sorted(places):
        return None, "the events stand out of the schema's order"
    return Record(header, events, end), None
