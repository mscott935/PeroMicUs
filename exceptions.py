# Use a sys.excepthook!
# https://stackoverflow.com/questions/35233823/grab-any-exception-in-pyqt

class PipelineError(Exception):
    pass

class TimeBoundError(PipelineError):
    def __init__(self, start, end, filename):
        self.start = start
        self.end = end
        self.filename = filename

    def error_string(self):
        return f"Start {self.start}ms and end {self.end}ms invalid on file {self.filename}!"

class FilenameParseError(PipelineError):
    def __init__(self, filename):
        self.filename = filename

    def error_string(self):
        return f"Filename {self.filename} does not match given parsing categories!"

class NoInputError(PipelineError):
    def __init__(self, input_dir):
        self.input_dir = input_dir

    def error_string(self):
        return f"Specified input directory \"{self.input_dir}\" not found!"