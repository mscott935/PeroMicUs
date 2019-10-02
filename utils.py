import exceptions

def toInt(n):
    # Convert string to int if valid, otherwise return None
    n = n.strip()
    return int(n) if n else None

def validTimeBounds(start, end, length):
    # Ensure time bounds are valid for given file length
    if start != None != end:
        if (start < end) and (start >= 0) and (end <= length):
                return True
    elif start == end == None:
        return True
    return False

def parseFileName(filename, delimiter, categories):
    # Split filename into user-defined categories.
    # Error raised if category length does not match extracted filename segments.
    segs = filename.split(delimiter)
    if len(segs) != len(categories):
        raise exceptions.FilenameParseError(filename)
    else:
        filename_info = {}
        for c, s in zip(categories, segs):
            filename_info[c] = s
        return filename_info