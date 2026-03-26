import base64
from io import BytesIO
from typing import Optional,List
from PIL import Image
IMAGES_MIME_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/gif",
    "image/bmp",
}
IMAGES_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
    ".bmp"
}
MAX_IMAGE_SIZE = 5 * 1024 * 1024
MAX_RESOLUTION = (1024,1024)
MAX_IMAGES = 2
def is_image_file(uploaded_file)->bool:
    if uploaded_file is None:
        return False
    file_type = getattr(uploaded_file,"type") or ""
    if file_type.lower() in IMAGES_MIME_TYPES:
        return True
    name = getattr(uploaded_file,"name") or ""
    ext="."+name.rsplit(".",1)[-1].lower() if "." in name else ""
    return ext in IMAGES_EXTENSIONS
def encode_image_to_base64(uploaded_file)->Optional[str]:
    try:
        uploaded_file.seek(0)
        raw_bytes=uploaded_file.read()
        if len(raw_bytes)>MAX_IMAGE_SIZE:
            print("image too large")
            return None
        img=Image.open(BytesIO(raw_bytes))
        img=img.convert("RGB")
        img.thumbnail(MAX_RESOLUTION)
        buffer=BytesIO()

        img.save(
            buffer,
            format="JPEG",
            quality=85,
            optimize=True
        )
        return base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")
    except Exception as e:
        print("failed to encode image:",e)
        return None
def validate_images(image_files)->List[str]:
    valid=[]
    for f in image_files:
        encoded=encode_image_to_base64(f)
        if encoded:
            valid.append(encoded)
    return valid[:MAX_IMAGES]
def build_llava_message(user_text:str,images:List[str])->dict:
    prompt=user_text.strip() if user_text else "Describe this image"
    return{
        "role":"user",
        "content":prompt,
        "images":images
    }
def get_image_info(uploaded_file)->dict:
    try:
        uploaded_file.seek(0)
        data=uploaded_file.read()
        uploaded_file.seek(0)
        size=round(len(data)/1024,1)
    except Exception:
        size="?"
    return{
        "name":getattr(uploaded_file,"name"),
        "mime_type":getattr(uploaded_file,"type"),
        "size":size,
    }