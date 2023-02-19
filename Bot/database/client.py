from pymongo import MongoClient

client = MongoClient('localhost', 27017, connectTimeoutMS=5000)
db = client['mydatabase']


DATABASE_URL = 'mongodb://localhost:27017/'
OWNER_ID = 1234

# Constants for collection names
TYPEDB = 'SoheruGroup'
USERS = 'users'
CHANNELS = 'channels'
GLOBALDB = 'globaldb'
RSS = 'rss'

clientdb = MongoClient(DATABASE_URL)
typedb = clientdb[TYPEDB]
users = typedb[USERS]
channels = typedb[CHANNELS]
globaldb = typedb[GLOBALDB]
rss = typedb[RSS]


def startup():
    """
    Initializes the database with default values if they don't exist.
    """
    x = globaldb.find_one({'setup_done': True})
    if x is not None:
        return

    # Insert default resolutions with auth as True
    resolutions = [
        {'resolution': '360p', 'auth': True},
        {'resolution': '480p', 'auth': True},
        {'resolution': '720p', 'auth': True},
        {'resolution': '1080p', 'auth': True}
    ]
    globaldb.insert_many(resolutions)

    # Insert owner user with auth as True
    owner = {'userid': OWNER_ID, 'auth': True}
    users.insert_one(owner)

    # Mark setup as done
    globaldb.insert_one({'setup_done': True})


def fileformat(query):
    """
    Adds a new file format to the 'globaldb' collection.
    :param query: the file format query to be added.
    """
    globaldb.insert_one({'fileformat': query, 'file': True})


def update_format(query):
    """
    Updates an existing file format query in the 'globaldb' collection.
    :param query: the file format query to be updated.
    """
    globaldb.update_one({'fileformat': query})


def enable_resolution(resolution, yes):
    """
    Enables or disables a resolution in the 'globaldb' collection.
    :param resolution: the resolution to be enabled or disabled.
    :param yes: True to enable the resolution, False to disable it.
    """
    globaldb.update_one({'resolution': resolution}, {'$set': {'auth': yes}})


def check_resolution(resolution):
    """
    Checks whether a resolution is enabled in the 'globaldb' collection.
    :param resolution: the resolution to be checked.
    :return: True if the resolution is enabled, False otherwise.
    """
    x = globaldb.find_one({'resolution': resolution})
    return x['auth'] if x else False


def currentformat():
    """
    Returns the current file format query from the 'globaldb' collection.
    :return: the current file format query.
    """
    x = globaldb.find_one({'file': True})
    return x['fileformat'] if x else None
