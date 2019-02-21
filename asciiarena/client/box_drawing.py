from common.util.vec2 import Vec2

class BoxLine:
    NONE = 0
    CENTER = 1
    UP = 1 << 1
    DOWN = 1 << 2
    LEFT = 1 << 3
    RIGHT = 1 << 4
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
    CROSS = CENTER + UP + DOWN + LEFT + RIGHT


    @staticmethod
    def includes(box_line, box_lines_included):
        return box_lines_included == box_lines_included & box_line


    @staticmethod
    def excludes(box_Line, box_lines_excludes):
        return box_lines_excludes == box_lines_excludes & box_line


    @staticmethod
    def fragments_size(box_line):
        bits = 0
        while 0 != box_line:
            box_line &= box_line - 1
            bits += 1
        return bits


    @staticmethod
    def parse(reference_list, table, dimension):
        lines = [BoxLine.NONE] * len(table)
        for i, _ in enumerate(table):
            pos = Vec2((i % dimension.x), i // dimension.x)

            if BoxLine._is_reference(reference_list, table, pos, dimension):
                up = BoxLine._is_reference(reference_list, table, Vec2(pos.x, pos.y - 1), dimension)
                down = BoxLine._is_reference(reference_list, table, Vec2(pos.x, pos.y + 1), dimension)
                left = BoxLine._is_reference(reference_list, table, Vec2(pos.x - 1, pos.y), dimension)
                right = BoxLine._is_reference(reference_list, table, Vec2(pos.x + 1, pos.y), dimension)

                lines[i] = BoxLine.CENTER + up * BoxLine.UP + down * BoxLine.DOWN + left * BoxLine.LEFT + right * BoxLine.RIGHT

        return lines


    @staticmethod
    def _is_reference(reference_list, table, pos, dim):
        if 0 <= pos.x and pos.x < dim.x and 0 <= pos.y and pos.y < dim.y:
            for reference in reference_list:
                if reference == table[pos.y * dim.x + pos.x]:
                    return True
        return False


TILES_INDEX = {
    BoxLine.NONE: 0,
    BoxLine.VERTICAL: 1,
    BoxLine.HORIZONTAL: 2,
    BoxLine.CORNER_LEFT_UP: 3,
    BoxLine.CORNER_LEFT_DOWN: 4,
    BoxLine.CORNER_RIGHT_UP: 5,
    BoxLine.CORNER_RIGHT_DOWN: 6,
    BoxLine.VERTICAL_LEFT: 7,
    BoxLine.VERTICAL_RIGHT: 8,
    BoxLine.HORIZONTAL_UP: 9,
    BoxLine.HORIZONTAL_DOWN: 10,
    BoxLine.CROSS: 11,
}

NO_TILE_AVAILABLE = len(TILES_INDEX)

class BoxLineDrawing:
    class Style:
        SINGLE =       ["", "│", "─", "┌", "└", "┐", "┘", "┤", "├", "┴", "┬", "┼", "?"]
        SINGLE_ROUND = ["", "│", "─", "╭", "╰", "╮", "╯", "┤", "├", "┴", "┬", "┼", "?"]
        DOUBLE =       ["", "║", "═", "╔", "╚", "╗", "╝", "╣", "╠", "╩", "╦", "╬", "?"]


    def __init__(self, pencil, tile_set):
        self._pencil = pencil
        self._tile_set = tile_set


    def set_tile_line_style(self, box_line, tile):
        self._tile_set[TILES_INDEX.get(box_line, NO_TILE_AVAILABLE)] = tile


    def get_tile_line_style(self, box_line):
        return self._tile_set[TILES_INDEX.get(box_line, NO_TILE_AVAILABLE)]


    def draw(self, line_table, dimension, scale):
        for i, box_line in enumerate(line_table):
            tile_line_list = self._get_line_tiles(box_line, scale)

            for offset_y, tile_line in enumerate(tile_line_list):
                if tile_line != "":
                    position = Vec2((i % dimension.x) * scale.x, (i // dimension.x) * scale.y + offset_y)

                    if position.y <= (dimension.y - 1) * scale.y: #skip last line if scale > 1
                        if position.x == (dimension.x - 1) * scale.x: #skip last line if scale > 1
                            tile_line = tile_line[0]

                        self._pencil.draw(position, tile_line)


    def _get_line_tiles(self, box_line, scale):
        tile_line_list = []

        extend = BoxLine.HORIZONTAL if BoxLine.includes(box_line, BoxLine.RIGHT) else BoxLine.NONE
        tile_line = self.get_tile_line_style(box_line)
        tile_line += self.get_tile_line_style(extend) * (scale.x - 1)
        tile_line_list.append(tile_line)

        for i in range(1, scale.y):
            extend = BoxLine.VERTICAL if BoxLine.includes(box_line, BoxLine.DOWN) else BoxLine.NONE
            tile_line = self.get_tile_line_style(extend)
            tile_line += self.get_tile_line_style(BoxLine.NONE) * (scale.x - 1)
            tile_line_list.append(tile_line)

        return tile_line_list


