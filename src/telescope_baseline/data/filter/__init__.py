class __Filters:
    """This class handles the filter data stored in the data directory.

    Attributes:
        json_list (list): List of the json files
    """
    def __init__(self):
        import pkg_resources
        import pathlib
        self.__data_path = pkg_resources.resource_filename('telescope_baseline', 'data/filter')
        self.json_list = []
        for p in pathlib.Path(self.__data_path).glob('*.json'):
            self.json_list.append(p.name)


    def get_efficiency(self, json_name):
        """This function returns an Efficiency instance created from the input json data

        Arguments:
            json_name: Filename of the input json file (see the 'json_list' of this class).

        Returns:
            efficiency: Efficiency instance created from the input json file.
        """
        import os
        from telescope_baseline.dataclass.efficiency import Efficiency
        return Efficiency.from_json(os.path.join(self.__data_path, json_name))


filters = __Filters()
