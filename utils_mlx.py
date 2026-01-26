from __future__ import annotations

from dataclasses import dataclass
import sys
from typing import Any


@dataclass
class MlxImage:
    """holds mlx image data"""

    img: Any
    data: memoryview
    bpp: int
    line_length: int
    endian: int
    width: int
    height: int


def in_bounds(x: int, y: int, width: int, height: int) -> bool:
    """check point in bounds"""
    if x < 0 or y < 0:
        return False
    if x >= width or y >= height:
        return False
    return True


def create_new_img(mlx: Any, mlx_ptr: Any, width: int, height: int) -> MlxImage:
    """create new mlx image"""
    if width <= 0 or height <= 0:
        raise ValueError("image size must be positive")
    img_ptr = mlx.mlx_new_image(mlx_ptr, width, height)
    if not img_ptr:
        raise ValueError("mlx new image failed")
    data, bpp, line_length, endian = mlx.mlx_get_data_addr(img_ptr)
    return MlxImage(img_ptr, data, bpp, line_length, endian, width, height)


def load_xpm_to_img(mlx: Any, mlx_ptr: Any, filename: str) -> MlxImage:
    """load xpm image"""
    img_ptr, width, height = mlx.mlx_xpm_file_to_image(mlx_ptr, filename)
    if not img_ptr:
        message = "mlx xpm load failed for file: " + filename + " so check it"
        raise ValueError(message)
    data, bpp, line_length, endian = mlx.mlx_get_data_addr(img_ptr)
    return MlxImage(img_ptr, data, bpp, line_length, endian, width, height)


def _bytes_per_pixel(img: MlxImage) -> int:
    """get bytes per pixel"""
    if img.bpp % 8 != 0:
        message = str(img.bpp) + " is not multiple of 8 u little bastard"
        raise ValueError(message)
    return img.bpp // 8


def _color_bytes(color: int, endian: int, size: int) -> bytes:
    """pack color to bytes"""
    order = "little" if endian == 0 else "big"
    masked = color & ((1 << (size * 8)) - 1)
    return masked.to_bytes(size, order)


def _pixel_view(img: MlxImage) -> memoryview:
    """get pixel view for 32 bpp image"""
    if img.bpp != 32:
        raise ValueError("only 32 bpp supported")
    if img.endian != 0:
        raise ValueError("only little endian supported")
    if sys.byteorder != "little":
        raise ValueError("unsupported byteorder")
    return img.data.cast("I")


def put_pixel_to_img(img: MlxImage, x: int, y: int, color: int) -> None:
    """write one pixel"""
    if not in_bounds(x, y, img.width, img.height):
        return
    bpp = _bytes_per_pixel(img)
    offset = y * img.line_length + x * bpp
    img.data[offset: offset + bpp] = _color_bytes(color, img.endian, bpp)


def get_pixel_color(img: MlxImage, x: int, y: int) -> int:
    """read one pixel"""
    if not in_bounds(x, y, img.width, img.height):
        return 0
    bpp = _bytes_per_pixel(img)
    offset = y * img.line_length + x * bpp
    pixel = img.data[offset: offset + bpp]
    order = "little" if img.endian == 0 else "big"
    return int.from_bytes(pixel, order)


def fill_img_color(img: MlxImage, color: int) -> None:
    """fill image with color"""
    bpp = _bytes_per_pixel(img)
    color_bytes = _color_bytes(color, img.endian, bpp)
    row = color_bytes * img.width
    row_length = img.width * bpp
    for y in range(img.height):
        start = y * img.line_length
        img.data[start: start + row_length] = row


def fill_rect(
    img: MlxImage,
    x: int,
    y: int,
    width: int,
    height: int,
    color: int,
) -> None:
    """fill rect area"""
    if width <= 0 or height <= 0:
        return
    start_x = max(x, 0)
    start_y = max(y, 0)
    end_x = min(x + width, img.width)
    end_y = min(y + height, img.height)
    if start_x >= end_x or start_y >= end_y:
        return
    view = _pixel_view(img)
    stride = img.line_length // 4
    for yy in range(start_y, end_y):
        row = yy * stride
        for xx in range(start_x, end_x):
            view[row + xx] = color


def draw_line(
    img: MlxImage,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    color: int,
) -> None:
    """draw a line using Bresenham's algorithm"""
    view = _pixel_view(img)
    stride = img.line_length // 4
    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        if in_bounds(x0, y0, img.width, img.height):
            view[y0 * stride + x0] = color
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def _calc_bounds(
    dst: MlxImage,
    src: MlxImage,
    x: int,
    y: int,
) -> tuple[int, int, int, int]:
    """calculate copy bounds for put_img_to_img"""
    start_x = 0
    start_y = 0
    if x < 0:
        start_x = -x
    if y < 0:
        start_y = -y
    end_x = src.width
    end_y = src.height
    if x + src.width > dst.width:
        end_x = dst.width - x
    if y + src.height > dst.height:
        end_y = dst.height - y
    return start_x, start_y, end_x, end_y


def _blend_color(dst: int, src: int, alpha: int) -> int:
    """blend two colors with alpha (0-255)"""
    inv = 255 - alpha
    r = (((dst >> 16) & 0xFF) * inv + ((src >> 16) & 0xFF) * alpha) // 255
    g = (((dst >> 8) & 0xFF) * inv + ((src >> 8) & 0xFF) * alpha) // 255
    b = ((dst & 0xFF) * inv + (src & 0xFF) * alpha) // 255
    return (r << 16) | (g << 8) | b


def put_img_to_img_transparent(
    dst: MlxImage,
    src: MlxImage,
    x: int,
    y: int,
    transparent_color: int,
) -> None:
    """copy image with transparent color skipped because mlx is bad"""
    if x + src.width < 0 or x >= dst.width or y + src.height < 0 or y >= dst.height:
        return
    dst_view = _pixel_view(dst)
    src_view = _pixel_view(src)
    stride_dst = dst.line_length // 4
    stride_src = src.line_length // 4
    start_x, start_y, end_x, end_y = _calc_bounds(dst, src, x, y)
    transparent = transparent_color & 0x00FFFFFF
    for yy in range(start_y, end_y):
        src_row = yy * stride_src
        dst_row = (y + yy) * stride_dst + x
        for xx in range(start_x, end_x):
            color = src_view[src_row + xx]
            if (color & 0x00FFFFFF) != transparent:
                dst_view[dst_row + xx] = color


def put_img_to_img_alpha(
    dst: MlxImage,
    src: MlxImage,
    x: int,
    y: int,
    alpha: int,
) -> None:
    """copy image with alpha blending (0-255)"""
    if alpha <= 0:
        return
    if alpha > 255:
        alpha = 255
    if x + src.width < 0 or x >= dst.width or y + src.height < 0 or y >= dst.height:
        return
    dst_view = _pixel_view(dst)
    src_view = _pixel_view(src)
    stride_dst = dst.line_length // 4
    stride_src = src.line_length // 4
    start_x, start_y, end_x, end_y = _calc_bounds(dst, src, x, y)
    for yy in range(start_y, end_y):
        src_row = yy * stride_src
        dst_row = (y + yy) * stride_dst + x
        for xx in range(start_x, end_x):
            src_color = src_view[src_row + xx]
            dst_color = dst_view[dst_row + xx]
            dst_view[dst_row + xx] = _blend_color(dst_color, src_color, alpha)


def blur_img_downscale(src: MlxImage, dst: MlxImage, scale: int) -> bool:
    """blur image by downscaling with box filter
    by making avg of scale x scale pixels just for style"""
    if scale < 1:
        return False
    if src.width != dst.width or src.height != dst.height:
        return False
    src_view = _pixel_view(src)
    dst_view = _pixel_view(dst)
    stride_src = src.line_length // 4
    stride_dst = dst.line_length // 4
    width = src.width
    height = src.height
    for y in range(0, height, scale):
        y_end = min(y + scale, height)
        for x in range(0, width, scale):
            x_end = min(x + scale, width)
            sum_r = 0
            sum_g = 0
            sum_b = 0
            count = 0
            for yy in range(y, y_end):
                row = yy * stride_src
                for xx in range(x, x_end):
                    color = src_view[row + xx]
                    sum_r += (color >> 16) & 0xFF
                    sum_g += (color >> 8) & 0xFF
                    sum_b += color & 0xFF
                    count += 1
            if count == 0:
                out_color = 0x000000
            else:
                out_color = (
                    ((sum_r // count) << 16)
                    | ((sum_g // count) << 8)
                    | (sum_b // count)
                )
            for yy in range(y, y_end):
                row = yy * stride_dst
                for xx in range(x, x_end):
                    dst_view[row + xx] = out_color
    return True


def draw_cell_walls(
    img: MlxImage,
    cell_x: int,
    cell_y: int,
    cell_size: int,
    walls: int,
    color: int,
) -> None:
    """draw cell walls given wall bitmask
    0x01=top 0x02=right 0x04=bottom 0x08=left"""
    if cell_size <= 0:
        return
    x0 = cell_x * cell_size
    y0 = cell_y * cell_size
    x1 = x0 + cell_size - 1
    y1 = y0 + cell_size - 1
    mask = walls & 0x0F
    if mask & 0x01:
        draw_line(img, x0, y0, x1, y0, color)
    if mask & 0x02:
        draw_line(img, x1, y0, x1, y1, color)
    if mask & 0x04:
        draw_line(img, x0, y1, x1, y1, color)
    if mask & 0x08:
        draw_line(img, x0, y0, x0, y1, color)
