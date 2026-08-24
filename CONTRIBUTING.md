# Contributing to TOS-Watch

Thanks for helping improve the project. Contributions should keep the application simple, local, and safe for sensitive health data.

## Before opening a pull request

1. Create a focused branch from `main`.
2. Set up the project using the instructions in [README.md](README.md).
3. Exercise hardware-independent changes with the symbol preview:

   ```bash
   python visualize.py UP
   python visualize.py WIFI
   ```

4. Run `git diff --check` and review the complete diff.
5. If you tested on hardware, describe the host, matrix arrangement, and SPI setup.

There is currently no automated hardware test suite. Avoid requiring a physical display for code paths that can be tested independently.

## Pull requests

Please explain what changed, why it changed, and how it was tested. Keep unrelated refactors out of feature or bug-fix pull requests. Do not include real names, glucose readings, device serial numbers, IP addresses, logs, or credentials in commits, screenshots, or examples.

## Issues

For a useful bug report, include:

- Operating system and Python version.
- MAX7219 module count and wiring/orientation.
- The local provider version or API shape, if relevant.
- Sanitized logs and reproducible steps.

Use a private report instead of a public issue for security vulnerabilities or exposed personal data; see [SECURITY.md](SECURITY.md).

## Style

Prefer small, readable Python changes that match the existing structure. Update the README or changelog when behavior visible to users changes.
