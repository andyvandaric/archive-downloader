import os
import sys
import PyInstaller.__main__

if __name__ == '__main__':
    # Nama file aplikasi Anda
    script_name = 'main.py'  # Ganti dengan nama file skrip utama Anda
    output_name = 'archive-downloader'  # Ganti dengan nama output yang diinginkan

    # Buat executable untuk berbagai OS
    PyInstaller.__main__.run([
        '--name={}'.format(output_name),
        '--onefile',
        '--windowed',  # Gunakan ini jika Anda tidak ingin menampilkan konsol (hanya untuk aplikasi GUI)
        script_name,
    ])
