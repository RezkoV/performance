"""
Базовый класс для всех отчетов
"""

import csv
from abc import ABC, abstractmethod
from tabulate import tabulate


class BaseReport(ABC):
    def __init__(self, files, columns):
        self.files = files
        self.columns = columns
        self.data = []
    
    def read_files(self):
        """Чтение данных из всех переданных файлов"""
        all_data = []
        for file_path in self.files:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    file_data = list(reader)
                    all_data.extend(file_data)
            except FileNotFoundError:
                raise FileNotFoundError(f"Файл не найден: {file_path}")
            except Exception as e:
                raise Exception(f"Ошибка чтения файла {file_path}: {e}")
        
        return all_data
    
    @abstractmethod
    def process_data(self):
        """Абстрактный метод для обработки данных - должен быть реализован в подклассах"""
        pass
    
    def generate(self):
        """Генерация отчета"""
        self.data = self.read_files()
        self.process_data()
    
    def display(self):
        """Отображение отчета в виде таблицы"""
        if not self.data:
            print("Нет данных для отображения")
            return
        
        # Добавляем номер строки
        table_data = []
        for i, row in enumerate(self.data, 1):
            table_row = [i] + [row.get(col, '') for col in self.columns]
            table_data.append(table_row)
        
        headers = ['#'] + self.columns
        print(tabulate(table_data, headers=headers, tablefmt='simple'))