Screen: https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(B)

Install doing: http://www.lcdwiki.com/3.5inch_RPi_Display

Add this to the end of `/boot/config.txt`:
```
dtparam=i2c_arm=on
dtoverlay=i2c-gpio,bus=4,i2c_gpio_sda=20,i2c_gpio_scl=21
```