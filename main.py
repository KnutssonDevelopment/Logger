from Logger import Logger

if __name__ == '__main__':
    logger = Logger('test.log').get_logger()
    logger.info('Test')


