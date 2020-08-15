"""Classes to help interacting with pytest nodeids."""

import collections
from typing import List

NodeidFragment = collections.namedtuple("NodeidFragment", ["val", "is_path"])


class Nodeid:
    """Wraps a nodeid string and helps with splitting into components."""

    _PATH_SEP = "/"
    _NONPATH_SEP = "::"

    def __init__(self, raw_nodeid: str, fragments: List[NodeidFragment]):
        self._raw_nodeid = raw_nodeid
        self._fragments = fragments

    @classmethod
    def from_string(cls, raw_nodeid: str) -> "Nodeid":
        raw_components = raw_nodeid.split("::")
        path_components = [
            NodeidFragment(val=frag, is_path=True)
            for frag in raw_components[0].split("/")
        ]
        nonpath_components = [
            NodeidFragment(val=frag, is_path=False) for frag in raw_components[1:]
        ]
        fragments = path_components + nonpath_components
        return cls(raw_nodeid, fragments)

    @classmethod
    def from_fragments(cls, fragments: List[NodeidFragment]) -> "Nodeid":
        if not fragments:
            return cls("", [])

        str_components = [fragments[0].val]
        for frag in fragments[1:]:
            separator = cls._PATH_SEP if frag.is_path else cls._NONPATH_SEP
            str_components.append(separator)
            str_components.append(frag.val)

        raw_nodeid = "".join(str_components)
        return cls(raw_nodeid, fragments)

    def __iter__(self):
        return iter(self._fragments)

    def __str__(self):
        return self._raw_nodeid

    @property
    def raw(self) -> str:
        return self._raw_nodeid

    @property
    def fragments(self) -> List[NodeidFragment]:
        return self._fragments

    def append(self, fragment: NodeidFragment) -> "Nodeid":
        """Returns a new nodeid with the new fragment appended."""
        return Nodeid.from_fragments(self._fragments + [fragment])