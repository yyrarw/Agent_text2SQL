# Agent_text2SQL

# 0. Получает запрос пользователя -> 1. 
# ------Memory------ #
    # *question




                                   # Пробуем еще раз если не нашли подходящие таблицы (3 раза)
# 1. Выбираем нужные таблицы ->    # -> 2.
                                   # Возбуждаем ошибку: "Вопрос не по теме"
# ------Memory------ #
    # *question
    # *relevant_tables:
                # {{
                    # 'table': [column_name]
                # }}





                                   # Пробуем еще раз если не нашли подходящие таблицы (3 раза)
# 2. Выбираем нужные колонки ->    # -> 3.
                                   # Возбуждаем ошибку: "В БД недостаточно информации"
# ------Memory------ #
    # *question
    # *relevant_tables:     **МОЖЕМ УДАЛИТЬ**
                # {{
                    # 'table': [column_name]
                # }}
    # *relevant_tables_with_rel_columns
                # {{
                    # 'table': [relevant_column]
                # }}
                



# 3. Генерируем SQL запрос к базе данных, используя значения из relevant_tables_with_rel_columns -> 4. 
# ------Memory------ #
    # *question
    # *relevant_tables:     **МОЖЕМ УДАЛИТЬ**
                # {{
                    # 'table': [column_name]
                # }}
    # *relevant_tables_with_rel_columns
                # {{
                    # 'table': [relevant_column]
                # }}
    # *sql_request




                                              # Отправляемся к шагу 3. (3 раза)
# 4. Проверяем на валидность SQL запрос    -> # -> 5.
                                              # Возбуждаем ошибку: "Не получилось сгенерировать SQL запрос"
# ------Memory------#
    # *question
    # *relevant_tables:     **МОЖЕМ УДАЛИТЬ**
                # {{
                    # 'table': [column_name]
                # }}
    # *relevant_tables_with_rel_columns
                # {{
                    # 'table': [relevant_column]
                # }}
    # *sql_request
    # sql_request_is_valid
    # *valid_sql_recuest




# 5. Делаем SQL запрос (4.) к базе данны    -> # Обрабатываем запрос и выводим 
# ------Memory------#
    # *question
    # *relevant_tables:     **МОЖЕМ УДАЛИТЬ**
                # {{
                    # 'table': [column_name]
                # }}
    # *relevant_tables_with_rel_columns
                # {{
                    # 'table': [relevant_column]
                # }}
    # *sql_request
    # *valid_sql_recuest
    # *answer