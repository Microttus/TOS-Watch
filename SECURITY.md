# Security and privacy

## Scope

TOS-Watch is a local display client used with the [carelink-python-client](https://github.com/ondrej1024/carelink-python-client) proxy. That upstream project handles CareLink authentication and data retrieval; TOS-Watch requests the proxy's local HTTP endpoint and does not provide authentication, remote access, or a hosted data service. Runtime data may contain sensitive health information, names, device identifiers, and local network details.

## Safe handling

- Keep the local data provider and its logs on a trusted network.
- Do not commit `.env` files, credentials, private keys, API responses, exports, or screenshots containing real health data.
- Sanitize names, serial numbers, IP addresses, timestamps, and glucose values before opening an issue or pull request.
- If a credential is ever committed, revoke or rotate it immediately. Removing the file in a later commit is not sufficient because Git history may retain it.

## Reporting a vulnerability

Please report security issues privately through GitHub's private vulnerability reporting or Security Advisories feature for this repository. If that feature is unavailable, contact the repository owner through GitHub rather than posting sensitive details in a public issue.

Include a short description, affected file or component, reproduction steps that do not contain real health data, and any suggested mitigation. Please allow time for an assessment before publicly disclosing the issue.

## Medical safety

This project is not a medical device and must not be used as the sole source for treatment decisions. A security or availability failure can make the display incomplete, stale, or misleading; always verify information with approved medical equipment and follow professional guidance.
