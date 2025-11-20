import pytest
import tempfile
import os
from reports.performance_report import PerformanceReport


def create_test_csv(content, filename):
    """Создает временный CSV файл для тестирования"""
    file_path = os.path.join(tempfile.gettempdir(), filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return file_path


def test_performance_report_basic():
    """Тест базового функционала отчета по эффективности"""
    csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,45,4.8,Python,API Team,5
Maria Petrova,Frontend Developer,38,4.7,React,Web Team,4
John Smith,Backend Developer,29,4.6,Python,AI Team,3
Anna Lee,DevOps Engineer,52,4.9,AWS,Infrastructure Team,6"""
    
    test_file = create_test_csv(csv_content, 'test1.csv')
    
    report = PerformanceReport([test_file], ['position', 'performance'])
    report.generate()
    
    # Проверяем, что данные обработаны
    assert len(report.data) == 3  # 3 уникальные должности
    
    # Проверяем сортировку (по убыванию эффективности)
    performances = [row['performance'] for row in report.data]
    assert performances == sorted(performances, reverse=True)
    
    # Проверяем вычисление среднего значения
    backend_perf = next(row for row in report.data if row['position'] == 'Backend Developer')
    expected_avg = (4.8 + 4.6) / 2
    assert backend_perf['performance'] == round(expected_avg, 2)
    
    os.unlink(test_file)


def test_performance_report_multiple_files():
    """Тест обработки нескольких файлов"""
    csv_content1 = """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,45,4.8,Python,API Team,5"""
    
    csv_content2 = """name,position,completed_tasks,performance,skills,team,experience_years
Maria Petrova,Backend Developer,38,4.7,React,Web Team,4"""
    
    test_file1 = create_test_csv(csv_content1, 'test1.csv')
    test_file2 = create_test_csv(csv_content2, 'test2.csv')
    
    report = PerformanceReport([test_file1, test_file2], ['position', 'performance'])
    report.generate()
    
    # Проверяем, что данные из обоих файлов объединены
    backend_perf = next(row for row in report.data if row['position'] == 'Backend Developer')
    expected_avg = (4.8 + 4.7) / 2
    assert backend_perf['performance'] == round(expected_avg, 2)
    
    os.unlink(test_file1)
    os.unlink(test_file2)


def test_performance_report_invalid_data():
    """Тест обработки некорректных данных"""
    csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,45,invalid,Python,API Team,5
Maria Petrova,Frontend Developer,38,4.7,React,Web Team,4"""
    
    test_file = create_test_csv(csv_content, 'test_invalid.csv')
    
    report = PerformanceReport([test_file], ['position', 'performance'])
    report.generate()
    
    # Проверяем, что некорректные данные пропущены
    assert len(report.data) == 1
    assert report.data[0]['position'] == 'Frontend Developer'
    
    os.unlink(test_file)