import os
from time import sleep

from PyPDF2 import PdfFileReader, PdfFileWriter
from tqdm import tqdm

"""
Скрипт обрабатывает все pdf файлы в своем каталоге и оставляет только первую и последнюю страницу договора.  
Доделать:
Брать файлы в директории Originals и складывать в Modified
"""
# Создаем список для добавления в него пустых файлов
PLUS_OUTPUT_NAME = "_no_conditions"
all_pdf_files = []
count = 0
# Пробегаем по директории и собираем pdf файлы
for dirpath, dirnames, filenames in os.walk("."):
    for filename in [f for f in filenames if f.endswith(".pdf")]:
        all_pdf_files.append(os.path.join(dirpath, filename))
# Открываем в цикле все файлы по очереди
for file in all_pdf_files:
    if os.stat(file).st_size != 0:
        full_name = os.path.basename(file)
        name = os.path.splitext(full_name)[0]
        print(name)
        infile = PdfFileReader(file, 'rb')
        output = PdfFileWriter()
        number_of_pages = infile.numPages

        if number_of_pages >= 2:
            # Находим первую и последнюю страницу и добавляем в выходной файл
            first_page = infile.getPage(0)
            output.addPage(first_page)
            last_page = infile.getPage(number_of_pages - 1)
            output.addPage(last_page)
            new_name = f'{name}{PLUS_OUTPUT_NAME}.pdf'
            count += 1

            for i in tqdm(range(30)):
                sleep(0.002)

            with open(new_name, 'wb') as f:
                output.write(f)

        else:
            print(f'У файла "{file}" меньше двух страниц')

    else:
        print(f'"{file}" - пустой')
