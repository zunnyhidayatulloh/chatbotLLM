! pip install streamlit
# -*- coding: utf-8 -*-
# program Python untuk chatbot Sistem Informasi Sarana dan Prasarana Sekolah
# Dibuat menggunakan Google Gemini API.

import requests
import json
import os
import google.generativeai as genai

# Atur API Key Anda. Anda harus mengganti 'YOUR_API_KEY' dengan kunci API yang Anda miliki.
# Anda dapat memperolehnya dari Google AI Studio atau Google Cloud.
# API key harus disimpan dengan aman dan tidak dibagikan.
API_KEY = "AIzaSyB4ke1RpO1JycuPwssPxpC1-1338zvbgf0"
MODEL_NAME = "gemini-2.5-flash-preview-05-20"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=AIzaSyB4ke1RpO1JycuPwssPxpC1-1338zvbgf0"


# --- Data Sistem Informasi ---
# Ini adalah informasi dasar tentang sarana dan prasarana sekolah.
# Anda bisa menambahkan lebih banyak data di sini untuk membuat chatbot lebih informatif.
SYSTEM_DATA = """
Anda adalah chatbot Sistem Informasi Sarana dan Prasarana Sekolah. Tugas Anda adalah memberikan informasi akurat tentang fasilitas sekolah.
Informasi yang Anda ketahui:
Kategori: Bangunan dan Ruang Belajar

1. Ruang Kelas (Klasifikasi: Bangunan)
Definisi: Ruangan utama tempat proses belajar-mengajar berlangsung.
Spesifikasi:
Ukuran standar: Minimal 7m x 8m (untuk 32 siswa).
Ventilasi: Alami (jendela) atau buatan (AC).
Pencahayaan: Memadai (minimal 300 lux).
Furniture: Meja dan kursi siswa (berjumlah sesuai kapasitas), meja dan kursi guru, papan tulis (whiteboard atau blackboard), lemari penyimpanan.
Fungsi: Tempat utama interaksi antara guru dan siswa, penyampaian materi, dan evaluasi.
Contoh: Ruang Kelas X-IPA 1, Ruang Kelas XI-IPS 2.

2. Laboratorium (Klasifikasi: Bangunan)
Definisi: Ruangan khusus yang dilengkapi dengan peralatan untuk kegiatan praktikum dan eksperimen.
Jenis:
Lab IPA (Fisika, Kimia, Biologi): Meja kerja tahan bahan kimia, wastafel, lemari asam, alat-alat praktikum (mikroskop, tabung reaksi, alat ukur listrik).
Lab Komputer: Komputer (PC atau laptop) dengan spesifikasi memadai, jaringan internet, proyektor.
Lab Bahasa: Komputer dengan headset, software pembelajaran bahasa, meja sekat.
Spesifikasi: Sistem keamanan (alat pemadam kebakaran, P3K), ventilasi khusus, instalasi listrik dan air yang aman.
Fungsi: Mengembangkan keterampilan praktis siswa, menguji teori, dan melakukan penelitian sederhana.

3. Perpustakaan (Klasifikasi: Bangunan)
Definisi: Pusat sumber belajar yang menyediakan koleksi buku, majalah, jurnal, dan media informasi lainnya.
Spesifikasi:
Rak buku yang terklasifikasi (berdasarkan sistem Dewey Decimal Classification - DDC).
Area baca dengan meja dan kursi yang nyaman.
Area multimedia (komputer dengan akses internet, proyektor).
Sistem sirkulasi buku (kartu anggota, barcode scanner).
Fungsi: Mendukung literasi siswa dan guru, menyediakan referensi, dan menjadi tempat belajar mandiri.

Kategori: Fasilitas Penunjang Pembelajaran
4. Proyektor LCD (Klasifikasi: Peralatan Elektronik)
Definisi: Perangkat optik yang memproyeksikan gambar atau video dari komputer ke layar besar.
Spesifikasi: Resolusi (misal: XGA, Full HD), lumens (kecerahan), konektivitas (HDMI, VGA).
Fungsi: Memvisualisasikan materi pembelajaran, presentasi, dan media interaktif.

5. Papan Tulis Interaktif (Interactive Whiteboard) (Klasifikasi: Peralatan Elektronik)
Definisi: Layar sentuh yang berfungsi sebagai papan tulis digital dan dapat terhubung ke komputer.
Spesifikasi: Ukuran layar, teknologi sentuh (infrared, kapasitif), kompatibilitas software.
Fungsi: Memungkinkan interaksi langsung dengan materi digital, anotasi, dan menyimpan catatan pelajaran.

6. Jaringan Internet dan Wi-Fi (Klasifikasi: Infrastruktur IT)
Definisi: Infrastruktur yang menyediakan konektivitas internet di seluruh area sekolah.
Spesifikasi:
Jenis koneksi: Fiber optik, ADSL.
Kapasitas bandwidth: Disesuaikan dengan jumlah pengguna.
Akses poin: Penempatan Wi-Fi router di lokasi strategis.
Fungsi: Mendukung kegiatan pembelajaran berbasis digital, riset, dan komunikasi.

Kategori: Fasilitas Olahraga dan Seni
7. Lapangan Olahraga (Klasifikasi: Bangunan Luar Ruangan)
Definisi: Area terbuka yang dirancang untuk kegiatan olahraga.
Jenis:
Lapangan Basket: Ukuran standar (28m x 15m), ring, garis batas.
Lapangan Futsal/Sepak Bola: Gawang, garis batas.
Lapangan Voli: Net, garis batas.
Spesifikasi: Permukaan (beton, rumput sintetis, karet), drainase yang baik.
Fungsi: Mengadakan kegiatan ekstrakurikuler, PJJ Penjaskes, dan kompetisi antar kelas.

8. Ruang Seni (Klasifikasi: Bangunan)
Definisi: Ruangan khusus untuk kegiatan seni dan budaya.
Jenis:
Ruang Musik: Alat musik (keyboard, gitar, drum), sound system, peredam suara.
Ruang Seni Rupa: Meja gambar, kanvas, cat, alat pahat, lemari penyimpanan.
Fungsi: Mengembangkan bakat dan minat siswa di bidang seni, tempat latihan dan pameran.

Kategori: Fasilitas Administrasi dan Layanan Umum
9. Ruang Kepala Sekolah (Klasifikasi: Bangunan)
Definisi: Ruangan untuk kepala sekolah dalam melaksanakan tugas manajerial dan kepemimpinan.
Sarana: Meja kerja, kursi, lemari arsip, komputer, telepon, printer.
Fungsi: Pengambilan keputusan, koordinasi, dan pertemuan dengan tamu.

10. Kantin Sekolah (Klasifikasi: Bangunan)
Definisi: Area yang menyediakan makanan dan minuman untuk siswa dan staf.
Spesifikasi: Area bersih, meja dan kursi makan, wastafel, sanitasi yang baik.
Fungsi: Menyediakan kebutuhan nutrisi, tempat istirahat saat jam istirahat.

Kategori: Sarana Keamanan dan Kebersihan
11. CCTV (Closed-Circuit Television) (Klasifikasi: Peralatan Keamanan)
Definisi: Sistem kamera pengawas untuk memonitor area sekolah.
Spesifikasi: Resolusi kamera, kapasitas penyimpanan data (DVR/NVR), penempatan di area strategis (gerbang, koridor, parkiran).
Fungsi: Meningkatkan keamanan, mencegah tindak kejahatan atau perundungan, dan memantau kedisiplinan.

12. Alat Pemadam Api Ringan (APAR) (Klasifikasi: Peralatan Darurat)
Definisi: Perangkat portabel untuk memadamkan api pada tahap awal.
Jenis: APAR jenis CO2, powder, atau foam.
Spesifikasi: Berat (3 kg, 6 kg), jadwal inspeksi dan pengisian ulang.
Fungsi: Sarana keselamatan untuk menanggulangi kebakaran kecil
"""

# --- Fungsi untuk Memanggil Gemini API ---
def generate_content(prompt, system_instruction):
    """
    Mengirimkan prompt ke Google Gemini API dan mengembalikan respons teks.

    Args:
        prompt (str): Pertanyaan atau pesan dari pengguna.
        system_instruction (str): Instruksi yang mendefinisikan peran chatbot.

    Returns:
        str: Respons teks dari model, atau pesan error jika terjadi kegagalan.
    """
    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Angkat HTTPError untuk respons status kode buruk (4xx atau 5xx)

        # Ekstrak konten dari respons JSON
        result = response.json()
        candidate = result.get('candidates', [{}])[0]
        text_response = candidate.get('content', {}).get('parts', [{}])[0].get('text', 'Maaf, saya tidak dapat memproses permintaan ini saat ini.')

        return text_response

    except requests.exceptions.RequestException as e:
        return f"Terjadi kesalahan saat menghubungi API: {e}"
    except (json.JSONDecodeError, IndexError) as e:
        return f"Terjadi kesalahan saat memproses respons API: {e}. Respons mentah: {response.text}"

# --- Program Utama Chatbot ---
def main_chatbot():
    """
    Menjalankan loop interaksi chatbot.
    """
    print("Selamat datang di Chatbot SiSaras (Sistem Informasi Sarana dan Prasarana Sekolah)")
    print("Silakan tanyakan tentang fasilitas sekolah. Ketik 'keluar' untuk mengakhiri.")
    print("---------------------------------------------------------------------------")

    while True:
        user_input = input("Anda: ")

        if user_input.lower() in ['keluar', 'exit', 'quit']:
            print("Chatbot: Terima kasih telah menggunakan layanan ini. Sampai jumpa!")
            break

        if not user_input.strip():
            print("Chatbot: Silakan masukkan pertanyaan.")
            continue

        print("Chatbot: Sedang memproses...")

        # Panggil fungsi generate_content dengan input pengguna dan instruksi sistem
        response = generate_content(user_input, SYSTEM_DATA)
        print("Chatbot:", response)

if __name__ == "__main__":
    main_chatbot()

