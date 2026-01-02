#!/usr/bin/env python3
"""Test MELCloud API directly to diagnose token issues.

Usage: python test_api.py <email> <password>

This script logs in to MELCloud and fetches device state directly,
bypassing Home Assistant. Use it to verify API connectivity and
compare data with what Home Assistant sees.
"""
import asyncio
import aiohttp
import sys
from datetime import datetime


async def test_melcloud(email: str, password: str):
    """Test MELCloud login and data fetch."""
    async with aiohttp.ClientSession() as session:
        print(f"[{datetime.now().isoformat()}] Logging in as {email}...")

        # Login
        login_resp = await session.post(
            "https://app.melcloud.com/Mitsubishi.Wifi.Client/Login/ClientLogin",
            json={
                "Email": email,
                "Password": password,
                "Language": 0,
                "AppVersion": "1.19.1.1",
                "Persist": True,
            }
        )
        login_data = await login_resp.json()

        if login_data.get("ErrorId"):
            print(f"Login failed: {login_data}")
            return

        token = login_data["LoginData"]["ContextKey"]
        print(f"Token obtained: {token[:16]}...")

        # Fetch devices
        headers = {"X-MitsContextKey": token}
        devices_resp = await session.get(
            "https://app.melcloud.com/Mitsubishi.Wifi.Client/User/ListDevices",
            headers=headers
        )
        devices = await devices_resp.json()

        # Get device states
        for building in devices:
            building_name = building.get("Name", "Unknown Building")
            print(f"\nBuilding: {building_name}")

            all_devices = building["Structure"]["Devices"]
            for area in building["Structure"].get("Areas", []):
                all_devices.extend(area.get("Devices", []))
            for floor in building["Structure"].get("Floors", []):
                all_devices.extend(floor.get("Devices", []))
                for area in floor.get("Areas", []):
                    all_devices.extend(area.get("Devices", []))

            for device in all_devices:
                device_id = device["DeviceID"]
                building_id = device["BuildingID"]
                device_name = device["DeviceName"]

                state_resp = await session.get(
                    f"https://app.melcloud.com/Mitsubishi.Wifi.Client/Device/Get"
                    f"?id={device_id}&buildingID={building_id}",
                    headers=headers
                )
                state = await state_resp.json()

                print(f"\n  Device: {device_name}")
                print(f"    Device ID: {device_id}")
                print(f"    Room Temperature: {state.get('RoomTemperature')}")
                print(f"    Set Temperature: {state.get('SetTemperature')}")
                print(f"    Power: {state.get('Power')}")
                print(f"    LastCommunication: {state.get('LastCommunication')}")
                print(f"    HasPendingCommand: {state.get('HasPendingCommand')}")
                print(f"    Offline: {state.get('Offline')}")


async def continuous_poll(email: str, password: str, interval: int = 60):
    """Continuously poll MELCloud to observe data changes."""
    print(f"Starting continuous polling every {interval} seconds. Press Ctrl+C to stop.\n")

    while True:
        try:
            await test_melcloud(email, password)
            print(f"\n{'='*60}")
            print(f"Waiting {interval} seconds before next poll...")
            print(f"{'='*60}\n")
            await asyncio.sleep(interval)
        except KeyboardInterrupt:
            print("\nStopping...")
            break


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Single fetch: python test_api.py <email> <password>")
        print("  Continuous:   python test_api.py <email> <password> --poll [interval_seconds]")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]

    if "--poll" in sys.argv:
        interval = 60
        poll_idx = sys.argv.index("--poll")
        if poll_idx + 1 < len(sys.argv):
            try:
                interval = int(sys.argv[poll_idx + 1])
            except ValueError:
                pass
        asyncio.run(continuous_poll(email, password, interval))
    else:
        asyncio.run(test_melcloud(email, password))
