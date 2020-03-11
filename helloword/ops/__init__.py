from logging import Filter


class TestFilter(Filter):
    def filter(self, record):
        if 'lc' in record.msg:
            return False
        else:
            return True
