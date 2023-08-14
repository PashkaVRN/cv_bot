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
# keyboard.add('🙋‍♂️ Обо мне')
keyboard.add('🎓 Мое образование')
keyboard.add('👨‍💻 Опыт работы')
keyboard.add('👨🏼‍🔧 Стек')


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
        'ну вы прочитаете там 🤭.\n'
        'Ссылка на мое резюме на [Head Hunter](https://voronezh.hh.ru/resume/c1126776ff0b5ff3400039ed1f6237646f4159)'
    )
    await bot.send_document(
        message.chat.id,
        document=open('cv/Шевель Павел Эдуардович.pdf', 'rb'),
        caption=text_caption,
        parse_mode='Markdown'
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


@dp.message_handler(lambda message: 'опыт работы' in message.text.lower())
async def experience(message: types.Message):
    """Метод отправки ифнормации о моем опыте работы. """

    logging.info('Запрос на информацию об опыте работы.')
    text = (
        'У меня нет опыта в больших компаниях, но я разрабатываю небольшие '
        'проекты на фрилансе и для моих друзей. Так же я занимаюсь '
        'разработкой собственных пет проектов, которые мне интересны и '
        'которые помогают мне освоить новые инструменты программирования, '
        'и получить новый опыт, с помощью которого я развиваюсь. \n'
        '\n'
        'Вот несколько моих проектов:\n'
        ' - Скрипт для автоматического создания скриншотов страниц сайтов. '
        'Полезная программа для инженера сметчика, которому нужны скриншоты '
        'с сайтов товаров, которые входят в смету. Экономит время и силы.\n '
        'Ссылка на [GitHub](https://github.com/PashkaVRN/auto_screen)\n'
        '\n'
        ' - Скрипт мониторинга движения цен на ETH. При изменении цены на 1% '
        'за последние 60 минут, программа выводит сообщение в консоль.\n'
        'Ссылка на [GitHub](https://github.com/PashkaVRN/price_monitoring)\n'
        '\n'
        ' - Скрипт автоматического серфинга интернета который принимает сайт '
        'и в автоматическом режиме переходить по ссылкам, как внутренним так '
        'и внешним. Процесс продолжается до остановки скрипта. Создается '
        'видимость перехода по ссылкам сайтов пользователя.\n'
        'Ссылка на [GitHub](https://github.com/PashkaVRN/auto_surf)\n'
        '\n'
        ' - Настольный пет проект. Сервис Books Catalog, '
        '«Помощник Библиотекаря». Это API сервис. На этом сервисе '
        'библиотекарь может вести учет книг его библиотеки(добавление/'
        'удаление/редактирование информации о книгах в библиотеке), следить '
        'за нахождением книг на руках у читателей (когда взял/когда вернул), '
        'корректировать репутацию читателей на основе точной даты возврата '
        'книг читателями в библиотеку. В процессе разработки возможно '
        'добавление новых функций и возможностей.\n'
        'Ссылка на [GitHub](https://github.com/PashkaVRN/books_catalog)\n'
        '\n'
        ' - Проект Foodgram, «Продуктовый помощник». Это онлайн-сервис '
        'и API для него. На этом сервисе пользователи могут публиковать '
        'рецепты, подписываться на публикации других пользователей, '
        'добавлять понравившиеся рецепты в список «Избранное», а перед '
        'походом в магазин скачивать сводный список продуктов, '
        'необходимых для приготовления одного или нескольких выбранных блюд. '
        'Разработан на Django. \n'
        'Ссылка на [GitHub](https://github.com/PashkaVRN/foodgram-project-react)\n'
        '\n'
        ' - Проект YaMDb собирает отзывы пользователей на произведения, '
        'позволяет ставить произведениям оценку и комментировать чужие '
        'отзывы. Произведения делятся на категории, и на жанры. '
        'Список произведений, категорий и жанров может быть расширен '
        'администратором. Разработан на Django. \n'
        'Ссылка на [GitHub](https://github.com/PashkaVRN/yamdb_final)\n'
        '\n'
        'Ознакомиться с другими моими проектами вы можете перейдя по ссылке '
        'на мой профиль в [GitHub](https://github.com/PashkaVRN) '
        'во вкладке Repositories.'
        )
    await bot.send_message(message.chat.id, text, parse_mode='Markdown')
    logging.info('Информация об опыте работы отправлена.')


@dp.message_handler(lambda message: 'стек' in message.text.lower())
async def skills(message: types.Message):
    """Стек технологий которые я изучаю и владею. """

    logging.info('Запрос на отправку моего стека.')
    text = (
        'А тут я расскажу о стеке технологий, которыми я владею. '
        'На данный момент я владею такими языками программирования как, '
        'Python и SQL. Умею работать в фреймворке Django и дополнении к нему, '
        'Django REST framework для работы с API. Работаю с различными '
        'фреймворками для написания Telegram ботов, такими как '
        'Aiogram, Telebot, Telegram Bot API. Работал с несколькими типами '
        'реляционных баз данных SQLite, PostgreSQL. Умею пользоваться Docker, '
        'Postman и системой контроля версий Git. Знаком с процессом CI/CD.'
        'Я стараюсь изучать новые технологии и не забывать практиковать '
        'уже известные, по этому этот список постоянно расширяется.'
    )
    await bot.send_message(message.chat.id, text)
    logging.info('Информация о стеке отправлена.')


if __name__ == '__main__':
    """Точка входа. """

    # Настройки логирования.
    logging.basicConfig(filename='logs.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        encoding='utf-8-sig')

    # Запуск бота.
    executor.start_polling(dp, skip_updates=True)
