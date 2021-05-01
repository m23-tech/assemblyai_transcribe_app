# config.py

# Enable Debugging
DEBUG = True
MAX_CONTENT_LENGTH = 50 * 1024 * 1024 # 50 megabytes
UPLOAD_EXTENSIONS = ['.mp3', '.mp4', '.acc', '.flac']
# Change the Path according to the environment.
UPLOAD_PATH = 'F:\\assemblyai_project\\transcribe_application\\app\\audio'
TRANSCRIBE_PATH = 'F:\\assemblyai_project\\transcribe_application\\app\\transcribe'
SECRET_KEY = 'xxxxxxx' # CREATE A NEW SECRET KEY
ASSEMBLYAI = {'authorization': "XXXXXX"} # ADD PROPER ASSEMBLYAI API KEY
