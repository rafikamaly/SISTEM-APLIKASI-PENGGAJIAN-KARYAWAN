import sqlite3
import os
import pandas as pd

#Koneksi ke database & membuat cursor
connection = sqlite3.connect('db_perusahaan.db')
cursor = connection.cursor()

#Menu Payroll
def menu_payroll():
    print(f"{'='*33} PAYROLL {'='*33}\n{'='*75}")
    check = cursor.execute("SELECT k.nik, k.nama_lengkap, j.nama_jabatan FROM karyawan k INNER JOIN jabatan j ON k.id_jabatan = j.id_jabatan")
    row = pd.DataFrame(check,columns=["[ NIK ]","[ Nama ]","[ Jabatan ]"])
    modify = row.to_string(index=False, justify='center')
    print(modify)
    print(f"{'='*75}\n= 1. Slip Gaji \t\t\t\t\t\t\t\t  =\n= 2. Kembali \t\t\t\t\t\t\t\t  =\n{'='*75}")
    choice = int(input("Pilih Menu: "))
    if choice == 1:
        slip_gaji()
    elif choice == 2:
        os.system('cls')
        from index import dashboard
        dashboard()
    else:
        os.system('cls')
        print("Tidak ada didalam daftar pilihan !")
        menu_payroll()

#Menampilkan riwayat gaji karyawan
def slip_gaji():
    id = int(input("NIK Karyawan: "))
    check_id = cursor.execute(f"SELECT nik FROM karyawan WHERE nik = {id}")
    row_id = check_id.fetchall()
    if not row_id:
        os.system('cls')
        print("NIK tidak ditemukan !")
        menu_payroll()
    os.system('cls')
    print(f"{'='*33} PAYROLL {'='*33}\n{'='*75}")
    check = cursor.execute(f"""SELECT
                            s.id_slipgaji,
                            k.nama_lengkap,
                            j.nama_jabatan,
                            s.periode
                            FROM slip_gaji s INNER JOIN karyawan k, jabatan j ON s.nik = k.nik and k.id_jabatan = j.id_jabatan WHERE s.nik = {id}""")
    row = pd.DataFrame(check, columns=["[ ID ]","[ Nama ]","[ Jabatan ]","[ Periode ]"])
    modify = row.to_string(index=False, justify='center')
    print(modify)
    print(f"{'='*75}\n= 1. Cetak Slip Gaji \t\t\t\t\t\t\t  =\n= 2. Kembali \t\t\t\t\t\t\t\t  =\n{'='*75}")
    choice = int(input("Pilih Menu: "))
    if choice == 1:
        cetak_slipgaji()
    elif choice == 2:
        os.system('cls')
        menu_payroll()
    else:
        os.system('cls')
        menu_payroll()

#Mencetak Slip Gaji Karyawan
def cetak_slipgaji():
    id = int(input("ID Slip Gaji: "))
    os.system('cls')
    print(f"{'='*27} SLIP GAJI KARYAWAN {'='*28}\n{'='*75}")

    #Mengambil data satu persatu dari database

    #Periode
    ambil_periode = cursor.execute(f"SELECT periode FROM slip_gaji WHERE id_slipgaji = {id}")
    deklarasi_periode = ambil_periode.fetchall()
    for periode in deklarasi_periode:
        periode = periode[0]

    #NIK
    ambil_nik = cursor.execute(f"SELECT k.nik FROM slip_gaji s INNER JOIN karyawan k ON s.nik = k.nik WHERE s.id_slipgaji = {id}")
    deklarasi_nik = ambil_nik.fetchall()
    for nik in deklarasi_nik:
        nik = nik[0]
    #Nama
    ambil_nama = cursor.execute(f"SELECT k.nama_lengkap FROM slip_gaji s INNER JOIN karyawan k ON s.nik = k.nik WHERE id_slipgaji = {id}")
    deklarasi_nama = ambil_nama.fetchall()
    for nama in deklarasi_nama:
        nama = nama[0]
    
    #Jabatan
    ambil_jabatan = cursor.execute(f"SELECT j.nama_jabatan FROM karyawan k INNER JOIN jabatan j, slip_gaji s ON k.id_jabatan = j.id_jabatan WHERE s.id_slipgaji = {id}")
    deklarasi_jabatan = ambil_jabatan.fetchall()
    for jabatan in deklarasi_jabatan:
        jabatan = jabatan[0]

    #Gaji Pokok
    ambil_gapok = cursor.execute(f"SELECT gaji_pokok FROM slip_gaji WHERE id_slipgaji = {id}")
    deklarasi_gapok = ambil_gapok.fetchall()
    for gapok in deklarasi_gapok:
        gapok = gapok[0]

    #Tunjangan
    ambil_tunjangan = cursor.execute(f"SELECT tunjangan FROM slip_gaji WHERE id_slipgaji = {id}")
    deklarasi_tunjangan = ambil_tunjangan.fetchall()
    for tunjangan in deklarasi_tunjangan:
        tunjangan = tunjangan[0]

    #Lemburan
    ambil_lemburan = cursor.execute(f"SELECT lembur FROM slip_gaji WHERE id_slipgaji = {id}")
    deklarasi_lemburan = ambil_lemburan.fetchall()
    for lemburan in deklarasi_lemburan:
        lemburan = lemburan[0]

    #Potongan Ketidakhadiran
    ambil_absen = cursor.execute(f"SELECT potongan_absensi FROM slip_gaji WHERE id_slipgaji = {id}")
    deklarasi_absen = ambil_absen.fetchall()
    for potongan_absensi in deklarasi_absen:
        potongan_absensi = potongan_absensi[0]

    #Potongan BPJS Ketenagakerjaan
    ambil_jht = cursor.execute(f"SELECT potongan_jht FROM slip_gaji WHERE id_slipgaji = {id}")
    deklarasi_jht = ambil_jht.fetchall()
    for potongan_jht in deklarasi_jht:
        potongan_jht = potongan_jht[0]

    #Potongan BPJS Kesehatan
    ambil_kes = cursor.execute(f"SELECT potongan_kesehatan FROM slip_gaji WHERE id_slipgaji = {id}")
    deklarasi_kes = ambil_kes.fetchall()
    for potongan_kesehatan in deklarasi_kes:
        potongan_kesehatan = potongan_kesehatan[0]

    #Potongan Pajak
    ambil_pajak = cursor.execute(f"SELECT potongan_pajak FROM slip_gaji WHERE id_slipgaji = {id}")
    deklarasi_pajak = ambil_pajak.fetchall()
    for potongan_pajak in deklarasi_pajak:
        potongan_pajak = potongan_pajak[0]

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

    #Gaji Bersih
    ambil_gaji = cursor.execute(f"SELECT gaji_bersih FROM slip_gaji WHERE id_slipgaji = {id}")
    deklarasi_gaji = ambil_gaji.fetchall()
    for gaji_bersih in deklarasi_gaji:
        gaji_bersih = gaji_bersih[0]

    #Total Penghasilan
    total_gaji = gapok + tunjangan + lemburan
    total_potongan = potongan_absensi + potongan_jht + potongan_kesehatan + potongan_pajak

    print(f"""
    Periode   : {periode}
    Nama      : {nama}
    Jabatan   : {jabatan}
    NIK       : {nik}""")
    print("-"*75)
    print(f"[PENGHASILAN]\nGaji Pokok\t\t: Rp {gapok:,.2f}\nTunjangan\t\t: Rp {tunjangan:,.2f}\nLemburan\t\t: Rp {lemburan:,.2f}\nTotal Penghasilan\t: Rp {total_gaji:,.2f}")
    print(f"\n[POTONGAN]\nKetidakhadiran\t\t: Rp {potongan_absensi:,.2f}\nBPJS Ketenagakerjaan\t: Rp {potongan_jht:,.2f} (5.7%)\nBPJS Kesehatan\t\t: Rp {potongan_kesehatan:,.2f} (5%)\nPajak Penghasilan\t: Rp {potongan_pajak:,.2f} ({pajak}%)\nTotal Potongan\t\t: Rp {total_potongan:,.2f}\n\nGaji Bersih\t\t: Rp {gaji_bersih:,.2f}")
    print("="*75)
    choice = int(input("1.Kembali : "))
    if choice == 1:
        os.system('cls')
        menu_payroll()
    else:
        os.system('cls')
        menu_payroll()