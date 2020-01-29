
import os


class ResourcesContainer:
    """
    Class enables resources usage, given path.
    """
    inst = None

    def __init__(self, cntxt):
        self.app_path = cntxt.get_resource()
        self.base_path = os.path.join(cntxt.get_resource(), "resources")
        self.trees_path = os.path.join(cntxt.get_resource(), "sample-trees")
        ResourcesContainer.inst = self

    def get_resource_path(self, name):
        """
		Args:
			name:  string, name of the file

		Returns:
			string, path of resource        
		"""
        return os.path.join(self.base_path, name)

