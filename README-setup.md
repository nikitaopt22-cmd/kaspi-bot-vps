Пошаговая инструкция по развёртыванию на VPS (Ubuntu)

1) Подготовка сервера
- Откройте SSH доступ к VPS
- Обновите систему:
  sudo apt update && sudo apt upgrade -y
- Установите зависимости:
  sudo apt install -y python3 python3-venv python3-pip zip unzip git curl

2) Создание пользователя
- sudo adduser kaspi
- sudo usermod -aG sudo kaspi
- Войдите под этим пользователем: sudo su - kaspi

3) Создание проекта и окружения
- mkdir -p ~/kaspi_bot
- cd ~/kaspi_bot
- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt

4) Загрузка файлов проекта
- Создайте файлы bot.py, kaspi_api.py, layout.py и т.д. (можно взять из репозитория)
- Создайте data/sessions.json (или копируйте из data/sessions.json.example)

5) Конфигурация
- В системе: экспортируйте переменные окружения или используйте systemd Environment
- Пример:
  export TELEGRAM_TOKEN=YOUR_TELEGRAM_TOKEN
  export KASPI_BASE_URL=https://api.kaspi.example
  export KASPI_CLIENT_ID=YOUR_CLIENT_ID
  export KASPI_CLIENT_SECRET=YOUR_CLIENT_SECRET

6) systemd сервис
- Создайте /etc/systemd/system/kaspi_bot.service (как в примере выше)
- Примените:
  sudo systemctl daemon-reload
  sudo systemctl enable kaspi_bot
  sudo systemctl start kaspi_bot
  sudo systemctl status kaspi_bot

7) Мониторинг
- journalctl -u kaspi_bot -f

8) Безопасность
- Используйте SSH-ключи, смените порт SSH, настройте ufw
- Не храните токены в репозитории

Готовы начать? Я могу помочь вам с созданием приватного репозитория на GitHub и загрузкой архива в репозиторий. Сообщите, пожалуйста, желаемое имя репозитория и если нужен приватный доступ для вас и вашей команды. Также можно сразу дать ссылку на готовый приватный GitHub репозиторий, где будет полностью размещён код и инструкции.
