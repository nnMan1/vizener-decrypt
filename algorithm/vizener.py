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

def characters_count(text, key_length, offset):
    ret_val = [0] * 26
    text_length = len(text)
    br = 0

    for c in range(offset, text_length, key_length):
        if(ord(text[c]) >= ord('a') and ord(text[c]) <= ord('z')):
            ret_val[ord(text[c])- ord('a')] = ret_val[ord(text[c])- ord('a')] + 1
            br = br+1

    return ret_val, br

def get_max_index(arr):
    l = len(arr)
    max_ind = 0

    for i in range(l):
        if(arr[max_ind]<arr[i]):
            max_ind = i
    return max_ind

def get_min_index(arr):
    l = len(arr)
    min_ind = 0

    for i in range(l):
        if(arr[min_ind]>arr[i]):
            min_ind = i
    return min_ind

def decrypt(text):

    text_org = text
    text = text.lower()

    pl = []

    for i in range(1,25): #ogranicili smo se da nece duzina kljuca bit vece od 25
        cf, br = characters_count(text, i, 0)
        sum = 0
        for j in range(0, 25):
            sum = sum + (cf[j]*(cf[j]-1))
        sum = sum / (br * (br-1))
        pl.append(abs(sum - 0.0659731039))

    l = get_min_index(pl)
    
    ret_val = ""

    for i in range(l+1):
        cf, br = characters_count(text, l+1, i)
        i1 = get_max_index(cf)  
        offset = (26 - i1 + 4) % 26
        ret_val+= chr(ord('a') + offset)

    return encrypt(text, ret_val)