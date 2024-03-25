from __future__ import annotations
from typing import Type, TypeVar, Generic, List

T = TypeVar('T')

class FreeList(Generic[T]):
    class Iterator:
        def __init__(self, flist: FreeList, index: int) -> None:
            self.__flist: FreeList = flist
            self.__index: int = index
            
        def __iter__(self) -> Iterator:
            return self
        
        def __next__(self) -> T:
            while self.__index < len(self.__flist._elements) and self.__flist._elements[self.__index].removed:
                self.__index += 1
            if self.__index >= len(self.__flist._elements):
                raise StopIteration
            value = self.__flist._elements[self.__index].value
            self.__index += 1
            return value

    class Element:
        def __init__(self, value: T | None = None) -> None:
            self.value: T | None = value
            self.removed: bool = False
            self.next: int = -1
    
    def __init__(self) -> None:
        self._elements: List[Element] = list()
        self.__first_free: int = -1
        self.__size = 0
        
    def swap(self, other: FreeList[T]) -> None:
        self._elements, other._elements = other._elements, self._elements
        self.__first_free, other.__first_free = other.__first_free, self.__first_free
        self.__size, other.__size = other.__size, self.__size
        
    def push(self, value: T) -> int:
        self.__size += 1
        if self.__first_free != -1:
            index: int = self.__first_free
            self.__first_free = self._elements[self.__first_free].next
            self._elements[index].value = value
            self._elements[index].removed = False
            return index
        self._elements.append(self.Element(value = value))
        return len(self._elements) - 1
    
    def emplace(self, *ts) -> int:
        self.__size += 1
        if self.__first_free != -1:
            index: int = self.__first_free
            self.__first_free = self._elements[self.__first_free].next
            self._elements[index].value = T(*ts)
            self._elements[index].removed = False
            return index
        self._elements.append(self.Element(value = T(*Ts)))
        return len(self._elements) - 1
    
    def remove(self, index: int) -> None:
        self.__size -= 1
        self._elements[index].next = self.__first_free
        self._elements[index].removed = True
        self.__first_free = index
        
    def clear(self) -> None:
        self.__size = 0
        self._elements.clear()
        self.__first_free = -1
        
    def size(self) -> int:
        return self.__size
    
    def find(self, value: T)  -> int:
        for i in range(len(self._elements)):
            if self._elements[i].removed:
                continue
            if self._elements[i].value == value:
                return i
        return -1
    
    def __getitem__(self, index: int) -> T:
        return self._elements[index].value
        
    def __iter__(self) -> Iterator:
        i: int = 0
        while i < len(self._elements) and self._elements[i].removed:
            i += 1
        return self.Iterator(self, i)