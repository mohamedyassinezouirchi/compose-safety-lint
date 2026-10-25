# Demo: Docker Compose checks

A short, reproducible way to show what this repository currently does.

## Walkthrough

Install dependencies using `python -m pip install -r requirements.txt`, then run `python compose_safety_lint.py examples/insecure-compose.yml` to see example findings. Compare with `python compose_safety_lint.py examples/safer-compose.yml`.

## Suggested content for a public demo

- Show your terminal with the command and actual output.
- Explain the developer problem in one sentence.
- Share the repository link and the specific limitation below.
- Invite practical feedback or a reproducible issue instead of asking for stars.

## Honest limitations

The tool is a static YAML linter, not a full security audit. Never post real deployment secrets.

## Validation

Run the project's tests where applicable:

```bash
python -m unittest discover -s tests -v
```

Avoid presenting a demo output as a real performance measurement unless you actually collected it.
