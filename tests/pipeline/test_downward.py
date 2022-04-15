from src.tools.pipeline.visitor import SimVisitor
import pytest


class SimpleUpwardVisitor(SimVisitor):
    def __init__(self):
        self.__num = 0

    def visit_di(self, obj):
        print("DetectorImage")
        self.__num += 1

    def visit_si(self, obj):
        print("StellarImage")
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)
        self.__num += 10

    def visit_os(self, obj):
        print("OnTheSkyPosition")
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)
        self.__num += 100

    def visit_ap(self, obj):
        print("AstrometricCatalogue")
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)
        self.__num += 1000

    def num(self):
        return self.__num


@pytest.fixture(scope="module")
def fixture1():
    from src.tools.pipeline.stellarimage import StellarImage
    from src.tools.pipeline.detectorimage import DetectorImage
    print("Pre Processing\n")
    v = SimpleUpwardVisitor()
    a = DetectorImage()
    b = DetectorImage()
    c = StellarImage()
    c.add_child(a)
    c.add_child(b)
    c.accept(v)
    return v


def test_1(fixture1):
    assert fixture1.num() == 12
