# compose-safety-lint

**Spot risky Docker Compose settings before you deploy.** A small, read-only Python command-line linter for common container hardening mistakes.

[![Python tests](https://github.com/mohamedyassinezouirchi/compose-safety-lint/actions/workflows/ci.yml/badge.svg)](https://github.com/mohamedyassinezouirchi/compose-safety-lint/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Status:** Early-stage MVP with a limited rule set. The tool performs **static checks only**. It does not execute Compose, inspect running containers, or guarantee a secure deployment.

## Why this exists

Self-hosting can be rewarding, but seemingly small Compose configuration choices can increase risk. For example, running a service as `privileged`, exposing the Docker socket inside a container, or sharing the host network may significantly expand access. This tool highlights a handful of those decisions before deployment.

## Checks

| Rule | Severity | Finding |
| --- | --- | --- |
| CSL001 | High | `privileged: true` |
| CSL002 | High | Bind mount sourced from `/var/run/docker.sock` |
| CSL003 | Medium | `network_mode: host` |
| CSL004 | Medium | `pid: host` |
| CSL005 | Medium | `apparmor:unconfined` or `seccomp:unconfined` in `security_opt` |
| CSL006 | Medium | `SYS_ADMIN` added in `cap_add` |
| CSL007 | Medium | `read_only: true` not explicitly set |

These are **heuristic warnings**, not absolute declarations that a deployment is vulnerable. Some workloads legitimately require these settings.

## Install

Requires Python **3.10+** and PyYAML.

```bash
git clone https://github.com/mohamedyassinezouirchi/compose-safety-lint.git
cd compose-safety-lint
python -m pip install -r requirements.txt
```

## Quick start

Check the included intentionally insecure Compose sample:

```bash
python compose_safety_lint.py examples/insecure-compose.yml
```

Example output:

```text
[HIGH] CSL001 (app): Privileged container
  Suggestion: Remove privileged: true and grant only essential permissions.
[HIGH] CSL002 (app): Docker socket mounted
  Suggestion: Avoid mounting /var/run/docker.sock into containers.
[MEDIUM] CSL003 (app): Host networking enabled
  Suggestion: Use isolated Compose networking where possible.
[MEDIUM] CSL007 (app): Read-only root filesystem not enabled
  Suggestion: Consider read_only: true where compatible.
Findings: 4
```

For a sample that passes the current rules:

```bash
python compose_safety_lint.py examples/safer-compose.yml
```

Expected:

```text
No issues detected by the configured rules.
Findings: 0
```

**A clean result means only that the current rules found nothing**—it does not mean the configuration is secure.

### Scan your own file

```bash
python compose_safety_lint.py compose.yaml
```

### JSON output

```bash
python compose_safety_lint.py compose.yaml --json
```

JSON contains `ok`, `count`, and a `findings` array. Findings contain the service name, rule ID, severity, message, and remediation suggestion.

### Exit codes

| Code | Meaning |
| --- | --- |
| `0` | No findings under the current rules |
| `1` | One or more warnings |
| `2` | Invalid input, missing file, or YAML parsing error |

## How it works

1. Reads a local Compose YAML file.
2. Parses it using `yaml.safe_load_all`.
3. Inspects entries under `services` using the rules above.
4. Prints warnings or JSON.
5. Exits without starting Docker or changing any files.

The tool expects exactly **one YAML document**.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs tests against Python 3.10 and 3.12 on pushes and pull requests. The badge above reflects the workflow's current state.

## Project structure

```text
compose-safety-lint/
├── compose_safety_lint.py
├── requirements.txt
├── examples/
│   ├── insecure-compose.yml
│   └── safer-compose.yml
├── tests/
│   └── test_lint.py
├── .github/workflows/
│   └── ci.yml
├── .gitignore
├── LICENSE
└── README.md
```

## Important limitations

- It does not resolve Compose overrides, variable interpolation, extension fields, profiles, or `include` files as the Docker Compose CLI would.
- It does not inspect deployed containers, container images, network firewalls, file permissions, or exposed ports.
- It recognizes common Docker socket bind syntax but may miss alternative equivalent mounts.
- It does not report YAML source line numbers.
- The absence of a finding does not establish security.

**Tip:** Complement this tool with `docker compose config`, image vulnerability scanning, least-privilege deployment practices, and infrastructure review.

## Roadmap

Possible future improvements include effective-configuration inspection, configurable rules, better source locations, SARIF output, and integration into CI. These are **not implemented yet**.

## Contributing

Issues and pull requests are welcome. Add a focused fixture and test when proposing a new rule. Avoid sharing credentials or sensitive deployment configurations in public issues.

## Author

**Mohamed Yassine Zouirchi** · [GitHub](https://github.com/mohamedyassinezouirchi)

## License

[MIT](LICENSE).
