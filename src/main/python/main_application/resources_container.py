import os


class ResourcesContainer:
    inst = None

    def __init__(self, cntxt):
        self.base_path = os.path.join(cntxt.get_resource(), "resources")
        ResourcesContainer.inst = self

    def get_resource_path(self, name):
        return os.path.join(self.base_path, name)
