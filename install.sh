#!/usr/bin/env bash

ENABLE_SSH=true

if [[ $(id -u) -e 0 ]]
  then echo "Don't run as root/sudo"
  exit
fi

# ${password}
printf "password: "
read -s password
echo ${password} | sudo -S echo 'ok'

# fonts
echo ${password} | sudo -S apt-get install -y fonts-noto fonts-noto-cjk

# python
echo ${password} | sudo -S apt-get install -y python3 python3-pip
pip3 install --user --upgrade pip
ln -s /usr/bin/python3 ~/.local/bin/python

# kivy
echo ${password} | sudo -S apt-get install -y python3-setuptools python3-dev
echo ${password} | sudo -S apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} gstreamer1.0-{omx,alsa} libmtdev-dev xclip xsel
pip3 install --user --upgrade Cython==0.28.2
pip3 install --user --upgrade git+https://github.com/kivy/kivy.git@master
# TODO: Fix kivy version https://pip.pypa.io/en/stable/reference/pip_install/#vcs-support
# TODO: pip3 install --user git+https://github.com/kivy/kivy.git@1.10.1

# pip TODO: requirements.txt
pip3 install --user --upgrade qrcode requests

# ufw
echo ${password} | sudo -S apt-get install ufw
if ${ENABLE_SSH}; then
    echo ${password} | sudo -S ufw allow ssh comment 'ssh'
    echo ${password} | sudo -S ufw --force enable  # `--force` disable prompting y/n even when enabling over ssh.
else
    echo ${password} | sudo -S ufw enable
fi
echo ${password} | sudo -S ufw status verbose

# unattended-upgrades
echo ${password} | sudo -S apt-get unattended-upgrades
# Edits /etc/apt/apt.conf.d/20auto-upgrades
# autoclean
if ! grep -qF 'AutocleanInterval' /etc/apt/apt.conf.d/20auto-upgrades; then
    # -q: quiet
    # -F: Interpret PATTERN as a list of fixed strings (instead of regular expressions).
    echo ${password} | sudo -S sh -c "echo 'APT::Periodic::AutocleanInterval \"7\";' >> /etc/apt/apt.conf.d/20auto-upgrades"
fi
# Edits /etc/apt/apt.conf.d/50unattended-upgrades
edit_file=/etc/apt/apt.conf.d/50unattended-upgrades
# autoremove
before='\/\/Unattended-Upgrade::Remove-Unused-Dependencies "false";'
after='Unattended-Upgrade::Remove-Unused-Dependencies "true";'
echo ${password} | sudo -S sed -i "s/${before}/${after}/" ${edit_file}
# auto reboot
before='\/\/Unattended-Upgrade::Automatic-Reboot "false";'
after='Unattended-Upgrade::Automatic-Reboot "true";'
echo ${password} | sudo -S sed -i "s/${before}/${after}/" ${edit_file}
before='\/\/Unattended-Upgrade::Automatic-Reboot-Time "02:00";'
after='Unattended-Upgrade::Automatic-Reboot-Time "02:00";'
echo ${password} | sudo -S sed -i "s/${before}/${after}/" ${edit_file}
