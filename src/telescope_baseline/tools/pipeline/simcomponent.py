from abc import ABCMeta, abstractmethod


class SimComponent(metaclass=ABCMeta):
    """Component class of Composite pattern describing JASMINE data tree.

    Since JASMINE's data structure is a tree structure, the Composite pattern is applied. Unlike the normal
    Composite pattern, the Composite class is inherited by subclasses.

    Attributes:
        _parent: Parent node.
    """
    def __init__(self):
        self._parent = None

    def has_parent(self):
        return not (self._parent is None)

    @abstractmethod
    def get_child_size(self):
        pass

    @abstractmethod
    def get_child(self, i: int):
        pass

    @abstractmethod
    def accept(self, v):
        pass
