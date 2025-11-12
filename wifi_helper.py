#!/usr/bin/env python3
"""Waits for Wi-Fi connection and returns the local IP address."""

import socket
import time


def get_ip_address() -> str:
    """Returns the current local IP address, or None if not connected."""
    try:
        # This doesn't actually send data — just determines the outbound IP.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None


def wait_for_wifi(timeout: float = 30.0, interval: float = 1.0) -> str:
    """Waits until Wi-Fi is connected or timeout expires.

    Args:
        timeout: Max seconds to wait.
        interval: Seconds between checks.

    Returns:
        The IP address as a string if connected, else None.
    """
    print(f"Waiting for Wi-Fi (timeout={timeout}s)...")

    start = time.time()
    while time.time() - start < timeout:
        ip = get_ip_address()
        if ip and not ip.startswith("127."):
            print(f"✅ Connected with IP: {ip}")
            return ip
        time.sleep(interval)

    print("❌ Timed out waiting for Wi-Fi.")
    return None


if __name__ == "__main__":
    ip_address = wait_for_wifi(timeout=20, interval=1)
    if ip_address:
        print(f"Connected: {ip_address}")
    else:
        print("No connection detected.")
