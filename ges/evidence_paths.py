"""Canonical evidence paths with narrowly trusted Darwin directory aliases.

Caller-controlled symlinks remain invalid. The three fixed operating-system
aliases below are accepted only on Darwin, with root ownership, their exact
expected target, and a target ancestry containing no further symlinks.
"""
from __future__ import annotations

import os
from pathlib import Path
import sys


_DARWIN_SYSTEM_ALIASES = {
    Path('/etc'): Path('/private/etc'),
    Path('/tmp'): Path('/private/tmp'),
    Path('/var'): Path('/private/var'),
}


def _trusted_system_alias(path: Path) -> bool:
    if sys.platform != 'darwin' or path not in _DARWIN_SYSTEM_ALIASES:
        return False
    expected = _DARWIN_SYSTEM_ALIASES[path]
    if path.lstat().st_uid != 0:
        return False
    target = Path(os.readlink(path))
    if not target.is_absolute():
        target = path.parent / target
    return (target == expected and expected.is_dir() and
            not any(item.is_symlink() for item in (expected, *expected.parents)))


def canonical_path(path: Path, *, symlink_error: str) -> Path:
    """Resolve a path only after checking every component's symlink policy.

The final path may not exist yet, as with a new draft directory. This helper
does not grant file access or replace the caller's containment, file-type,
content-integrity, and post-observation checks.
"""
    absolute = path.absolute()
    for item in (absolute, *absolute.parents):
        if item.is_symlink() and not _trusted_system_alias(item):
            raise ValueError(symlink_error)
    return absolute.resolve()
