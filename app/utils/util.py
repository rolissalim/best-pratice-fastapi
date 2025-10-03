import secrets
from datetime import datetime
import pytz
# import aiofiles
from datetime import datetime

def unique_string(byte: int = 8) -> str:
    return secrets.token_urlsafe(byte)

def convert_date_to_timestamp(date_string: str):
    if date_string:
        date_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        return date_object.timestamp()
    
def format_currency(amount):
    formatted_amount = "{:,.2f}".format(amount)
    formatted_amount = "Rp " + formatted_amount
    return formatted_amount


# Mendapatkan zona waktu Indonesia
tz = pytz.timezone('Asia/Jakarta')

def get_local_time():
    return datetime.now(tz)

# async def generate_large_excel(path: str):
#     async with aiofiles.open(path, mode='rb') as excel_file:
#         while True:
#             chunk = await excel_file.read(1024 * 1024)  # Read in 1MB chunks
#             if not chunk:
#                 break
#             yield chunk
