# TOS-Watch

TOS-Watch is a small Raspberry Pi application that reads glucose and trend data from a local CareLink-compatible service and displays it on a MAX7219 LED matrix.

> **Important:** TOS-Watch is a personal display project, not a medical device or a replacement for a glucose monitor, pump, treatment guidance, or clinical advice. Verify readings against your approved devices and follow your care plan.

## What it does

The application:

1. Waits for a network connection and shows the host's local IP address.
2. Fetches the latest JSON data from `http://localhost:8081/carelink/nohistory`.
3. Validates the response with Pydantic.
4. Converts glucose values from mg/dL to mmol/L.
5. Displays the glucose value, trend symbol, and stale-data indication on a cascaded MAX7219 matrix.

The project does not fetch data directly from CareLink and does not contain or manage CareLink credentials. The local data provider used with TOS-Watch is [carelink-python-client](https://github.com/ondrej1024/carelink-python-client), an experimental Python client whose proxy exposes the `/carelink/nohistory` endpoint. TOS-Watch consumes that local proxy endpoint; it does not vendor or reimplement the upstream CareLink client.

The upstream client is an independent project and is not affiliated with or endorsed by Medtronic. Review its documentation, limitations, and license before deploying it.

## Hardware

The code is intended for a Linux-based Raspberry Pi setup with:

- A MAX7219 8×8 LED matrix module, or cascaded modules.
- SPI enabled on the host.
- The display wired and accessible through the `luma.led_matrix` library.
- A local service that exposes the expected CareLink-compatible JSON response.

The display is initialized with four cascaded modules and a block orientation of `-90` degrees. Adjust `main.py` if your hardware uses a different arrangement.

## Repository layout

| File | Purpose |
| --- | --- |
| `main.py` | Application loop and display workflow |
| `import_data.py` | HTTP fetch and Pydantic response models |
| `data_processing.py` | Unit conversion and timestamp handling |
| `screen_print.py` | MAX7219 rendering |
| `trend_symbols.py` | 8×8 display symbols |
| `visualize.py` | Preview symbols in a terminal |
| `tos-watch.service` | Example systemd unit |

## Installation

These steps assume a Raspberry Pi or another Linux host with SPI-enabled MAX7219 hardware.

```bash
git clone https://github.com/Microttus/TOS-Watch.git
cd TOS-Watch

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Before starting TOS-Watch, verify that the local data provider is running and responds at:

```text
http://localhost:8081/carelink/nohistory
```

The response must contain the fields required by `DeviceData` in `import_data.py`, including the latest sensor glucose value, trend, user name, and timestamps. The current client expects glucose values in mg/dL and converts them to mmol/L by dividing by 18.

## Run it

For a foreground run with visible logs:

```bash
source .venv/bin/activate
python main.py
```

The application needs access to the SPI device. Depending on the operating system, this may require enabling SPI and adding the service user to the appropriate device-access group.

### Run at boot with systemd

`tos-watch.service` is an install-specific example using `/home/tos-watch/TOS-Watch` and the `tos-watch` user. Review and edit those paths and the user/group for your host before installing it.

```bash
sudo cp tos-watch.service /etc/systemd/system/tos-watch.service
sudo systemctl daemon-reload
sudo systemctl enable --now tos-watch.service
sudo journalctl -u tos-watch.service -f
```

## Preview display symbols

The symbol preview does not require display hardware:

```bash
python visualize.py UP
python visualize.py WIFI
```

If you pass an unknown name, the tool prints the supported symbol names.

## Troubleshooting

**`Server not available`**

Confirm that the local provider is running, the URL and port are correct, and its response matches the `DeviceData` model. The client currently uses a five-second HTTP timeout.

**The matrix stays blank or shows rotated symbols**

Check SPI is enabled, verify wiring and power, and adjust `cascaded` or `block_orientation` in `main.py` for the physical arrangement.

**The displayed value looks wrong**

Confirm the provider returns mg/dL. TOS-Watch performs a simple `mg/dL ÷ 18` conversion and does not interpret or correct the source data.

**The reading is stale**

The display changes its status indication when the timestamp from the provider is no longer recent. Check the provider, network connection, and device communication before relying on the value.

## Privacy and security

Runtime data can include names, glucose values, device metadata, and a local IP address. Keep the local provider and logs private, do not paste real readings into issues, and never commit credentials, exports, or personal device data. See [SECURITY.md](SECURITY.md) for reporting guidance.

## Contributing

Bug reports, hardware notes, and improvements are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md), and include the operating system, Python version, hardware arrangement, and sanitized logs when reporting a problem.

## License

TOS-Watch is released under the [MIT License](LICENSE).
