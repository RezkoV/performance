import pytest
import tempfile
import os
import subprocess
import sys


def test_main_script_with_valid_args():
    """Тест запуска основного скрипта с валидными аргументами"""
    # Создаем тестовый CSV файл
    csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,45,4.8,Python,API Team,5
Maria Petrova,Frontend Developer,38,4.7,React,Web Team,4"""
    
    test_file = os.path.join(tempfile.gettempdir(), 'test_main.csv')
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(csv_content)
    
    # Запускаем скрипт
    result = subprocess.run([
        sys.executable, 'main.py',
        '--files', test_file,
        '--report', 'performance', 'position', 'performance'
    ], capture_output=True, text=True, cwd='.')
    
    # Проверяем успешное выполнение
    assert result.returncode == 0
    assert 'Backend Developer' in result.stdout
    assert 'Frontend Developer' in result.stdout
    
    os.unlink(test_file)


def test_main_script_with_invalid_file():
    """Тест запуска скрипта с несуществующим файлом"""
    result = subprocess.run([
        sys.executable, 'main.py',
        '--files', 'nonexistent.csv',
        '--report', 'performance', 'position', 'performance'
    ], capture_output=True, text=True, cwd='.')
    
    # Проверяем, что скрипт завершился с ошибкой
    assert result.returncode != 0
    assert 'Файл не найден' in result.stderr or 'Ошибка' in result.stderr


def test_main_script_with_invalid_report():
    """Тест запуска скрипта с неверным типом отчета"""
    result = subprocess.run([
        sys.executable, 'main.py',
        '--files', 'any.csv',
        '--report', 'invalid_report', 'position', 'performance'
    ], capture_output=True, text=True, cwd='.')
    
    # Проверяем, что скрипт завершился с ошибкой
    assert result.returncode != 0
    assert 'неизвестный тип отчета' in result.stderr.lower()