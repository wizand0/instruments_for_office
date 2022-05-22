import os
import shutil
from datetime import datetime

# Получаем список фотографий из папки originals
# Папка должна лежать рядом с этим скриптом
directory = 'originals'
z = "0000"
g = "00"
target_dir = f'modified/{z}/{g}'
files = os.listdir(directory)
# В списке файлов все символы делаем строчными
files_temp = []
tmp_str = ''
for el in files:
    tmp_str = el.lower()
    files_temp.append(tmp_str)

# Выбираем только JPG
files_jpg = filter(lambda file: file.endswith('.jpg'), files)
os.chdir('originals/')
# Перебираем каждый файл из списка фото и вытаскиваем из его EXIF дату фотографирования
for x in files_jpg:
    bool_is_date_in_name = True
    # Раздел для работы с тегами. НУЖНО ДОРАБОТАТЬ!!!!
    # Является ли файл папкой?
    #     if not os.path.isdir(x):
    #         try:
    #             picture = piexif.load(x)
    #         except Exception:
    #             qq = None
    #         else:
    #             qq = None
    #             for i in ("0th", "Exif", "GPS", "1st"):
    #                 for tag in picture[i]:
    #
    #                     # Нам нужны EXIF теги DateTime и DateTimeOriginal
    #                     if ((piexif.TAGS[i][tag]["name"] == "DateTime") or (
    #                     (piexif.TAGS[i][tag]["name"] == "DateTimeOriginal"))):
    #                         # В формате byte
    #                         qq = picture[i][tag]
    #                         # В формате str но с символом byte и кавычками
    #                         qq = str(qq)
    #                         # Обрезание ковычек
    #                         qq = qq[2:21]
    #
    #                         # Парсить дату
    #                         qq = parser.parse(qq)
    #                         # Определяем имена для папки Года и папки месяца
    #                         print(qq)
    #                         g_for_no_date_in_name = qq.strftime('%m')
    #                         z_for_no_date_in_name = qq.strftime('%Y')
    # Если у файла нет тега, то идет поиск даты в имени или присваиваются нули в качестве года и месяца
    # if qq:
    # Еcли в EXIF нет даты то имя папки будет 0000
    # В нее будут складываться фотки без даты в EXIF
    # Находим даты в имени
    if not os.path.isdir(x):
        full_name = os.path.basename(x)
        name = os.path.splitext(full_name)[0]
        if "_" in name:
            date_str = name.split("_")[1]
            if len(date_str) == 8:
                date_if_none = datetime.strptime(date_str, '%Y%m%d')
                g = date_if_none.strftime('%m')
                z = date_if_none.strftime('%Y')
            else:
                bool_is_date_in_name == False

        elif "-" in name:
            date_str = name.split("-")[1]
            if len(date_str) == 8:
                date_if_none = datetime.strptime(date_str, '%Y%m%d')
                g = date_if_none.strftime('%m')
                z = date_if_none.strftime('%Y')
            else:
                bool_is_date_in_name = False
        else:
            bool_is_date_in_name = False

    # Если дату спарсить не удалось, то создаем папку для дальнейшей обработки
    if not bool_is_date_in_name:
        g = " Месяц не определен"
        z = "Год не определен"

    # Создаем папку с подпапкой куда копировать файл
    dst_fldr = f'{z}/{g}'
    try:
        os.makedirs(dst_fldr);
    except:
        print("Folder already exist or some error")
    # Копируем фотку в папку и удаляем оригинал
    shutil.copy2(x, dst_fldr)
    os.remove(x)
