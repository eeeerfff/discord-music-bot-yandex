# Yandex Music Discord Bot

[RU] Простой Discord-бот для проигрывания музыки из Яндекс Музыки в голосовые каналы.  
[EN] A simple Discord bot to play tracks from Yandex Music in voice channels.


## ⚠️ Disclaimer / Дисклеймер

### [RU]
Данный проект создан **исключительно в образовательных целях** для демонстрации работы с Discord API и библиотеками стриминга звука. Автор не несет ответственности за любое нецелевое использование данного кода, нарушение условий обслуживания сторонних сервисов (включая Яндекс Музыку и Discord) или возможные блокировки аккаунтов. Проект не используется в коммерческих целях.

### [EN]
This project is created **strictly for educational purposes** to demonstrate working with the Discord API and audio streaming libraries. The author is not responsible for any misuse of this code, violation of third-party terms of service (including Yandex Music and Discord), or potential account bans. This project is not monetized.

## ⚙️ Prerequisites / Важное требование (FFmpeg)

### [RU] 
Для работы бота **обязательно** требуется установленный в системе **FFmpeg** (утилита для обработки аудио). Без него бот не сможет воспроизводить звук в голосовом канале.
- **Windows**: Скачайте архив с официального сайта [ffmpeg.org](https://ffmpeg.org), распакуйте его и обязательно добавьте путь к папке `bin` в переменные среды (PATH) вашей системы.
- **Linux (Ubuntu/Debian)**: Выполните команду в терминале:  
  `sudo apt update && sudo apt install ffmpeg`
- **macOS**: Выполните команду через Homebrew:  
  `brew install ffmpeg`

### [EN]
This bot **strictly requires** **FFmpeg** installed on your system to process and stream audio into voice channels.
- **Windows**: Download the build from [ffmpeg.org](https://ffmpeg.org), extract it, and add the path to the `bin` folder to your system's Environment Variables (PATH).
- **Linux (Ubuntu/Debian)**: Run `sudo apt update && sudo apt install ffmpeg` in your terminal.
- **macOS**: Run `brew install ffmpeg` using Homebrew.

## 🚀 Features / Возможности

- 🎧 Воспроизведение треков и плейлистов из Яндекс Музыки по ссылке.
- 🔊 Чистый звук и управление очередью (пропуск, пауза, стоп).
- ⚙️ Простая настройка через переменные окружения.

## 🛠️ Installation / Установка

### 1. Клонирование репозитория (Clone the repository)
```bash
git clone https://github.com
cd discord-music-bot-yandex
```

### 2. Установка зависимостей (Install dependencies)
*Если бот на Python:*
```bash
pip install -r requirements.txt
```

### 3. Настройка окружения (Configuration)
Создайте файл `.env` в корневой папке проекта и добавьте туда свои ключи (Create a `.env` file in the root directory and add your keys):

```env
DISCORD_TOKEN=ваш_токен_дискорд_бота
YANDEX_TOKEN=ваш_токен_яндекс_музыки
```

> **Важно / Important:** Никогда не делитесь файлом `.env` и не загружайте его на GitHub! (Never share your `.env` file or commit it to GitHub!).

### 4. Запуск (Run the bot)
*Если бот на Python:*
```bash
python bot.py
```

---

## 🛠️ Tags / Теги для поиска
`discord-bot` `yandex-music` `music-bot` `discord-audio` `yandex-music-api`
