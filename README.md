[![Discord](https://discordapp.com/api/guilds/1235469363050577950/widget.png?style=shield)](https://discord.gg/uYzHwJrCCV)

## PREVIEW

I have uploaded some preview videos in my discord server.

This is an old version of my Colorbot for valorant, i have played 6 months with it without getting banned. The reason i make it public is cuz i made it much better trough the time, and too give you a great starting base.

## DISCLAIMER

- **Compatibility**: This software is designed for Arduino Leonardo boards only (you will need an usb host shield aswell).
- **Undetected**: I used it myself for around 6 months without a ban. But use it at your own risk.
- **Responsibility**: This software is intended for educational purposes only. I am not responsible for any account bans, penalties, or any other consequences that may result from using this tool. Use it at your own risk and be aware of the potential implications.


## Setup Instructions

1. **Spoof Arduino**:
   - You will have to spoof your Arduino Leonardo yourself, by changing it to your mouse's VID and PID, Since valorant only allows only 1 input.
   - You also NEED a external power source for your Arduino so its not going in the bootloader.

3. **Configure `settings.ini`**:
   - Adjust the settings in `settings.ini` according to your preferences, if you want to change keybinds you can find the values [here](https://learn.microsoft.com/windows/win32/inputdev/virtual-key-codes).

4. **Run the Colorbot**:
  - Now you can run the colorbot in cmd by typing:
     ```bash
     py colorbot.py
     ```

6. **In-Game Settings**:
   - I prefer my ingame sens to **0.45**.
   - Make sure to change enemy outline to **Purple**.
