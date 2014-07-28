# Ben Eysenbach
# Tested on python 2.7 on Linux
# Analyzes character usage to find an unknown key
# Contains solutions to problems 3 and 4
# Run demo2() to see solutions to problems 3 and 4
# Requires certain functions from caesar.py
# Also requires the ciphertext in enctext.txt, as well as test1.txt

from caesar import *

def char_freq(text):
    '''computes the frequency of characters in text'''
    ftext = filtered_input(text)
    char_count = len(ftext)
    freq_dict = {}
    for char in ftext:
        if char in freq_dict:
            freq_dict[char] += 1
        else:
            freq_dict[char] = 1
            
    # example freq_list: [(125, 'j', 6.12), ...]
    freq_list = [(freq_dict[key], key, round(100.*freq_dict[key]/char_count, 2)) for key in freq_dict.keys()]
    return sorted(freq_list, reverse=True)
    

def compare_freq(enc_freq, norm_freq, char_dict=get_char_dict()):
    '''compares the frequency of characters in the text, and finds the most likely offset.
    The skew factor allows the 4th most common encrypted letter to be compared to the 3rd
    most common plaintext letter, and so on.
    Narrowing the skew_factor will increase speed at the expense of accuracy'''
    offsets = []
    skew_factor = (-2,3)
    for skew in range(*skew_factor):
        for n in range(-skew, 15):
            offsets.append(char_dict[enc_freq[n+skew][1]] - char_dict[norm_freq[n][1]])
            print enc_freq[n][1], '--->', norm_freq[n][1]
            print 'Likely offset:', offsets[-1]
    return offsets
    

def mode(offsets_list):
    '''computes the most common values in a list'''
    modes = [(offsets_list.count(element), element) for element in set(offsets_list)]
    # converts to set to remove duplicate items
    return sorted(set(modes), reverse=True)

def find_key(enc_text, norm_text):
    '''finds the key'''
    valid_chars = 'abcdefghijklmnopqrstuvwxyz.,!?'
    offsets = compare_freq(char_freq(enc_text), char_freq(norm_text))
    num_key = mode(offsets)[0][1]
    key = valid_chars[num_key]
    return key

def demo2():
    '''demonstrates what the program does
    note: running find_key() is faster than this, but less verbose'''
    enc_text = open('enctext.txt', 'r').read()
    norm_text = open('test1.txt', 'r').read()
    offsets = compare_freq(char_freq(enc_text), char_freq(norm_text))
    modes = mode(offsets)
    valid_chars = 'abcdefghijklmnopqrstuvwxyz.,!?'
    print
    print 'Most likely keys \t "likely factor"(1-10)\n'
    for mode_tuple in modes:
        print '%10s \t\t %10d' % (valid_chars[mode_tuple[1]], mode_tuple[0])
    key = valid_chars[modes[0][1]]
    print
    print 'Decrypting using most likely key, ', key
    print
    print decrypt(enc_text, key)
    print
    
    
if __name__ == '__main__':
    demo2()
