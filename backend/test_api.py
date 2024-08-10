import httpx
import asyncio
from datetime import datetime

BASE_URL = "http://10.2.0.125:8000"


async def main():
    async with httpx.AsyncClient() as client:
        # Ввод данных для регистрации бизнеса
        business_name = input("Введите название бизнеса: ")
        business_data = {
            "name": business_name
        }
        response = await client.post(f"{BASE_URL}/register_business/", json=business_data)
        print("Регистрация бизнеса статус:", response.status_code)
        print("Регистрация бизнеса ответ:", response.text)
        if response.status_code == 200:
            print("Регистрация бизнеса:", response.json())
        else:
            print("Ошибка регистрации бизнеса:", response.text)
            return

        # Ввод данных для регистрации пользователя
        username = input("Введите имя пользователя: ")
        phone_number = input("Введите номер телефона: ")
        password = input("Введите пароль: ")
        role = input(
            "Введите роль (финансовый директор, менеджер объекта, прораб): ")
        worker_data = {
            "username": username,
            "phone_number": phone_number,
            "password": password,
            "role": role
        }
        response = await client.post(f"{BASE_URL}/register_worker/?business_name={business_name}", json=worker_data)
        print("Регистрация пользователя статус:", response.status_code)
        print("Регистрация пользователя ответ:", response.text)
        if response.status_code == 200:
            print("Регистрация пользователя:", response.json())
        else:
            print("Ошибка регистрации пользователя:", response.text)
            return

        # Ввод данных для входа пользователя
        login_phone_number = input("Введите номер телефона для входа: ")
        login_password = input("Введите пароль для входа: ")
        login_data = {
            "username": login_phone_number,
            "password": login_password
        }
        response = await client.post(f"{BASE_URL}/token", data=login_data)
        print("Вход пользователя статус:", response.status_code)
        print("Вход пользователя ответ:", response.text)
        if response.status_code == 200:
            if "businesses" in response.json():
                businesses = response.json()["businesses"]
                print("Выберите бизнес для входа:")
                for i, business in enumerate(businesses):
                    print(f"{i + 1}. {business['name']}")
                selected_business_index = int(
                    input("Введите номер бизнеса: ")) - 1
                selected_business_id = businesses[selected_business_index]["_id"]

                selection_data = {
                    "phone_number": login_phone_number,
                    "business_id": selected_business_id
                }
                response = await client.post(f"{BASE_URL}/select_business", json=selection_data)
                print("Выбор бизнеса статус:", response.status_code)
                print("Выбор бизнеса ответ:", response.text)
                if response.status_code == 200:
                    tokens = response.json()
                    print("Вход пользователя:", tokens)
                else:
                    print("Ошибка выбора бизнеса:", response.text)
                    return
            else:
                tokens = response.json()
                print("Вход пользователя:", tokens)
        else:
            print("Ошибка входа пользователя:", response.text)
            return

        # Установка заголовка авторизации
        headers = {
            "Authorization": f"Bearer {tokens['access_token']}"
        }

        # Ввод данных для создания задания
        task_title = input("Введите название задания: ")
        task_description = input("Введите описание задания: ")
        task_role = input("Введите роль для задания: ")
        task_due_date = input("Введите срок выполнения задания (YYYY-MM-DD): ")
        task_document = input(
            "Введите имя файла для загрузки (если есть, иначе оставьте пустым): ")
        task_data = {
            "title": task_title,
            "description": task_description,
            "role": task_role,
            "due_date": datetime.strptime(task_due_date, "%Y-%m-%d")
        }
        if task_document:
            with open(task_document, "rb") as file:
                files = {'file': (task_document, file.read())}
                response = await client.post(f"{BASE_URL}/upload_document/?business_name={business_name}", headers=headers, files=files, data={})
                if response.status_code == 200:
                    document_info = response.json()
                    task_data["document"] = document_info["document_id"]
                else:
                    print("Ошибка загрузки документа:", response.text)
                    return

        response = await client.post(f"{BASE_URL}/create_task/", json=task_data, headers=headers)
        print("Создание задания статус:", response.status_code)
        print("Создание задания ответ:", response.text)
        if response.status_code == 200:
            print("Создание задания:", response.json())
        else:
            print("Ошибка создания задания:", response.text)

        # Получение списка заданий
        task_role = input("Введите роль для получения заданий: ")
        response = await client.get(f"{BASE_URL}/tasks/?role={task_role}", headers=headers)
        print("Список заданий статус:", response.status_code)
        print("Список заданий ответ:", response.text)
        if response.status_code == 200:
            print("Список заданий:", response.json())
        else:
            print("Ошибка получения списка заданий:", response.text)

        # Ввод данных для отправки отчета о выполнении задания
        task_id = input("Введите ID задания для отправки отчета: ")
        task_report = input("Введите отчет о выполнении задания: ")
        report_data = {
            "task_id": task_id,
            "report": task_report
        }
        response = await client.post(f"{BASE_URL}/submit_task_report/", json=report_data, headers=headers)
        print("Отправка отчета статус:", response.status_code)
        print("Отправка отчета ответ:", response.text)
        if response.status_code == 200:
            print("Отправка отчета:", response.json())
        else:
            print("Ошибка отправки отчета:", response.text)

        # Подтверждение выполнения задания
        task_id = input("Введите ID задания для подтверждения: ")
        response = await client.post(f"{BASE_URL}/confirm_task/", json={"task_id": task_id}, headers=headers)
        print("Подтверждение задания статус:", response.status_code)
        print("Подтверждение задания ответ:", response.text)
        if response.status_code == 200:
            print("Подтверждение задания:", response.json())
        else:
            print("Ошибка подтверждения задания:", response.text)

        # Отклонение отчета о выполнении задания
        task_id = input("Введите ID задания для отклонения отчета: ")
        response = await client.post(f"{BASE_URL}/reject_task_report/", json={"task_id": task_id}, headers=headers)
        print("Отклонение отчета статус:", response.status_code)
        print("Отклонение отчета ответ:", response.text)
        if response.status_code == 200:
            print("Отклонение отчета:", response.json())
        else:
            print("Ошибка отклонения отчета:", response.text)

asyncio.run(main())
