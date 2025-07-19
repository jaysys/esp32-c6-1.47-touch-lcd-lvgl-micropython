main.py

- touch, lvgl display, animation 을 모두 수행하는 샘플 코드 추가함
- plotting touch points on the screen




---

참조

```
pip install adafruit-ampy
pip install esptool 

ampy --port /dev/cu.usbmodem11101 put main.py
ampy --port /dev/cu.usbmodem11101 ls
```

마이크로파이썬 + lvgl 빌드 -> bin 만들기

```
git clone https://github.com/lvgl-micropython/lvgl_micropython.git
cd lvgl_micropython
python3 make.py esp32 clean --flash-size=4 BOARD=ESP32_GENERIC_C6 DISPLAY=jd9853 INDEV=axs5106
```

빌드한 바이너리 파일 lvgl_micropy_ESP32_GENERIC_C6-4.bin -> esp32c6에 플래싱!

```
esptool.py --chip esp32c6 -b 460800 --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size 4MB --flash_freq 40m --erase-all 0x0 build/lvgl_micropy_ESP32_GENERIC_C6-4.bin
```




https://peter.quantr.hk/2025/07/waveshare-esp32-c6-1-47-touch-micropython-lvgl/

https://github.com/quantrpeter/Waveshare-ESP32-C6-1.47-Touch-Micropython-LVGL


---
<img src="https://github.com/user-attachments/assets/9c94f96e-9021-4736-a534-0ab66389a119" width="30%"> 

https://peter.quantr.hk/2025/07/waveshare-esp32-c6-1-47-touch-micropython-lvgl/
