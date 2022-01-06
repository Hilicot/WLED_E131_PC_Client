class GUI_colors():
    colorScheme = None

    def __init__(self):
        self.schemes = dict()
        self.setColorscheme("light")

    def setColorscheme(self, scheme_name: String) -> bool:
        """
        Changes the active color scheme.
        :param scheme_name:
        :return: False if the color scheme doesn't exist
        """
        if scheme_name in self.schemes.keys():
            self.colorScheme = self.schemes[scheme_name]
            return True
        else:
            return False


