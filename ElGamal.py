import random

# Function untuk membuat kunci
def generate_keys(p, g):
    # Mencari secara acak nilai x
    x = random.randint(1, p - 2)
    
    # Mencari kunci y
    y = pow(g, x, p)
    
    return x, y

# Function untuk Proses Enkripsi
def encrypt(p, g, y, plaintext):
    # Memilih nilai k secara random
    k = random.randint(1, p - 2)
    
    # Ubah pesan ke ASCII
    plaintext_nums = [ord(char) for char in plaintext]
    
    # Mencari ciphertext dari setiap karakter
    ciphertext = []
    kList = []
    
    for num in plaintext_nums:
        c1 = pow(g, k, p)
        c2 = (num * pow(y, k, p)) % p
        ciphertext.append((c1, c2))
        kList.append(k)
    
    return ciphertext, kList

def decrypt(p, a, ciphertext):
    
    shared_secrets = [pow(c1, a, p) for c1, _ in ciphertext]
    
    # Mengambil invers modulus setiap karakter
    inv_shared_secrets = [pow(secret, p - 2, p) for secret in shared_secrets]
    
    # Mengambil hasil dekripsi
    plaintext_nums = [(c2 * inv_secret) % p for (_, c2), inv_secret in zip(ciphertext, inv_shared_secrets)]
    
    # Ubah hasil dekripsi ke Huruf plaintext
    plaintext = "".join(chr(num) for num in plaintext_nums)
    
    return plaintext

# Function untuk cek bilangan prima
def cekPrima(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

# Function untuk cek apakah g adalah generator modulo dari p
def cekGeneratorModulo(x, y):
    if x < 1 or y < 2:
        return False

    visited = set()
    result = 1
    for _ in range(y - 1):
        result = (result * x) % y
        if result in visited:
            return False
        visited.add(result)

    return len(visited) == y - 1

def signAndVerify (kList, pt, g, p, x, y):
    #Proses Signing
    k = kList[0]
    m = ord(pt[0])
    a = pow(g, k, p)
    inverse_k = pow(k, -1, p-1)
    b = (m - x * a) * inverse_k % (p-1)
    eea = mod_inverse(k, p)
    print("Sign : ", eea)
    
    # Proses Verifikasi
    v1 = (y**a * a**b) % p
    v2 = pow(g, m, p)
    
    if (v1 == v2): 
        print("VALID")
    else: 
        print("TIDAK VALID")

def mod_inverse(a, b):
    if b == 0:
        raise ValueError("Modulus b cannot be zero.")
    
    # Menggunakan Algoritma Euclidean Diperpanjang untuk menghitung invers modulo
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    
    if old_r > 1:
        raise ValueError("The given values a and b are not relatively prime.")
    
    # Jika old_s negatif, ubah menjadi positif dengan menambahkan b
    inverse = old_s % b
    if inverse < 0:
        inverse += b
    
    return inverse    

# Proses Verifikasi
def verify (y, b, p, g, m, k):
    a = pow(g, k, p)
    v1 = (y**a * a**b) % p
    v2 = pow(g, m, p)

# Awal program
try:
    p = int(input("Masukkan nilai p : "))
    if not cekPrima(p):
        raise ValueError('p harus bilangan prima!')
    g = int(input("Masukkan nilai g : "))
    if not cekGeneratorModulo(g, p):
        raise ValueError('g bukan generator modulo dari p!')
    
    # Generate keys
    private_key, public_key = generate_keys(p, g)
    print("Private Key")
    print("x : ", private_key)
    print()
    print("Public Key")
    print("y :", public_key)
    print("p :", p)
    print("g :", g)
    print()

    # Encryption
    plaintext = input("Masukkan pesan : ")
    print()

    # Proses Enkripsi
    ciphertext, kList = encrypt(p, g, public_key, plaintext)
    print("Hasil Enkripsi :")
    for c1, c2 in ciphertext:
        print(f"({c1}, {c2})")

    print()
    # Proses Dekripsi
    decrypted_text = decrypt(p, private_key, ciphertext)
    print("Hasil Dekripsi :", decrypted_text)
    print()
    
    signAndVerify(kList, plaintext, g, p, private_key, public_key)
    print()
except ValueError as e:
    print(str(e))