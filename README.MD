# Тестовое задание для Fabrique Studio»

## Приложение для рассылки сообщений клиентам

> С помощью этого приложения можно создавать рассылки по клиентам (в том числе и отложенные) через стороний api-сервис для отправки смс-сообщений.

## Запуск приложения:

- Клонируйте репозиторий командой <code>git clone https://github.com/EvilCOre88/test_work_FS.git</code>

> Для создания и запуска контейнеров введите команду <code>docker-compose up -d</code>

<details>
<summary>Опции:</summary>
Порты можете поменять на любые свои в docker-compose файле.  
</details>

- Теперь можете проверить работу приложения перейдя на [ваш сервер](http://localhost:8888/) (http://localhost:8888/)
- Для работы через браузер перейдите по адресу [api](http://localhost:8888/api/) (http://localhost:8888/api/)
  
> Для проверки работоспособности посылайте api-запросы удобным способом (IDE, postman, curl-запросы)

## Структура ссылок и api-запросов сервиса:

- Если развертвание проекта происходит на удаленном сервере, то вместо <code>localhost</code> используйте ваш домен или ip-адрес.

- список рассылок: <code>http://localhost:8888/api/mailing-lists/</code>

	<details>
	<summary>Структура тела POST api-запроса:</summary>

	```
	{
		"mailing_date_time": null,
		"message": "",
		"filter_code": null,
		"filter_tag": "",
		"finish_date_time": null
	}
	```
	
	**Сообщения будут отправлены клиентам с подходящим тегом или кодом оператора и временем рассылки (есть отложенная рассылка)** 
	> "mailing_date_time": время начала рассылки в формате <code>"2023-01-12T04:49:00"</code>
	
	> "message": сообщение клиенту (строка)
	
	> "filter_code": фильтр кода рассылки в формате <code>925</code>
	
	> "filter_tag": фильтр тега рассылки (строка)
	
	> "finish_date_time": время окончания рассылки в формате <code>"2023-01-12T04:49:00"</code>
	</details>

- детальный список рассылок: <code>http://localhost:8888/api/mailing-lists-details/</code>

- список клиентов: <code>http://localhost:8888/api/clients/</code>

	<details>
	<summary>Структура тела POST api-запроса:</summary>

	```
	{
		"phone": null,
		"code": null,
		"tag": "",
		"timezone": ""
	}
	```

	> "phone": телефон клиента в формате <code>7XXXXXXXXXX</code>
	
	> "code": код клиента в формате <code>925</code>
	
	> "tag": тег клиента (строка)
	
	> "timezone": часовой пояс клиента (чтобы корректировать время рассылки относительно часового пояса клиента) в формате <code>+3</code>
	</details>

- список сообщений: <code>http://localhost:8888/api/messages/</code>

- детальный список сообщений: <code>http://localhost:8888/api/message-detail/</code>

- отправка рассылок: <code>http://localhost:8888/api/send/</code>

	<details>
	<summary>Структура тела POST api-запроса:</summary>

	```
	{
		"mailing_list_id": ""
	}
	```

	> "mailing_list_id": <code><id рассылки></code> для отправки

	</details> 

## Примеры:

```
GET http://localhost:8888/api/clients/
Content-Type: application/json
```

```
POST http://localhost:8888/api/clients/
Content-Type: application/json

{  
  "id": 1,
  "phone": 79773232186,
  "code": 977,
  "tag": "tele",
  "timezone": "+3"  
}
```

```
POST http://localhost:8888/api/mailing-lists/
Content-Type: application/json

{
  "mailing_date_time": "2023-01-09T18:00:00",
  "message": "somessage",
  "filter_code": 977,
  "filter_tag": "tele",
  "finish_date_time": "2023-01-09T23:00:00"
}
```

```
POST http://localhost:8888/api/send/
Content-Type: application/json

{
	"mailing_list_id": 1
}
```

