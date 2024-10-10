import json

from connections.beanstalk_conn import Connection
from config.base import app_setting


class Producer:
    def __init__(self):
        self.conn = Connection().connect()
        self.tube_result = app_setting.BEANSTALK_TUBE_RESULT
        self.tube_config = app_setting.BEANSTALK_TUBE_DATA

    def produce(self, message):
        """
        use untuk menentukan tube mana yang akan dituju
        "put" untuk mengirim datanya
        :param message:
        :return:
        """
        self.conn.use(self.tube_result)
        json_str = json.dumps(message)
        self.conn.put(
            json_str,
            ttr=3600,
            priority=2 ** 16,
            delay=10
        )
        print(">>> result push into queue")