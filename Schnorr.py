import hashlib
import random

# Function untuk membuat kunci
def generateKey(p):
    # Pilih bilangan prima dengan panjang bit yang cukup besar
    q = (p - 1) // 2

    # Pilih bilangan acak untuk kunci privat
    x = random.randint(1, q)

    # Hitung kunci publik
    y = pow(2, x, p)

    return x, y, p

# Function untuk membuat signature
def signing(message, private_key):
    x, _, p = private_key

    # Hasilkan nilai acak k
    k = random.randint(1, p - 1)

    # Hitung nilai r = (g^k mod p)
    r = pow(2, k, p)

    # Hitung nilai e = H(m || r)
    e = int(hashlib.sha256((str(message) + str(r)).encode()).hexdigest(), 16)

    # Hitung nilai s = (k - x * e) mod q
    s = (k - x * e) % (p - 1)

    return r, s

# Function untuk memverifikasi tanda tangan
def verify(message, signature, public_key):
    y, p = public_key
    r, s = signature

    # Hitung nilai e = H(m || r)
    e = int(hashlib.sha256((str(message) + str(r)).encode()).hexdigest(), 16)

    # Hitung nilai v = (g^s * y^e mod p) mod q
    v = (pow(2, s, p) * pow(y, e, p)) % p

    # Verifikasi tanda tangan: Jika v = r, tanda tangan valid
    if v == r:
        print("VALID")
    else:
        print("TIDAK VALID")

p = int(input("Masukkan bilangan prima : "))
message = input("Masukkan pesan : ")

private_key = generateKey(p)
public_key = (private_key[1], private_key[2])

signature = signing(message, private_key)
print()
print("Sign :", signature)

print()
verify(message, signature, public_key)