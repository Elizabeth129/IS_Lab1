from bot import Bot

if __name__ == '__main__':
    bot = Bot()
    while True:
        print(bot.process_message(input()))
