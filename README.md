# DaVinci Resolve Discord Rich Presence

A Python project that shows your current DaVinci Resolve status in Discord using the `pypresence` package. (Only tested to be working on Windows!)

## Prerequisites:

- Windows 10+
- DaVinci Resolve Studio(?) 20.X
- [Python 3.6+](https://www.python.org/downloads/)

## Download:

Go to the [releases](https://github.com/EndCod3r/Resolve-RPC/releases/latest), and open the Assets drop down, and download the `resolve-rpc_vX.X.X.zip` file. Extract it once it's done.

## Usage:

Ensure you have [Python](https://www.python.org/downloads/) installed and select 'Add Python to PATH' during the installation process.

Open a terminal in the Resolve-RPC directory and run:

```
pip install -r requirements.txt
```

Add environment variables by running `add_env.bat` (or as Administrator for all users) or manually by

1. Searching for `Edit environment variables` in Windows Search and press enter.
2. Click `Environment Variables` in the bottom right of the window that just opened.
3. Under `System variables` click `New...`
4. Add a variable named: `PYTHONPATH` and variable value: `%PYTHONPATH%;%RESOLVE_SCRIPT_API%\Modules\`
5. Add another variable named: `RESOLVE_SCRIPT_API` and variable value: `%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting`
6. Add a final variable named: `RESOLVE_SCRIPT_LIB` and variable value `C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll` or if you installed DaVinci Resolve in a different location make sure you set it to the correct location.

Finally, run `python main.py` in the `src` directory.

## Startup with Resolve:

If you want the script to run when DaVinci Resolve starts up move the `discord-rpc` folder to one of the `Fuses` folders. You can delete the `add_env.bat` script and `requirements.txt` as they are only needed during setup. Be warned that a command prompt window may pop when launching DaVinci Resolve which is normal as it's just starting the script and I couldn't figure out how to hide it.

### You can find one of the Fuse folders by:

1. Going to Fusion in any project.
2. Double-clicking the percentage in the bottom right.
3. Click the `Path Map` on the left-side.
4. Find and right-click `Fuses:` and select one of the top three directories.

## Configuration:

Find `config.py` in the `src` directory and open it in any text editor and edit the text in the quotes to change what is displayed on your Discord profile.

## Using your own Discord application:

If you want to change the icons or the name the shows up on Discord you'll have to create your own Discord application.

To start go to the [Discord Developer Portal](https://discord.com/developers/applications) and click `New Application`. Give it the name you want to show up as your status on Discord (eg. DaVinci Resolve Studio, Resolve, etc.)

Now that you've created your Discord application, give it the icon you want to be displayed as the large image on your Discord status. If that's all you wanted to do then you're done just copy the `Application ID` in the General Information page and replace the one in `config.py`!

If you want to add custom images for each page then you'll have to name them correctly, which you can find in the [Images](https://github.com/EndCod3r/Resolve-RPC/tree/main/Images) directory. Just give it the name of the page in all lowercase so for the Color page name it `color.png`, etc. To upload them, find `Art Assests` under the Rich Presence dropdown in the Developer Portal, click add images, and select all your images and make sure they are still named correctly!
