import random

# Function untuk melakukan kalkulasi invers modulus
def modInverse(a, b):
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

# Function untuk cek bilangan prima
def cekPrima(number):
	for i in range(2, number):
		if number % i == 0:
			return False
			break
	return True

# Untuk generate private key
def generate_private_key(p):
    return random.randint(1, p-1)

base = 32
p = int(input("Masukkan bilangan prima 32-bit : "))

# Memastikan p adalah bilangan prima
for i in range(10, p):
	if (p-1) % i == 0 and cekPrima(i):
		q = i
		break

a = int((p-1)/q)
g = pow(base, a, p)

# Membentuk kunci
x = generate_private_key(p)
y = pow(g, x, p)

# Menampilkan kunci
print("Private Key :", x)
print("Public Key :", y)
print("p :", p)
print("q :", q)
print("g :", g)
print()

# Untuk dapatkan nilai random ke k
k = random.randint(1, p-1)

h = 123

# Pembentukan Signature
r = pow(g, k, p) % q
s = modInverse(k, q) * (h + x*r) % q

print("Signature: (r =",r,", s =",s,")")
print()

# Proses Verifikasi
w = modInverse(s, q)
u1 = h * w % q
u2 = r * w % q
v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q

if v == r:
	print("VALID")
else:
	print("TIDAK VALID")