![demo](https://github.com/ryomo/btc-register/blob/media/demo.gif)

[English] [[日本語]](README.ja.md)

# btc-register

[![CircleCI](https://circleci.com/gh/ryomo/btc-register.svg?style=svg)](https://circleci.com/gh/ryomo/btc-register)

## What is this ?

A register which accepts Bitcoin Lightning Network payment.


## Requirements

* LND node for Lightning Network payment
    * v0.5.2-beta or newer
    * REST connection must be enabled. (e.g. `lnd --restlisten=0.0.0.0:10443`)
* Raspberry Pi
* Raspberry Pi Official Touch Display
* (Optional) HDMI Display
* Keyboard



## Install

1. Download Raspbian Stretch Lite from [Raspberry Pi Official site](https://www.raspberrypi.org/downloads/raspbian/) and install it.

2. To use the official display upside down, write `lcd_rotate=2` at the end of `config.txt` in the `boot` partition.

    * If you want to use an HDMI display and you need to set the resolution in `config.txt`, you can do it now.

3. Create a `btc-register-config` folder in the boot partition. And create a file `settings.ini` with the following text.

    ```
    [app]
    shop_name = {Your Shop's Name}
    
    [lnd]
    url = https://{your-lnd-node}:{port}
    ```

    * Do not add `{}`.
    * {port} is the rest listening port. If you did `--restlisten=0.0.0.0:10443`, {port} is `10443`.

4. Put LND's `tls.cert` and `invoice.macaroon` in the `btc-register-config` folder.

5. Insert the SD Card, boot it, and login. Your default user/pass is `pi`/`raspberry`.

6. `sudo raspi-config` and set the following.

    * `Change User Password`
    * `Localization Options` > `Change Locale`
        * Note 1: Select locale by space key.
        * Note 2: To press OK button, you need to press the tab key.
        * Select `{your_locale}.UTF-8`.
    * `Localisation Options` > `Change Timezone`
    * `Localisation Options` > `Change Keyboard Layout`
    * When connecting with WiFi, `Network Options` > `Wi-fi`
    * For automatic login, `Boot Options` > `Desktop / CLI` > `Console Autologin`

7. Run the following commands.

    ```bash
    git clone https://github.com/ryomo/btc-register.git
    cd btc-register
    ./install.sh
    ```

8. Wait about 30 to 60 minutes.

    * Automatically restart after completion, and the app starts.



## Notes

* For conversion from fiat when paying by bitcoin, decimal places are rounded off.
* Keyboard is not supported in this app for now.
    * Input is going to be duplicated.
    * Keyboard input passes to background terminal.



## Licenses

* This project is under the MIT License. # TODO: Add `LICENSE` file
* This project uses open source components.

### Kivy

* Open source UI framework
* Licensed under the MIT License
* [[link]](https://github.com/kivy/kivy)

### Open Iconic

* Icons under `assets/open_iconic` directory
* Licensed under the MIT License
* [[link]](https://github.com/iconic/open-iconic)
