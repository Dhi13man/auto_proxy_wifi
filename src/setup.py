from os import getcwd, remove
from services.system_calls import exec_output

def generate_sch_task_config_xml(input_template_xml_name: str = "sch_task_config_template.xml") -> None:
    """
    Generate the task configuration XML file for Windows Scheduler: sch_task_config.xml

    PARAMETERS
    ----------
    input_template_xml_name: str
        The name of the template XML file.
    
    RETURNS
    -------
    None
    """
    read_file = open(input_template_xml_name, "r")
    write_file = open("sch_task_config.xml", "w")
    for line in read_file.readlines():
        line = line.replace(r"{LOCATION}", getcwd())
        write_file.write(line)
    read_file.close()
    write_file.close()


if __name__ == "__main__":
    # Generates dynamic xml file "./sch_task_config.xml"
    generate_sch_task_config_xml()
    
    # Set up the scheduled task with the generated XML
    out: str = exec_output('schtasks /Create /TN auto_proxy /F /XML "./sch_task_config.xml"')
    # Below command is simple but doesn't work if laptop on battery
    # schtasks /Create /TN auto_proxy /TR "%~dp0main.py" /SC ONEVENT /EC Microsoft-Windows-WLAN-AutoConfig/Operational /MO *[System/EventID=8001]

    # Validate whether the script was successfully set up.
    if "SUCCESS" in out: 
        print("Auto Proxy Wi-FI SET UP! :)")
        # Remove generated xml file, since it is no longer needed
        remove("./sch_task_config.xml")
    else: print("Auto Proxy Wi-FI SETUP FAILED! :(")

    input("Press Enter to continue...")
