# Задание №1
import zipfile
import hashlib
import requests
import re
import os
import csv

# Создать новую директорию, в которую будет распакован архив
# С помощью модуля zipfile извлечь содержимое архива в созданную директорию
arch_file = 'C:\\Users\\andre\\Архив Тест\\'  # путь к архиву
test_zip = zipfile.ZipFile(arch_file + 'tiff-4.2.0_lab1.zip')
"""
#Просмотр содержимого архива
test_zip_files = test_zip.namelist()
print(test_zip_files)
"""

"""
# os.mkdir("Test_folder")
current_directory = os.getcwd()
test_zip.extractall(current_directory + "\\Test_folder")
"""
# Задание №2.1
# Получить список файлов (полный путь) формата txt, находящихся в directory_to_extract_to.
# Сохранить полученный список в txt_files
txt_files = []
directory_to_extract_to = 'Test_folder'
for root, dirs, files in os.walk(directory_to_extract_to):
    for file in files:
        if file.endswith('.txt'):
            txt_files.append(os.path.join(root, file))
print(txt_files)
# Задание №2.2
# Получить значения MD5 хеша для найденных файлов и вывести полученные данные на экран.
print("Значения хеша для всех файлов тхт")
for file in txt_files:
    # Чтение файла
    target_file_data = open(file, 'rb').read() # было битовое считывание
    # Получение MD5 хеша
    result = hashlib.md5(target_file_data).hexdigest() # стереть encode и как было
    print(result)
# Задание №3
print("Найти файл MD5 хеш которого равен target_hash")
target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
# target_hash = "5abeabc600bac08d641612b14cf66dae" # файл READ.txt
target_file = ''
target_file_data = ''  # содержимое искомого файла
# Найти файл MD5 хеш которого равен target_hash в directory_to_extract_to
# Отобразить полный путь к искомому файлу и его содержимое на экране
for root, dirs, files in os.walk(directory_to_extract_to):
    for file in files:
        target_file_data_current = open(root + '\\' + file, 'rb').read()
        # Unicode-objects must be encoded before hashing
        result = hashlib.md5(target_file_data_current).hexdigest()
        if result == target_hash:
            target_file = file
            target_file_data = target_file_data_current
print(target_file)
print(target_file_data)

# Задание №4
# Ниже представлен фрагмент кода парсинга HTML страницы с помощью регулярных выражений. Возможно выполнение этого задания иным способом (например, с помощью сторонних модулей).
r = requests.get(target_file_data)
result_dct = {}  # словарь для записи содержимого таблицы
counter = 0
headers = []
# Получение списка строк таблицы
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
headers = re.sub("<.*?>", " ", lines[0])
headers = re.sub("\  +", " ", headers)
del lines[0]
ln = len(lines)-1

for line in lines:
        temp = re.sub("<.*?>", ';', line)
        # Значения в таблице, заключенные в скобках, не учитывать. Для этого удалить скобки и символы между ними.
        temp = re.sub(r'\(.+?\)', '', temp)
        # Удаление смайлика (для конца, но можно все коды символов передать) СТРОЧКА НЕ РАБОТАЕТ
        temp = re.sub(r'/\xF0\x9F\x93\x9D/u', '', temp)
        # Замена последовательности символов ';' на одиночный символ
        temp = re.sub("\;+",';', temp)
        # Удаление символа ';' в начале и в конце строки
        temp = temp.strip(";")
        # Разбитие строки на подстроки
        tmp_split = temp.split(";")
        # Извлечение и обработка (удаление "лишних" символов) данных из первого столбца
        if counter != ln:# вставка из за того что не получилось удалить смайлик
            country_name = tmp_split[0]
            country_name = country_name[country_name.find(" ") + 1:]
            country_name = country_name[1:]
        else:
            del tmp_split[0]
            country_name = tmp_split[0]
        # Извлечение данных из оставшихся столбцов. Данные из этих столбцов должны иметь числовое значение (прочерк можно заменить на -1).
        """
        if tmp_split[3] == '0*':
            tmp_split[3] = 0
        if tmp_split[3] != '0' and tmp_split[3] != 0:
            tmp_split[3] = re.sub('\xa0', "", tmp_split[3])
        """
        if tmp_split[3] == '_':
            tmp_split[3] = '0%'
        #if tmp_split[4] != -1:
         #   tmp_split[4] = re.sub('\xa0', "", tmp_split[4])
        # Некоторые строки содержат пробелы в виде символа '\xa0'.
        col1_val = int(re.sub('\xa0', "", tmp_split[1]))
        col2_val = int(re.sub('\xa0', "", tmp_split[2]))
        col3_val = str(re.sub('\xa0', "", tmp_split[3]))

        # Запись извлеченных данных в словарь
        result_dct.update({country_name: (col1_val, col2_val, col3_val)})
        """
        for key, value in result_dct.items():
            print(key, ':', value)
        """
        # Задание №5
        # Запись данных из полученного словаря в файл
        output = open('data.csv', 'w')
        output.write(headers)
        output.write('\n')
        for key, value in result_dct.items():
            output.write(key)
            output.write(" ; ")
            output.write(str(value))
            output.write('\n')
        counter += 1

# Задание №6
#Вывод данных на экран для указанного первичного ключа (первый столбец таблицы)
target_country = input("Введите название страны: ")
print(result_dct[target_country][0], result_dct[target_country][1], result_dct[target_country][2])
output.close()