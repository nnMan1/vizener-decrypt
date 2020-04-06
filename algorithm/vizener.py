import numpy as np

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

def shift(xs, n):
    e = np.empty_like(xs)
    f = xs[len(xs) - 1]
    if n >= 0:
        e[:n] = np.nan
        e[n:] = xs[:-n]
    else:
        e[n:] = np.nan
        e[:n] = xs[-n:]
    e[0] = f
    return e


def decrypt_key(text, key):
    key_length = len(key)
    text_length = len(text)
    encrypted = ''

    text1 = text
    text = text.lower()

    for i in range(text_length):
        if text[i] <= 'z' and text[i] >= 'a':
            encrypted += chr((ord(text[i]) + 26 - ord(key[i % key_length])) % 26 + ord('a')) 
        else:
            encrypted += text[i]
    
    encrypted = change_text_case(encrypted, text1)

    return encrypted

def decrypt(text):
    text_org = text
    text = text.lower()
    
    text_length = len(text)
    pl = []

    for i in range(1,text_length): #ogranicili smo se da nece duzina kljuca bit vece od 25
        cf, br = characters_count(text, i, 0)
        sum = 0
        for j in range(0, 25):
            sum = sum + (cf[j]*(cf[j]-1))

        if(br < 2): #ako ima previse bjelina
            break

        sum = sum / (br * (br-1))
        pl.append(abs(sum - 0.065))
        if(abs(sum - 0.065) < 0.008):
            break
    if(len(pl) == 0):
        return "Tekst ne moze biti dekriptovan"

    l = get_min_index(pl)
    
    stat = np.array([0.08167, 0.01492, 0.02202,	0.04253, 0.12702,	
                     0.02228, 0.02015, 0.06094, 0.06966, 0.00153,	
                     0.01292, 0.04025, 0.02406, 0.06749, 0.07507,
                     0.01929, 0.00095, 0.05987, 0.06327, 0.09356,	
                     0.02758, 0.00978, 0.02560, 0.00150, 0.01994,	
                     0.00077])
    
    ret_val = ""

    for i in range(l+1):
        offset = 25
        cf, br = characters_count(text, l+1, i)
        
        if(br == 0):
            return "Tekst ne moze biti dekriptovan"

        stat_res = np.array([])
        for i in cf:
            stat_res = np.append(stat_res, i/br)

        offset_dist = np.linalg.norm(stat_res - stat)

        for j in range(25):
            stat_res = shift(stat_res, 1)
            if(offset_dist > np.linalg.norm(stat_res - stat)):
                offset = j
                offset_dist = np.linalg.norm(stat_res - stat)
                 
        ret_val+= chr(ord('z') - offset)
    
    print(ret_val)

    return decrypt_key(text, ret_val)