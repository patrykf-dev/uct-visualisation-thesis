import os


class ResourcesContainer:
    inst = None

    def __init__(self, cntxt):
        self.app_path = cntxt.get_resource()
        self.base_path = os.path.join(cntxt.get_resource(), "resources")
        self.trees_path = os.path.join(cntxt.get_resource(), "sample-trees")
        ResourcesContainer.inst = self

    def get_resource_path(self, name):
        return os.path.join(self.base_path, name)
