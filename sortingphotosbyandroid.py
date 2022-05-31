import os
import shutil
from datetime import datetime

# Получаем список фотографий из папки originals
# Папка должна лежать рядом с этим скриптом
directory = 'originals'
start_time = datetime.now()
count_of_files = 0
files_size = 0
count_of_mistakes = 0
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

# Выбираем только JPG; У меня в облакене только jpg но и видео и jpeg, png
# files_jpg = filter(lambda file: file.endswith('.jpg'), files)
files_jpg = files
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
                if date_str.isdigit():
                    try:
                        date_if_none = datetime.strptime(date_str, '%Y%m%d')
                        g = date_if_none.strftime('%m')
                        z = date_if_none.strftime('%Y')
                    except Exception:
                        print("Ошибка с распознаванием даты")
                        count_of_mistakes += 1
            else:
                bool_is_date_in_name == False
        elif "-" in name:
            date_str = name.split("-")[1]
            if_first_phrase_is_year = name.split("-")[0]
            if_second_phrase_is_month = name.split("-")[1]
            if_second_phrase_is_year = name.split("-")[1]
            if len(date_str) == 8:
                if date_str.isdigit():
                    try:
                        date_if_none = datetime.strptime(date_str, '%Y%m%d')
                        g = date_if_none.strftime('%m')
                        z = date_if_none.strftime('%Y')
                    except Exception:
                        print("Ошибка с распознаванием даты")
                        count_of_mistakes += 1
            elif len(if_first_phrase_is_year) == 4:
                if if_first_phrase_is_year.isdigit():
                    try:
                        year_of_file = int(if_first_phrase_is_year)
                        if 2000 < year_of_file < 2100:
                            z = year_of_file
                    except Exception:
                        print("Ошибка с распознаванием даты")
                        count_of_mistakes += 1
                    if len(if_second_phrase_is_month) == 2:
                        if if_second_phrase_is_month.isdigit():
                            try:
                                month_of_file = int(if_second_phrase_is_month)
                                if 0 < month_of_file < 13:
                                    if 0 < month_of_file < 10:
                                        g = "0" + str(month_of_file)
                                    else:
                                        g = month_of_file
                            except Exception:
                                print("Ошибка с распознаванием даты")
                                count_of_mistakes += 1
            elif len(if_second_phrase_is_year) == 4:
                if if_second_phrase_is_year.isdigit():
                    try:
                        year_of_file = int(if_second_phrase_is_year)
                        if 2000 < year_of_file < 2100:
                            z = year_of_file
                    except Exception:
                        print("Ошибка с распознаванием даты")
                        count_of_mistakes += 1
                    try:
                        if_third_phrase_is_month = name.split("-")[2]

                        if len(if_third_phrase_is_month) == 2:
                            if if_third_phrase_is_month.isdigit():
                                try:
                                    month_of_file = int(if_third_phrase_is_month)
                                    if 0 < month_of_file < 13:
                                        g = month_of_file
                                except Exception:
                                    print("Ошибка с распознаванием даты")
                                    count_of_mistakes += 1
                    except Exception:
                        print("Месяца нет!")
                        count_of_mistakes += 1
                        g = "00"
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
    count_of_files += 1
    files_size += os.path.getsize(x)
    try:
        shutil.copy2(x, dst_fldr)
        os.remove(x)
        print(f'{count_of_files}: Файл {x} скопирован')
    except Exception:
        print("Ошибка с копированием у файла {x}")
        count_of_mistakes += 1


print(f'Скопировано: {count_of_files} файлов')
all_size = round(files_size/1024, 2)
end_time = datetime.now()
print(f'Общий размер {all_size} Мб')
print(f'Количество ошибок: {count_of_mistakes}')
print('Время выполнения скрипта: {}'.format(end_time - start_time))
