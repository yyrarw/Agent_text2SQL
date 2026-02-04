from agent import WorkflowManager

question = 'Вывести список всех транзакций по кредитным картам за последний месяц с указанием имени клиента и названия торговой точки. Результат отсортировать по дате транзакции по убыванию.'

graph = WorkflowManager(db_id='banking', url='localhost:1234').return_graph()

for massage in graph.stream({'question': question}):
    print(massage)

            