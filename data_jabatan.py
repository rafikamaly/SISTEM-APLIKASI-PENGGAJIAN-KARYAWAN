import sqlite3
import os
import pandas as pd

#Koneksi ke database & membuat cursor
connection = sqlite3.connect('db_perusahaan.db')
cursor = connection.cursor()

#Menu Jabatan
def menu_jabatan():
    print(f"{'='*30} DATA JABATAN {'='*31}\n{'='*75}")
    check = cursor.execute("SELECT * FROM jabatan")
    row = pd.DataFrame(check, columns = ["[ ID ]", "[ NAMA JABATAN ]", "[ GAJI POKOK ]", "[ TUNJANGAN ]"])
    modify = row.to_string(index=False, justify='center')
    print(modify)
    action()

#Aksi CRUD pada menu Jabatan
def action():
    print("="*75)
    print(f"= 1. Buat Data Baru \t\t\t\t\t\t\t  =\n= 2. Ubah Data \t\t\t\t\t\t\t\t  =\n= 3. Hapus Data \t\t\t\t\t\t\t  =\n= 4. Kembali \t\t\t\t\t\t\t\t  =\n{'='*75}")
    choice = int(input("Pilih Menu: "))
    if choice == 1:
        os.system('cls')
        tambah_jabatan()
    elif choice == 2:
        ubah_jabatan()
    elif choice == 3:
        hapus_jabatan()
    elif choice == 4:
        os.system('cls')
        from index import dashboard
        dashboard()
    else:
        os.system('cls')
        print("Tidak ada didaftar pilihan !")
        menu_jabatan()

#Menambah data baru ke dalam database
def tambah_jabatan():
    print(f"{'='*29} INPUT DATA BARU {'='*29}\n{'='*75}")
    nama = input("Note: Tunjangan (20% Gaji)\n\n= Nama Jabatan : ")
    gapok = float(input("= Gaji Pokok   : "))
    tunjangan = gapok * 20 / 100
    cursor.execute("""INSERT INTO jabatan (nama_jabatan, gaji_pokok, tunjangan) VALUES (?, ?, ?)""",
                    (nama, gapok, tunjangan))
    connection.commit()
    os.system('cls')
    print("Data berhasil ditambah !")
    menu_jabatan()

#Mengubah data di dalam database
def ubah_jabatan():
    id = int(input("ID Jabatan: "))
    #Memastikan ID Jabatan lama ada di dalam daftar ID Jabatan
    check_nik = cursor.execute(f"SELECT id_jabatan FROM jabatan WHERE id_jabatan = {id}")
    row_nik = check_nik.fetchall()
    if len(row_nik) == 0:
        os.system('cls')
        print("ID tidak ditemukan !")
        menu_jabatan()
    os.system('cls')
    print(f"{'='*32} UBAH DATA {'='*32}\n{'='*75}")
    nama = input("Note: Tunjangan (20% Gaji)\n\n= Nama Jabatan : ")
    gapok = float(input("= Gaji Pokok   : "))
    tunjangan = gapok * 20 / 100
    cursor.execute('''UPDATE jabatan SET
                    nama_jabatan = ?,
                    gaji_pokok = ?,
                    tunjangan = ?
                    WHERE id_jabatan = ?''',
                    (nama, gapok, tunjangan, id))
    connection.commit()
    os.system('cls')
    print("Data berhasil diubah !")
    menu_jabatan()

#Menghapus data di dalam database
def hapus_jabatan():
    id = int(input("ID Jabatan: "))
    #Memastikan ID Jabatan ada di dalam daftar ID Jabatan
    check_nik = cursor.execute(f"SELECT id_jabatan FROM jabatan WHERE id_jabatan = {id}")
    row_nik = check_nik.fetchall()
    if len(row_nik) == 0:
        os.system('cls')
        print("ID tidak ditemukan !")
        menu_jabatan()
    os.system('cls')
    print(f"{'='*31} HAPUS DATA {'='*32}\n{'='*75}\n")
    check_id = cursor.execute(f"SELECT * FROM jabatan WHERE id_jabatan = {id}")
    row = pd.DataFrame(check_id, columns = ["[ ID ]", "[ NAMA JABATAN ]", "[ GAJI POKOK ]", "[ TUNJANGAN ]"])
    modify = row.to_string(index=False, justify='center')
    print(modify)
    choice = int(input("\nKonfirmasi (1.YA/2.TIDAK): "))
    if choice == 1:
        cursor.execute(f"DELETE FROM jabatan WHERE id_jabatan = {id}")
        connection.commit()
        os.system('cls')
        print("Data berhasil dihapus !")
        menu_jabatan()
    elif choice == 2:
        os.system('cls')
        print("Berhasil dibatalkan !")
        menu_jabatan()
    else:
        os.system('cls')
        print("Tidak ada didaftar pilihan !")
        menu_jabatan()