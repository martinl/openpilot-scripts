from pcapng import FileScanner

with open('./wifi-test.pcapng') as fp:
    scanner = FileScanner(fp)
    for block in scanner:
        pass  # do something with the block...
