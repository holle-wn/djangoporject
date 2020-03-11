import os
import django
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helloword.settings')
django.setup()


def logdemo():
    logger = logging.getLogger('django')
    logger.info('slkafakljfesa')
    logger.info('fwefw efwe lc ewf')
    logger.info('ef fefe few wef')


if __name__ == '__main__':
    logdemo()
