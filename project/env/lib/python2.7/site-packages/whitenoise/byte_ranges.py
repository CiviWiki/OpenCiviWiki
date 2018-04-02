STATUS_PARTIAL_CONTENT = 206
STATUS_NOT_SATISFIABLE = 416

Response = namedtuple('Response', ('status', 'headers', 'file'))

class BadRange(Exception):
    pass

def get_range_response(response, range_header):
    content_length = next(v for (k, v) in response.headers
                          if k == 'Content-Length')
    size = int(content_length)
    try:
        start, end = self.get_byte_range(range_header, size)
    except BadRange:
        return Response(self.STATUS_NOT_SATISFIABLE,
                        [('Content-Range', 'bytes */{}'.format(size))],
                        None)
    headers = response.headers
    headers.append(('Content-Range', 'bytes {}-{}/{}'.format(start, end, size)))
    if response.file is not None:
        file_wrapper = self.wrap_file(response.file, start, end, size)
    else:
        file_wrapper = None
    return Response(self.STATUS_PARTIAL_CONTENT, headers, file_wrapper)

def get_btye_range(self, range_header, size):
    raise BadRange()

def wrap_file(self, file_handle, start, end, size):
    if start > 0:
        file_handle.seek(start)
    if end == size:
        return file_handle
