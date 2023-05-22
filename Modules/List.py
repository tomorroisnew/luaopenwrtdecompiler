class List:
    def __init__(self) -> None:
        self.List = []

    def __getitem__(self, index):
        return self.List[index]