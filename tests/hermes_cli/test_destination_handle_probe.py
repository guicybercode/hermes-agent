"""Native diagnostic receipt for mutable directory handle sharing modes."""

import json
import os
from pathlib import Path

import pytest


@pytest.mark.windows_only
def test_directory_handle_modes_allow_child_moves_and_pin_the_parent(tmp_path):
    import win32file

    rows = []
    modes = (
        ("read_read", win32file.GENERIC_READ, win32file.FILE_SHARE_READ),
        ("read_readwrite", win32file.GENERIC_READ, win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE),
        ("attributes_readwrite", 0x0080, win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE),
        ("zero_readwrite", 0, win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE),
    )
    for label, access, sharing in modes:
        case = tmp_path / label
        source, destination = case / "source", case / "destination"
        source.mkdir(parents=True)
        destination.mkdir()
        (source / "payload").write_text("approved")
        row = {"mode": label, "access": access, "sharing": sharing}
        handles = []
        try:
            ancestors = dict.fromkeys((*reversed(source.parents), source, *reversed(destination.parents), destination))
            for parent in ancestors:
                handles.append(win32file.CreateFile(
                    str(parent), access, sharing, None, win32file.OPEN_EXISTING,
                    win32file.FILE_FLAG_OPEN_REPARSE_POINT | win32file.FILE_FLAG_BACKUP_SEMANTICS, None,
                ))
            try:
                os.replace(source / "payload", destination / "payload")
            except OSError as error:
                row["child_move_error"] = error.winerror
            else:
                row["child_move_ok"] = (destination / "payload").read_text() == "approved"
            try:
                destination.rename(case / "moved")
            except OSError as error:
                row["parent_move_error"] = error.winerror
            else:
                row["parent_move_ok"] = True
        finally:
            for handle in reversed(handles):
                win32file.CloseHandle(handle)
        rows.append(row)
    Path(__file__).with_suffix(".json").write_text(json.dumps(rows, indent=2))
    assert any(row.get("child_move_ok") and row.get("parent_move_error") in (5, 32) for row in rows), rows
