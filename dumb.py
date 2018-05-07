import sys
import logging


def dumb():
    logger = logging.getLogger(__name__)
    logger.info("dumb has been called")


if __name__ == '__main__':
    # Setup logging facility
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(name)s %(message)s'))
    log = logging.getLogger('')
    log.addHandler(console)
    log.setLevel(logging.INFO)

    # Run the main function of this module
    log.info('Run module directly here!!!')
    dumb()
