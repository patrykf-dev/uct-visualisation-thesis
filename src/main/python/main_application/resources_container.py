import os


class ResourcesContainer:
    inst = None

    def __init__(self, cntxt):
        self.base_path = cntxt.get_resource()
        ResourcesContainer.inst = self

    def get_resource_path(self, name):
        return os.path.join(self.base_path, name)
