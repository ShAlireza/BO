class MultipleJobsWithGivenId(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NoJobFoundWithGivenId(Exception):
    def __init__(self, *args):
        super().__init__(*args)
