"""
Отчет по эффективности работы по должностям
"""

from .base_report import BaseReport
from collections import defaultdict


class PerformanceReport(BaseReport):
    def process_data(self):
        """Обработка данных для отчета по эффективности"""
        # Группируем по должности и вычисляем среднюю эффективность
        position_performance = defaultdict(list)
        
        for row in self.data:
            position = row.get('position', '').strip()
            performance = row.get('performance', '')
            
            if position and performance:
                try:
                    performance_value = float(performance)
                    position_performance[position].append(performance_value)
                except ValueError:
                    # Пропускаем некорректные значения
                    continue
        
        # Вычисляем среднее значение для каждой должности
        result_data = []
        for position, performances in position_performance.items():
            if performances:  # Проверяем, что есть данные
                avg_performance = sum(performances) / len(performances)
                result_data.append({
                    'position': position,
                    'performance': round(avg_performance, 2)
                })
        
        # Сортируем по эффективности (по убыванию)
        self.data = sorted(result_data, 
                          key=lambda x: x['performance'], 
                          reverse=True)