from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_artist_keyboard(artists):
    buttons = [
        [InlineKeyboardButton(name, callback_data=f"artist_{id}")]
        for id, name in artists
    ]
    return InlineKeyboardMarkup(buttons)

def create_albums_keyboard(albums):
    buttons = [
        [InlineKeyboardButton(title, callback_data=f"album_{id}")]
        for id, title in albums
    ]
    return InlineKeyboardMarkup(buttons)

def create_tracks_keyboard(tracks):
    buttons = [
        [InlineKeyboardButton(title, callback_data=f"track_{id}")]
        for id, title in tracks
    ]
    return InlineKeyboardMarkup(buttons)
