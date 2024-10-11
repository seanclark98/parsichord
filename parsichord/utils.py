from typing import TypeVar

T = TypeVar("T")


def partition(lst: list[T], part_size: int) -> list[list[T]]:
    return [
        lst[i * part_size : (i + 1) * part_size] for i in range(len(lst) // part_size)
    ]
