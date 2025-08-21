# aHaHaUpdate
Автоматическое обновление резюме на сайте hh.ru

![Static Badge](https://img.shields.io/badge/diemonic1-aHaHaUpdate-aHaHaUpdate)
![GitHub top language](https://img.shields.io/github/languages/top/diemonic1/aHaHaUpdate)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub Repo stars](https://img.shields.io/github/stars/diemonic1/aHaHaUpdate)
![GitHub issues](https://img.shields.io/github/issues/diemonic1/aHaHaUpdate)

[Получение HH API](#Получение-HH-API)

[Регистрация приложения](#Регистрация-приложения)

[Получаем токены для HH API](#Получаем-токены-для-HH-API)

[Настройка программы](#Настройка-программы)

[Для разработчиков](#Для-разработчиков)

# Получение HH API
## Регистрация приложения
1) Переходим на https://dev.hh.ru/admin 
2) Регистрируем новое приложение

Указываем параметры:
- название приложения: 
любое, какое хотите
- сайт редиректа (редирект URL): 
любая ссылка на ваш сайт/аккаунт (например ссылка на гитхаб, на аккаунт в соцсетях, содержащая https)
- предназначение: 

```только для соискателей```
- Информация о создателе приложения: 

```Вольный разработчик```
- Кто будет его использовать: 

```Только я```
- Какие задачи должно решать приложение: 

```Парсинг интересующих вакансий с помощью python скрипта, составление таблицы с вакансиями для собственной БД, их анализ```
- Опишите все функциональные возможности приложения и укажите используемые методы API:

```
Авторизация с помощью токена, поиск по вакансиям
https://hh.ru/oauth/token/
https://api.hh.ru/resumes/{RESUME_ID}/publish/
https://api.hh.ru/vacancies
```

> [!IMPORTANT]
> После создания заявки ждем от 1 до 20 рабочих дней, пока одобрят доступ к API.

## Получаем токены для HH API
1) Переходим по ссылке, вставив в конце ваш client_id со страницы https://dev.hh.ru/admin 

```https://hh.ru/oauth/authorize?response_type=code&client_id=<ваш client_id из личного кабинета разработчика>```

2) Нас перекидывает на сайт, который вы указали для редиректа. При этом в адресной строке браузера будет добавлен параметр code=<ваш код> - копируем этот код
3) Далее копируем эту команду и в любом редакторе заполняем своими данными - client_id, client_secret (со страницы https://dev.hh.ru/admin) и code (code - полученный на предыдущем шаге)
```
curl -X POST https://hh.ru/oauth/token -F grant_type=authorization_code -F client_id=<ваш client_id из личного кабинета разработчика> -F client_secret=<ваш client_secret из личного кабинета разработчика> -F code=<code, полученный на предыдущем шаге> --ssl-no-revoke
```
4) Копируем команду с заполненными данными и запускаем ее в терминале windows
5) В результате получаем сообщения, где среди прочего будут access_token и refresh_token - копируем их для создания пользователя внутри программы

# Настройка программы
Перед запуском программы необходимо настроить список пользователей, чьи резюме будут обновляться. Найдите в папке программы файл settings.json и откройте его через любой текстовый редактор. В списке пользователей добавьте нужных пользователей, указав им имя (используется для записи в логах и для уведомлений через телеграмм бота), токены, и список ID тех резюме, которые необходимо обновлять.

В настройках вы также можете указать токен телеграмм бота, а так же ваш ID в телеграмм. Бот будет присылать вам сообщения о работе программы (была запущена, обновила резюме, произошла ошибка). Можно настроить, какие сообщения будут приходить - все, или только ошибки ("tg_notify_only_on_errors": "True" - будет уведомлять только при ошибках, "tg_notify_only_on_errors": "False" - при всех событиях). Если вам не нужен телеграмм бот, оставьте настройки токена бота и ID юзера пустыми.

Примеры:
Один пользователь:
```
{
  "users":
  [
    {
      "name": "дядя Дима",
      "access_token": "DFGKKOSGJEJT8745FGJKDKLJ895435",
      "refresh_token": "SDFWSERWE87945903769DFGSDKLGJK3457834965",
      "resumes_ids": ["b7bgfh4564ff0d25cdde00dfg57664gng41"]
    }
  ],
  "telegram_bot_token": "3546741123:GHT_Jq95xMNpiM-3MdObx2fgdfgyx5Ode_VB",
  "tg_user_id": "3456876",
  "tg_notify_only_on_errors": "True"
}
```
Два пользователя:
```
{
  "users":
  [
    {
      "name": "дядя Дима",
      "access_token": "DFGKKOSGJEJT8745FGJKDKLJ895435",
      "refresh_token": "SDFWSERWE87945903769DFGSDKLGJK3457834965",
      "resumes_ids": ["b7bgfh4564ff0d25cdde00dfg57664gng41"]
    },
    {
      "name": "дядя Петя",
      "access_token": "FGIUTRWMS786SDF067SDFSFSDF",
      "refresh_token": "FDGDKJTIJ45456SDGFKSNG89",
      "resumes_ids": ["hdf80jjk45688fghkklj58", "x5476cvn465465nbvcn995ccvb"]
    }
  ],
  "telegram_bot_token": "",
  "tg_user_id": "",
  "tg_notify_only_on_errors": "True"
}
```
Несколько резюме у одного пользователя:
```
{
  "users":
  [
    {
      "name": "дядя Федя",
      "access_token": "DJGKDLFJHG7987CJGSDKFG45467",
      "refresh_token": "DFNBDFBNG8973464CVXSDGGSg",
      "resumes_ids": ["nb56bvcb80968f6gh9bnvn", "cvbnj2345bbhj56f4lbhj547"]
    }
  ],
  "telegram_bot_token": "",
  "tg_user_id": "",
  "tg_notify_only_on_errors": "False"
}
```

Если вы хотите, чтобы программа автоматически запускалась при старте системы, создайте ярлык aHaHaUpdate.exe и поместите его в папку автозагрузки Windows:
```
C:\Users\Имя_пользователя\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

> [!TIP]
> В папке Logs будут записывать логи по всем действиям программы. Логи именуются по текущему месяцу и году.

После настройки запустите файл aHaHaUpdate.exe

# Для разработчиков
Для сборки exe приложения используется pyinstaller.exe
Если вы хотите как-то модифицировать программу, вам необходимо изменять python файл aHaHaUpdate.py - в нем содержится весь код.
После этого:
1. Откройте консоль от имени администратора в папке, в которой лежит aHaHaUpdate.py
2. Выполните команду: ```pyinstaller.exe —onedir —icon=CatPilot.ico —windowed aHaHaUpdate.py```
3. После окончания сборки в папке dist появится папка aHaHaUpdate, это готовая сборка
4. Скопируйте из папки ADD все содержимое в папку aHaHaUpdate, в которой находится сборка (это дополнительные файлы, нужные для работы программы)
5. Теперь программу можно как обычно запускать с помощью aHaHaUpdate.exe
