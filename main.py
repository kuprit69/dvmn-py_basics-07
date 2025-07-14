import ptbot
import os
from pathlib import Path
from dotenv import load_dotenv
from pytimeparse import parse

script_dir = Path(__file__).resolve().parent
os.chdir(script_dir)
load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")
bot = ptbot.Bot(TG_TOKEN) 

def wait(chat_id, message):
    delay = parse(message.strip())
    message_id = bot.send_message(chat_id, f"Осталось {delay} секунд")
    bot.create_countdown(delay, notify, chat_id=chat_id, message_id=message_id, total=delay)

def notify(secs_left, chat_id, message_id, total):
    progress_bar = render_progressbar(total, total - secs_left)
    if secs_left > 0:
        bot.update_message(chat_id, message_id, f"{progress_bar}\nОсталось {secs_left} секунд")
    else:
        bot.update_message(chat_id, message_id, "Время вышло!")

def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return f'{prefix} |{pbar}| {percent}% {suffix}'

def main():
    bot.reply_on_message(wait)
    bot.run_bot()

if __name__ == '__main__':
    main()


