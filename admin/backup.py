import dropbox
from django.conf import settings
import os
from datetime import datetime as dt


def backup_and_upload_to_dropbox():
    # Chạy lệnh sao lưu cơ sở dữ liệu
    os.system('python manage.py dbbackup')

    # Đường dẫn đến thư mục lưu trữ sao lưu
    backup_location = settings.DBBACKUP_STORAGE_OPTIONS.get('location')

    # Tạo tên file sao lưu mới sử dụng hàm tên file tùy chỉnh
    formatted_datetime =dt.now().strftime('%Y-%m-%d')
    backup_file = f"{formatted_datetime}.psql.bin"

    # Access token từ Dropbox App Console
    access_token = 'sl.Bpdff8ea_TpY-mLi7p2hJjzJGj_Pw4YA1Gx2UJkdQBY7FQVMJH_cBs3w2jPnXPh--q6lSKqyiyAjqShLhTNO3v-ERYUzQbU2gYtkJLKThRjhfPD_8ctIt5weED7a7izNJv7nGC2iu71z'

    # Khởi tạo Dropbox client
    dbx = dropbox.Dropbox(access_token)

    # Tải lên tệp sao lưu lên Dropbox
    with open(os.path.join(backup_location, backup_file), 'rb') as f:
        dbx.files_upload(f.read(), f'/DjangoBackups/{backup_file}')


