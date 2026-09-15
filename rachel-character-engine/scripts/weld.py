#!/usr/bin/env python3
"""Rachel character-engine weld stub.

Verbs: resolve, weld, inventory
Fallback: 5 -> 3 -> 2 -> 1 if the image API rejects N sources.
Does not mint plates. Does not call Imagine unless --live is passed
(live path is a stub in v0.1).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SLOTS_5 = ["pose", "hair", "tattoo", "top", "bottom"]
DNA = ["face", "eyes", "body", "bust", "hair_length", "chest_mark_on_mannequin"]


def load_linker(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def cmd_inventory(_: argparse.Namespace) -> int:
    print(json.dumps({"slots": SLOTS_5, "dna": DNA, "max_sources": 5}, indent=2))
    return 0


def cmd_resolve(args: argparse.Namespace) -> int:
    # rachel H4 riverboat  ->  pose + hair + tattoo + W06-or-H-RIVER top/bottom
    out = {
        "agent": args.agent,
        "heat": args.heat,
        "mode": args.mode,
        "stack": SLOTS_5,
        "note": "resolver maps mode names to Drive UIDs in MANIFEST.json; stub only",
    }
    print(json.dumps(out, indent=2))
    return 0


def cmd_weld(args: argparse.Namespace) -> int:
    srcs = [s for s in (args.pose, args.hair, args.tattoo, args.top, args.bottom) if s]
    plan = []
    n = len(srcs) or args.n
    while n >= 1:
        plan.append({"n": n, "action": "edit_image" if n >= 2 else "generate_or_copy"})
        if not args.fallback:
            break
        n -= 1 if n == 2 else 2 if n >= 4 else 1
        if n == 4:
            n = 3
    receipt = {
        "ok": True,
        "schema": "rachel-weld/v0.1",
        "sources": srcs,
        "requested_n": args.n,
        "plan": plan,
        "live": False,
        "rule": "keep failures; never overwrite; Drive UID is canonical",
    }
    print(json.dumps(receipt, indent=2))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="weld", description="Rachel character-engine welder")
    sub = p.add_subparsers(dest="cmd", required=True)

    inv = sub.add_parser("inventory", help="print slot + DNA contract")
    inv.set_defaults(func=cmd_inventory)

    r = sub.add_parser("resolve", help="rachel <heat> <mode> -> planned stack")
    r.add_argument("--agent", default="rachel")
    r.add_argument("--heat", default="H3")
    r.add_argument("--mode", default="yard")
    r.set_defaults(func=cmd_resolve)

    w = sub.add_parser("weld", help="plan a 1/2/3/5 image weld")
    w.add_argument("-n", type=int, default=2, choices=[1, 2, 3, 5])
    w.add_argument("--pose")
    w.add_argument("--hair")
    w.add_argument("--tattoo")
    w.add_argument("--top")
    w.add_argument("--bottom")
    w.add_argument("--fallback", action="store_true", default=True)
    w.add_argument("--live", action="store_true")
    w.set_defaults(func=cmd_weld)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
