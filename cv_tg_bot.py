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
keyboard.add('🙋‍♂️ Обо мне')
keyboard.add('🎓 Мое образование')


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


@dp.message_handler(lambda message: 'мое резюме' in message.text.lower())
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


@dp.message_handler(lambda message: 'контакты' in message.text.lower())
async def my_contacts(message: types.Message):
    """Отправка моих контактов. """

    logging.info('Запрос на отправку контактов.')
    text = (
        'Telegram предпочитаемый способ связи: @pashkavrn\n'
        '📧 Моя электронная почта: pavelshevel96@gmail.com\n'
        '📷 Instagram: [pashka_vrn](https://www.instagram.com/pashka_vrn/)\n'
        '👨‍💻 GitHub: [PashkaVRN](https://github.com/PashkaVRN)\n'
    )
    await bot.send_message(message.chat.id, text, parse_mode='Markdown')
    logging.info('Контакты отправлены.')


@dp.message_handler(lambda message: 'мое образование' in message.text.lower())
async def education(message: types.Message):
    """Информация о моем образовании. """

    logging.info('Запрос на отправку информации об образовании.')
    text = (
        'В период с 2012 по 2016 год учился в Филиале '
        'Московского государственного университета путей сообщения, Воронеж. '
        'Учился по специальности Автоматика и Телемеханика на ЖД транспорте. '
        'Успешно освоил программу и получил диплом (СПО).\n'
        '\n'
        'В 2022 года прошел 9-и месячный курс профессиональной переподготовки '
        'по направлению «Python-разработчик».\n'
        'За время обучению освоил следующие темы и инструменты:\n'
        ' - Основы Python\n'
        ' - Git и GitHub'
        ' - Бэкенд на Django\n'
        ' - API: Django REST framework\n'
        ' - Алгоритмы и структуры данных\n'
        ' - Управление проектом на удалённом сервере. Docker, CI CD\n'
        '\n'
        'В настоящее время не останавливаюсь в своем развитии и обучении, '
        'прохожу онлайн программы обучения на stepik.org.\n'
        'Например:\n'
        ' - Поколение Python\n'
        ' - Интерактивный тренажер по SQL\n'
        '\n'
        'Так же самостоятельно изучаю документацию к фреймворкам, языкам '
        'программирования и другим инструментам которые нужны в '
        'профессии Backend и Python разработчика.'
    )

    # Получаем список файлов из папки education
    folder_path = 'education'
    files = [
        f for f in os.listdir(folder_path) if os.path.isfile(
            os.path.join(folder_path, f)
            )
        ]
    # Создаем список объектов MediaGroup
    media = types.MediaGroup()
    # Добавляем файлы в MediaGroup
    for file in files:
        file_path = os.path.join(folder_path, file)
        if file == files[-1]:
            # Добавляем последний файл с описанием
            media.attach_document(types.InputFile(file_path), caption=text)
        else:
            # Добавляем остальные файлы без описания
            media.attach_document(types.InputFile(file_path))
    # Отправляем сообщение с несколькими файлами и описанием к последнему файлу
    await bot.send_media_group(chat_id=message.chat.id, media=media)
    logging.info('Информация об образовании отправлена. ')


if __name__ == '__main__':
    """Точка входа. """

    # Настройки логирования.
    logging.basicConfig(filename='logs.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        encoding='utf-8-sig')

    # Запуск бота.
    executor.start_polling(dp, skip_updates=True)
