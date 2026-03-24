import base64
from io import BytesIO
from typing import Optional
IMAGES_MINE_TYPES = {
    "image/jpeg" ,
    "image/jpg" ,
    "image/png" ,
    "image/webp" ,
    "image/gif" ,
    "image/bmp",
    }
IMAGES_EXTENTIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}
def is_image_file(uploaded_file) -> bool :
    if uploaded_file is None :
        return False
    file_type = getattr(uploaded_file , "type" , "") or ""
    if file_type.lower() in IMAGES_MINE_TYPES :
        return True
    name = getattr(uploaded_file , "name" , "") or ""
    ext = "." + name.rsplit("." , 1)[-1].lower() if "." in name else ""
    return ext in IMAGES_MINE_TYPES
def encode_image_to_base64(uploaded_file) -> Optional[str] :
    try :
        try :
            uploaded_file.seek(0)
        except Exception :
            pass
        raw_bytes = uploaded_file.read()
        if isinstance(raw_bytes , str) :
            raw_bytes = raw_bytes.encode("utf-8")
        b64_string = base64.b64encode(raw_bytes).decode("utf-8")
        return b64_string
    except Exception as e :
        print( "failed to encode image")
        return None
def build_llava_message(user_text : str , b64_image : str) -> dict :
    prompt = user_text.strip() if user_text and user_text.strip() else (
        "describe the photo"
    )
    return {
        "role" : "user" ,
        "content" : prompt ,
        "images" : [b64_image],
    }
def get_image_info(uploaded_file) -> dict :
    try :
        uploaded_file.seek(0)
        data = uploaded_file.read()
        uploaded_file.seek(0)
        size = round(len(data) / 1024 , 1)
    except Exception :
        size = "?"
    return{
        "name" :getattr(uploaded_file , "name" , "unknown") ,
        "mime_type" : getattr(uploaded_file , "type" , "unknown") ,
        "size" : size ,
    }
