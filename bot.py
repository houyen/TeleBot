import json
import sys

import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
from telegram.ext.dispatcher import run_async
import Constants as keys
import Response as R
import requests
import dog
sys.path.append('Method/News')
import News

sys.path.append('Method/New2')
import New2

sys.path.append('Method/Games')
import Games

import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#bodyBODYbody
print("Bot Starting....")
def start(update_obj, context):
  # send the question, and show the keyboard markup (suggested answers)
  update_obj.message.reply_text("Hello there, do you want to using me? (Yes/No)",
                                reply_markup=telegram.ReplyKeyboardMarkup([['Yes', 'No']], one_time_keyboard=True)
                                )
  return welcome
# in the WELCOME state, check if the user wants to answer a question
def welcome(update_obj, context):
    if update_obj.message.text.lower() in ['yes', 'y']:
        return help_command
    else:
        # go to the CANCEL state
        return cancel

def hello_command(update: Update, context: CallbackContext) -> None:
  update.message.reply_text(f'Chào {update.effective_user.first_name}')

def help_command(update: Update, context: CallbackContext):
  update.message.reply_text("Bạn muốn tôi giúp gì? \n 1. Đọc báo -> /news <số lượng> \n 2. Quotes -> /random  \n  3.Dog_cute ->/bop"
                            "\n 4. Xem ngày giờ -> /time  \n ")


def random_command(update, context):
    # fetch data from the api
    response = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    data = response.json()
    # send message
    context.bot.send_message(chat_id=update.effective_chat.id, text=data['quote'])

def news2_command(update: Update, context: CallbackContext):
  try:
    limit_news = int(context.args[0]) # Lấy tham số từ input truyền vào -> cào về bao nhiêu tin
    news = New2.GetNews(limit_news)
    for x in range(0, len(news)): # Deserialize dữ liệu json trả về từ file News.py lúc nãy
      message = json.loads(news[x])
      update.message.reply_text(message['title'] + "\n"
        + message['link'] + "\n" + message['description'])
  except (IndexError, ValueError):
    update.message.reply_text('Vui lòng chọn số lượng tin hiển thị!!')

def news_command(update: Update, context: CallbackContext):
  try:
    limit_news = int(context.args[0]) # Lấy tham số từ input truyền vào -> cào về bao nhiêu tin
    news = News.GetNews(limit_news)
    for x in range(0, len(news)): # Deserialize dữ liệu json trả về từ file News.py lúc nãy
      message = json.loads(news[x])
      update.message.reply_text(message['title'] + "\n"
        + message['link'] + "\n" + message['description'])
  except (IndexError, ValueError):
    update.message.reply_text('Vui lòng chọn số lượng tin hiển thị!!')

def games_command(update: Update, context: CallbackContext):
  try:
    limit_games = int(context.args[0]) # Lấy tham số từ input truyền vào -> cào về bao nhiêu tin
    games = Games.GetGames(limit_games)
    for x in range(0, len(games)): # Deserialize dữ liệu json trả về từ file News.py lúc nãy
      message = json.loads(games[x])
      update.message.reply_text(message['title'] + "\n"
        + message['link'] + "\n" + message['description'])
  except (IndexError, ValueError):
    update.message.reply_text('Vui lòng chọn số lượng tin hiển thị!!')

def handle_message(update: Update, context: CallbackContext):
  text = str(update.message.text).lower()
  response = R.sample_response(text)
  update.message.reply_text(response)

def dog_command(update, context):
    url = dog.get_image_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)


# Function dùng để xác định lỗi gì khi có thông báo lỗi
def error(update: Update, context: CallbackContext):
  print(f"Update {update} cause error {context.error}")

def cancel(update_obj, context):
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(
      f"Okay, no question for you then, take care, {first_name}!", reply_markup=telegram.ReplyKeyboardRemove()
    )
    return telegram.ext.ConversationHandler.END


def main():

  updater = Updater(keys.API_KEY, use_context=True)
  dp = updater.dispatcher
  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(CommandHandler("news2", news2_command))
  dp.add_handler(CommandHandler('random', random_command))
  dp.add_handler(CommandHandler("hello", hello_command))
  dp.add_handler(CommandHandler("help", help_command))
  dp.add_handler(CommandHandler("news", news_command))
  dp.add_handler(CommandHandler("games", games_command))
  dp.add_handler(CommandHandler('bop', dog_command))
  dp.add_handler(MessageHandler(Filters.text, handle_message))
  dp.add_error_handler(error)

  updater.start_polling()
  updater.idle()

main()