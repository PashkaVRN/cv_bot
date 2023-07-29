import logging
import os

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

# Инициализируйте бота и диспетчера:
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

# Блок кнопок меню.
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add('📄 Мое резюме')
keyboard.add('📡 Контакты')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Запуск бота и отправка приветствия. """

    logging.info('Отправка приветствия.')
    await message.reply(
        'Привет, я бот резюме!🙋‍♂️ \n'
        '\n'
        '🟡 Я создал этого бота чтобы вы могли познакомиться со мной поближе'
        '👨‍💻\n'
        '\n'
        '🟢 Бот умеет распознавать текстовые команды и нажатия кнопок, '
        'использование нижнего и верхнего регистра символов поддерживается.\n'
        '\n'
        '🟣 Вы можете узнать о моих увлечениях, послушать о том где я учился, '
        'о том как я начал программировать, посмотреть мой github, '
        'и получить представление о моем опыте 🤓\n'
        '\n'
        '🔵 Если пропадает меню выбора кнопок, нажмите на символ 4 точек '
        'в нижнем правом углу.⬇️\n'
        'Если возникнут вопросы пишите мне в телеграм: @pashkavrn\n'
        'Хорошего времени суток, надеюсь вы получите информацию которую '
        'искали и мы сможем продолжить знакомство дальше 🥳🥳🥳🥳🥳🥳🥳',
        reply_markup=keyboard
        )


@dp.message_handler(text='📄 Мое резюме')
async def send_cv(message: types.Message):
    """Метод отправки резюме. """

    logging.info('Отправка резюме.')
    text_caption = (
        'Мое резюме на данный момент.\n'
        'Специальность - Python разработчик, но я так же владею SQL, '
        'немного умею в DevOps и другую всякую всячину 😅, '
        'ну вы прочитаете там 🤭'
    )
    await bot.send_document(
        message.chat.id,
        document=open('cv/Шевель Павел Эдуардович.pdf', 'rb'),
        caption=text_caption
    )
    logging.info('Резюме отправлено.')


@dp.message_handler(text='📡 Контакты')
async def my_contacts(message: types.Message):
    """Отправка моих контактов. """

    text = (
        'Telegram предпочитаемый способ связи: @pashkavrn\n'
        '📧 Моя электронная почта: pavelshevel96@gmail.com\n'
        '📷 Instagram: @pashka_vrn\n'
    )
    await bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    """Точка входа. """

    # Настройки логирования.
    logging.basicConfig(filename='logs.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        encoding='utf-8-sig')

    # Запуск бота.
    executor.start_polling(dp, skip_updates=True)
