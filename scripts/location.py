class Location:
    # str: url
    def __init__(self, name):
        self.url = None
        self.name = name

    def get_url(self) -> str:
        return self.url

    def set_url(self):

        return

    def __str(self):
        return

    def __repr__(self) -> str:
        return f"Location({self.name})"
