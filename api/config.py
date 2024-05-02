from decouple import config
import os


# --------------------------------------------------
#                enviroment variables
# --------------------------------------------------


GOOGLE_API_KEY=config('GOOGLE_API_KEY')
MODEL=config('MODEL')
MODEL_EMBEDDING=config('MODEL_EMBEDDING')

DB_URL=config('DB_URL')


# --------------------------------------------------
#                      settings
# --------------------------------------------------


os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
