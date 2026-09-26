"""Small standard-library PO-to-MO compiler for environments without GNU gettext."""
import ast
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def parse(path):
    entries = {}
    fields = {}
    active = None
    for line in path.read_text(encoding="utf-8").splitlines() + [""]:
        line = line.strip()
        if not line:
            if "msgid" in fields and "msgstr" in fields:
                entries[fields["msgid"]] = fields["msgstr"]
            fields = {}
            active = None
        elif line.startswith("msgid "):
            if "msgid" in fields and "msgstr" in fields:
                entries[fields["msgid"]] = fields["msgstr"]
            fields = {}
            active = "msgid"
            fields[active] = ast.literal_eval(line[6:])
        elif line.startswith("msgstr "):
            active = "msgstr"
            fields[active] = ast.literal_eval(line[7:])
        elif line.startswith('"') and active:
            fields[active] += ast.literal_eval(line)
    return entries

def compile_file(source, target):
    entries = parse(source)
    keys = sorted(entries)
    offsets = []
    ids = b""
    strs = b""
    for key in keys:
        encoded = key.encode("utf-8")
        offsets.append((len(encoded), len(ids)))
        ids += encoded + b"\0"
    trans_offsets = []
    for key in keys:
        encoded = entries[key].encode("utf-8")
        trans_offsets.append((len(encoded), len(strs)))
        strs += encoded + b"\0"
    n = len(keys)
    header_size = 7 * 4
    orig_start = header_size + 16*n
    orig_table = b"".join(struct.pack("<2I", length, orig_start + offset) for length, offset in offsets)
    trans_start = header_size + 16*n + len(ids)
    trans_table = b"".join(struct.pack("<2I", length, trans_start + offset) for length, offset in trans_offsets)
    blob = struct.pack("<7I", 0x950412de, 0, n, header_size, header_size + 8*n, 0, 0) + orig_table + trans_table + ids + strs
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(blob)

if __name__ == "__main__":
    for language in ("kk", "en"):
        source = ROOT / "locale" / language / "LC_MESSAGES" / "django.po"
        compile_file(source, source.with_suffix(".mo"))
        print(f"Compiled {source}")
