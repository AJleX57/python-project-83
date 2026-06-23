### Hexlet tests and linter status:
[![Actions Status](https://github.com/AJleX57/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/AJleX57/python-project-83/actions)

### Code quality:
[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=AJleX57_python-project-83)](https://sonarcloud.io/summary/new_code?id=AJleX57_python-project-83)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=AJleX57_python-project-83&metric=bugs)](https://sonarcloud.io/summary/new_code?id=AJleX57_python-project-83)

### Описание проекта
 
**Page Analyzer** — веб-приложение на Flask, которое анализирует указанные
страницы на SEO-пригодность по аналогии с PageSpeed Insights.
 
Приложение позволяет:
- добавлять сайты для анализа;
- запускать проверку доступности сайта;
- получать данные о коде ответа, содержимом тегов `h1`, `title`
  и `meta description`;
- просматривать историю всех проверок.
### Стек технологий
 
- Python, Flask
- PostgreSQL, psycopg
- Bootstrap 5
- BeautifulSoup, requests
- render.com (деплой)
### Установка и запуск локально
 
1. Клонировать репозиторий:
```bash
git clone https://github.com/AJleX57/hexlet-code.git
cd hexlet-code
```
 
2. Установить зависимости:
```bash
make install
```
 
3. Создать локальную базу данных PostgreSQL:
```bash
createdb page_analyzer
psql -d page_analyzer -f database.sql
```
 
4. Создать файл `.env` на основе `.env.example` и заполнить переменные:
```bash
cp .env.example .env
```
```
SECRET_KEY=любая-случайная-строка
DATABASE_URL=postgresql://localhost/page_analyzer
```
 
5. Запустить приложение в режиме разработки:
```bash
make dev
```
 
Приложение будет доступно по адресу [http://localhost:5000](http://localhost:5000)
 
### Запуск в продакшен-режиме
 
```bash
make start
```


### Ссылка на приложение:
https://python-project-83-kbhe.onrender.com