from nodes import WorkflowManager

question = 'Найти клиентов, у которых есть активные страховые полисы с суммой покрытия более 500000 рублей, и показать их имена, тип полиса и дату окончания. Результат отсортировать по сумме покрытия по убыванию.'

graph = WorkflowManager(db_id='banking', url='localhost:1234').return_graph()

for massage in graph.stream({'question': question}):
    print(massage)


