# Function untuk melakukan rotate ke kanan
def rol(angka: int, jlhShift: int, size: int = 32):
    return (angka >> jlhShift) | (angka << size - jlhShift)

# Function utama untuk proses hash 
def encrypt(inputX: bytearray) -> bytearray:
    
    # Memastikan input adalah tipe data bytearray
    if isinstance(inputX, str):
        inputX = bytearray(inputX, 'ascii')
    elif isinstance(inputX, bytes):
        inputX = bytearray(inputX)
    elif not isinstance(inputX, bytearray):
        raise TypeError
    
    # Step 1 - Bit Padding
    # Untuk menambahkan 00 setelah input 
    panjangInput = len(inputX) * 8
    inputX.append(0x80)
    while (len(inputX) * 8 + 64) % 512 != 0:
        inputX.append(0x00)

    # Untuk menambahkan panjang input ke 8 bit terakhir
    inputX += panjangInput.to_bytes(8, 'big')

    blok = []
    for i in range(0, len(inputX), 64):
        blok.append(inputX[i:i+64])
    
    # Step 2 - Initialing Hash Values (h)
    # inisiasi nilai hash (h)
    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h5 = 0x9b05688c
    h4 = 0x510e527f
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19

    # Step 4 - Main Loop
    # Loop utama
    for blokMsg in blok:
        msg = []
        
        # Step 5 - Create A Message Queue (w)
        # Di dalam loop dilakukan rotate ke kanan lalu hasilnya dimasukkan ke array msg
        for t in range(0, 64):
            if t <= 15:
                msg.append(bytes(blokMsg[t*4:(t*4)+4]))
            else:
                t1 = int.from_bytes(msg[t-2], 'big')
                t1 = rol(t1, 17) ^ rol(t1, 19) ^ (t1 >> 10)
                t2 = int.from_bytes(msg[t-7], 'big')
                t3 = int.from_bytes(msg[t-15], 'big')
                t3 = rol(t3, 7) ^ rol(t3, 18) ^ (t3 >> 3)
                t4 = int.from_bytes(msg[t-16], 'big')

                schedule = ((t1 + t2 + t3 + t4) % 2**32).to_bytes(4, 'big')
                msg.append(schedule)

        assert len(msg) == 64

        # Step 6 - Compression Cycle
        # Inisiasi variable a-h dan set nilai a-h menjadi nilai h0-h7
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7

        # Melakukan 64 kali iterasi 
        for t in range(64):
            t1 = ((h + (rol(e, 6) ^ rol(e, 11) ^ rol(e, 25)) 
                    + ((e & f) ^ (~e & g)) + k[t] + int.from_bytes(msg[t], 'big')) % 2**32)

            t2 = ((rol(a, 2) ^ rol(a, 13) ^ rol(a, 22)) 
                    + ((a & b) ^ (a & c) ^ (b & c)) ) % 2**32

            h = g
            g = f
            f = e
            e = (d + t1) % 2**32
            d = c
            c = b
            b = a
            a = (t1 + t2) % 2**32
        
        # Step 7 - Changing The Final Values
        # Memasukkan hasil akhir hash ke h0 - h7 
        h0 = (h0 + a) % 2**32
        h1 = (h1 + b) % 2**32
        h2 = (h2 + c) % 2**32
        h3 = (h3 + d) % 2**32
        h4 = (h4 + e) % 2**32
        h5 = (h5 + f) % 2**32
        h6 = (h6 + g) % 2**32
        h7 = (h7 + h) % 2**32

    # Step 8 - Get The Final Hash
    # Mengembalikan nilai hash akhir dalam bentuk hex
    return ((h0).to_bytes(4, 'big') + (h1).to_bytes(4, 'big') +
            (h2).to_bytes(4, 'big') + (h3).to_bytes(4, 'big') +
            (h4).to_bytes(4, 'big') + (h5).to_bytes(4, 'big') +
            (h6).to_bytes(4, 'big') + (h7).to_bytes(4, 'big'))

# Step 3 - Initialization of Rounded Constants (k)
# Inisiasi nilai k sebanyak 64 konstanta
k = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

# Program dimulai dari sini
print("SHA256")
print()

# Melakukan Input
inputX = input("Input : ")
print()

# Memanggil program utama
result = encrypt(inputX).hex()

# Menampilkan hasil Hash
print("Hash Result :", result)