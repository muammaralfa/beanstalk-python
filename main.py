from services.consumer import Consumer


class Main:
    def run(self):
        consumer = Consumer()
        consumer.consume()


if __name__ == "__main__":
    app = Main()
    app.run()