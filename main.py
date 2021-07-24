from core import HelperBot
from utils.keep_alive import keep_alive

bot = HelperBot()

if __name__ == '__main__':
    keep_alive()
    bot.run()
