import sqlite3
import os
import pandas as pd

#Koneksi ke database & membuat cursor
connection = sqlite3.connect('db_perusahaan.db')
cursor = connection.cursor()

#Menu Karyawan
def menu_karyawan():
    print(f"{'='*30} DATA KARYAWAN {'='*30}\n{'='*75}")
    check = cursor.execute("""SELECT 
                    k.nik,
                    k.nama_lengkap,
                    j.nama_jabatan,
                    k.jenis_kelamin,
                    k.domisili,
                    k.no_hp,
                    k.email,
                    k.tanggal_masuk
                    FROM karyawan k INNER JOIN jabatan j ON k.id_jabatan = j.id_jabatan
                    """)
    row = pd.DataFrame(check, columns = [" [ NIK ] ", " [ NAMA ] ", " [ JABATAN ] ", " [ JENIS KELAMIN ] ", " [ DOMISILI ] ", " [ NO.HP ] ", " [ EMAIL ] ", " [ TGL BERGABUNG ] "])
    modify = row.to_string(index=False, justify='center')
    print(modify)
    action()

#Aksi CRUD pada menu Karyawan
def action():
    print("="*75)
    print(f"= 1. Buat Data Baru \t\t\t\t\t\t\t  =\n= 2. Ubah Data \t\t\t\t\t\t\t\t  =\n= 3. Hapus Data \t\t\t\t\t\t\t  =\n= 4. Kembali \t\t\t\t\t\t\t\t  =\n{'='*75}")
    choice = int(input("Pilih Menu: "))
    if choice == 1:
        os.system('cls')
        tambah_karyawan()
    elif choice == 2:
        ubah_karyawan()
    elif choice == 3:
        hapus_karyawan()
    elif choice == 4:
        os.system('cls')
        from index import dashboard
        dashboard()
    else:
        os.system('cls')
        print("Tidak ada didaftar pilihan !")
        menu_karyawan()

#Menambah data baru ke dalam database
def tambah_karyawan():
    print(f"{'='*29} INPUT DATA BARU {'='*29}\n{'='*75}")
    nik = int(input("= NIK                         : "))
    #Memastikan bahwa NIK tidak boleh sama
    check_nik = cursor.execute(f"SELECT nik from karyawan WHERE nik = {nik}")
    row_nik = check_nik.fetchall()
    if len(row_nik) != 0:
        os.system('cls')
        print("NIK tidak boleh sama !")
        tambah_karyawan()
    nama = input("= Nama                        : ")
    print()
    check = cursor.execute("SELECT * FROM jabatan")
    row = pd.DataFrame(check, columns = ["[ ID ]", "[ NAMA JABATAN ]", "[ GAJI POKOK ]", "[ TUNJANGAN ]"])
    modify = row.to_string(index=False, justify='center')
    print(modify)
    jabatan = input(("\n= ID Jabatan                  : "))
    jenis_kelamin = input("= Jenis Kelamin (Pria/Wanita) : ")
    domisili = input("= Domisili                    : ")
    nohp = int(input("= No. HP                      : "))
    email = input("= Email                       : ")
    cursor.execute("""INSERT INTO karyawan (nik, nama_lengkap, id_jabatan, jenis_kelamin, domisili, no_hp, email) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (nik, nama, jabatan, jenis_kelamin, domisili, nohp, email))
    connection.commit()
    os.system('cls')
    print("Data berhasil ditambah !")
    menu_karyawan()

#Mengubah data di dalam database
def ubah_karyawan():
    nik_lama = int(input("NIK Lama: "))
    #Memastikan NIK lama ada di dalam daftar NIK Karyawan
    check_nik = cursor.execute(f"SELECT nik FROM karyawan WHERE nik = {nik_lama}")
    row_nik = check_nik.fetchall()
    if len(row_nik) == 0:
        os.system('cls')
        print("NIK tidak ditemukan !")
        menu_karyawan()
    os.system('cls')
    print(f"{'='*32} UBAH DATA {'='*32} \n{'='*75}")
    nik_baru = int(input("= NIK        : "))
    nama = input(f"= Nama       : ")
    print()
    check = cursor.execute("SELECT * FROM jabatan")
    row = pd.DataFrame(check, columns = ["[ ID ]", "[ NAMA JABATAN ]", "[ GAJI POKOK ]", "[ TUNJANGAN ]"])
    modify = row.to_string(index=False, justify='center')
    print(modify)
    print()
    jabatan = input(("= ID Jabatan : "))
    domisili = input("= Domisili   : ")
    nohp = int(input("= No. HP     : "))
    email = input("= Email      : ")
    cursor.execute("""UPDATE karyawan SET
                    nik = ?,
                    nama_lengkap = ?,
                    id_jabatan = ?,
                    domisili = ?,
                    no_hp = ?,
                    email = ?
                    WHERE nik = ?""",
                    (nik_baru, nama, jabatan, domisili, nohp, email, nik_lama))
    connection.commit()
    os.system('cls')
    print("Data berhasil diubah !")
    menu_karyawan()

#Menghapus data di dalam database
def hapus_karyawan():
    nik = int(input("NIK Karyawan: "))
    #Memastikan NIK ada di dalam daftar NIK Karyawan
    check_nik = cursor.execute(f"SELECT nik FROM karyawan WHERE nik = {nik}")
    row_nik = check_nik.fetchall()
    if len(row_nik) == 0:
        os.system('cls')
        print("NIK tidak ditemukan !")
        menu_karyawan()
    os.system('cls')
    print(f"{'='*31} HAPUS DATA {'='*32} \n{'='*75}\n")
    check = cursor.execute(f"""SELECT 
                    k.nik,
                    k.nama_lengkap,
                    j.nama_jabatan,
                    k.jenis_kelamin,
                    k.domisili,
                    k.no_hp,
                    k.email,
                    k.tanggal_masuk
                    FROM karyawan k INNER JOIN jabatan j ON k.id_jabatan = j.id_jabatan WHERE nik = {nik}
                    """)
    row = pd.DataFrame(check, columns = ["[ NIK ]", "[ NAMA ]", "[ JABATAN ]", "[ JENIS KELAMIN ]", "[ DOMISILI ]", "[ NO.HP ]", "[ EMAIL ]", "  [ TGL BERGABUNG ]"])
    modify = row.to_string(index=False, justify='center')
    print(modify)
    choice = int(input("\nKonfirmasi (1.YA/2.TIDAK): "))
    if choice == 1:
        cursor.execute(f"DELETE FROM karyawan WHERE nik = {nik}")
        connection.commit()
        os.system('cls')
        print("Data berhasil dihapus !")
        menu_karyawan()
    elif choice == 2:
        os.system('cls')
        print("Berhasil dibatalkan !")
        menu_karyawan()
    else:
        os.system('cls')
        print("Tidak ada didaftar pilihan !")
        menu_karyawan()