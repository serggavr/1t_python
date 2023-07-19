# Задание 3.2 ПРО

### Анализ VK группы  

Берем группу VK  [Онлайн-курсы 1Т Спринт](https://vk.com/1tsprint).

Используя API VK, проанализировать группу по следующим характеристикам:

Количество постов в группе. *DONE*

Количество подписчиков в группе. *DONE*

Количество репостов в группе. *DONE*

Найти TOP 10 самых популярных новостей за последние 3 месяца (популярность новости определяется количеством лайков). Вывести новость и количество лайков.

Найти TOP 10 постов с комментариями (выводятся посты с максимальным количеством комментариев). Вывести посты и количество комментариев.

Вывести в отдельный csv файл следующую информацию: (PRO)
id поста, дата поста, текст поста, id комментария, дата комментария, текст комментария, автор комментария

(выводим только те комментарии, в которых есть упоминание о Data Engineering).

Результатом парсинга по данному заданию должно быть: 
1. csv файл со сводной информацией о группе (пункты 1–3).

2. csv файл с постами и комментариями (пункты 4–6).

Результаты парсинга записать в csv файл.


***
Решение:  

`parser_vk.py` - Парсер  
CSV сохраняются в папку `csv/`




