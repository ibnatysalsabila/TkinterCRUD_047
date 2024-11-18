import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi untuk membuat database dan tabel
def create_database():
    # Membuat koneksi ke database (akan membuat file 'buku.db' jika belum ada)
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    """)
    conn.commit()
    conn.close()

# Fungsi untuk mengambil semua data dari database
def fetch_data():
    # Membuka koneksi ke database SQLite
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    # Menjalankan query untuk mengambil semua data dari tabel 'nilai_siswa'
    cursor.execute("SELECT * FROM nilai_siswa")
    # Mengambil seluruh hasil query dan menyimpannya dalam variable 'rows'
    rows = cursor.fetchall()
    conn.close()
    return rows

# Fungsi untuk menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    # Perintah SQL untuk menambahkan data ke tabel
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()
    conn.close()

# Fungsi untuk memperbarui data di database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    # Menjalankan query UPDATE untuk memperbarui data
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()
    conn.close()

# Fungsi untuk menghapus data dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai tertinggi
def calculate_prediction(biologi, fisika, inggris):
    # Jika nilai Biologi paling tinggi, maka hasil prediksi = Kedokteran
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    # Jika nilai Fisika paling tinggi, maka hasil prediksi = Teknik
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    #Jika nilai Inggris paling tinggi, maka hasil prediksi = Bahasa
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Diketahui"

# Fungsi untuk menangani tombol submit
def submit():
    try:
        # Membaca input dari user
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())
        
         # Validasi input nama agar tidak kosong
        if not nama:
            raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        save_to_database(nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menangani tombol update
def update():
    try:
        # Validasi: Pastikan ada data yang dipilih
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk di-update!")
        
        # Mengambil input dari form
        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)
        
        # Mengosongkan input dan memperbarui tabel di GUI
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")


# Fungsi untuk menangani tombol delete
def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())
        delete_database(record_id)
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        
        # Mengosongkan input form dan memperbarui tabel
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk mengosongkan input
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_data():    #fetch_data()adalah fungsi yang mengambil data dari database
        tree.insert("", "end", values=row)

# Fungsi untuk mengisi input dengan data dari tabel
def fill_inputs_from_table(event):
    try:
        # Mengambil item yang dipilih dari tabel
        selected_item = tree.selection()[0]
        # Mengambil data dari baris yang dipilih
        selected_row = tree.item(selected_item)['values']
        
        # Mengisi input form dengan data yang dipilih
        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")
