from common.util.vec2 import Vec2

class Direction:
    NONE = 0
    UP = 1 << 0
    DOWN = 1 << 1
    RIGHT = 1 << 2
    LEFT = 1 << 3
    LEFT_UP = 1 << 4
    LEFT_DOWN  = 1 << 5
    RIGHT_UP  = 1 << 6
    RIGHT_DOWN = 1 << 7

    _ANY_ORTHOGONAL = UP | DOWN | RIGHT | LEFT
    _ANY_DIAGONAL = LEFT_UP | LEFT_DOWN | RIGHT_UP | RIGHT_DOWN
    _ANY = _ANY_ORTHOGONAL | _ANY_DIAGONAL

    ORTHOGONAL_LIST = [UP, DOWN, RIGHT, LEFT]
    DIAGONAL_LIST = [LEFT_UP, LEFT_DOWN, RIGHT_UP, RIGHT_DOWN]
    ALL_LIST = ORTHOGONAL_LIST + DIAGONAL_LIST

    _TO_VEC2 = {
        NONE:       Vec2(0, 0),
        UP:         Vec2(0, -1),
        DOWN:       Vec2(0, 1),
        LEFT:       Vec2(-1, 0),
        RIGHT:      Vec2(1, 0),
        LEFT_UP:    Vec2(-1, -1),
        LEFT_DOWN:  Vec2(-1, 1),
        RIGHT_UP:   Vec2(1, -1),
        RIGHT_DOWN: Vec2(1, 1),
    }

    ORTHOGONAL_VECTOR_LIST = [_TO_VEC2.get(UP), _TO_VEC2.get(DOWN), _TO_VEC2.get(LEFT), _TO_VEC2.get(RIGHT)]
    DIAGONAL_VECTOR_LIST = [_TO_VEC2.get(LEFT_UP), _TO_VEC2.get(LEFT_DOWN), _TO_VEC2.get(RIGHT_UP), _TO_VEC2.get(RIGHT_DOWN)]
    ALL_VECTOR_LIST = ORTHOGONAL_VECTOR_LIST + DIAGONAL_VECTOR_LIST


    @staticmethod
    def is_orthogonal(direction):
        return Direction._ANY_ORTHOGONAL | direction == Direction._ANY_ORTHOGONAL


    @staticmethod
    def is_diagonal(direction):
        return Direction._ANY_DIAGONAL | direction == Direction._ANY_DIAGONAL


    @staticmethod
    def as_vector(direction):
        return Direction._TO_VEC2.get(direction, Direction.NONE)


    @staticmethod
    def get_orthogonal_list(direction):
        if direction == Direction.LEFT or direction == Direction.RIGHT:
            return [Direction.UP, Direction.DOWN]
        elif direction == Direction.UP or direction == Direction.DOWN:
            return [Direction.LEFT, Direction.RIGHT]

        return []


    @staticmethod
    def as_vector_list(direction_list):
        vector_list = []
        for direction in direction_list:
            vector_list.append(Direction.as_vector(direction))

        return vector_list

