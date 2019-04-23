import hgtk

consonants = ('ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ')
dual_consonants = ('ㄲ', 'ㄸ', 'ㅃ', 'ㅆ', 'ㅉ')
vowels = ('ㅣ', 'ㅔ', 'ㅐ', 'ㅏ', 'ㅜ', 'ㅗ', 'ㅓ', 'ㅡ', 'ㅟ', 'ㅚ', 'ㅑ', 'ㅕ',
          'ㅛ', 'ㅠ', 'ㅒ', 'ㅖ', 'ㅘ', 'ㅝ', 'ㅙ', 'ㅞ', 'ㅢ')
numbers = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
alphabets = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', "K", 'L', 'M',
             'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')

VERSION = 2.0
ENC = 0
DEC = 1
DEFAULT_LEVEL = 3
HEADER = ("HS", "VER", str(VERSION), "KEY", None, "HEN", "")


def is_consonant(char):
    if char in consonants:
        return True
    return False


def is_dual_consonant(char):
    if char in dual_consonants:
        return True
    return False


def is_vowel(char):
    if char in vowels:
        return True
    return False


def is_number(char):
    if char in numbers:
        return True
    return False


def is_alphabet(char):
    if char in alphabets:
        return True
    else:
        for i in alphabets:
            if i.lower() == char:
                return True
    return False


def create_header(key):
    header = list(HEADER)
    for i in range(len(header)):
        if header[i] == "KEY":
            header[i + 1] = str(key)
    txt = ' '.join(header)
    return txt


def decrypt_header(target):
    length = len(HEADER) - 1
    header = target.split()[:length]
    target = target.split()[length:]

    return header[header.index("VER") + 1], int(header[header.index("KEY") + 1]), ' '.join(target)


def cezaro(msg, key=DEFAULT_LEVEL, mode=ENC, header=True):
    ret = ''

    if mode == ENC:
        msg = hgtk.text.decompose(msg)
        if header:
            ret += create_header(key)
        for c in msg:
            if is_consonant(c):
                ret += consonants[(consonants.index(c) + key) % len(consonants)]
            elif is_dual_consonant(c):
                ret += dual_consonants[(dual_consonants.index(c) + key) % len(dual_consonants)]
            elif is_vowel(c):
                ret += vowels[(vowels.index(c) + key) % len(vowels)]
            elif is_number(c):
                ret += numbers[(numbers.index(c) + key) % len(numbers)]
            elif is_alphabet(c):
                if c.isupper():
                    tmp = alphabets[(alphabets.index(c) + key) % len(alphabets)]
                else:
                    tmp = alphabets[(alphabets.index(c.upper()) + key) % len(alphabets)].lower()
                ret += tmp
            else:
                ret += c
    else:
        ver, lvl, msg = decrypt_header(msg)
        msg = hgtk.text.decompose(msg)
        for c in msg:
            if is_consonant(c):
                ret += consonants[(consonants.index(c) - lvl) % len(consonants)]
            elif is_dual_consonant(c):
                ret += dual_consonants[(dual_consonants.index(c) - lvl) % len(dual_consonants)]
            elif is_vowel(c):
                ret += vowels[(vowels.index(c) - lvl) % len(vowels)]
            elif is_number(c):
                ret += numbers[(numbers.index(c) - key) % len(numbers)]
            elif is_alphabet(c):
                if c.isupper():
                    tmp = alphabets[(alphabets.index(c) - key) % len(alphabets)]
                else:
                    tmp = alphabets[(alphabets.index(c.upper()) - key) % len(alphabets)].lower()
                ret += tmp
            else:
                ret += c

    return hgtk.text.compose(ret)


def encrypt(key, num, text, header=True):
    tmp = text
    for i in range(num):
        tmp = cezaro(tmp, key, ENC, header)
    return tmp


def decrypt(key, num, text):
    tmp = text
    for i in range(num):
        tmp = cezaro(tmp, key, DEC)
    return tmp


if __name__ == '__main__':
    key = int(input("Enter the encryption level: "))
    num = int(input("Enter the number of encryption: "))

    while True:
        text = input("Enter the target text: ")
        print('Original:\t%s' % text)
        print('Caesar Cipher:\t%s' % encrypt(key, num, text))
        print('Deciphered Text:\t%s' % decrypt(num, encrypt(key, num, text)))