# Workaround for kivy's logging issue (https://stackoverflow.com/questions/36106353/)
import logging
from kivy.logger import Logger
logging.Logger.manager.root = Logger

import os

APP_HOME = os.environ['APP_HOME']
APP_PATH = os.path.dirname(os.path.abspath(__file__))


def run():
    logger = logging.getLogger()
    try:
        from multiprocessing import Process, Pipe
        from controllers.main.main_app import MainApp
        from library.config import Config

        logger.info('MAIN: Main process started')

        main_pipe, sub_pipe = Pipe()

        app_config = Config('{}/config.ini'.format(APP_HOME))
        app_config.write()

        # Starts the sub screen process
        sub_proc = Process(target=run_sub, args=(sub_pipe, app_config), daemon=True)
        sub_proc.start()

        os.environ["KIVY_BCM_DISPMANX_ID"] = '4'  # DISPMANX_ID_FORCE_LCD
        main_app = MainApp(main_pipe, app_config)
        main_app.run()

    except KeyboardInterrupt:
        logger.warning('MAIN: KeyboardInterrupt')

    finally:
        logger.info('MAIN: stop')


def run_sub(sub_pipe, app_config):
    logger = logging.getLogger(__name__)
    try:
        from kivy.config import Config
        from controllers.sub.sub_app import SubApp

        logger.info('SUB: Sub process started')

        os.environ["KIVY_BCM_DISPMANX_ID"] = '5'  # 5: DISPMANX_ID_FORCE_TV
        # Config.set('graphics', 'height', '480')
        # Config.set('graphics', 'width', '800')

        sub_app = SubApp(sub_pipe, app_config)
        sub_app.run()

    except KeyboardInterrupt:
        logger.warning('SUB: KeyboardInterrupt')

    finally:
        logger.info('SUB: stop')


if __name__ == '__main__':
    run()
