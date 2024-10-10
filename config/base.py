from pydantic import BaseSettings


class Config(BaseSettings):
    BEANSTALK_HOST: str
    BEANSTALK_PORT: int
    BEANSTALK_TUBE_DATA: str
    BEANSTALK_TUBE_RESULT: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


app_setting = Config()
