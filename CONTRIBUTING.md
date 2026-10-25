# Contributing to compose-safety-lint

Thanks for your interest in improving **compose-safety-lint**.

## Before opening a pull request

1. Open an issue describing the problem or proposed improvement, particularly for a larger change.
2. Fork this repository and work on a descriptive branch.
3. Keep each pull request focused, with a concise motivation and clear description.
4. Add or update tests when changing executable behavior.
5. Run the available tests locally:

```bash
python -m unittest discover -s tests -v
```

6. Explain what you actually ran and what remains unverified.

## Good first contributions

- Clarify documentation or examples.
- Report reproducible bugs with sanitized inputs.
- Improve input validation or error messages.
- Add focused tests or additional useful examples.

## Safety and privacy

The tool is a static YAML linter, not a full security audit. Never post real deployment secrets.

Do not submit credentials, private datasets, or copied material that you are not licensed to redistribute. Disclose potential security issues privately to the maintainer instead of sharing sensitive exploit details in a public issue.

## Code of conduct

Be respectful, constructive, and welcoming. Disagreements about technical choices should focus on evidence and helpful alternatives.

## License

By contributing, you agree your submissions will be distributed under this project's MIT license.
