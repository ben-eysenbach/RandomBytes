# Ben Eysenbach
# Tested on python 2.7 on Linux
# Analyzes character usage to crack cigenere cipher
# Includes solutions to problem 7
# Run demo5() to see solution to problem 7
# Run test_improvement() to see how my improvement to the Vigenere cipher makes the cipher harder to crack
# For more detail on problem 7, see 'problem 7 explanation.txt'
# Requires some functions from caesar_analyze.py and from vigenere.py

from caesar_analyze import *
from vigenere import *

def deviation(enc_freq, norm_freq):
    '''compares the patterns of frequencies of characters to determine if an encrypted string displays patterns of an unencrypted string
    Note: this is used instead of compare_freq() because compare_freq tries to find a best offset, while deviation() determines if a good offset exists'''
    dev = 0
    for n in range(10):
        dev += abs(enc_freq[n][2] - norm_freq[n][2])
    return dev

def recombine(text, key_len):
    '''returns a list of strings that are formed by taking characters that are a certain distance apart
    Ex: recombine('abcdefghijklnop', 5) -->  ['afk', 'bgl', 'chn', 'dio', 'ejp'] '''
    new_strings = []
    text_len = len(text)
    for start in range(key_len):         #where to start
        gen_str = ''                     #string being generated
        counter = start
        while counter < text_len:
            gen_str += text[counter]
            counter += key_len
        new_strings.append(gen_str)
    return new_strings

def find_key_len(enc_text, norm_text):
    '''finds the length of the key used to encrypt a string using a Vigenere cipher'''
    minimum_dev = (0,100)     # (key_len, deviation)
    norm_freq = char_freq(norm_text)
    for key_len in range(3,16):
        devs = []
        test_strings = recombine(enc_text, key_len)
        for string in test_strings:
            devs.append(deviation(char_freq(string), norm_freq))
        avg_dev = sum(devs)/len(devs)
        print 'Average deviation using %d length key was %d' % (key_len, avg_dev)
        if avg_dev < minimum_dev[1]:
            minimum_dev = (key_len, avg_dev)
    return minimum_dev[0]
    
    
    
    
def find_v_key(enc_text, norm_text, key_len):
    '''finds the key to a ciphertext encrypted using a Vigenere cipher'''
    key = ''
    new_strings = recombine(enc_text, key_len)
    for string in new_strings:
        key += find_key(string, norm_text)
        print 'Key: ', key
    return key

def demo5():
    norm_text = open('test1.txt', 'r').read()
    enc_text = open('test2.txt', 'r').read()
    key_len = find_key_len(enc_text, norm_text)
    print '\n'*2, '-'*30, '\nThe key is %d letters long!' % key_len
    key = find_v_key(enc_text, norm_text, key_len)
    print '\n'*2, '-'*30, '\nThe key is "%s"' % key
    print 'Press [enter] to see the decryption using this key:'
    raw_input()
    print 'The decryption using this key is: '
    print v_decrypt(enc_text, key)
    return

def test_improvement():
    '''tests to see if frequency analysis can be performed on the improved Vigenere Cipher
    to find the key length
    Note: this is meant to fail to show that my improvement is valid; this function therefore
    takes a long time to run'''
    norm_text = open('test1.txt', 'r').read()
    new_strings = recombine(norm_text, 10)
    for counter in range(10):
        print '\nTest %d\n' % (counter+1)
        string = new_strings[counter]
        print 'Attempting to find key length:'
        key_len = find_key_len(v_encrypt(string, 'math!', True), norm_text)
        print 'Key Length: ', key_len
    return

    
if __name__ == '__main__':
    demo5()
    #test_improvement()
