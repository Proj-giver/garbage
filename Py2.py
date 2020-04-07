import hashlib

def lfsr(l):
    return (l[23] ^ l[22] ^ l[21] ^ l[16])
    # f(L) = L24 + L23 + L22 + L17

def nfsr(n, xb):
    return (xb ^ n[0] ^ n[1] ^ n[4] ^ n[14] ^ n[19] ^ (n[2] & n[5]) ^ (n[9] & n[11]) ^ (n[17] & n[21] & n[23]))
    # g(n,extra bit) = extra_bit + N1 + N2 + N5 + N15 + N20 + N3*N6 + N10*N12 + N18*N22*N24

def H(z,y,x8,x7,x6,x5,x4,x3,x2,x1):
    # z + y + x1*x2 + x3*x4 + x5*x6 + x7*x8
    return (z ^ y ^ (x1 & x2) ^ (x3 & x4) ^ (x5 & x6) ^ (x7 & x8))

def rounds(l, n):
    lsb = lfsr(l)
    msb = l[0]
    l = l[1:] + [lsb]
    lsb = nfsr(n, msb)
    n = n[1:] + [lsb]
    # H(L1,N2,N5,L2,L6,L12,N15,L18,L20,L24)
    return l, n, H(l[0], n[1], n[4], l[1], l[5], l[11], n[14], l[17], l[19], l[23])

def initialRounds48(l, n):
    h = H(l[0], n[1], n[4], l[1], l[5], l[11], n[14], l[17], l[19], l[23])
    l = l[1:] + [h]
    n = n[1:] + [h]
    return l, n

def cypherStream(l, n, numBits):
    for i in range(48):
        l, n = initialRounds48(l, n)
    stream = []
    for i in range(numBits):
        l, n, temp = rounds(l, n)
        stream.append(temp)
    # Convert stream to string then bytearray
    stream2 = ''
    for i in stream:
        stream2 += str(i)
    stream3 = [stream2[8*i:8*(i+1)] for i in range(len(stream2)//8)]
    stream4 = [int(i, base=2) for i in stream3]
    return stream4

def encript(plain, key):
    plaintxt = bytearray(plain, 'utf-8')
    temp = bytearray(hashlib.sha1(bytearray(key, 'utf-8')).digest())[0:3]
    temp2 = ''
    for i in temp:
        temp3 = bin(i)[2:]
        for i in range(8-len(temp3)):
            temp3 = '0' + temp3
        temp2 += temp3
    n = []
    l = []
    for i in temp2:
        n.append(int(i))
        l.append(~int(i) + 2)
    stream = cypherStream(l, n, len(plaintxt*8))
    return [x ^ y for x, y in zip(plaintxt, stream)]


plaintext = "Stream ciphers generate pseudorandom bits from a key and a nonce and encrypt the plaintext by XORing it with these pseudorandom bits, similar to the one time pad"
key = "This is a very complex key that if handeled properly should result in an ample amount of entopy! 1$dmft85^&30d(852cpdUTS"
print("This is the plain text with legth: ", len(plaintext), ":\n", plaintext)
print("This is the key with legth: ", len(key), ": \n",key)
cyphertext = encript(plaintext, key)
print("This is the cypher text with legth ", len(cyphertext), ":\n", encript(plaintext, key))







# z = 19
# x = bin(z)
# print(x)
# print(x[0], x[1], x[2], int(x[3]) + 2)

# print('Enter the initial value of L')
# # l = int(input())
# l = 541
# lengthL = len(bin(l))-2
# print("L: ", l," The type of l is: ", type(l), "\nIt's binary is : ", bin(l), "With length : ",lengthL)
# print("Converting L to proper format .... bep bop ... ")
# temp = bin(l)
# print(temp)
# print(temp[2:])
# temp = temp[2:]
# L = []
# for i in temp:
#     L.append(int(i))
#     # print(L, " building ", end='')
# print(L, "  Complete! \n")
# a = bytearray(hashlib.sha1('key'.encode('utf-8')).digest())[0:3]
# print(a)
# print(len(a))
# b = ''
# for i in a:
#     b += bin(i)[2:]
# print(b)
# c = []
# for i in b:
#     c.append(int(i))
# print(c)
