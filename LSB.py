from PIL import Image
import numpy as np
import math

# Function untuk menyisipkan pesan pada citra
def Encode(src, message, dest):

    # Mengambil citra
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    # Mengecek format citra
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size//n
    
    # Menyisipkan penanda pada citra
    message += "$t3g0"
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)
    
    # Cek apakah panjang pesan cukup untuk ukuran citra
    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")
    else:
        index=0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    # Menyisipkan pesan pada bit tertentu pada citra
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1
    
    # Membangun ulang citra yang telah dimodifikasi
    array=array.reshape(height, width, n)
    enc_img = Image.fromarray(array.astype('uint8'), img.mode)
    enc_img.save(dest)
    print("Citra telah dimodifikasi")
    
# Function untuk mengekstraksi pesan rahasia dari citra
def Decode(src):

    # Membuka citra
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    # Cek format citra
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size//n

    # Mulai ekstraksi citra
    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    
    # Cek apakah terdapat penanda rahasia pada citra
    for i in range(len(hidden_bits)):
        if message[-5:] == "$t3g0":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
            
    # Menampilkan pesan rahasia pada citra
    if "$t3g0" in message:
        print("Pesan Rahasia :", message[:-5])
    else:
        print("Tidak ada pesan ditemukan")
        
# Menghitung PSNR
def psnr(original_image, encoded_image):
    # Membuka citra asli dan citra stego 
    img_original = Image.open(original_image, 'r')
    img_encoded = Image.open(encoded_image, 'r')

    # Konversi ke grayscale
    img_original = img_original.convert("L")
    img_encoded = img_encoded.convert("L")

    # Kalkulasi Mean Squared Error (MSE)
    mse = np.mean((np.array(img_original) - np.array(img_encoded)) ** 2)

    # Mencari maksimal ukuran pixel
    max_pixel_value = np.max(np.array(img_original))

    # Menghitung PSNR
    psnr = 20 * math.log10(max_pixel_value / math.sqrt(mse))
    return psnr
        
# Program utama
def Stego():
    print("LSB")
    print("1: Encode")
    print("2: Decode")

    func = input()

    if func == '1':
        print("Masukkan path citra yang ingin disisipkan pesan : ")
        src = input()
        print("Masukkan pesan yang ingin disisipkan : ")
        message = input()
        print("Masukkan nama output : ")
        dest = input()
        Encode(src, message, dest)
        psnrResult = psnr(src, dest)
        print("PSNR :", psnrResult)

    elif func == '2':
        print("Masukkan path citra yang ingin diekstraksi : ")
        src = input()
        Decode(src)
    else:
        print("ERROR: Invalid option chosen")
        
Stego()