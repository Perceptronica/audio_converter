import os
from telegram import Update, ReplyKeyboardMarkup, InputFile
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TYER, TCON, TPUB, TRCK
from database import Database
from bot_logic import (
    create_artist_keyboard,
    create_albums_keyboard,
    create_tracks_keyboard
)
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

(
    WAITING_FILE,
    ARTIST_SEARCH,
    ARTIST_SELECT,
    ALBUM_SELECT,
    TRACK_SELECT
) = range(5)

MENU_KEYBOARD = ReplyKeyboardMarkup(
    [["/start", "/help"], ["/cancel"]],
    resize_keyboard=True,
    one_time_keyboard=True
)

async def menu(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Выберите команду:",
        reply_markup=MENU_KEYBOARD
    )

async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Я бот для тегирования аудиофайлов. Вот что я могу:\n"
        "/start - начать работу с ботом\n"
        "/menu - открыть меню\n"
        "/help - показать эту справку\n"
        "/cancel - отменить текущую операцию"
    )

MAX_FILE_SIZE = 10 * 1024 * 1024

async def start(update: Update, context: CallbackContext):
    context.user_data.clear()
    await update.message.reply_text(
        "Привет! Я бот для тегирования аудиофайлов. Отправьте мне файл в формате MP3 или FLAC.",
        reply_markup=MENU_KEYBOARD
    )
    return WAITING_FILE

async def handle_file(update: Update, context: CallbackContext):
    logger.info("Пользователь %s отправил файл", update.message.from_user.username)
    file = update.message.document or update.message.audio

    if not file.mime_type in ['audio/mpeg', 'audio/flac']:
        await update.message.reply_text("Неподдерживаемый формат файла! Отправьте файл в формате MP3 или FLAC.")
        return ConversationHandler.END

    if file.file_size > MAX_FILE_SIZE:
        await update.message.reply_text(f"Файл слишком большой! Максимальный размер — {MAX_FILE_SIZE / 1024 / 1024} МБ.")
        return ConversationHandler.END

    user_id = update.message.from_user.id
    file_ext = 'mp3' if file.mime_type == 'audio/mpeg' else 'flac'
    file_name = f"temp/{user_id}_input.{file_ext}"

    os.makedirs("temp", exist_ok=True)
    file = await context.bot.get_file(file.file_id)
    await file.download_to_drive(file_name)

    context.user_data['file_path'] = file_name
    await update.message.reply_text("Введите имя исполнителя:")
    return ARTIST_SEARCH

async def process_artist_search(update: Update, context: CallbackContext):
    db = Database()
    artists = db.search_artists(update.message.text)
    db.close()

    if not artists:
        await update.message.reply_text("Исполнители не найдены. Попробуйте еще раз:")
        return ARTIST_SEARCH

    keyboard = create_artist_keyboard(artists)
    await update.message.reply_text("Выберите исполнителя:", reply_markup=keyboard)
    return ARTIST_SELECT

async def process_artist_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    artist_id = int(query.data.split("_")[1])

    db = Database()
    albums = db.get_albums_by_artist(artist_id)
    db.close()

    if not albums:
        await query.answer("У этого исполнителя нет альбомов!")
        return ARTIST_SELECT

    keyboard = create_albums_keyboard(albums)
    await query.edit_message_text("Выберите альбом:", reply_markup=keyboard)
    return ALBUM_SELECT

async def process_album_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    album_id = int(query.data.split("_")[1])

    db = Database()
    tracks = db.get_tracks_by_album(album_id)
    db.close()

    if not tracks:
        await query.answer("В этом альбоме нет треков!")
        return ALBUM_SELECT

    keyboard = create_tracks_keyboard(tracks)
    await query.edit_message_text("Выберите трек:", reply_markup=keyboard)
    return TRACK_SELECT

async def process_track_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    track_id = int(query.data.split("_")[1])

    db = Database()
    track_info = db.get_track_info(track_id)
    db.close()

    if not track_info:
        await query.answer("Информация о треке не найдена!")
        return TRACK_SELECT

    title, artist, album, year, genre, label, track_number = track_info

    file_path = context.user_data.get('file_path')
    logger.info(f"Применение тегов к файлу: {file_path}")
    logger.info(f"Теги: title={title}, artist={artist}, album={album}, year={year}")
    if not file_path or not os.path.exists(file_path):
        await query.answer("Файл не найден!")
        return TRACK_SELECT

    try:
        if file_path.endswith('.mp3'):
            audio = MP3(file_path, ID3=ID3)
            audio.delete()
            audio.save()
            audio.update({
                'TIT2': TIT2(encoding=3, text=title),
                'TPE1': TPE1(encoding=3, text=artist),
                'TALB': TALB(encoding=3, text=album),
                'TYER': TYER(encoding=3, text=str(year)),
                'TCON': TCON(encoding=3, text=genre),
                'TPUB': TPUB(encoding=3, text=label),
                'TRCK': TRCK(encoding=3, text=str(track_number))
            })
            audio.save()
        else:
            audio = FLAC(file_path)
            audio.clear()
            audio['title'] = title
            audio['artist'] = artist
            audio['album'] = album
            audio['genre'] = genre
            audio['date'] = str(year)
            audio['organization'] = label
            audio['tracknumber'] = str(track_number)
            audio.save()

        new_filename = f"{artist} - {title}"
        with open(file_path, 'rb') as f:
            audio_file = InputFile(f, filename=new_filename)
            await context.bot.send_audio(
                chat_id=query.message.chat_id,
                audio=audio_file,
                title=title,
                performer=artist,
                # album=album
                caption=f"Альбом: {album}\nГод: {year}\nЖанр: {genre}\nЛейбл: {label}\nНомер трека: {track_number}"
            )

        os.remove(file_path)
        await query.answer("Файл успешно обработан!")
        logger.info(f"Отправка файла пользователю {query.message.chat_id}")
    except Exception as e:
        logger.error(f"Ошибка при обработке файла: {e}")
        await query.answer(f"Ошибка: {str(e)}")

    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    if 'file_path' in context.user_data:
        os.remove(context.user_data['file_path'])
    await update.message.reply_text("Операция отменена.")
    return ConversationHandler.END
