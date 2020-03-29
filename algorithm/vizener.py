def change_text_case(text, text_case):
    case_corect = ""

    text_length = min(len(text), len(text_case))

    for i in range(text_length):
        if text_case[i] <= 'Z' and text_case[i] >= 'A':
            case_corect += chr(ord(text[i]) - ord('a') + ord('A'))    
        else:
            case_corect += text[i]

    return case_corect

def encrypt(text, key):
    key_length = len(key)
    text_length = len(text)
    encrypted = ''

    text1 = text
    text = text.lower()

    for i in range(text_length):
        if text[i] <= 'z' and text[i] >= 'a':
            encrypted += chr((ord(text[i]) - 2*ord('a') + ord(key[i % key_length])) % 26 + ord('a')) 
        else:
            encrypted += text[i]
    
    encrypted = change_text_case(encrypted, text1)

    return encrypted

