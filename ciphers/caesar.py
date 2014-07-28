# Ben Eysenbach
# Tested on python 2.7 on Linux
# Basic encryption and decryption functionality
# Includes solutions to problems 1 and 2
# Run demo() to see solutions to problems 1 and 2



def get_char_dict():
    '''Creates a dictionary for finding the number associated with a letter'''
    valid_chars = 'abcdefghijklmnopqrstuvwxyz.,!?'
    char_dict = {}
    for n in range(0, 30):
        char_dict[valid_chars[n]] = n
    return char_dict

def filtered_input(text):
    '''converts letters to lowercase and filtereds out invalid characters'''
    text = text.lower()
    valid_chars = 'abcdefghijklmnopqrstuvwxyz.,!?'
    valid_text = ''
    for char in text:
        if char in valid_chars:
            valid_text += char
    return valid_text

def text_to_num(filtered_input, char_dict=get_char_dict()):
    '''converts characters in filtered_input into a list of corresponding numbers'''
    return [char_dict[char] for char in filtered_input]

def num_to_text(num_text):
    '''converts a list of numbers into a string of corresponding characters'''
    valid_chars = 'abcdefghijklmnopqrstuvwxyz.,!?'
    return ''.join([valid_chars[n] for n in num_text])


def modulo(number, base):
    '''performs the modulo operator'''
    return number % base

def encrypt(text, key, char_dict=get_char_dict()):
    '''encrypts text using a given key'''
    ftext = filtered_input(text)
    num_text = text_to_num(ftext, char_dict)
    num_key = char_dict[key]
    enc_num_text = [modulo(num+num_key, 30) for num in num_text]
    enc_text = num_to_text(enc_num_text)
    return enc_text

def decrypt(enc_text, key, char_dict=get_char_dict()):
    '''encrypts text using a given key'''
    enc_text = filtered_input(enc_text)
    num_key = char_dict[key]
    enc_num_text = text_to_num(enc_text, char_dict)
    dec_num_text = [modulo(num+30-num_key, 30) for num in enc_num_text]
    text = num_to_text(dec_num_text)
    return text

def demo():
    text = 'Neil Armstrong, Mike Collins, and Buzz Aldrin flew on the Apollo 11 mission.'
    print 'Problem 1:'
    print 'The encryption of \n %s \n\n using the key "m" is:' % text
    print encrypt(text, 'm')
    print
    enc_text = '?i?mbt?sdnondihzitajmhnc?zowgdbcow,c?hd,zg?i?mbtwzi!?g?,omd,zg?i?mbtv'
    print 'Problem 2:'
    print 'The decryption of \n %s \n\n using the key "z" is:' % enc_text
    print decrypt(enc_text, 'z')

if __name__ == '__main__':
    demo()
