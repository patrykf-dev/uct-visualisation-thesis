import abc


class BaseSerializator(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        self.extension = ""

    def get_file_path(self, file_name):
        return "../trees/{}.{}".format(file_name, self.extension)

    @abc.abstractmethod
    def save_node_to_file(self, node, file_name):
        pass

    @abc.abstractmethod
    def get_node_from_file(self, file_name):
        pass
