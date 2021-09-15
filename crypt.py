""" please install numpy and egcd module"""

import numpy as np  # pip install numpy
from egcd import egcd  # pip install egcd

# characters that are usually be used in a string

alphabet ='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*_-=+/.<>:;?\|`~ '


letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


def matrix_mod_inverse(matrix, modulus):
    """ solve matrix problem"""

    det = int(np.round(np.linalg.det(matrix)))
    det_inv = egcd(det, modulus)[1] % modulus
    matrix_modulus_inverse = det_inv * np.round(det*np.linalg.inv(matrix)).astype(int) % modulus
    return matrix_modulus_inverse


K = np.matrix([[3, 10, 20], [20, 19, 17], [23, 78, 17]])  # for length of alphabet 27
Kinv = matrix_mod_inverse(K, len(alphabet))


def encrypt(message, K):
    """ encrypt a string"""

    encrypted = ""
    message_in_numbers = []
    # make message into numbers
    for letter in message:
        message_in_numbers.append(letter_to_index[letter])

    # split into the size of matrix K

    split_P = [message_in_numbers[i:i+int(K.shape[0])] for i in range(0, len(message_in_numbers), int(K.shape[0]))]

    # iterate through each partial message nad encrypt using p

    for P in split_P:
        P = np.transpose(np.asarray(P))[:, np.newaxis]
        while P.shape[0] != K.shape[0]:
            P = np.append(P, letter_to_index[' '])[:, np.newaxis]
        numbers = np.dot(K, P) % len(alphabet)
        n = numbers.shape[0]

        # Map it back to text

        for idx in range(n):
            number = int(numbers[idx, 0])
            encrypted += index_to_letter[number]
    return encrypted


def decrypt(cipher, Kinv):
    """ decrypt a string encrypted by this program"""

    decrypted = ''

    cipher_in_numbers = []

    # Make ciphered tect into number

    for letter in cipher:
        cipher_in_numbers.append(letter_to_index[letter])

    # Split it into the size ofm matrix inv(K) so we can do matrix multiplication.

    split_C = [cipher_in_numbers[i:i + int(Kinv.shape[0])] for i in range(0, len(cipher_in_numbers), int(Kinv.shape[0]))]

    # iterate through each partial cipher text and decrypt using inv(k)*C mod(26)

    for C in split_C:
        C =np.transpose(np.asarray(C))[:, np.newaxis]
        numbers = np.dot(Kinv, C) % len(alphabet)
        n = numbers.shape[0]

    # Map back numbers to decrypt text

        for idx in range(n):
            number = int(numbers[idx, 0])
            decrypted += index_to_letter[number]
    return decrypted


'''
    # Extra matrix keys to switch entryption if required
     K = np.array([[3, 3], [2, 5]])
    K = np.matrix([[3, 10, 20], [20, 19, 17], [23, 78, 17]])  # for length of alphabet 27
    Kinv = matrix_mod_inverse(K, len(alphabet))
'''