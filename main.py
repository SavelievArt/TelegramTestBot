from telegram import Bot, Update
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler
import os
import datetime
telegramToken = "739996565:AAHdVrMZ_nHNCXFRKR0PXm_R7lwZpiVwfnE"


def makeFilename(path, fileInfo):
	return "\{name}_{number}.{type}".format(name='audio_message',
											number=len(os.listdir(path=path)),
											type=fileInfo.file_path.split('.')[-1])


def start(bot: Bot, update: Update):
	"""
	Метод начала чата
	:param bot: Представляет самого Telegram бота
	:param update: Входящее обновление
	:return:
	"""
	bot.sendMessage(chat_id=update.message.chat_id, text="""Привет, я обрабатываю только голосовые сообщения\n
	Отправь мне голосовое сообщение!""")


def sendMessage(bot: Bot, update: Update, text):
	" Метод для отправки сообщений пользователю "
	bot.send_message(chat_id=update.message.chat_id, text=text)


def process(bot: Bot, update: Update):
	"""
	Метод, который отвечает за обработку входящих аудиосообщений
	:param bot: Представляет самого Telegram бота
	:param update: Входящее обновление
	:return:
	"""
	print("Получил аудио! от", update.message.chat_id, datetime.datetime.now())
	try:
		chat_id = update.message.chat.id
		file_info = bot.get_file(update.message.voice.file_id)
		downloaded_file = bot.getFile(file_id=file_info.file_id)
		src = os.getcwd() + '\Audio' + "\{}".format(chat_id)
		if not os.path.exists(src):
			os.mkdir(src)
		fileName = makeFilename(src, file_info)
		downloaded_file.download(custom_path=(src + fileName))
		sendMessage(bot, update, 'Ваше сообщение успешно обработано')
	except Exception as e:
		sendMessage(bot, update, e)


def main():
	bot = Bot(token=telegramToken, base_url="https://telegg.ru/orig/bot", base_file_url="https://telegg.ru/orig/file/bot")
	updater = Updater(bot=bot)
	handler = CommandHandler("start", start)
	messHandler = MessageHandler(Filters.voice, process)  # voice filter
	updater.dispatcher.add_handler(handler)
	updater.dispatcher.add_handler(messHandler)
	if not os.path.exists("Audio"):
		os.mkdir("Audio")
	print("Запускаем бота...")
	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()