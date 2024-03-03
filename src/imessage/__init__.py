from subprocess import Popen
import json
import os

TEMP_FILE_NAME = 'temp_py_imessage_shortcuts.json'
REPOSITORY_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_FILE_PATH = os.path.join(REPOSITORY_ROOT_DIR, TEMP_FILE_NAME)

HOME_PATH = os.path.expanduser('~')
SHORTCUTS_DB_PATH = os.path.join(HOME_PATH, 
                                'Library', 'Shortcuts', "Shortcuts.sqlite")
SHORTCUT_NAME = 'send-imessage'
SHORTCUT_PHOTO_NAME = 'send-photo'
SQL_CMD = f'SELECT ZNAME FROM ZSHORTCUT WHERE ZNAME LIKE "{SHORTCUT_NAME}";'
SHORTCUTS_DOCUMENTS_DIR = os.path.join(HOME_PATH, 'Library', 'Mobile Documents', 'iCloud~is~workflow~my~workflows', 'Documents')


def _dump_file(recipients: list[str], message: str) -> None:
    with open(TEMP_FILE_PATH, 'w') as f:
        message_details = {
            'recipients': recipients, 
            'message': message
            }
        json.dump(message_details, f)

def send_image(recipients: list[str], message: str, image_path: str) -> None:
    _dump_file(recipients, message)

    Popen([
        'shortcuts',
        'run',
        SHORTCUT_PHOTO_NAME,
        '--input-path',
        TEMP_FILE_PATH,
        '--input-path',
        image_path,
    ])

def check_shortcut_exists() -> bool:
    """ Validates that the shortcut exists by querying the shortcuts database. 
        Wrap in a try/except in case db connection fails.

    Raises:
        e: if sqlte3 cannot make a database connection this will pass on the exception. 
        Most likely your application needs to be given disk access

    Returns:
        bool: True if 'send-imessage' exists in shortcuts, False if not. 
    """
    import sqlite3
    try:
        conn = sqlite3.connect(SHORTCUTS_DB_PATH)
        cur = conn.cursor()
        cur.execute(SQL_CMD)
        shortcuts = cur.fetchall()
        return len(shortcuts) > 0
    except Exception as e:
        raise e


def send(recipients: list[str], message: str) -> None:
    # Write message details to temp file (Shortcuts via command line only accepts files as inputs)
    _dump_file(recipients, message)

    # Run the shortcut
    Popen([
        'shortcuts',
        'run',
        SHORTCUT_NAME,
        '--input-path',
        TEMP_FILE_PATH,
    ])
