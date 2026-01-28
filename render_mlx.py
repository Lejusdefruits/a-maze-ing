from mlx import Mlx
from utils_mlx import (
    MlxImage,
    create_new_img,
    load_xpm_to_img,
    fill_img_color,
    fill_rect,
    draw_cell_walls,
    put_img_to_img_transparent,
)


def mymouse(button, x, y, mystuff):
    print(f"Got mouse event! button {button} at {x},{y}.")


def mykey(keynum, mystuff):
    print(f"Got key {keynum}, and got my stuff back:")
    print(mystuff)
    if keynum == 32:
        m.mlx_mouse_hook(win_ptr, None, None)


def gere_close(dummy):
    m.mlx_loop_exit(mlx_ptr)


m = Mlx()
mlx_ptr = m.mlx_init()
(ret, w, h) = m.mlx_get_screen_size(mlx_ptr)
print(f"Got screen size: {w} x {h} .")
win_ptr = m.mlx_new_window(mlx_ptr, w, h, "win title")
m.mlx_clear_window(mlx_ptr, win_ptr)

stuff = [1, 2]
m.mlx_mouse_hook(win_ptr, mymouse, None)
m.mlx_key_hook(win_ptr, mykey, stuff)
m.mlx_hook(win_ptr, 33, 0, gere_close, None)

m.mlx_loop(mlx_ptr)
sceen_buffer = create_new_img(m, win_ptr, w, h)
fill_img_color(sceen_buffer, (0xFFFF0000).to_bytes(4, "little"))
m.mlx_put_image_to_window(m, win_ptr, sceen_buffer, 0, 0)
