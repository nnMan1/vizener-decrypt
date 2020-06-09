import numpy as np
import nltk
from nltk.corpus import words
import string
import math


def change_text_case(text, text_case):                 # da sacuvamo velika slova 
    case_corect = ""                                   # sve prebacamo da radimo sa malim slovima ali pamtimo koje je slovo bilo veliko

    text_length = min(len(text), len(text_case))       # i na kraju vracemo 

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
    key = key.lower()                               # sva velika slova smanjujemo i onda kriptujemo 

    for i in range(text_length):                                                                       #                                 
        if text[i] <= 'z' and text[i] >= 'a' and key[i % key_length] >= 'a' and key[i % key_length]<='z':                                                          # "sabiramo" sa kljucem tekst
            encrypted += chr((ord(text[i]) - 2*ord('a') + ord(key[i % key_length])) % 26 + ord('a'))   #
        else:
            encrypted += text[i]
    
    encrypted = change_text_case(encrypted, text1)                #vracamo velika slova koristeci originalni tekst 

    return encrypted

def characters_count(text, key_length, offset): #broji slova u kriptogramu text na  pozicijama offset,offset+key_lenght ,....
    ret_val = [0] * 26  # ret_val je niz od 26 brojeva koji govore koliko se puta i-to slovo pojavilo u podnizu
    text_length = len(text)
    br = 0

    for c in range(offset, text_length, key_length):
        if(ord(text[c]) >= ord('a') and ord(text[c]) <= ord('z')):
            ret_val[ord(text[c])- ord('a')] = ret_val[ord(text[c])- ord('a')] + 1
            br = br+1

    return ret_val, br 

def get_max_index(arr):          # vraca indeks najveceg elementa u nizu 
    l = len(arr)  
    max_ind = 0

    for i in range(l):
        if(arr[max_ind]<arr[i]):
            max_ind = i
    return max_ind

def get_min_index(arr):          # vraca indeks najmanjeg elementa u nizu 
    l = len(arr)
    min_ind = 0

    for i in range(l):
        if(arr[min_ind]>arr[i]):
            min_ind = i
    return min_ind

def shift(xs, n):                # funkcija za siftovanje niza xs ulijevo za n mjesta 
    e = np.empty_like(xs)        # primjer xs  =[4 , 5 ,8 ,1] -> [1, 4 ,5 ,8 ]
    f = xs[len(xs) - 1]
    if n >= 0:
        e[:n] = np.nan
        e[n:] = xs[:-n]
    else:
        e[n:] = np.nan
        e[:n] = xs[-n:]
    e[0] = f
    return e

def decrypt_key(text, key):      #za dati kljuc key radi dekriptovanje teksta text
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

def decrypt(text):               #glavna funkcija  kriptoanalize
    text_org = text              #za dati kriptovani tekst nalazi "najboljU" duzinu kljuca 
    text = text.lower()          #,zatim bira napogodniju od 26 ciklicnih permutaicja i nakon toga kljuc ce bit ipoynat u potpunosti 
    
    text_length = len(text)
    pl = []

    for i in range(1,math.floor(text_length/10)):
    
        najgoriDoSad=0
        for k in range(0,i):
            cf, br = characters_count(text, i, k)
            sum = 0
            for j in range(0, 25):
                sum = sum + (cf[j]*(cf[j]-1)) #racunamo index koincidencije podniza 

            if(br < 2):                       #ako ima previse bjelina,znakova pitanja,specijalnih znakova,itd
                break

            sum = sum / (br * (br-1))
            if(abs(sum - 0.06653846)> najgoriDoSad):
                najgoriDoSad=abs(sum - 0.06653846)

           
        pl.append(najgoriDoSad)      #ako naiđemo na duzinu ciji je IC 0.008 udaljen od 0.065 zavrsavamo  jer          
        #if(abs(sum - 0.065) < 0.008):    # ako budemo "dobar" IC za 4 ,i npr malo bolji IC za 8 i 12 i neki drugi umnozak od 4   
        #    break                        # bira se  4 jer se slovs lakse nalaze
        
    if(len(pl) == 0):                   
        return "Tekst ne moze biti dekriptovan"

    #l = get_min_index(pl)
    
    stat = np.array([0.08167, 0.01492, 0.02202,	0.04253, 0.12702,	
                     0.02228, 0.02015, 0.06094, 0.06966, 0.00153,	
                     0.01292, 0.04025, 0.02406, 0.06749, 0.07507,
                     0.01929, 0.00095, 0.05987, 0.06327, 0.09356,	
                     0.02758, 0.00978, 0.02560, 0.00150, 0.01994,	
                     0.00077])
    
    ret_val = ""
    bestFitness = -1
    bestKey = ""
    nizMinimalnihIndeksa = get_First_Min_Elements(pl,20)

    for cnt in range(0,20):
        l = nizMinimalnihIndeksa[cnt]
        ret_val = ""
        for i in range(l+1):   # petlja koja prolazi svaki od l+1 podnizova 
            offset = 25
            cf, br = characters_count(text, l+1, i)
            
            if(br == 0):
                return "Tekst ne moze biti dekriptovan"

            stat_res = np.array([])
            for i in cf:
                stat_res = np.append(stat_res, i/br)            #pravi statistiku za dati podniz  

            offset_dist = np.linalg.norm(stat_res - stat)       

            for j in range(25):                                         #
                stat_res = shift(stat_res, 1)                           #
                if(offset_dist > np.linalg.norm(stat_res - stat)):      #odredjujemo koja je od 26 cilicnih permutacija najbliza 
                    offset = j                                          #poznatoj raspodjeli slova engleskog jezika 
                    offset_dist = np.linalg.norm(stat_res - stat)       #
                    
            ret_val+= chr(ord('z') - offset)   # dodajemo slovo na kljuc 
        temp=fitnessLevel(decrypt_key(text_org, ret_val)); 
       # print(ret_val,temp, l)
            
        if( temp > bestFitness or (temp == bestFitness and len(ret_val)<len(bestKey) )):
            bestFitness=temp
            bestKey=ret_val

    
    
    #print("||||||||| "+ret_val+" |||||||| ") # stampa se cijelu kljuc koji smo nasli  

    return [decrypt_key(text_org,bestKey),bestKey]

def fitnessLevel(text):
    cnt=0
    file=open("rijeci.txt", "r")  #fajl koji sadrzi 250 najcescih rijeci engleskog jezika
    temp = file.readline()
    while len(temp) > 1:          #necemo gledati rijeci duzine jedan
        temp = temp[:-1] 
        temp=" "+temp+" "         #ucita newline pa onda njega brisem
        if temp in text:
            cnt=cnt+1
        temp=file.readline()   

    return cnt

def get_First_Min_Elements(array , k):
    length = len(array)
    result=[]
    if (length < k):
     print("Greska !")
     return []
    
    l=get_min_index(array)
    result.append(l)
    array[l]=100

    for i in range(0,k-1):
        l=get_min_index(array)
        result.append(l)
        array[l]=100

    print(result)
    return result
