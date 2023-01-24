# Laptops_Web_Scraping

Цель: выбрать новый компьютер для покупки. 
Веб-скрапинг ноутбуков реализован для помощи в выполнении данной задачи. Необходимо собрать и сравнить компьютеры с разных сайтов и выбрать из них ТОП-5 лучших (согласно внутреннему ранжированию). 

Собранные данные хранятся в таблице, к записям автоматически выставляется рейтинг "привлекательности для покупки".

## _Стек технологий_
- [Python 3.7.9](https://www.python.org/downloads/release/python-379/)
- [Scrapy 2.7](https://docs.scrapy.org/en/latest/)
- [SQLite3](https://www.sqlite.org/docs.html)

## _Как запустить проект_:

1) Клонируйте репозиторий с проектом:
```
git clone git@github.com:NBN879/laptops_web_scraping.git
```
2) В созданной директории установите виртуальное окружение, активируйте его и установите необходимые зависимости:
```
python3 -m venv venv

. venv/bin/activate

pip install -r requirements.txt
```

3) Запустите файл "main_spider.py". Результаты веб-скрапинга будут записаны в таблицу "laptops.db".

4) Запустите файл "top_5_laptops.py". На экран будут выведены ТОП-5 лучших ноутбуков согласно рейтингу.
______________________________________________________________________

Для каждого ноутбука вычисляется его рейтинг согласно следующей формуле:
```
rank = COEFF_CPU_HHZ * cpu_hhz + COEFF_RAM_GB * ram_gb + COEFF_SSD_GB * ssd_gb + COEFF_PRICE * price_rub
```
где:
- cpu_hhz -- частота процессора, ГГЦ
- ram_gb -- объем ОЗУ, Гб
- ssd_gb -- объем SSD, Гб
- price_rub -- цена, руб
- COEFF_CPU_HHZ, COEFF_RAM_GB, COEFF_SSD_GB, COEFF_PRICE -- веса (коэффициенты)

## _Частный случай вычисления рейтинга_:
При указанных ниже весах (коэффициентах):
- COEFF_CPU_HHZ = 5
- COEFF_RAM_GB = 6
- COEFF_SSD_GB = 2
- COEFF_PRICE = -0.001

получил следующий список ТОП-5 ноутбуков:
1. [MSI Titan GT77 12UHS-208RU](https://www.notik.ru/goods/notebooks-msi-titan-gt77-12uhs-208ru-black-91471.htm)
2. [MSI Stealth GS77 12UHS-030RU](https://www.notik.ru/goods/notebooks-msi-stealth-gs77-12uhs-030ru-black-91481.htm)
3. [MSI Stealth GS66 12UHS-267RU](https://www.notik.ru/goods/notebooks-msi-stealth-gs66-12uhs-267ru-black-91489.htm)
4. [MSI Creator Z17 A12UHST-258RU](https://www.notik.ru/goods/notebooks-msi-creator-z17-a12uhst-258ru-gray-92333.htm)
5. [MSI CreatorPro Z16P B12UMST-223RU](https://www.notik.ru/goods/notebooks-msi-creatorpro-z16p-b12umst-223ru-gray-91967.htm)
______________________________________________________________________
## _Автор_:
> [Николай Бахаруев](https://github.com/NBN879)