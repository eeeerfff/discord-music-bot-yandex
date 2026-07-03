import os
import asyncio
import random
from dotenv import load_dotenv
import discord
from discord.ext import commands
from yandex_music import ClientAsync

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True 
bot = commands.Bot(command_prefix="!", intents=intents, heartbeat_timeout=120.0)

queue = []
bass_boost = False

# ОПТИМИЗИРОВАНО: Убран флаг -re, добавлены заголовки мобильного приложения Яндекс Музыки
FFMPEG_OPTIONS = {
    'before_options': (
        '-reconnect 1 '
        '-reconnect_streamed 1 '
        '-reconnect_delay_max 5 '
        '-headers "User-Agent: Yandex-Music-API\r\n"' # Маскировка под официальное приложение
    ),
    'options': '-vn'
}

BASS_BOOST_FILTER = '-af equalizer=f=40:width_type=o:width=2:g=17,volume=-1dB'

async def play_next(ctx):
    """Логика воспроизведения следующего трека с защитой от бесконечного цикла"""
    global bass_boost
    if not queue: 
        await ctx.send("📋 Очередь пуста!")
        return
    
    vc = ctx.voice_client
    # Если бот уже отключился или отключается — выходим из функции
    if not vc or not vc.is_connected():
        return

    track = queue.pop(0)
    
    try:
        download_info = await track.get_download_info_async()
        if not download_info:
            raise Exception("Яндекс не отдал информацию о треке")
            
        best_track_info = max(download_info, key=lambda x: x.bitrate_in_kbps)
        direct_link = await best_track_info.get_direct_link_async()
        
        opts = FFMPEG_OPTIONS.copy()
        if bass_boost: 
            opts['options'] += f" {BASS_BOOST_FILTER}"
        
        source = discord.FFmpegPCMAudio(direct_link, **opts)
        
        def after_playing(error):
            if error:
                print(f"Ошибка воспроизведения: {error}")
            # Запускаем следующий трек только ПОСЛЕ того, как текущий полностью завершился
            coro = play_next(ctx)
            fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
            try:
                fut.result()
            except Exception as e:
                print(f"Ошибка в callback: {e}")

        vc.play(source, after=after_playing)
        
        artists = ", ".join([a.name for a in track.artists]) if track.artists else "Неизвестен"
        await ctx.send(f"🎶 Сейчас играет: **{track.title}** — *{artists}*")
        
    except Exception as e:
        print(f"Ошибка загрузки трека '{track.title}': {e}")
        await ctx.send(f"⚠️ Пропущен трек **{track.title}** (Яндекс выдал ограничение или ошибку).")
        
        # ЗАЩИТА: Ждем 2 секунды перед попыткой включить следующий трек,
        # чтобы дать Яндексу "остыть" и не вешать бота в бесконечный цикл.
        await asyncio.sleep(2.0)
        
        # Проверяем, не отключили ли бота за эти 2 секунды
        if vc and vc.is_connected():
            await play_next(ctx)

@bot.command(name='pl')
async def play_liked(ctx):
    """Команда !pl: Подключение к каналу и загрузка лайкнутых треков"""
    if not ctx.author.voice:
        await ctx.send("❌ Сначала зайдите в голосовой канал!")
        return

    vc = ctx.voice_client
    if not vc:
        vc = await ctx.author.voice.channel.connect()
    elif vc.channel != ctx.author.voice.channel:
        await vc.move_to(ctx.author.voice.channel)

    await ctx.send("⏳ Загружаю ваши лайкнутые треки из Яндекс Музыки (до 400 шт)...")

    try:
        # Инициализируем клиента с User-Agent
        client = ClientAsync(os.getenv("YANDEX_TOKEN"))
        await client.init()
        
        likes = await client.users_likes_tracks()
        
        if not likes or not likes.tracks:
            await ctx.send("📂 У вас нет лайкнутых треков или токен не имеет к ним доступа.")
            return

        track_ids = [t.id for t in likes.tracks][:400]
        
        chunk_size = 100
        loaded_tracks = []
        
        for i in range(0, len(track_ids), chunk_size):
            chunk = track_ids[i:i + chunk_size]
            tracks_chunk = await client.tracks(chunk)
            loaded_tracks.extend(tracks_chunk)
            await asyncio.sleep(0.5) # Пауза в полсекунды между пачками, чтобы Яндекс не банил
        
        queue.extend(loaded_tracks)
        await ctx.send(f"✅ Добавлено в очередь треков: {len(loaded_tracks)}")

        if not vc.is_playing(): 
            await play_next(ctx)
            
    except Exception as e:
        await ctx.send(f"❌ Не удалось авторизоваться в Яндекс Музыке. Проверьте YANDEX_TOKEN. ({e})")

@bot.command(name='skip')
async def skip(ctx):
    """Команда !skip: Пропуск текущего трека"""
    vc = ctx.voice_client
    if vc and vc.is_playing():
        vc.stop()
        await ctx.send("⏭️ Трек пропущен.")
    else:
        await ctx.send("Ничего не играет прямо сейчас.")

@bot.command(name='shuffle')
async def shuffle_queue(ctx):
    """Команда !shuffle: Случайное перемешивание текущей очереди треков"""
    global queue
    if not queue:
        await ctx.send("🔀 Очередь пуста, нечего перемешивать!")
        return
    
    if len(queue) == 1:
        await ctx.send("🔀 В очереди всего один трек.")
        return

    random.shuffle(queue)
    await ctx.send(f"🔀 Очередь успешно перемешана! (Всего треков: {len(queue)})")

@bot.command(name='bass')
async def toggle_bass(ctx, mode: str):
    """Команда !bass on/off"""
    global bass_boost
    if mode.lower() == 'on':
        bass_boost = True
        await ctx.send("🔥 **BassBoost включен!** (Изменения вступят со следующего трека)")
    elif mode.lower() == 'off':
        bass_boost = False
        await ctx.send("📉 **BassBoost выключен.** (Изменения вступят со следующего трека)")
    else:
        await ctx.send("Используйте: `!bass on` или `!bass off`")

@bot.command(name='stp')
async def stop(ctx):
    """Команда !stop: Полная остановка и выход из канала"""
    global queue
    queue.clear()
    vc = ctx.voice_client
    if vc:
        await vc.disconnect()
        await ctx.send("👋 Очередь очищена, бот отключился.")
    else:
        await ctx.send("Бот не находится в голосовом канале.")

bot.run(os.getenv("DISCORD_TOKEN"))
