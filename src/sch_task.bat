schtasks /Create /TN test /TR "%~dp0main.py" /SC ONEVENT /EC Microsoft-Windows-WLAN-AutoConfig/Operational /MO *[System/EventID=8001]