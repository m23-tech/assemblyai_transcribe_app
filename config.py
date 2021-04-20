# config.py

# Enable Debugging
DEBUG = True
MAX_CONTENT_LENGTH = 50 * 1024 * 1024 # 50 megabytes
UPLOAD_EXTENSIONS = ['.mp3', '.mp4', '.acc', '.flac']
# Change the Path according to the environment.
UPLOAD_PATH = 'F:\\assemblyai_project\\transcribe_application\\app\\audio'
TRANSCRIBE_PATH = 'F:\\assemblyai_project\\transcribe_application\\app\\transcribe'
SECRET_KEY = 'm&MIL5w#"lKd|gE'
ASSEMBLYAI = {'authorization': "0d22530347e64a18a9650ee0300638f5"}