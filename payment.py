import sqlite3
import os
import pandas as pd

#Koneksi ke database & membuat cursor
connection = sqlite3.connect('db_perusahaan.db')
cursor = connection.cursor()

#Menu Payment
def menu_payment():
    print(f"{'='*33} PAYMENT {'='*33}\n{'='*75}")
    check = cursor.execute("""SELECT 
                    k.nik,
                    k.nama_lengkap,
                    j.nama_jabatan,
                    j.gaji_pokok,
                    j.tunjangan
                    FROM karyawan k INNER JOIN jabatan j ON k.id_jabatan = j.id_jabatan
                    """)
    row = pd.DataFrame(check, columns = ["[ NIK ]", "[ NAMA ]", "[ JABATAN ]", "[ GAJI POKOK ]", "[ TUNJANGAN ]"])
    modify = row.to_string(index=False, justify='center')
    print(modify)
    choice = int(input(f"{'='*75}\n= 1. Pembayaran Gaji\n= 2. Kembali\n{'='*75}\nPilih Menu: "))
    if choice == 1:
        pay()
    elif choice == 2:
        os.system('cls')
        from index import dashboard
        dashboard()
    else:
        os.system('cls')
        print("Tidak ada didaftar pilihan !")
        menu_payment()

#Menu Pembayaran Gaji
def pay():
    id = int(input("NIK Karyawan: "))
    check_id = cursor.execute(f"SELECT nik from karyawan WHERE nik = {id}")
    row_id = check_id.fetchall()
    if len(row_id) == 0:
        os.system('cls')
        print("NIK tidak ditemukan !")
        menu_payment()
        
    os.system('cls')
    print(f"{'='*33} PAYMENT {'='*33}\n{'='*75}")
    check = cursor.execute(f"""SELECT 
                    k.nik,
                    k.nama_lengkap,
                    j.nama_jabatan,
                    j.gaji_pokok,
                    j.tunjangan
                    FROM karyawan k INNER JOIN jabatan j ON k.id_jabatan = j.id_jabatan WHERE nik = {id}
                    """)
    row = pd.DataFrame(check, columns = ["[ NIK ]", "[ NAMA ]", "[ JABATAN ]", "[ GAJI POKOK ]", "[ TUNJANGAN ]"])
    modify = row.to_string(index=False, justify='center')
    print(modify)
    periode = input("\nPeriode (Bulan & Tahun) : ")
    absensi = int(input("Jumlah Ketidakhadiran   : "))
    lembur = int(input("Jumlah Jam Lembur       : "))
    confirmation = int(input("Konfirmasi Pembayaran (1.YA/2.TIDAK): "))
    if confirmation == 1:
        pass
    elif confirmation == 2:
        os.system('cls')
        print("Berhasil dibatalkan !")
        menu_payment()
    else:
        os.system('cls')
        print("Tidak ada didaftar pilihan !")
        menu_payment()
    os.system('cls')

    #Mengambil data gaji pokok dari database
    ambil_gapok = cursor.execute(f"SELECT j.gaji_pokok FROM karyawan k INNER JOIN jabatan j ON k.id_jabatan = j.id_jabatan WHERE nik = {id}")
    deklarasi_gapok = ambil_gapok.fetchall()
    for gapok in deklarasi_gapok:
        gapok = gapok[0]

    #Mengambil data tunjangan dari database
    ambil_tunjangan = cursor.execute(f"SELECT j.tunjangan FROM karyawan k INNER JOIN jabatan j ON k.id_jabatan = j.id_jabatan WHERE nik = {id}")
    deklarasi_tunjangan = ambil_tunjangan.fetchall()
    for tunjangan in deklarasi_tunjangan:
        tunjangan = tunjangan[0]

    #Menghitung lemburan
    upah_per_jam = gapok / 173
    for jam in range(0, lembur + 1):
        if jam == 0:
            lembur += 0 * upah_per_jam
        elif jam == 1:
            lembur += 1.5 * upah_per_jam
        else:
            lembur += 2 * upah_per_jam

    #Menghitung potongan berdasarkan ketidakhadiran
    potongan_absensi = (gapok / 24) * absensi

    #Menghitung potongan pajak
    gapok_pertahun = gapok * 12
    if gapok_pertahun <= 60000000:
        pajak = 5
    elif gapok_pertahun > 60000000 and gapok_pertahun <= 250000000:
        pajak = 15
    elif gapok_pertahun > 250000000 and gapok_pertahun <= 500000000:
        pajak = 25
    elif gapok_pertahun > 500000000 and gapok_pertahun <= 5000000000:
        pajak = 30
    else:
        pajak = 35
    pajak = gapok * pajak / 100
    potongan_pajak = pajak / 12

    #Menghitung potongan bpjs JHT
    potongan_jht = gapok * 5.7 / 100

    #Menghitung potongan bpjs kesehatan
    potongan_kesehatan = gapok * 5 / 100

    #Menghitung gaji bersih
    gaji_bersih = gapok + tunjangan + lembur - potongan_absensi - potongan_pajak - potongan_jht - potongan_kesehatan

    #Memasukan data kedalam table slip gaji
    cursor.execute("""INSERT INTO slip_gaji
                   (nik,
                   gaji_pokok,
                   tunjangan,
                   lembur,
                   potongan_absensi,
                   potongan_pajak,
                   potongan_jht,
                   potongan_kesehatan,
                   gaji_bersih,
                   periode)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   (id, gapok, tunjangan, lembur, potongan_absensi, potongan_pajak, potongan_jht, potongan_kesehatan, gaji_bersih, periode))
    connection.commit()
    os.system('cls')
    print("Pembayaran berhasil !")
    menu_payment()