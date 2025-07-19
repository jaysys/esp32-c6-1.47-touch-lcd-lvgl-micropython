#
# touch, lvgl display, animation
# plotting touch points on the screen
#


import lcd_bus
from micropython import const
import machine
from time import sleep
import jd9853
import axs5106
import lvgl as lv
from i2c import I2C

lv.init()

# display settings
_WIDTH = 172
_HEIGHT = 320
_BL = 23
_RST = 22
_DC = 15

_MOSI = 2  # SDA
_MISO = 5
_SCK = 1   # SCL
_HOST = 1  # SPI2

_LCD_CS = 14
_LCD_FREQ = 2000000
_TOUCH_FREQ = 2000000
_TOUCH_CS = 21

_OFFSET_X = 34
_OFFSET_Y = 0

print('s1 spi bus init...');
spi_bus = machine.SPI.Bus(
    host=_HOST,
    mosi=_MOSI,
    #miso=_MISO,
    sck=_SCK
)

print('s2 lcd spi bus init...');
display_bus = lcd_bus.SPIBus(
    spi_bus=spi_bus,
    freq=_LCD_FREQ,
    dc=_DC,
    cs=_LCD_CS,
)

print('s3 jd9853 init...');
display = jd9853.JD9853(
    data_bus=display_bus,
    display_width=_WIDTH,
    display_height=_HEIGHT,
    backlight_pin=_BL,
    reset_pin=_RST,
    reset_state=jd9853.STATE_LOW,
    backlight_on_state=jd9853.STATE_HIGH,
    color_space=lv.COLOR_FORMAT.RGB565,
    color_byte_order=jd9853.BYTE_ORDER_BGR,
    rgb565_byte_swap=True,
    offset_x=_OFFSET_X,
    offset_y=_OFFSET_Y
)

print('s4 jd9853 init...');
display.set_power(True)
display.init()
display.set_color_inversion(True)
display.set_backlight(100)

# Initialize touch controller
print('s5 touch controller init...')
i2c_bus = I2C.Bus(host=0, sda=18, scl=19)
touch_i2c = I2C.Device(i2c_bus, axs5106.I2C_ADDR, axs5106.BITS)
indev = axs5106.AXS5106(
    touch_i2c,
    debug=True,
    reset_pin=20,
    # startup_rotation=lv.DISPLAY_ROTATION._270
)

scrn = lv.screen_active()
scrn.set_style_bg_color(lv.color_hex(0xff0000), 0)

label = lv.label(scrn)
label.set_text('lvgl & micropython!')
label.set_style_text_color(lv.color_hex(0xffffff), 0)
label.align(lv.ALIGN.CENTER, 0, 30)

# Draw a rectangle
rect1 = lv.obj(scrn)
rect1.set_size(10, 10)
rect1.set_style_bg_color(lv.color_hex(0x00aa00), 0)
rect1.set_style_border_color(lv.color_hex(0xffffff), 0)
rect1.set_style_border_width(1, 0)
rect1.set_style_radius(0, 0)
rect1.align(lv.ALIGN.TOP_LEFT, 0, 0)

rect2 = lv.obj(scrn)
rect2.set_size(10, 10)
rect2.set_style_bg_color(lv.color_hex(0xaa0000), 0)
rect2.set_style_border_color(lv.color_hex(0xffffff), 0)
rect2.set_style_border_width(1, 0)
rect2.set_style_radius(0, 0)
rect2.align(lv.ALIGN.TOP_RIGHT, 0, 0)

rect3 = lv.obj(scrn)
rect3.set_size(10, 10)
rect3.set_style_bg_color(lv.color_hex(0xaa00aa), 0)
rect3.set_style_border_color(lv.color_hex(0xffffff), 0)
rect3.set_style_border_width(1, 0)
rect3.set_style_radius(0, 0)
rect3.align(lv.ALIGN.BOTTOM_RIGHT, 0, 0)

rect4 = lv.obj(scrn)
rect4.set_size(10, 10)
rect4.set_style_bg_color(lv.color_hex(0x0000aa), 0)
rect4.set_style_border_color(lv.color_hex(0xffffff), 0)
rect4.set_style_border_width(1, 0)
rect4.set_style_radius(0, 0)
rect4.align(lv.ALIGN.BOTTOM_LEFT, 0, 0)

# Draw a circle
circle = lv.obj(scrn)
circle.set_size(50, 50)
circle.set_style_bg_color(lv.color_hex(0x0000ff), 0)
circle.set_style_border_color(lv.color_hex(0xff00ff), 0)
circle.set_style_border_width(3, lv.STATE.DEFAULT)
circle.set_style_radius(25, 0)  # Make it circular (radius = half of width/height)
circle.align(lv.ALIGN.CENTER, 0, -10)

# Animation setup
import math
animation_angle = 0
animation_speed = 0.05  # Animation speed
animation_radius = 60   # Radius of circular motion
center_x = _WIDTH // 2
center_y = _HEIGHT // 2

# Background color animation
color_angle = 0
color_speed = 0.3  # Color change speed

print('end')

import utime as time
import math

time_passed = 1000

# Create a label to show touch coordinates
coord_label = lv.label(scrn)
coord_label.set_text("Touch the screen")
coord_label.align(lv.ALIGN.TOP_MID, 0, 10)

# Create a small dot that follows touch
touch_dot = lv.obj(scrn)
touch_dot.set_size(20, 20)
touch_dot.set_style_bg_color(lv.color_hex(0xFFFFFF), 0)
touch_dot.set_style_radius(10, 0)
touch_dot.set_style_border_width(0, 0)
touch_dot.set_style_bg_opa(lv.OPA._50, 0)
# Initialize as hidden by moving it off-screen
touch_dot.set_pos(-100, -100)

# Animation variables
animation_angle = 0
animation_speed = 0.05
animation_radius = 60
center_x = _WIDTH // 2
center_y = _HEIGHT // 2

# Background color animation
color_angle = 0
color_speed = 0.3  # Color change speed

while True:
    start_time = time.ticks_ms()
    time.sleep_ms(1)  # sleep for 1 ms
    
    # Handle touch input
    state, x, y = indev._get_coords()
    if state == indev.PRESSED:
        # Move dot to touch position
        touch_dot.set_pos(x - 10, y - 10)
        coord_label.set_text(f"X: {x:3d}, Y: {y:3d}")
    else:
        # Move dot off-screen when not touched
        touch_dot.set_pos(-100, -100)
    
    # # Update background color animation
    # color_angle += color_speed
    # if color_angle >= 2 * math.pi:
    #     color_angle = 0
    
    # # Calculate RGB values for background color (smooth color transition)
    # red = int(127 + 127 * math.sin(color_angle))
    # green = int(127 + 127 * math.sin(color_angle + 2 * math.pi / 3))
    # blue = int(127 + 127 * math.sin(color_angle + 4 * math.pi / 3))
    
    # # Update background color
    # bg_color = (red << 16) | (green << 8) | blue
    # scrn.set_style_bg_color(lv.color_hex(bg_color), 0)
    
    # Update animation
    animation_angle += animation_speed
    if animation_angle >= 2 * math.pi:
        animation_angle = 0
        
    # Calculate new position for circle
    offset_x = int(animation_radius * math.cos(animation_angle))
    offset_y = int(animation_radius * math.sin(animation_angle))
    
    # Update circle position
    circle.align(lv.ALIGN.CENTER, offset_x, offset_y)
    
    lv.tick_inc(time_passed)
    lv.task_handler()
    end_time = time.ticks_ms()
    time_passed = time.ticks_diff(end_time, start_time)
