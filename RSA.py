import random

# Function untuk mencari greatest common denominator
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Proses mencari nilai e dengan algoritma EEA
def multiplicativeInverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    tempPhi = phi

    while e > 0:
        temp1 = tempPhi//e
        temp2 = tempPhi - temp1 * e
        tempPhi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if tempPhi == 1:
        return d + phi

# Function untuk mengecek apakah input merupakan bilangan prima atau bukan
def cekPrima(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

# Function untuk membuat key
def generateKey(p, q):
    
    # Cek apakah input adalah bilangan prima
    if not (cekPrima(p) and cekPrima(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    
    # Hitung nilai n
    n = p * q

    # Hitung Ø(n)
    phi = (p-1) * (q-1)

    # Cari bilangan random range[max(p,q)+1, Ø(n) – 1]
    # Agar bilangan tersebut relatif prima terhadap Ø(n) 
    e = random.randrange(1, phi)

    # membuktikan e dan Ø(n) relatif prima
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Generate nilai d untuk mendapatkan private key
    d = multiplicativeInverse(e, phi)

    # Return hasil public key dan private key
    # Public key = e dan n
    # Private key = d
    return ((e, n), (d, n))

# Function untuk melakukan enkripsi menggunakan a^b mod m
def encrypt(pk, plaintext):
    key, n = pk
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher

# Function untuk melakukan dekripsi menggunakan a^b mod m
def decrypt(pk, ciphertext):
    key, n = pk
    aux = [str(pow(char, key, n)) for char in ciphertext]
    plain = [chr(int(char2)) for char2 in aux]
    return ''.join(plain)

# Function untuk melakukan Signing
def signAndVerify(encMsg, d, n, e):
    # Proses Signing
    # Ambil 16 bit dari hasil enkripsi dan ubah ke desimal
    y = encMsg[:4]
    x = int(y, 16)
    
    # Lakukan x ^ d mod n
    s = pow(x, d, n)
    print("Sign : ", s)
    print()
    
    # Proses Verify
    # s ^ e mod n
    md1 = pow(s, e, n)
    md1 = hex(md1)
    md2 = hex(x)
    
    # Bandingkan dalam bentuk hexadecimal
    if (md1 == md2): 
        print (md1, "=", md2)
        print("VALID")
    else:
        print (md1, "!=", md2)
        print("TIDAK VALID")

# Program Utama
if __name__ == '__main__':
    print("RSA")
    print()

    p = int(input("p : "))
    q = int(input("q : "))

    #Memanggil Function untuk mencari kunci
    public, private = generateKey(p, q)

    # Menampilkan Kunci
    print()
    print("Public Key")
    print("e = ", public[0])
    print("n = ", public[1])
    print()
    print("Private Key")
    print("d = ", private[0])
    print("p = ", p)
    print("q = ", q)
    print()

    # Proses Enkripsi dan Dekripsi
    message = input("Pesan yang ingin dienkripsi : ")
    print()
    encryptedMsg = encrypt(public, message)

    print("Hasil enkripsi : ", ''.join(map(lambda x: str(x), encryptedMsg)))
    print()
    print("Pesan berhasil terdekripsi : ", decrypt(private, encryptedMsg))
    
    print()
    # Proses Signing dan Verifikasi
    signAndVerify(''.join(map(lambda x: str(x), encryptedMsg)), private[0], public[1], public[0])
    
    