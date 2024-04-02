# Discord Access Trojan (DAT)

## Description
Discord Access Trojan (DAT) is a Remote Access Trojan (RAT) designed to enable remote control and monitoring of target devices. It offers a range of features, including capturing screenshots, taking webcam photos, retrieving system information, downloading files remotely, and more. Please note that this tool is created for educational and ethical purposes exclusively. Unauthorized use is strictly prohibited.

## Features
- [x] Capture screenshots
- [x] Take webcam photos
- [x] Retrieve system information
- [x] Download files remotely
- [x] Grab saved passwords from browsers
- [x] Grab saved cookies from browsers
- [x] Grab Discord user token
- [x] Retrieve system logs
- [x] Kill specified processes
- [x] Control screenlogger functionality
- [x] Set and execute payloads from URLs
- [x] Grab saved WiFi passwords
- [x] Ping functionality to check bot responsiveness

## Prerequisites
- Python 3.6 or higher
- Discord.py library
- Other required Python packages listed in `requirements.txt`

## Usage
To utilize the RAT, follow these steps:
1. Clone or download the repository.
2. Install the required Python packages by executing: `pip install -r requirements.txt`
3. Replace `BOT_TOKEN` in `Main.py` with your actual Discord bot token.
4. Build the RAT, preferably using PyCharm IDE, by running the script: `python Builder.py`
5. Invite the bot to your Discord server and utilize the available commands.

## Building the RAT
1. Ensure that the necessary prerequisites are installed.
2. Save your bot token in `Main.py`.
3. Use PyCharm IDE to build the RAT by executing `Builder.py`, which generates a standalone executable (`rat.exe`) from the scripts.
4. Check the "dist" folder for the `rat.exe` file.

## Defender Evasion
This RAT is designed to evade detection by traditional antivirus software. However, it's important to acknowledge that the effectiveness of evasion techniques may vary over time as antivirus systems improve. While efforts have been made to make the RAT undetectable, it cannot be guaranteed that it will evade all antivirus solutions. It's always recommended to use such tools responsibly and legally.

## Contribution
Contributions to this project are welcome. If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License
DAT is released under the MIT License. See the [LICENSE](https://github.com/agent-alli0t/Discord-RAT/blob/main/LICENSE) file for more details.

## Disclaimer
The creators of this project are not responsible for any unauthorized use or misuse of the software. This tool is intended for educational and ethical purposes only. Use it responsibly and only on devices that you own or have explicit permission to access.