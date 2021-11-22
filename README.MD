# auto_proxy_wifi

Python Automation Script for Windows devices to configure a proxy server on a wifi network based on the network's SSID. Works using Windows environment variables, registry and CLI tools (Netsh).

## Usage

There are two potential ways to use this script:

### Using Python Script `./src/main_loop.py` (More Memory-Intensive)

- Just execute `./src/main_loop.py` with Python and watch the magic happen every time you switch Wi-Fi networks. :)

### Using Windows Scheduled Task Triggering with `./src/main.py` (Less Memory-Intensive)

- Run `./src/sch_task.bat` once with Administrator privileges.
