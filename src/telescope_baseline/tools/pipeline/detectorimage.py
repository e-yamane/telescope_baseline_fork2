from telescope_baseline.tools.pipeline.simcomponent import SimComponent


class DetectorImage(SimComponent):
    def get_child_size(self):
        pass

    def get_child(self, i: int):
        pass

    def accept(self, v):
        v.visit(self)
