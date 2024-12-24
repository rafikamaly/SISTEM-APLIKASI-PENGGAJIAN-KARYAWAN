from data_karyawan import menu_karyawan
from data_jabatan import menu_jabatan
from payment import menu_payment
from payroll import menu_payroll
import os
import sqlite3

#Koneksi ke database & membuat cursor
connection = sqlite3.connect('db_perusahaan.db')
cursor = connection.cursor()

#Membuat table jabatan
cursor.execute("""CREATE TABLE IF NOT EXISTS jabatan
                (
                id_jabatan INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_jabatan VARCHAR(100),
                gaji_pokok FLOAT,
                tunjangan FLOAT
                )""")

#Membuat table karyawan
cursor.execute("""CREATE TABLE IF NOT EXISTS karyawan
                (
                nik INTEGER PRIMARY KEY AUTOINCREMENT DEFAULT 110,
                nama_lengkap VARCHAR(100),
                id_jabatan INTEGER,
                jenis_kelamin TEXT CHECK (jenis_kelamin IN ('Pria', 'Wanita')),
                domisili VARCHAR (100),
                no_hp TEXT,
                email VARCHAR (100),
                tanggal_masuk DATE DEFAULT CURRENT_DATE,
                FOREIGN KEY (id_jabatan) REFERENCES jabatan(id_jabatan)
                )""")

#Membuat table slip_gaji
cursor.execute("""CREATE TABLE IF NOT EXISTS slip_gaji
                (
                id_slipgaji INTEGER PRIMARY KEY AUTOINCREMENT,
                nik INTEGER,
                gaji_pokok FLOAT,
                tunjangan FLOAT,
                lembur FLOAT,
                potongan_absensi FLOAT,
                potongan_pajak FLOAT,
                potongan_jht FLOAT,
                potongan_kesehatan FLOAT,
                gaji_bersih FLOAT,
                periode VARCHAR(50),
                FOREIGN KEY (nik) REFERENCES karyawan(nik)
                )""")

#Cek data karyawan & jabatan. Jika belum ada satupun, maka otomatis memasukan data awal yang berisi anggota kelompok
check_karyawan = cursor.execute("SELECT * FROM karyawan")
check_jabatan = cursor.execute("SELECT * FROM jabatan")
row_count_karyawan = check_karyawan.fetchall()
row_count_jabatan = check_jabatan.fetchall()
if len(row_count_karyawan) == 0 and len(row_count_jabatan) == 0:
    cursor.execute("""INSERT INTO jabatan (nama_jabatan, gaji_pokok, tunjangan) VALUES
                    ('Direktur', 10000000, 2000000),
                    ('Manager', 7500000, 1500000),
                    ('Staff', 5000000, 1000000)""")
    cursor.execute("""INSERT INTO karyawan (nik, nama_lengkap, id_jabatan, jenis_kelamin, domisili, no_hp, email) VALUES
                    (100, 'Rafi Kamaly', 1, 'Pria', 'Bogor', 895383146202, 'rafikamaly@gmail.com'),
                    (101, 'Haryady Laksana Putra', 2, 'Pria', 'Depok', 89577834587, 'haryady@gmail.com'),
                    (102, 'Dian Abdul Manan', 3, 'Pria', 'Jakarta', 81277359412, 'yanskuy@gmail.com'),
                    (103, 'Timotius Darius Januarto', 3, 'Pria', 'Depok', 87854229185, 'timotius@gmail.com'),
                    (104, 'Fitriani', 3, 'Wanita', 'Bandung', 89821963340, 'fitriani@gmail.com')""")
    connection.commit()

#Menu Dashboard
def dashboard():
    print(f"{'='*32} DASHBOARD {'='*32} \n{'='*75}")
    print(f"= 1. Data Karyawan {'\t'*7}  = \n= 2. Data Jabatan {'\t'*7}  = \n= 3. Payment {'\t'*8}  = \n= 4. Payroll \t\t{'\t'*6}  = \n= 5. Keluar {'\t'*8}  = \n{'='*75}")
    choice = int(input("Pilih Menu: "))
    if choice == 1:
        os.system('cls')
        menu_karyawan()
    elif choice == 2:
        os.system('cls')
        menu_jabatan()
    elif choice == 3:
        os.system('cls')
        menu_payment()
    elif choice == 4:
        os.system('cls')
        menu_payroll()
    elif choice == 5:
        os.system('cls')
        print("Terimakasih telah menggunakan aplikasi kami :)")
        exit()
    else:
        os.system('cls')
        print("Tidak ada didalam daftar pilihan !")
        dashboard()

#Memanggil fungsi menu Dashboard
dashboard()