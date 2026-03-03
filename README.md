Kaspi Bot на VPS (Вариант А)

Описание
- Telegram-бот объединяет накладные Kaspi в один PDF.
- Поддержка раскладки на A4: 4/8/9 накладных на страницу.
- Поддержка печати: 75/120 мм, 100/150 мм, и A4 полноформат.
- ZIP и PDF входящие файлы.
- Автоматическая загрузка накладных через Kaspi API (OAuth2 client_credentials).
- Сессии без БД — сохраняются в data/sessions.json.

Как запустить
1. Установите зависимости (см. requirements.txt).
2. Настройте переменные окружения:
   - TELEGRAM_TOKEN
   - KASPI_BASE_URL
   - KASPI_CLIENT_ID
   - KASPI_CLIENT_SECRET
3. Разверните как systemd сервис (см. systemd/kaspi_bot.service).
4. Логи смотрите через journalctl -u kaspi_bot -f
