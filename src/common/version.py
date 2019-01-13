from enum import Enum

CURRENT = "0.1.0"

COMPATIBLE = 1
COMPATIBLE_WARNING = 2
INCOMPATIBLE = 3

def check(version):
    if CURRENT == version:
        return COMPATIBLE

    if CURRENT[0:CURRENT.rindex('.')] == version[0:version.rindex('.')]:
        return COMPATIBLE_WARNING

    return INCOMPATIBLE

