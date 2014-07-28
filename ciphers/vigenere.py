# Ben Eysenbach
# Tested on python 2.7 on Linux
# Implementation of Vigenere cipher
# Also includes an implementation of an improvement to the Vigenere cipher
# Includes solutions to problems 5, 6, and 8
# Run demo3() for solutions to problems 5 and 6
# Run demo4() for proof that my improvement on the Vigenere Cipher works
# See 'problem 8 explanation.txt' for more detail on my solution to problem 8
# Requires some functions from caesar.py

from caesar import *

def shift(num_text, key_len):
    '''Adds a string xxxxxxx the same length of the key where x equals the number of times
    the key has already been used (i.e. will add 55555 to characters 20-25 if using a
    key of length 5).'''
    shifted_num_text = []
    while len(num_text) > key_len:
        for counter in range(0, key_len):
            shifted_num_text.extend([modulo(num+counter, 30) for num in num_text[:key_len]])
            if len(num_text) < key_len:
                break            
            num_text = num_text[key_len:]
    return shifted_num_text
    
def unshift(num_text, key_len):
    '''Reverses the shift() operation'''
    unshifted_num_text = []
    while len(num_text) > key_len:
        for counter in range(0, key_len):
            unshifted_num_text.extend([modulo(num-counter, 30) for num in num_text[:key_len]])
            if len(num_text) < key_len:
                break
            num_text = num_text[key_len:]
    return unshifted_num_text

def v_encrypt(text, key, shifted=False, char_dict = get_char_dict()):
    '''encrypts text using the Vigenere cipher'''
    ftext = filtered_input(text)
    num_text = text_to_num(ftext)
    num_key = text_to_num(key)
    enc_num_text = []
    while num_text:
        for num in num_key:
            enc_num_text.append(modulo(num+num_text[0], 30))
            num_text = num_text[1:]
            if not num_text:
                break
    if shifted == True:
        enc_num_text = shift(enc_num_text, len(key))
    enc_text = num_to_text(enc_num_text)
    return enc_text

def v_decrypt(enc_text, key, shifted=False, char_dict = get_char_dict()):
    '''encrypts text using the Vigenere cipher'''
    enc_text = filtered_input(enc_text)
    enc_num_text = text_to_num(enc_text)
    num_key = text_to_num(key)
    num_text = []
    while enc_num_text:
        for num in num_key:
            num_text.append(modulo(enc_num_text[0]-num, 30))
            enc_num_text = enc_num_text[1:]
            if not enc_num_text:
                break
    if shifted == True:
        num_text = unshift(num_text, len(key))
    text = num_to_text(num_text)
    return text

def demo3():
    '''demo for problems 5 and 6'''
    text = 'Cryptography is the study of techniques for secure communicationin the presence of third parties.'
    print 'Problem 5:'
    print 'The encryption of \n %s \n\n using the key "primes!" is:' % text
    print v_encrypt(text, 'primes!')
    print
    enc_text = ',blqvbaclxbsyppcpgmg?pfmpsbkpgpqqsrxtixxzc?ecmrva??xcxwpdtqqrucaeiox.at'
    print 'Problem 6:'
    print 'The decryption of \n %s \n\n using the key "primes!" is:' % enc_text
    print v_decrypt(enc_text, 'primes!')
 
def demo4():
    '''example of better Vigenere cipher usage'''
    text = 'Cryptography is the study of techniques for secure communicationin the presence of third parties.'
    enc = v_encrypt(text, 'primes!', True)
    print enc
    print
    plain = v_decrypt(enc, 'primes!', True)
    print plain
    
if __name__ == '__main__':
    demo3()
    #demo4()
