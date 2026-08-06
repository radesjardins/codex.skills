#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from audit import audit_path
from convert import convert_in_place, convert_marketplace, convert_to_target
from models import AuditReport, ConversionResult


def _print_audit(report: AuditReport, as_json: bool) -> None:
    if as_json:
        print(json.dumps(report.to_dict(), indent=2))
        return
    print(f"Audited: {report.root}")
    print(f"Sources: {', '.join(report.source_types) if report.source_types else 'none'}")
    print(f"Errors: {report.error_count}  Warnings: {report.warning_count}  Info: {report.info_count}")
    for finding in report.findings:
        location = finding.path
        if finding.line is not None:
            location += f":{finding.line}"
        print(f"{finding.severity.upper()} {finding.code} {location}: {finding.message}")


def _print_conversion(result: ConversionResult, as_json: bool) -> None:
    if as_json:
        print(json.dumps(result.to_dict(), indent=2))
        return
    print(f"Converted: {result.root}")
    print(f"Changed: {', '.join(result.changed_files) if result.changed_files else 'none'}")
    for finding in result.findings:
        location = finding.path
        if finding.line is not None:
            location += f":{finding.line}"
        print(f"{finding.severity.upper()} {finding.code} {location}: {finding.message}")


def _print_marketplace(results: list[ConversionResult], as_json: bool) -> None:
    if as_json:
        print(json.dumps([result.to_dict() for result in results], indent=2))
        return
    for index, result in enumerate(results):
        if index:
            print()
        _print_conversion(result, False)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit and convert plugins for Agent Plugins 1.0.0.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    audit_parser = commands.add_parser("audit", help="Audit one plugin or Agent Skill without writing files.")
    audit_parser.add_argument("path", type=Path)
    audit_parser.add_argument("--json", action="store_true", help="Emit JSON output.")

    convert_parser = commands.add_parser("convert", help="Convert one plugin or Agent Skill.")
    convert_parser.add_argument("path", type=Path)
    mode = convert_parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--in-place", action="store_true", help="Add or repair portable files in the source package.")
    mode.add_argument("--target", type=Path, help="Copy the source to a new target, then convert the target.")
    convert_parser.add_argument("--json", action="store_true", help="Emit JSON output.")

    marketplace_parser = commands.add_parser("marketplace", help="Audit or convert local marketplace plugins.")
    marketplace_parser.add_argument("path", type=Path)
    marketplace_parser.add_argument("--apply", action="store_true", help="Write safe conversion changes.")
    marketplace_parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "audit":
        report = audit_path(args.path)
        _print_audit(report, args.json)
        return 0 if report.conforming else 1
    if args.command == "convert":
        result = convert_in_place(args.path) if args.in_place else convert_to_target(args.path, args.target)
        _print_conversion(result, args.json)
        return 0 if result.successful else 1
    results = convert_marketplace(args.path, args.apply)
    _print_marketplace(results, args.json)
    return 0 if all(result.successful for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
