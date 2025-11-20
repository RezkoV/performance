#!/usr/bin/env python3
"""
Скрипт для анализа эффективности работы разработчиков
"""

import argparse
import sys
from reports.performance_report import PerformanceReport


def main():
    parser = argparse.ArgumentParser(description='Анализ эффективности разработчиков')
    parser.add_argument('--files', nargs='+', required=True, 
                       help='Пути к CSV файлам с данными')
    parser.add_argument('--report', nargs='+', required=True,
                       help='Тип отчета и колонки для вывода')
    
    args = parser.parse_args()
    
    if len(args.report) < 2:
        print("Ошибка: для отчета нужно указать как минимум 2 колонки")
        sys.exit(1)
    
    report_type = args.report[0]
    columns = args.report[1:]
    
    # Регистрация доступных отчетов
    report_classes = {
        'performance': PerformanceReport,
    }
    
    if report_type not in report_classes:
        print(f"Ошибка: неизвестный тип отчета '{report_type}'")
        print(f"Доступные отчеты: {list(report_classes.keys())}")
        sys.exit(1)
    
    try:
        # Создание и выполнение отчета
        report = report_classes[report_type](args.files, columns)
        report.generate()
        report.display()
    except Exception as e:
        print(f"Ошибка при выполнении отчета: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()