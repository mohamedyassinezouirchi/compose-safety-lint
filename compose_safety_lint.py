#!/usr/bin/env python3
"""Read-only Docker Compose YAML configuration linter."""
import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Missing dependency: PyYAML. Install it with: pip install -r requirements.txt", file=sys.stderr)
    raise SystemExit(2)

RULES = {
    "CSL001": ("high", "Privileged container", "Remove privileged: true and grant only essential permissions."),
    "CSL002": ("high", "Docker socket mounted", "Avoid mounting /var/run/docker.sock into containers."),
    "CSL003": ("medium", "Host networking enabled", "Use isolated Compose networking where possible."),
    "CSL004": ("medium", "Host PID namespace enabled", "Avoid pid: host unless essential."),
    "CSL005": ("medium", "Unconfined security profile", "Avoid unconfined AppArmor or seccomp settings."),
    "CSL006": ("medium", "SYS_ADMIN capability added", "Remove SYS_ADMIN unless specifically required."),
    "CSL007": ("medium", "Read-only root filesystem not enabled", "Consider read_only: true where compatible."),
}

def lint_document(doc):
    if not isinstance(doc, dict):
        raise ValueError("Compose document must be a YAML mapping")
    services = doc.get("services", {})
    if not isinstance(services, dict):
        raise ValueError("'services' must be a mapping")
    findings = []
    def add(name, code):
        severity, title, advice = RULES[code]
        findings.append({"service": name, "rule": code, "severity": severity, "message": title, "remediation": advice})
    for name, service in services.items():
        if not isinstance(service, dict):
            continue
        if service.get("privileged") is True:
            add(name, "CSL001")
        for volume in service.get("volumes") or []:
            if isinstance(volume, str):
                source = volume.split(":", 1)[0]
            elif isinstance(volume, dict):
                source = volume.get("source", "") if volume.get("type") == "bind" else ""
            else:
                source = ""
            if source == "/var/run/docker.sock" or source.startswith("/var/run/docker.sock/"):
                add(name, "CSL002")
        if service.get("network_mode") == "host":
            add(name, "CSL003")
        if service.get("pid") == "host":
            add(name, "CSL004")
        security_opt = service.get("security_opt") or []
        if isinstance(security_opt, list) and any(
            isinstance(x, str) and x in ("apparmor:unconfined", "seccomp:unconfined")
            for x in security_opt
        ):
            add(name, "CSL005")
        cap_add = service.get("cap_add") or []
        if isinstance(cap_add, list) and any(str(c).upper() == "SYS_ADMIN" for c in cap_add):
            add(name, "CSL006")
        if service.get("read_only") is not True:
            add(name, "CSL007")
    return findings

def scan(path):
    if not path.is_file():
        raise ValueError(f"File not found: {path}")
    with path.open(encoding="utf-8") as f:
        documents = list(yaml.safe_load_all(f))
    if len(documents) != 1:
        raise ValueError("Expected exactly one Compose YAML document")
    return lint_document(documents[0])

def main(argv=None):
    parser = argparse.ArgumentParser(description="Read-only Docker Compose security configuration checks")
    parser.add_argument("file", type=Path, help="Compose YAML file to inspect")
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    args = parser.parse_args(argv)
    try:
        findings = scan(args.file)
    except (ValueError, OSError, yaml.YAMLError) as exc:
        if args.json:
            print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"ok": not findings, "count": len(findings), "findings": findings}, indent=2))
    else:
        if not findings:
            print("No issues detected by the configured rules.")
        for item in findings:
            print(f"[{item['severity'].upper()}] {item['rule']} ({item['service']}): {item['message']}")
            print(f"  Suggestion: {item['remediation']}")
        print(f"Findings: {len(findings)}")
    return 1 if findings else 0

if __name__ == "__main__":
    sys.exit(main())
