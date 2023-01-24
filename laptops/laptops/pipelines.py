# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import sqlite3
from datetime import datetime


COEFF_CPU_HHZ = 5
COEFF_RAM_GB = 6
COEFF_SSD_GB = 2
COEFF_PRICE = -0.001


class LaptopsPipeline:
    def __init__(self):
        self.con = sqlite3.connect('laptops.db')
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS laptops(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            visited_at TEXT,
            name TEXT,
            cpu_hhz REAL,
            ram_gb INTEGER,
            ssd_gb INTEGER,
            price_rub REAL,
            rank REAL)""")

    def process_item(self, item, spider):
        rank = (COEFF_CPU_HHZ * item['cpu_hhz'] +
                COEFF_RAM_GB * item['ram_gb'] +
                COEFF_SSD_GB * item['ssd_gb'] +
                COEFF_PRICE * item['price_rub']
                )
        self.cur.execute("""
            INSERT OR IGNORE INTO laptops (
                url, visited_at, name, cpu_hhz,
                ram_gb, ssd_gb, price_rub, rank
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
                item['url'],
                datetime.now(),
                item['name'],
                item['cpu_hhz'],
                item['ram_gb'],
                item['ssd_gb'],
                item['price_rub'],
                rank
            ))
        self.con.commit()
        return item
