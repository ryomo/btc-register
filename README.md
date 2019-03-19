# btc-register[WIP]

## What is this ?

A cash register which also accepts Bitcoin Lightning Network payment.


## Requirements

* LND node for Lightning Network payment
* Raspberry Pi
* Raspberry Pi Official Touch Display
* (Optional) HDMI Display
* Keyboard
    * Needed to install this app. # TODO: Remove keyboard requirement.

You needs your own LND node for now. It may be difficult, so I'm working on easier way to build a LND node. Or you may use Casa Node (I don't know it so much). 

## Getting started

### Software install

1. Download Raspbian Stretch Lite from [Raspberry Pi Official site](https://www.raspberrypi.org/downloads/raspbian/) and install it.
2. Boot, login and run commands below.

```bash
cd ~
git clone git@github.com:ryomo/btc-register.git
cd btc-register/
./install.sh
```

Wait 10~ minutes...

### Initial settings

Make `~/.btc-register/` directory.

Put your lnd node's files to `~/.btc-register/`.

* `admin.macaroon`
* `tls.cert`

Make `app_config.ini` file under `~/.btc-register/`, and write

```ini
[lnd]
url = https://your.lnd.url.here
```

Run commands below.

```bash
cd ~/.btc-register
chmod 400 admin.macaroon
chmod 400 tls.cert
chmod 600 app_config.ini
```

### Run

```bash
./run.sh
```


## Warning

* If the storage is stolen, your bitcoin on LN can be stolen, too.
* Keyboard is not supported.
     * Keyboard input passes to background terminal.
     * Input is going to be duplicated.


## Notes

* For conversion from fiat when paying by bitcoin, decimal places are rounded off.


## Development

### Test

Write your wallet password at `tests/.secret`, and run `sh tests.sh`. # TODO: Remove password requirement.


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
