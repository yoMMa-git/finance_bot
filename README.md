# Реализация бота для учета финансов

  **Цель**: реализовать telegram-бота для учёта финансов. 
  В качестве СУБД используется PostgreSQL, в качестве библиотеки для интеграции с Telegram - aiogram 3.
  
  **Задачи**: 
  - Создание БД: реализация таблиц users (id, name) и operations (id, date, sum, chat_id, type_operation)
  - Реализация регистрации: реализовать функциональность регистрации посредством ввода команды '/reg'
  - Реализация добавления операции: реализовать функциональность добавления операции посредством ввода команды '/add_operation'
  - Реализация просмотра операций пользователя: реализовать функциональность просмотра всех совершённых операций посредством ввода команды '/operations'
  - Реализация функциональности вывода операций с сортировкой по возрастанию/убыванию
