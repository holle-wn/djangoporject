import logging
import time

logger = logging.getLogger('statistics')


class TestMiddle:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response


class StatisticsMiddle:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        path = request.path
        response = self.get_response(request)
        end_time = time.time()
        log_dict = {
            'start_time': start_time,
            'used_time': end_time-start_time,
            'path': path
        }
        logger.info(repr(log_dict))
        return response
