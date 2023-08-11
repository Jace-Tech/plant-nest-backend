import cloudinary
from dotenv import dotenv_values

ENV = dotenv_values()
          
cloudinary.config( 
    cloud_name = ENV['CLOUD_NAME'], 
    api_key = ENV['CLOUD_API_KEY'], 
    api_secret = ENV['CLOUD_API_SECRET']
)

def upload_file(file, filename):
    try:
        data = cloudinary.uploader.upload(file, public_id=filename)
        return data
    except Exception as e:
        print(str(e))
        return None