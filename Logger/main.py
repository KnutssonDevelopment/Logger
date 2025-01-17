from Logger import Logger

if __name__ == '__main__':
    # TODO: Create Log rotation
    logger = Logger('test.log').get_logger()
    logger.info('Test')


