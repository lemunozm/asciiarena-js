from common.util.vec2 import Vec2

import enum

class PathFragment:
    NONE = 0
    CENTER = 1
    UP = 1 << 1
    DOWN = 1 << 2
    LEFT = 1 << 3
    RIGHT = 1 << 4
    LEFT_UP = 1 << 5
    LEFT_DOWN = 1 << 6
    RIGHT_UP = 1 << 7
    RIGHT_DOWN = 1 << 8
    ALL = (1 << 9) - 1
    VERTICAL = CENTER + UP + DOWN
    HORIZONTAL = CENTER + LEFT + RIGHT
    CORNER_LEFT_UP = CENTER + RIGHT + DOWN
    CORNER_LEFT_DOWN = CENTER + RIGHT + UP
    CORNER_RIGHT_UP = CENTER + LEFT + DOWN
    CORNER_RIGHT_DOWN = CENTER + LEFT + UP
    VERTICAL_LEFT = CENTER + UP + DOWN + LEFT
    VERTICAL_RIGHT = CENTER + UP + DOWN + RIGHT
    HORIZONTAL_UP = CENTER + LEFT + RIGHT + UP
    HORIZONTAL_DOWN = CENTER + LEFT + RIGHT + DOWN
    INTERSECTION = CENTER + UP + DOWN + LEFT + RIGHT
    CORNER_LEFT_UP_EXTEND = ALL - RIGHT_DOWN
    CORNER_LEFT_DOWN_EXTEND = ALL - RIGHT_UP
    CORNER_RIGHT_UP_EXTEND = ALL - LEFT_DOWN
    CORNER_RIGHT_DOWN_EXTEND = ALL - LEFT_UP


    @staticmethod
    def includes(fragment_to_check, fragments):
        return fragments == fragments & fragment_to_check


    @staticmethod
    def excludes(fragment_to_check, fragments):
        return fragments == fragments & fragment_to_check


    @staticmethod
    def fragments_size(fragment_to_check):
        bits = 0
        while 0 != n:
            n &= n - 1
            bits += 1
        return bits


def create_path_image(path_element_list, image, dimension):
    path_image = [PathFragment.NONE] * len(image)
    for i, _ in enumerate(image):
        pos = Vec2((i % dimension.x), int(i / dimension.y))

        if _is_path(path_element_list, image, pos, dimension):
            up = _is_path(path_element_list, image, Vec2(pos.x, pos.y - 1), dimension)
            down = _is_path(path_element_list, image, Vec2(pos.x, pos.y + 1), dimension)
            left = _is_path(path_element_list, image, Vec2(pos.x - 1, pos.y), dimension)
            right = _is_path(path_element_list, image, Vec2(pos.x + 1, pos.y), dimension)
            left_up = _is_path(path_element_list, image, Vec2(pos.x - 1, pos.y - 1), dimension)
            left_down = _is_path(path_element_list, image, Vec2(pos.x - 1, pos.y + 1), dimension)
            right_up = _is_path(path_element_list, image, Vec2(pos.x + 1, pos.y - 1), dimension)
            right_down = _is_path(path_element_list, image, Vec2(pos.x + 1, pos.y + 1), dimension)

            ortogonal_key = (
                up * PathFragment.UP +
                down * PathFragment.DOWN +
                left * PathFragment.LEFT +
                right * PathFragment.RIGHT
            )

            diagonal_key = (
                left_up * PathFragment.LEFT_UP +
                left_down * PathFragment.LEFT_DOWN +
                right_up * PathFragment.RIGHT_UP +
                right_down * PathFragment.RIGHT_DOWN
            )

            path_image[i] = PathFragment.CENTER + ortogonal_key + diagonal_key

    return path_image


def _is_path(path_element_list, image, pos, dim):
    if 0 <= pos.x and pos.x < dim.x and 0 <= pos.y and pos.y < dim.y:
        for path_element in path_element_list:
            if path_element == image[pos.y * dim.x + pos.x]:
                return True
    return False

