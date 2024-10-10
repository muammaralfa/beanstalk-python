from greenstalk import Client
from config.base import app_setting


class Connection:
    def __init__(self):
        pass

    def connect(self):
        beanstalkd = Client((app_setting.BEANSTALK_HOST, int(app_setting.BEANSTALK_PORT)))
        return beanstalkd
