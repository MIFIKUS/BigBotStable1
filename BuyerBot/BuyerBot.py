from ahk import AHK

import pyscreenshot
import numpy as np
import cv2
import pytesseract

import telebot

import win32gui
import win32com.client
import win32con

import random
import time
import json

MULTIPLIER = 1

MODE = 1

SECOND_MODE_PRICE = 20
SECOND_MODE_PRICE_FOR_RED = 500
SECOND_MODE_PRICE_FOR_RED_ACCESORIES = 200


PATH_TO_BUYER = r'C:\Us\MIFIKUS\PycharmProjects\BigBot\BuyerBot\\'

AMOUNT_ITEMS_TO_BUY = 5
account_lvls = {}
TG_USER_ID = 420909529
TG_API_KEY = '6030586977:AAEPBYOO-za3FoNCdkdVcDvQd63YoD_7PKk'
bot = telebot.TeleBot(TG_API_KEY)


LIST_OF_RARE_ITEMS = (
    'Кешанберк',
    'Длинный Меч Самурая',
    'Цуруги',
    'Меч Кошмаров',
    'Меч Стихий',
    'Меч Налетчика',
    'Меч Затмения',
    'Меч Духов',
    'Меч Ипоса',
    'Двуручный Меч Берсерка',
    'Фламберг',
    'Двуручный Меч Хранителя',
    'Мастер Инферно',
    'Клинок Первой Крови',
    'Двуручный Меч Злых Духов',
    'Двуручный Меч Гигантов',
    'Язык Темис',
    'Парные Мечи Гигантов',
    'Парные Экскалибуры',
    'Парные Дамаскусы',
    'Слезы Воителя',
    'Парные Мечи Гомункула',
    'Мистические Парные Мечи',
    'Святые Парные Мечи',
    'Двуручный Топор',
    'Кромсатель',
    'Копье Гигантов',
    'Селекционер',
    'Скорпион',
    'Боевая Коса',
    'Тяжелый Топор Войны',
    'Боевое Копье',
    'Кинжал Гигантов',
    'Нож Ада',
    'Кристальный Кинжал',
    'Кровавая Орхидея',
    'Стилет',
    'Кортик Духовного Пламени',
    'Кинжал Маны',
    'Длинный Лук Аката',
    'Лук Превосходства',
    'Лук Стихий',
    'Ледяной Лук',
    'Лунный Лук',
    'Лук Аса',
    'Лук Демона',
    'Лук Забвения',
    'Лук Гигантов',
    'Усиленный Арбалет',
    'Арбалет Гигантов',
    'Миротворец',
    'Татлум',
    'Старинный Арбалет',
    'Кристальный Арбалет',
    'Баллиста',
    'Орб Демона',
    'Орб Гигантов',
    'Орб Затмения',
    'Рассеиватель Заклинаний',
    'Кости Каим Ванула',
    'Нирвана',
    'Жезл Верований',
    'Королева Фей',
    'Посох Даспариона',
    'Посох Гигантов',
    'Кристальный Посох',
    'Посох Злых Духов',
    'Посох Мертвеца',
    'Посох Вурдалака',
    'Посох Инферно',
    'Ветвь Жизни',
    'Кираса Синего Волка',
    'Кираса Зубея',
    'Мантия Авадона',
    'Полный Латный Доспех',
    'Кожаный Доспех Молнии',
    'Доспех Правосудия',
    'Латный Доспех Рока',
    'Кираса Хаоса',
    'Набедренники Синего Волка',
    'Набедренники Кровавого Пакта',
    'Полные Латные Набедренники',
    'Набедренники Базила',
    'Набедренники Бездны',
    'Штаны Рока',
    'Набедренники Правосудия',
    'Набедренники Хаоса',
    'Штаны Воспоминаний',
    'Перчатки Синего Волка',
    'Полные Латные Рукавицы',
    'Кожаные Перчатки Дрейка',
    'Благословенные Перчатки',
    'Перчатки Зубея',
    'Перчатки Авадона',
    'Перчатки Горгоны',
    'Рукавицы Авелиуса',
    'Кожаные Перчатки Молнии',
    'Перчатки Аса',
    'Перчатки Правосудия',
    'Латные Рукавицы Рока',
    'Рукавицы Хаоса',
    'Полные Латные Сапоги',
    'Кожаные Сапоги Дрейка',
    'Сапоги Божества',
    'Сапоги Зубея',
    'Сапоги Авадона',
    'Сапоги Синего Волка',
    'Сапоги Кронвиста',
    'Кожаные Сапоги Молнии',
    'Сапоги Правосудия',
    'Сапоги Хаоса',
    'Латные Сапоги Рока',
    'Диадема Злого Рока',
    'Полный Латный Шлем',
    'Шлем Синего Волка',
    'Шлем Имплозии',
    'Шляпа Лакисиса',
    'Шлем Правосудия',
    'Латный Шлем Рока',
    'Шлем Кирица',
    'Плащ Святого Духа',
    'Плащ Саламандры',
    'Плащ Сильфов',
    'Плащ Ундины',
    'Плащ Медузы',
    'Плащ Кронвиста',
    'Плащ Гермункуса',
    'Плащ Монарха',
    'Плащ Ассасина',
    'Плащ Алчности',
    'Плащ Хаоса',
    'Крылья Смотрителя',
    'Мифриловая Рубаха Силы',
    'Мифриловая Рубаха Ловкости',
    'Мифриловая Рубаха Мудрости',
    'Футболка Героя',
    'Кристалл Крови',
    'Символ Мечты',
    'Святой Символ',
    'Элдарейк',
    'Символ Фатальности',
    'Символ Фатальности',
    'Символ Алчности',
    'Куб Лабиринта',
    'Проклятие Кирица',
    'Ожерелье Пана Драйда',
    'Ожерелье Беспокойного Злого Духа',
    'Волшебное Ожерелье Черной Лилии',
    'Ожерелье Души Чертубы',
    'Ожерелье Пробуждения',
    'Ожерелье Мольбы',
    'Ожерелье из Слез Русалки',
    'Бирюзовое Ожерелье',
    'Ожерелье Гермункуса',
    'Ожерелье Жреца',
    'Ожерелье Демона Алчности',
    'Ожерелье Деревьев',
    'Ожерелье Сафироса',
    'Лунное Ожерелье',
    'Серьга Инферно',
    'Серьга Нассена',
    'Серьга Духовного Пламени',
    'Серьга Иллюзии',
    'Серьга Лабиринта',
    'Серьги Деревьев',
    'Кольцо Инферно',
    'Кольцо Дерзости',
    'Кольцо Хранителя: Вода',
    'Кольцо Хранителя: Земля',
    'Кольцо Хранителя: Ветер',
    'Кольцо Хранителя: Огонь',
    'Кольцо Хранителя: Тьма',
    'Кольцо Королевской Стражи',
    'Кольцо Благословения',
    'Бирюзовое Кольцо',
    'Кольцо Гермункуса',
    'Кольцо Духовного Пламени',
    'Глаз Небесного Дворца',
    'Кольцо Короля Енотов',
    'Кольцо Сглаза',
    'Глаз Вечности Кронвиста',
    'Лунное Кольцо',
    'Пояс Благословения',
    'Пояс Цербера',
    'Кожаный Пояс Чудовища',
    'Адамантитовый Пояс',
    'Пояс Гермункуса',
    'Пояс Духовного Пламени',
    'Пояс Авелиуса',
    'Золотой Пояс',
    'Пояс Лабиринта',
    'Браслет Благословения',
    'Браслет Грации',
    'Браслет Рассвета',
    'Бирюзовый Браслет',
    'Золотой Браслет',
    'Браслет Лабиринта',
    'Магический Камень Духа Огня',
    'Магический Камень Духа Воды',
    'Магический Камень Духа Ветра',
    'Магический Камень Духа Земли',
    'Магический Камень Духа Тьмы',
    'Магический Камень Сияния',
    'Магический Камень Иного Измерения',
    'Древний Иллюзорный Камень',
    'Магический Камень Командира Грации',
    'Магический Камень Старшины Грации',
    'Магический Камень Новичка Грации',
)

LIST_OF_RED_ITEMS = (
    'Клинок Сирры',
    'Клинок Архангела',
    'Легендарный Меч',
    'Меч Вальхаллы',
    'Меч Стража',
    'Крушитель Хаоса',
    'Тирбинг',
    'Большой Меч Архангела',
    'Крылатый Клинок Небес',
    'Убийца Драконов',
    'Парные Мечи Таллума',
    'Темный Легион',
    'Парные Мечи Архангела',
    'Ярость Мардил',
    'Парные Мечи Лорда Смерти',
    'Глефа Таллума',
    'Пика',
    'Алебарда Архангела',
    'Алебарда',
    'Аскалон',
    'Кинжал Демона',
    'Убийца Архангела',
    'Рог Крумы',
    'Душегуб',
    'Рассеиватель Пламени',
    'Лук Архангела',
    'Кровавый Лук',
    'Лук Угрозы',
    'Пронзатель Душ',
    'Плазменный Лук',
    'Арбалет Шипов',
    'Певец Судьбы',
    'Арбалет Архангела',
    'Жнец',
    'Песня Мести',
    'Пылающий Череп Дракона',
    'Рука Кабрио',
    'Орб Архангела',
    'Глаз Духа',
    'Элизиум',
    'Доспех Кошмаров',
    'Кираса Кристалла Тьмы',
    'Латный Доспех Апеллы',
    'Туника Совершенства',
    'Мантия Величия',
    'Мантия Сабана',
    'Кираса Полины',
    'Доспех Невитт',
    'Мантия Терси',
    'Кираса Забытого Героя',
    'Доспех Демона',
    'Древний Доспех Эльфов',
    'Кираса Лунной Души',
    'Набедренники Крови',
    'Кристальные Набедренники',
    'Набедренники Духа Шилен',
    'Набедренники Света',
    'Набедренники Ледяного Кристалла',
    'Набедренники Забытого Героя',
    'Набедренники Пылающего Огня',
    'Набедренники Терпения',
    'Набедренники Духов',
    'Перчатки Кристалла Тьмы',
    'Перчатки Благословения',
    'Рукавицы Кошмаров',
    'Перчатки Величия',
    'Ярнглофар',
    'Хранитель Видений',
    'Рукавицы Полины',
    'Перчатки Невитт',
    'Перчатки Терси',
    'Перчатки Забытого Героя',
    'Рукавицы Демона',
    'Древние Рукавицы Эльфов',
    'Рукавицы Оглушения',
    'Перчатки Терпения',
    'Рукавицы Лунной Души',
    'Сапоги Кристалла Тьмы',
    'Сапоги Карли',
    'Древние Сапоги Эльфов',
    'Сапоги Демона',
    'Сапоги Кошмаров',
    'Сапоги Величия',
    'Сапоги Полины',
    'Сапоги Невитт',
    'Сапоги Терси',
    'Сапоги Забытого Героя',
    'Сапоги Эпох',
    'Сапоги Посланника',
    'Сапоги Лунной Души',
    'Шлем Кошмаров',
    'Шлем Кристалла Тьмы',
    'Диадема Величия',
    'Шлем Медузы',
    'Шлем Полины',
    'Диадема Невитт',
    'Диадема Терси',
    'Шлем Демона',
    'Древний Шлем Эльфов',
    'Хильдегрим',
    'Корона Древа Жизни',
    'Плащ Фреи',
    'Плащ Безмолвия',
    'Плащ Деревьев',
    'Чешуя Дракона',
    'Плащ Закена',
    'Крылья Королевы Муравьев',
    'Плащ Айгис',
    'Плащ Властителя',
    'Крылья Селиходена',
    'Плащ Лунной Души',
    'Сердце Сусцептора',
    'Символ Стрелка',
    'Символ Парадии',
    'Панцирь Крумы',
    'Символ Адского Пламени',
    'Рог Селиходена',
    'Кристалл Забвения',
    'Владение Копьем',
    'Последний Выстрел',
    'Духовный Страж',
    'Увеличение Силы',
    'Увеличение Ловкости',
    'Увеличение Интеллекта',
    'Увеличение Проворства',
    'Увеличение Мудрости',
    'Увеличение Выносливости',
    'Сопротивление Оглушению',
    'Сопротивление Удержанию',
    'Спасение',
    'Улучшение Оглушения',
    'Увеличение Мощности Умений',
    'Увеличение Снижения Урона',
    'Высокая Точность',
    'Агрессия',
    'Двойной Шок',
    'Железная Воля',
    'Прикосновение Жизни',
    'Мастер Схватки',
    'Великое Владение Мечом',
    'Священный Удар',
    'Ударная Сила',
    'Возмездие',
    'Выдержка',
    'Отражение Оглушения',
    'Адский Огонь',
    'Щит Стражника',
    'Дрожь',
    'Волновой Меч',
    'Гнев Войны',
    'Великое Владение Двуручным Мечом',
    'Мастер Восстановления',
    'Крещендо Выносливости',
    'Тройное Рассечение',
    'Звуковой Импульс',
    'Обнаружить Уязвимость',
    'Танец Ярости',
    'Разум Чемпиона',
    'Великое Владение Парными Мечами',
    'Двойное Парирование',
    'Владение Звуом',
    'Наказание',
    'Феникс',
    'Топот Гиганта',
    'Удар Вечности',
    'Безумие',
    'Разрушение Энергии',
    'Великое Владение Древковым Оружием',
    'Разоружение',
    'Великолепное Копье',
    'Герой Войны',
    'Незаметность',
    'Зрение Ассасина',
    'Теневой Клинок',
    'Отрава',
    'Критическая Рана',
    'Великое Владение Кинжалом',
    'Сброс Движений',
    'Ядовитый Террор',
    'Отравляющая Бомба',
    'Фатальный Взрыв',
    'Главная Цель',
    'Укол Смерти',
    'Опутывание',
    'Восстановление Маны',
    'Великое Владение Луком',
    'Импульсивный Выстрел',
    'Быстрое Натяжение Тетивы',
    'Мультиудар',
    'Дух Снайпера',
    'Неподвижность',
    'Дисциплина',
    'Разум Вампира',
    'Последнее Уклонение',
    'Великое Владение Арбалетом',
    'Цепной Выстрел',
    'Побег',
    'Ограничивающий Выстрел Болтом',
    'Героизм',
    'Кувырок Назад',
    'Божественная Вспышка',
    'Улучшенный Орб',
    'Правосудие',
    'Мистический Щит',
    'Великое Владение Орбом',
    'Божественная Кара',
    'Последнее Средство',
    'Священный Свет',
    'Массовое Лечение',
    'Снежный Шторм',
    'Отмена',
    'Замешательство',
    'Тайная Мощь',
    'Великое Владение Посохом',
    'Кристалл Инея',
    'Шквальный Удар',
    'Щит Мудреца'
)

LIST_OF_RED_ACCESSORIES = (
    'Ожерелье Баюма',
    'Ожерелье Души Лилит',
    'Ожерелье Души Анаким',
    'Ожерелье Закена',
    'Ожерелье Орфен',
    'Ожерелье Бессмертия',
    'Ожерелье Велчия',
    'Ожерелье Апеллы',
    'Ожерелье Грации',
    'Сияющее Ожерелье',
    'Кольцо Лилит',
    'Кольцо Анаким',
    'Кольцо Баюма',
    'Кольцо Белефа',
    'Кольцо Ядра',
    'Сердце Королевы Муравьев',
    'Кольцо Забытого Героя',
    'Кольцо Страсти',
    'Кольцо Величия',
    'Кольцо Лорда Смерти',
    'Сияющее Кольцо',
    'Пояс Экимуса',
    'Пояс Тиады',
    'Пояс Дракона',
    'Пояс Эратоны',
    'Пояс Октависа'
)

autohotkey = AHK()

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



class Telegram_bot():
    def send_msg_to_tg(self, message, price):

        bot.send_message(TG_USER_ID, f'Куплен {message} за {price}')


class AHKActions():

    # Переменная action отвечает за то, какое действие нужно сделать. (кликнуть, перевести мышку, провести мышкой с нажатием)
    def mouse_actions(self, action, x=0, y=0, direction='R', text=''):

        if action == 'move':
            move = f'''\
            #NoEnv
            #Persistent
            #SingleInstance Off
            #MaxThreads 20
            CoordMode, Mouse, Screen  ;
            MouseMove, {x}, {y}, 0
            Sleep, 300


            '''
            try:
                while autohotkey.get_mouse_position(coord_mode='Screen') != (x, y):
                    autohotkey.run_script(move)
            except:
                pass

            return

        elif action == 'click':
            click = '''\
                #NoEnv
                #Persistent
                #SingleInstance Off
                #MaxThreads 20
                SendEvent {Click}
                Sleep, 300
    
                '''
            try:
                autohotkey.run_script(click)
            except:
                pass

            return

        elif action == 'drag':
            drag = f'''\
            #NoEnv
            #Persistent
            #SingleInstance Off
            #MaxThreads 20
            Click down
            Sleep, 120
            MouseMove, {x}, {y}, 3, R
            Sleep, 120
            Click
            Sleep, 120
            Sleep, 120

            '''
            try:
                autohotkey.run_script(drag)
            except:
                pass
            time.sleep(1*MULTIPLIER)
            return


        elif action == 'wheel':
            wheel = f'''\
            #NoEnv
            #Persistent
            #SingleInstance Off
            #MaxThreads 20
            MouseClick,WheelDown,,,1,0,D,R
            Sleep, 120 

            '''
            autohotkey.run_script(wheel)
            return

        elif action == 'esc':
            esc = '''\
            #NoEnv
            #Persistent
            #SingleInstance Off
            SendInput, {Esc}
            Sleep, 120

            '''
            autohotkey.run_script(esc)
            return

        elif action == 'y':
            y = '''\
            #NoEnv
            #Persistent
            #SingleInstance Off
            SendInput, {y}
            Sleep, 120

            '''
            autohotkey.run_script(y)
            return

        elif action == 'press':
            click_down = '''\
            #NoEnv
            #Persistent
            #SingleInstance Off
            Click down
            Sleep, 120


            '''

            click_up = '''\
            #NoEnv
            #Persistent
            #SingleInstance Off
            Click up
            Sleep, 120

            '''

            try:
                autohotkey.run_script(click_down)
            except:
                pass
            time.sleep(2)
            try:
                autohotkey.run_script(click_up)
            except:
                pass
            return

        elif action == 'type':
            type = f'''\
            #NoEnv
            #Persistent
            #SingleInstance Off
            #MaxThreads 20
            SendInput {text}
            Sleep, 200

            '''
            try:
                autohotkey.run_script(type)
            except:
                pass

class Image():

    def matching(self, main_image_name, template_image_name, need_for_taking_screenshot=False, threshold=0.8,
                 func=None, area_of_screenshot=None):

        if need_for_taking_screenshot is True:
            if area_of_screenshot:
                main_screen = pyscreenshot.grab(bbox=area_of_screenshot)
            else:
                main_screen = pyscreenshot.grab()
            main_screen.save(main_image_name)

        img_rgb = cv2.imread(main_image_name)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template_image_name, 0)

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        if func is None:

            for pt in zip(*loc[::-1]):
                print("Найдено совпадение")
                return True
            return False

        for pt in zip(*loc[::-1]):
            try:
                return pt
            except:
                return False


    def take_screenshot(self, image_name, area_of_screenshot=None):
        if area_of_screenshot:
            main_screen = pyscreenshot.grab(bbox=area_of_screenshot)
        else:
            main_screen = pyscreenshot.grab()
        main_screen.save(image_name)

    def image_to_string(self, image_name, is_digits):
        self._denoise_image(image_name)
        self.fill_the_diamond_with_black()

        if is_digits is True:
            text = pytesseract.image_to_string(image_name, config='--psm 11 -c tessedit_char_whitelist=0123456789')
            print(text)
            return text
        text = pytesseract.image_to_string(image_name, lang='rus', config='--psm 3')
        return text

    def _denoise_image(self, image_name):

        img = cv2.imread(image_name)
        img_bw = 255 * (cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) > 5).astype('uint8')

        se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        mask = cv2.morphologyEx(img_bw, cv2.MORPH_CLOSE, se1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se2)

        mask = np.dstack([mask, mask, mask]) / 255
        out = img * mask
        cv2.imwrite(image_name, out)

    def is_inventory_overflow(self):
        if self.matching(f'{PATH_TO_BUYER}is_inventory_overflow.jpg', f'{PATH_TO_BUYER}inventory_is_overlow.png', need_for_taking_screenshot=True, threshold=0.65) is True:
            return True
        return False

    def fill_the_diamond_with_black(self):
        #смотрим минимальную цену, чтобы потом закрасить там кристалик
        img_rgb = cv2.imread(f'{PATH_TO_BUYER}minimal_price.png')

        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(f'{PATH_TO_BUYER}diamond.png', 0)

        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

        threshold = 0.8
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (15, 18, 22), -1)

        cv2.imwrite(f'{PATH_TO_BUYER}minimal_price.png', img_rgb)

ahk = AHKActions()
image = Image()

class Windows():

    def switch_windows(self, func):
        shell = win32com.client.Dispatch("WScript.Shell")

        windows_list = self.__find_windows()

        print('Спиок открытых окок с линейкой', windows_list)

        if len(windows_list) > 0:
            for window in windows_list:
                for i in range(3):
                    shell.SendKeys('%')

                win32gui.ShowWindow(window, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(window)
                for i in range(2):
                    if self.is_screen_locked() is True:
                        self.unlock_screen()
                if self._is_dead() is True:
                    self._revive()
                    time.sleep(5)
                func()

    def _is_dead(self):
        image.take_screenshot(f'{PATH_TO_BUYER}main_screen.jpg')
        if image.matching(f'{PATH_TO_BUYER}main_screen.jpg', f'{PATH_TO_BUYER}dead.png', need_for_taking_screenshot=True) is True:
            return True
        elif image.matching(f'{PATH_TO_BUYER}main_screen.jpg', f'{PATH_TO_BUYER}dead2.png', need_for_taking_screenshot=True) is True:
            return True

    def _revive(self):
        def __send_to_last_location():
            ahk.mouse_actions('move', x=350, y=180)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=250, y=350)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=420, y=460)
            ahk.mouse_actions('click')

            time.sleep(4)

            ahk.mouse_actions('move', x=1530, y=550)
            ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=900, y=870)
        ahk.mouse_actions('click')

        time.sleep(5)

        ahk.mouse_actions('move', x=1250, y=80)
        ahk.mouse_actions('click')
        image.take_screenshot('amount_of_free_revives.png', area_of_screenshot=(385, 600, 420, 640))
        try:
            amount_of_free_revives = int(pytesseract.image_to_string('amount_of_free_revives.png',
                                                                     config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
        except:
            ahk.mouse_actions('move', x=1050, y=700)
            ahk.mouse_actions('click')

            __send_to_last_location()
            return

        print(amount_of_free_revives)

        if amount_of_free_revives == 0:
            ahk.mouse_actions('esc')
            __send_to_last_location()
            return

        counter = 0
        if amount_of_free_revives > 3:
            amount_of_free_revives = 3
        else:
            amount_of_free_revives = 1

        for i in range(amount_of_free_revives):
            ahk.mouse_actions('move', x=500, y=250+counter)
            ahk.mouse_actions('click')
            counter += 100

        ahk.mouse_actions('move', x=520, y=740)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1050, y=700)
        ahk.mouse_actions('click')

        counter = 0
        #if image.matching('is_items_lose_via_death.png', 'adena.png',need_for_taking_screenshot=True, area_of_screenshot=(325, 600, 420, 650)) is True:
        #    for i in range(4):
        #        ahk.mouse_actions('move', x=500, y=250+counter)
        #        ahk.mouse_actions('click')
        #        counter += 100
        #    ahk.mouse_actions('move', x=520, y=740)
        #    ahk.mouse_actions('click')
        #
        #    ahk.mouse_actions('move', x=1050, y=700)
        #    ahk.mouse_actions('click')


        ahk.mouse_actions('move', x=530, y=170)
        ahk.mouse_actions('click')


        __send_to_last_location()

    def is_screen_locked(self):
        for i in range(2):
            is_locked = image.matching(f'{PATH_TO_BUYER}main_screen.jpg', f'{PATH_TO_BUYER}screen_is_locked.png', need_for_taking_screenshot=True)
        return is_locked

    def unlock_screen(self):
        ahk.mouse_actions('move', x=960, y=540)
        ahk.mouse_actions('drag', x=100, y=100)

    def lock_screen(self):
        ahk.mouse_actions('move', x=73, y=633)
        ahk.mouse_actions('click')
        time.sleep(1)
        ahk.mouse_actions('move', x=960, y=540)
        ahk.mouse_actions('click')

    def __find_windows(self, window_name='Lineage2M'):

        hwnd_list = []  # список для хранения hwnd найденных окон

        # функция для проверки, является ли окно верхним уровнем
        def __is_toplevel(hwnd):
            return win32gui.GetParent(hwnd) == 0 and win32gui.IsWindowVisible(hwnd)  # убедиться, что окно видимо

        # перечисление всех верхних уровней окон
        win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd) if __is_toplevel(hwnd) else None, hwnd_list)

        # фильтрация только окон с нужным именем
        lst_processes = [hwnd for hwnd in hwnd_list if window_name in win32gui.GetWindowText(hwnd)]

        if lst_processes:
            return lst_processes  # возвращает список hwnd, если окна найдены
        else:
            return None  # возвращает None, если окна не найдены


ahk = AHKActions()
image = Image()
telegram = Telegram_bot()
class InGame:
    def go_to_market(self):
        ahk.mouse_actions('move', x=1780, y=80)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1690, y=340)
        ahk.mouse_actions('click')

    def first_mode(self):
        prices_and_goods = self._find_goods_and_prices()
        counter = AMOUNT_ITEMS_TO_BUY
        for i in prices_and_goods.items():
            if counter == 0:
                break
            item_name = i[0]
            print(item_name)

            ahk.mouse_actions('move', x=800, y=280)
            ahk.mouse_actions('click')


            ahk.mouse_actions('move', x=300, y=200)
            ahk.mouse_actions('click')
            name_of_item = item_name.replace(' ', '')
            autohotkey.type(name_of_item)


            ahk.mouse_actions('move', x=260, y=300)
            ahk.mouse_actions('click')
            item_price = i[1]
            print(item_price)

            telegram.send_msg_to_tg(item_name, item_price)

            self._buy_item()
            counter -=1
        ahk.mouse_actions('press')

    def second_mode(self):
        ahk.mouse_actions('move', x=80, y=380)
        ahk.mouse_actions('click')
        for i in LIST_OF_RARE_ITEMS:

            ahk.mouse_actions('move', x=800, y=280)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=300, y=200)
            ahk.mouse_actions('click')
            name_of_item = i.replace(' ', '')
            while True:
               try:
                   autohotkey.type(name_of_item)
                   break
               except:
                   pass


            ahk.mouse_actions('move', x=260, y=300)
            ahk.mouse_actions('click')

            time.sleep(0.8*MULTIPLIER)
            image.take_screenshot(f'{PATH_TO_BUYER}price.png', area_of_screenshot=(1100, 450, 1230, 490))
            price = image.image_to_string(f'{PATH_TO_BUYER}price.png', is_digits=True)
            if int(price) >= 10:
                if int(price) <= SECOND_MODE_PRICE:
                    telegram.send_msg_to_tg(i, price)
                    self._buy_item()


        for i in LIST_OF_RED_ITEMS:

            ahk.mouse_actions('move', x=800, y=280)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=300, y=200)
            ahk.mouse_actions('click')
            name_of_item = i.replace(' ', '')
            autohotkey.type(name_of_item)


            ahk.mouse_actions('move', x=260, y=300)
            ahk.mouse_actions('click')

            time.sleep(0.8*MULTIPLIER)

            image.take_screenshot(f'{PATH_TO_BUYER}price.png', area_of_screenshot=(1103, 440, 1230, 490))
            price = image.image_to_string(f'{PATH_TO_BUYER}price.png', is_digits=True)
            try:
                price = int(price)
            except:
                continue
            if int(price) >= 10:
                if int(price) <= SECOND_MODE_PRICE_FOR_RED:
                    telegram.send_msg_to_tg(i, price)
                    self._buy_item()

        for i in LIST_OF_RED_ACCESSORIES:

            ahk.mouse_actions('move', x=800, y=280)
            ahk.mouse_actions('click')


            ahk.mouse_actions('move', x=300, y=200)
            ahk.mouse_actions('click')
            name_of_item = i.replace(' ', '')
            while True:
                try:
                    autohotkey.type(name_of_item)
                    break
                except:
                    pass


            ahk.mouse_actions('move', x=260, y=300)
            ahk.mouse_actions('click')

            time.sleep(0.8*MULTIPLIER)
            image.take_screenshot(f'{PATH_TO_BUYER}price.png', area_of_screenshot=(1100, 450, 1230, 490))
            price = image.image_to_string(f'{PATH_TO_BUYER}price.png', is_digits=True)
            if int(price) >= 10:
                if int(price) <= SECOND_MODE_PRICE_FOR_RED_ACCESORIES:
                    telegram.send_msg_to_tg(i, price)
                    self._buy_item()

        ahk.mouse_actions('press')

    def third_mode(self):
        PLUS_3_ITEMS = [
        'Символ Нимф'
        ]

        PLUS_5_ITEMS = (
        'Браслет Мучений',
        'Бронзовый Браслет',
        'Кольцо Ветра',
        'Кольцо Мучений',
        'Кольцо Огня',
        'Коралловая Серьга',
        'Магическое Кольцо',
        'Ожерелье Бесстрашия',
        'Ожерелье с Синим Алмазом',
        'Перчатки Шамана Платинового Клана',
        'Серьга Ониксового Зверя',
        'Серьга Подлеска',
        'Синее Коралловое Кольцо',
        'Тигровый Глаз',
        'Тряпичный Пояс',
        )

        PLUS_6_ITEMS = (
        'Мантия Грабителей Могил',
        'Мифриловый Плащ Эльфов',
        'Перчатки Грабителей Могил',
        'Перчатки Шамана Платинового Клана',
        'Туника Шамана Платинового Клана',
        'Шлем Хранителя Хаффа',
        )

        PLUS_7_ITEMS = (
        'Белый Плащ',
        'Бронзовый Шлем',
        'Диадема Духа Ветра',
        'Диадема Кармиана',
        'Доспех Клятвы',
        'Доспех Ящеров Лито',
        'Кинжал Рыцаря-Хранителя Платинового Клана',
        'Кираса Грабителей Могил',
        'Кираса Орков',
        'Кираса Сатиров',
        'Кожаный Доспех Орков',
        'Кожаный Доспех Тека',
        'Композитный Доспех',
        'Копье Пикинера Небесного Дворца',
        'Льняная Рубаха',
        'Льняная Рубаха Ловкости',
        'Льняная Рубаха Мудрости',
        'Льняная Рубаха Силы',
        'Мантия Грабителей Могил',
        'Мифриловая Кираса',
        'Мифриловые Перчатки',
        'Мифриловые Сапоги',
        'Мифриловый Плащ Эльфов',
        'Мифриловый Шлем',
        'Набедренники Орков',
        'Наручи',
        'Панцирная Кираса',
        'Панцирные Рукавицы',
        'Панцирный Шлем',
        'Парные Мечи Пехотинца Орков Кетра',
        'Перчатки Грабителей Могил',
        'Перчатки Кармиана',
        'Перчатки Паагрио',
        'Перчатки Сатиров',
        'Плащ Магии',
        'Плащ Старейшины',
        'Рубаха из Толстой Кожи',
        'Рубаха Концентрации',
        'Рубаха Мстителя',
        'Рукавицы Грабителей Могил',
        'Сапоги Кармиана',
        'Сверкающая Диадема',
        'Туника Кармиана',
        'Туника Командира Фавнов',
        'Туника Орков',
        'Туника Преданности',
        'Туника Шамана',
        'Туника Ящеров Лито',
        'Усиленная Кираса Орков Тимак',
        'Усиленная Кираса Фавнов',
        'Усиленная Туника Орков',
        'Усиленные Кольчужные Сапоги',
        'Усиленные Латные Набедренники',
        'Шлем грабителей Могил',
        'Шляпа Грабителей Могил'
        )

        PLUS_8_ITEMS = (
        'Двуручный Меч Воина-Хранителя Младших Гигантов',
        'Двуручный меч Ящеров Лито',
        'Лук Опытного Стрелка Небесного Дворца',
        'Лук Орков Катера',
        'Лук Платинового Клана',
        'Орб Мага-Хранителя Младших Гигантов',
        'Орб Провидца Небесного Дворца',
        'Орб Шамана Платинового Клана',
        'Парные Мечи Рыцаря-Хранителя Младших Гигантов',
        'Посох Мага-Хранителя Младших Гигантов',
        'Посох Шамана Платинового Клана',
        'Трезубец'
        )

        PLUS_9_ITEMS = (
        'Боевой Арбалет',
        'Боевой Молот',
        'Гастрафет',
        'Гизарма Путешественника',
        'Двуручный Меч Ящеров Лито',
        'Длинный Меч Эльфов',
        'Дубовый Арбалет',
        'кедровый Посох',
        'Кинжал Рыцаря-Хранителя Платинового Клана',
        'Лук Платинового Клана',
        'Меч Рыцаря',
        'Орб Маны',
        'Парные Мечи Рубежа',
        'Парные Шамширы',
        'Посох Жизни',
        'Прочный Арбалет',
        'Скипетр Адепта',
        'Трезубец',
        'Тренировочный Двуручный Меч',
        'Фальшион',
        'Цвайхендер',
        'Эльфийский Лук'
        )

        BOOKS = (
        'Отклонение Стрел',
        'Групповое Лечение',
        'Критическая Магия',
        'Регенерация Маны',
        'Эхо Воодушевления',
        'Истинное Копье',
        'Парирование',
        'Смертельный Импульс',
        'Орлиный взор',
        'Аура Маны'
        )
        ahk.mouse_actions('move', x=80, y=380)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=500, y=280)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=310, y=250)
        ahk.mouse_actions('click')

        ahk.mouse_actions('drag', x=400, y=0)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1770, y=250)
        ahk.mouse_actions('click')

        ahk.mouse_actions('drag', x=-1060, y=0)
        ahk.mouse_actions('click')

        ahk.mouse_actions('move', x=1050, y=950)
        ahk.mouse_actions('click')

        for i in PLUS_3_ITEMS:
            print(i)

            ahk.mouse_actions('move', x=800, y=280)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=300, y=200)
            ahk.mouse_actions('click')
            name_of_item = i.replace(' ', '')
            while True:
                try:
                    autohotkey.type(name_of_item)
                    break
                except:
                    pass


            ahk.mouse_actions('move', x=260, y=300)
            ahk.mouse_actions('click')

            time.sleep(0.8*MULTIPLIER)
            ahk.mouse_actions('move', x=800, y=450)
            ahk.mouse_actions('click')
            time.sleep(1*MULTIPLIER)

            image.take_screenshot(f'{PATH_TO_BUYER}price.png', area_of_screenshot=(1100, 450, 1230, 490))
            price = image.image_to_string(f'{PATH_TO_BUYER}price.png', is_digits=True)
            if int(price) >= 10:
                if int(price) <= account_lvls[i.lower()]:
                    telegram.send_msg_to_tg(i, price)
                    self._buy_item()


        ahk.mouse_actions('press')

        time.sleep(1*MULTIPLIER)



        self.go_to_market()
        ahk.mouse_actions('move', x=80, y=380)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=500, y=280)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=310, y=250)
        ahk.mouse_actions('click')
        ahk.mouse_actions('drag', x=700, y=0)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=1770, y=250)
        ahk.mouse_actions('click')
        ahk.mouse_actions('drag', x=-760, y=0)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=1050, y=950)
        ahk.mouse_actions('click')


        for i in PLUS_5_ITEMS:
            print(i)
            ahk.mouse_actions('move', x=800, y=280)
            ahk.mouse_actions('click')
            ahk.mouse_actions('move', x=300, y=200)
            ahk.mouse_actions('click')
            name_of_item = i.replace(' ', '')
            while True:
                try:
                    autohotkey.type(name_of_item)
                    break
                except:
                    pass

            ahk.mouse_actions('move', x=260, y=300)
            ahk.mouse_actions('click')
            time.sleep(0.8*MULTIPLIER)
            ahk.mouse_actions('move', x=800, y=450)
            ahk.mouse_actions('click')
            time.sleep(1*MULTIPLIER)
            image.take_screenshot(f'{PATH_TO_BUYER}price.png', area_of_screenshot=(1100, 450, 1230, 490))
            price = image.image_to_string(f'{PATH_TO_BUYER}price.png', is_digits=True)
            try:
                if int(price) >= 10:
                    if int(price) <= account_lvls[i.lower()]:
                        telegram.send_msg_to_tg(i, price)
                        self._buy_item()
            except:
                continue


        ahk.mouse_actions('press')

        time.sleep(1*MULTIPLIER)


        self.go_to_market()
        ahk.mouse_actions('move', x=80, y=380)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=500, y=280)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=310, y=250)
        ahk.mouse_actions('click')
        ahk.mouse_actions('drag', x=800, y=0)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=1770, y=250)
        ahk.mouse_actions('click')
        ahk.mouse_actions('drag', x=-660, y=0)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=1050, y=950)
        ahk.mouse_actions('click')


        for i in PLUS_6_ITEMS:
            print(i)

            ahk.mouse_actions('move', x=800, y=280)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=300, y=200)
            ahk.mouse_actions('click')
            name_of_item = i.replace(' ', '')
            while True:
                try:
                    autohotkey.type(name_of_item)
                    break
                except:
                    pass

            ahk.mouse_actions('move', x=260, y=300)
            ahk.mouse_actions('click')
            time.sleep(0.8*MULTIPLIER)
            ahk.mouse_actions('move', x=800, y=450)
            ahk.mouse_actions('click')
            time.sleep(1*MULTIPLIER)
            image.take_screenshot(f'{PATH_TO_BUYER}price.png', area_of_screenshot=(1100, 450, 1230, 490))
            price = image.image_to_string(f'{PATH_TO_BUYER}price.png', is_digits=True)
            try:
                if int(price) >= 10:
                    if int(price) <= account_lvls[i.lower()]:
                        telegram.send_msg_to_tg(i, price)
                        self._buy_item()
            except:
                continue


        ahk.mouse_actions('press')

        time.sleep(1*MULTIPLIER)

        self.go_to_market()
        ahk.mouse_actions('move', x=80, y=380)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=500, y=280)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=310, y=250)
        ahk.mouse_actions('click')
        ahk.mouse_actions('drag', x=900, y=0)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=1770, y=250)
        ahk.mouse_actions('click')
        ahk.mouse_actions('drag', x=-560, y=0)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=1050, y=950)
        ahk.mouse_actions('click')

        for i in PLUS_7_ITEMS:
            print(i)

            ahk.mouse_actions('move', x=800, y=280)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=300, y=200)
            ahk.mouse_actions('click')
            name_of_item = i.replace(' ', '')
            while True:
                try:
                    autohotkey.type(name_of_item)
                    break
                except:
                    pass

            ahk.mouse_actions('move', x=200, y=300)
            ahk.mouse_actions('click')
            time.sleep(0.8*MULTIPLIER)
            ahk.mouse_actions('move', x=800, y=450)
            ahk.mouse_actions('click')
            time.sleep(1*MULTIPLIER)
            image.take_screenshot(f'{PATH_TO_BUYER}price.png', area_of_screenshot=(1100, 450, 1230, 490))
            price = image.image_to_string(f'{PATH_TO_BUYER}price.png', is_digits=True)
            try:
                if int(price) >= 10:
                    if int(price) <= account_lvls[i.lower()]:
                        telegram.send_msg_to_tg(i, price)
                        self._buy_item()
            except:
                continue


        ahk.mouse_actions('press')

        time.sleep(1*MULTIPLIER)


        self.go_to_market()
        ahk.mouse_actions('move', x=80, y=380)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=500, y=280)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=310, y=250)
        ahk.mouse_actions('click')
        ahk.mouse_actions('drag', x=1000, y=0)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=1770, y=250)
        ahk.mouse_actions('click')
        ahk.mouse_actions('drag', x=-460, y=0)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=1050, y=950)
        ahk.mouse_actions('click')

        for i in PLUS_8_ITEMS:
            print(i)

            ahk.mouse_actions('move', x=800, y=280)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=300, y=200)
            ahk.mouse_actions('click')
            name_of_item = i.replace(' ', '')
            while True:
                try:
                    autohotkey.type(name_of_item)
                    break
                except:
                    pass

            ahk.mouse_actions('move', x=260, y=300)
            ahk.mouse_actions('click')
            time.sleep(0.8*MULTIPLIER)
            ahk.mouse_actions('move', x=800, y=450)
            ahk.mouse_actions('click')
            time.sleep(1*MULTIPLIER)
            image.take_screenshot(f'{PATH_TO_BUYER}price.png', area_of_screenshot=(1100, 450, 1230, 490))
            price = image.image_to_string(f'{PATH_TO_BUYER}price.png', is_digits=True)
            try:
                if int(price) >= 10:
                    if int(price) <= account_lvls[i.lower()]:
                        telegram.send_msg_to_tg(i, price)
                        self._buy_item()
            except:
                continue


        ahk.mouse_actions('press')

        time.sleep(1*MULTIPLIER)

        self.go_to_market()
        ahk.mouse_actions('move', x=80, y=380)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=500, y=280)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=310, y=250)
        ahk.mouse_actions('click')
        ahk.mouse_actions('drag', x=1100, y=0)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=1770, y=250)
        ahk.mouse_actions('click')
        ahk.mouse_actions('drag', x=-360, y=0)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=1050, y=950)
        ahk.mouse_actions('click')

        for i in PLUS_8_ITEMS:
            print(i)

            ahk.mouse_actions('move', x=800, y=280)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=300, y=200)
            ahk.mouse_actions('click')
            name_of_item = i.replace(' ', '')
            while True:
                try:
                    autohotkey.type(name_of_item)
                    break
                except:
                    pass

            ahk.mouse_actions('move', x=260, y=300)
            ahk.mouse_actions('click')
            time.sleep(0.8*MULTIPLIER)
            ahk.mouse_actions('move', x=800, y=450)
            ahk.mouse_actions('click')
            time.sleep(1*MULTIPLIER)
            image.take_screenshot(f'{PATH_TO_BUYER}price.png', area_of_screenshot=(1100, 450, 1230, 490))
            price = image.image_to_string(f'{PATH_TO_BUYER}price.png', is_digits=True)
            try:
                if int(price) >= 10:
                    if int(price) <= account_lvls[i.lower()]:
                        telegram.send_msg_to_tg(i, price)
                        self._buy_item()
            except:
                continue


        ahk.mouse_actions('press')

        time.sleep(1*MULTIPLIER)

        self.go_to_market()
        ahk.mouse_actions('move', x=80, y=380)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=500, y=280)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=310, y=250)
        ahk.mouse_actions('click')
        ahk.mouse_actions('drag', x=1200, y=0)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=1770, y=250)
        ahk.mouse_actions('click')
        ahk.mouse_actions('drag', x=-260, y=0)
        ahk.mouse_actions('click')
        ahk.mouse_actions('move', x=1050, y=950)
        ahk.mouse_actions('click')

        for i in PLUS_9_ITEMS:
            print(i)

            ahk.mouse_actions('move', x=800, y=280)
            ahk.mouse_actions('click')

            ahk.mouse_actions('move', x=300, y=200)
            ahk.mouse_actions('click')
            name_of_item = i.replace(' ', '')
            while True:
                try:
                    autohotkey.type(name_of_item)
                    break
                except:
                    pass

                ahk.mouse_actions('move', x=260, y=300)
                ahk.mouse_actions('click')
            time.sleep(0.8*MULTIPLIER)
            ahk.mouse_actions('move', x=800, y=450)
            ahk.mouse_actions('click')
            time.sleep(1*MULTIPLIER)
            image.take_screenshot(f'{PATH_TO_BUYER}price.png', area_of_screenshot=(1100, 450, 1230, 490))
            price = image.image_to_string(f'{PATH_TO_BUYER}price.png', is_digits=True)
            try:
                if int(price) >= 10:
                    if int(price) <= account_lvls[i.lower()]:
                        telegram.send_msg_to_tg(i, price)
                        self._buy_item()
            except:
                continue


        ahk.mouse_actions('press')

        time.sleep(1*MULTIPLIER)

    def check_if_enchanted_correct(self, text):
        for i in range(3):
            image.take_screenshot(f'{PATH_TO_BUYER}enchanted.png', area_of_screenshot=(275, 255, 640, 320))
            if image.image_to_string(f'{PATH_TO_BUYER}enchanted.png', is_digits=False).replace(' ', '').lower() == text.lower():
                print("Enchanted Correct")
                return True
            else:
                if i == 3:
                    time.sleep(1)
                    print("Enchated Error")
                    return False
                time.sleep(1)

    def _find_goods_and_prices(self):
        prices_and_goods = {}
        ahk.mouse_actions('move', x=80, y=380)
        ahk.mouse_actions('click')
        time.sleep(2)
        for i in LIST_OF_RARE_ITEMS:

            ahk.mouse_actions('move', x=800, y=280)
            ahk.mouse_actions('click')


            ahk.mouse_actions('move', x=300, y=200)
            ahk.mouse_actions('click')
            name_of_item = i.replace(' ', '')
            while True:
                try:
                    autohotkey.type(name_of_item)
                    break
                except:
                    pass

            ahk.mouse_actions('move', x=260, y=300)
            ahk.mouse_actions('click')

            time.sleep(0.5*MULTIPLIER)
            image.take_screenshot(f'{PATH_TO_BUYER}price.png', area_of_screenshot=(1100, 450, 1230, 490))
            price = image.image_to_string(f'{PATH_TO_BUYER}price.png', is_digits=True)
            try:
                if int(price) == 10:
                    self._buy_item()
            except:
                continue
            if int(price) >= 10:
                prices_and_goods[i] = int(price)

            print(prices_and_goods)

        prices_and_goods = self.__sort_dict(prices_and_goods)
        return prices_and_goods

    def _buy_item(self):
        for i in range(3):
            ahk.mouse_actions('move', x=900, y=470)
            ahk.mouse_actions('click')
            time.sleep(0.5*MULTIPLIER)
        ahk.mouse_actions('move', x=1100, y=920)
        ahk.mouse_actions('click')

        time.sleep(1.5*MULTIPLIER)
        ahk.mouse_actions('move', x=930, y=900)
        ahk.mouse_actions('click')

    def __sort_dict(self, dict_for_sort):
        sorted_dict = {}
        sorted_keys = sorted(dict_for_sort, key=dict_for_sort.get)
        for w in sorted_keys:
            sorted_dict[w] = dict_for_sort[w]
        return sorted_dict

    def _compare_price(self, neccesary_price):
        image.take_screenshot(f'{PATH_TO_BUYER}price.png', area_of_screenshot=(1100, 450, 1230, 490))
        price = image.image_to_string(f'{PATH_TO_BUYER}price.png', is_digits=True)
        if neccesary_price == price:
            return True
        return False

ingame = InGame()
windows = Windows()

def main():
    ingame.go_to_market()
    if MODE == 1:
        ingame.first_mode()
    if MODE == 2:
        ingame.second_mode()
    if MODE == 3:
        ingame.third_mode()
    if MODE == 4:
        ingame.second_mode()
        ingame.third_mode()

    windows.lock_screen()
def run(mode, minimal_price, minimal_price_for_red, minimal_price_for_red_accesories, amount_items_to_buy, schedule, multiplier, path):
    global MODE
    global SECOND_MODE_PRICE
    global SECOND_MODE_PRICE_FOR_RED
    global SECOND_MODE_PRICE_FOR_RED_ACCESORIES
    global AMOUNT_ITEMS_TO_BUY
    global PATH_TO_BUYER
    global MULTIPLIER


    MODE = int(MODE)
    print('mode is', mode)
    SECOND_MODE_PRICE = int(minimal_price)
    SECOND_MODE_PRICE_FOR_RED = int(minimal_price_for_red)
    SECOND_MODE_PRICE_FOR_RED_ACCESORIES = int(minimal_price_for_red_accesories)

    AMOUNT_ITEMS_TO_BUY = int(amount_items_to_buy)

    PATH_TO_BUYER = f'{str(path)}\\BuyerBot\\'
    print(PATH_TO_BUYER)
    MULTIPLIER = float(multiplier.replace(' ', ''))
    with open(f'{PATH_TO_BUYER}enchanted_items_price_list.json', encoding='utf-8') as account_lvls_json:
        global account_lvls
        account_lvls = json.load(account_lvls_json)
    print(account_lvls)
    windows.switch_windows(main)
