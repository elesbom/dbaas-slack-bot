from time import sleep
from logging import info, basicConfig, INFO
from dbaas_api import DBaaS
from persist import Persistence
from slack_bot import Bot


def main():
    basicConfig(level=INFO)
    bot = Bot()
    dbaas = DBaaS()
    persistence = Persistence()

    info('Loading oldest data')
    tasks = dbaas.latest_tasks()
    for task in tasks:
        persistence.set_notified(task)
    info('Loaded')

    while True:
        tasks = dbaas.latest_tasks()
        for task in tasks:
            if not task.is_error:
                continue

            if not persistence.was_notified(task):
                info('Notifying {}'.format(task.id))
                bot.send_message(task.as_message())

            info('Updating TTL to {}'.format(task.id))
            persistence.set_notified(task)

        sleep(15)


if __name__ == '__main__':
    main()
