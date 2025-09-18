#!pip install google-generativeai
#LIBRARY IMPORT
import google.generativeai as genai

# Masukkan API key
genai.configure(api_key="AIzaSyANXe6nANE7WwOYZ2oR3L_-p4sGwAkIbI0")

# Buat model LLM
model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

# Fungsi chatbot
def chatbot(prompt):
    response = model.generate_content(prompt)
    return response.text

# Uji chatbot

# --- CONTOH : CHATBOT AHLI SEJARAH  ---

INITIAL_CHATBOT_CONTEXT = [
    {
        "role": "user",
        "parts": ["Kamu adalah Petugas Sarana Prasarana Sekolah. Jawaban detail dan faktual. Tolak pertanyaan non-sejarah."]
    },
    {
        "role": "model",
        "parts": ["Baik! Berikan Pertanyaan Anda tentang Sarpras."]
    }
]

#print(chatbot("Apa itu chatbot?"))
#print(chatbot("Ceritakan tentang SMAN 1 Kedungwuni"))


# ==============================================================================
# FUNGSI UTAMA CHATBOT (HINDARI MENGUBAH BAGIAN INI JIKA TIDAK YAKIN)
# ==============================================================================

# Cek apakah API Key sudah diganti
if API_KEY == f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=AIzaSyB4ke1RpO1JycuPwssPxpC1-1338zvbgf0" or not API_KEY:
    print("Peringatan: API Key belum diatur. Harap ganti 'YOUR_GEMINI_API_KEY_HERE' dengan API Key Anda.")
    print("Chatbot tidak akan berfungsi tanpa API Key yang valid.")
    exit()

try:
    genai.configure(api_key=API_KEY)
    print("Gemini API Key berhasil dikonfigurasi.")
except Exception as e:
    print(f"Kesalahan saat mengkonfigurasi API Key: {e}")
    print("Pastikan API Key Anda benar dan koneksi internet stabil.")
    exit()

# Inisialisasi model
try:
    model = genai.GenerativeModel(
        MODEL_NAME,
        generation_config=genai.types.GenerationConfig(
            temperature=0.4, # Kontrol kreativitas (0.0=faktual, 1.0=kreatif)
            max_output_tokens=500 # Batas maksimal panjang jawaban dalam token
        )
    )
    print(f"Model '{MODEL_NAME}' berhasil diinisialisasi.")
except Exception as e:
    print(f"Kesalahan saat inisialisasi model '{MODEL_NAME}': {e}")
    print("Pastikan nama model benar dan tersedia untuk API Key Anda.")
    exit()

# --- Memulai Chat ---
print("\n--- Chatbot Dimulai ---")
# Pesan pembuka umum, model akan membalas sesuai konteks awal
print(INITIAL_CHATBOT_CONTEXT[1]["parts"][0])
print("Ketik 'exit' untuk keluar.")
print("---")

# Inisialisasi sesi chat dengan riwayat awal (konteks)
chat = model.start_chat(history=INITIAL_CHATBOT_CONTEXT)

while True:
    user_input = input("Anda: ")
    user_input_lower = user_input.lower() # Optimasi: Konversi ke huruf kecil

    if user_input_lower == 'exit':
        print("Chatbot: Sampai jumpa!")
        break

    print("Chatbot: (Sedang membalas...)")

    try:
        # Kirim input pengguna langsung ke model.
        # Model akan memprosesnya berdasarkan INITIAL_CHATBOT_CONTEXT yang telah disetel.
        response = chat.send_message(user_input_lower, request_options={"timeout": 60})

        if response and response.text:
            print(f"Chatbot: {response.text}")
        else:
            print("Chatbot: Maaf, saya tidak bisa memberikan balasan.")
            print("Penyebab: Respons API kosong atau tidak valid.")

    except Exception as e:
        print(f"Chatbot: Maaf, terjadi kesalahan saat berkomunikasi dengan Gemini:")
        print(f"Error Detail: {e}")
        print("Kemungkinan penyebab:")
        print("  - Masalah koneksi internet atau timeout.")
        print("  - API Key mungkin dibatasi, tidak valid, atau melebihi kuota.")
        print("  - Masalah internal di server Gemini.")
