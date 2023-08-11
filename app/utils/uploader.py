import cloudinary
import cloudinary.uploader as uploader
from dotenv import dotenv_values

ENV = dotenv_values()

def upload_file(file, filename):      
    cloudinary.config( 
        cloud_name = ENV['CLOUD_NAME'], 
        api_key = ENV['CLOUD_API_KEY'], 
        api_secret = ENV['CLOUD_API_SECRET']
    )
    try:
        data = uploader.upload(file, public_id=filename)
        return data
    except Exception as e:
        print(str(e))
        return None