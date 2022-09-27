# -*- coding: utf-8 -*-
def max_width(x: list[str]) -> int:
    return max(list(map(lambda y: len(y), x)))


def set_width(x: str, width: int, spacer='\u202f') -> str:
    if len(x) < width:
        while len(x) < width:
            x += spacer
    elif len(x) > width:
        x = x[:width]
    return x
