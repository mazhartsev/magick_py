#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Скрипт для массового преобразования изображения для отправки в налоговую, согласно требованиям пункта 3.3 приказа ФНС России от 09.11.2010 N ММВ-7-6/535@
# Copyright (c) 2015, Dmitry Mazhartsev
# GNU General Public License Version 3
import __future__
import os
import sys
import shutil
########################################################################
######################## Параметры пользователя ########################

dpi = '250' # Значение DPI (точек на дюйм)
width = '250'   # DPI (точек на дюйм)
height = '250'  # DPI (точек на дюйм)
extension = ['jpg', 'JPG', 'JPEG','jpeg', 'tiff', 'tif'] # Расширения\Форматы

#################### Конец параметров пользователя #####################
########################################################################

out = 'magick_out'      # Папка для обработанных изображений

if len(sys.argv) == 1:
    img_dir = os.getcwd()
elif len(sys.argv) == 2:
    try:
        img_dir = sys.argv[1]
        os.chdir(img_dir)
    except:
        print('Неправильно указан путь к папке с изображениями')
        sys.exit()
else:
    print('Неправильно указан путь к папке с изображениями')
    sys.exit()

if not os.path.isdir(out):
    os.mkdir(out)

print('\nТекущая директория %s \n' % (os.getcwd()))
print('\nПапка с обработанными файлами %s \n' % (out))

img_list = [] # пустой список для изображений
file_list = os.listdir(img_dir) # список всех файлов в папке
print(file_list)

b = 0 # счетчик количества необработанных изображений

for file in file_list:
    for i in extension:
        if file.endswith(i):
            img_list.append(file)
            
trash_list = list(set(file_list).difference(img_list))


print('Файлы для обработки:')
print(img_list)
c = 0 # счетчик количества обработанных изображений
bl = [] # список для необработанных изображений

for file in img_list:
    c+=1
    str = 'identify -format "%[width]x%[height]" "{file}"'.format(file=file) #image resolution # Дополнительные кавычки вокруг имен файлов служать для экранирования пробелов в именах
    #print(str)
    p = os.popen(str)
    for line in p.readlines():
        img_res = line.split('x')
        print('\n\nРазмер файла %s' % (file)) 
        file_w = int(img_res[0])
        file_h = int(img_res[1][:-1])
        print('Ширина => %s' % (file_w))
        print('Высота => %s' % (file_w))
        
        
        if file_w >= file_h:    # если ширина больше высоты
           str = 'convert "%s" -density %sx -quality 80 -colorspace GRAY %s/"%s"' % (file, dpi, out, file) # Дополнительные кавычки вокруг имен файлов служать для экранирования пробелов в именах
           print('Выполняется преобразование')
           os.popen(str)
               
            
        else:   # если высота больше ширины
            str = 'convert "%s" -density x%s -quality 80 -colorspace GRAY %s/"%s"' % (file, dpi, out, file) # Дополнительные кавычки вокруг имен файлов служать для экранирования пробелов в именах
            print('Выполняется преобразование')
            #print(str)
            os.popen(str)
        print(c)

for i in trash_list:
    b+=1
    print('\nФайл %s имеет недопустимый формат. \nДопутисмый формат JPEG и TIFF.' % (i))
        
print('\n\nВсего обработано - %s' % (c))
print('Оставлено без изменений - %s' % (b))

input('\nНажмите Enter')
