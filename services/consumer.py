import asyncio
import json
import time
from config.base import app_setting
from services.producer import Producer
from connection.beanstalk_conn import Connection as BeanstalkConnection
from greenstalk import TimedOutError
from loguru import logger


class Consumer:
    def __init__(self):
        self.tube: str = app_setting.BEANSTALK_TUBE_DATA
        self.beanstalk_conn = BeanstalkConnection().connect()
        self.producer = Producer()

    def consume(self):
        """
        consume job/message dari beanstalk lalu bulk sampai 100 data
        :return:
        """

        self.beanstalk_conn.watch(tube=self.tube)
        logger.info("start consuming...")
        datas = []
        jobs = []
        try:
            while True:
                job = self.beanstalk_conn.reserve(timeout=60)
                if job:
                    time_start = time.time()
                    message = json.loads(job.body)
                    logger.info(message)
                    datas.append(message)
                    jobs.append(job)
                    if len(datas) == 100:
                        """
                        after processing message from beanstalk, we need to delete a job from tube, 
                        so message in queue will passed    
                        
                        """
                        datas.clear()
                        [self.beanstalk_conn.delete(done_job) for done_job in jobs]
                        jobs.clear()

        except TimedOutError:
            """
                do something when connection beanstalk is out           
            """
            if datas:
                # do something if there is data in datas

                datas.clear()
                [self.beanstalk_conn.delete(done_job) for done_job in jobs]
                jobs.clear()
            else:
                """
                    tujuan di sleep untuk memperlama waktu consumer berjalan, dan mencegah sering nya restart engine in deployment
                """
                logger.warning("No job available")
                time.sleep(30)



