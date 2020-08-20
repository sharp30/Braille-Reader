import numpy as np
from PIL import Image

wanted = [248,0,211]

x= {(True, False,False, False,False, False):'A',
    (True, False,True, False,False, False):'B',
  (True, True,False, False,False, False):'C',
    (True, True,False, True,False, False):'D',
     (True, False,False, True,False, False):'E',
     (True, True, True, False, False, False): 'F',
      (True, True,True, True,False, False):'G',
       (True, False,True, True,False, False):'H',
        (False, True,True, False,False, False):'I',
         (False, True,True, True,False, False):'J',
          (True, False,False, False,True, False):'K',
           (True, False,True, False,True, False):'L',
            (True, True,False, False,True, False):'M',
             (True, True,False, True,True, False):'N',
              (True, False,False, True,True, False):'O',
               (True, True,True, False,True, False):'P', 
               (True, True,True, True,True, False):'Q', 
               (True, False,True, True,True, False):'R',
                (False, True,True, False,True, False):'S',
                 (False, True,True, True,True, False):'T',
                  (True, False,False, False,True, True):'U',
                   (True, False,True, False,True, True):'V',
                    (False, True,True, True,False, True):'W',
                    (True, True, False, False, True, True) : 'X',
                     (True, True,False, True,True, True):'Y',
                      (True, False,False, True,True, True):'Z',
                       (False, True,False, True,True, True):'#',
                       (False,False,True,False,False,False):',',
                       (False,False,True,True,False,True) : '.'}

def is_full_or_not(im):
    global wanted
    npp=np.array(im.convert('RGB'))
    result = np.count_nonzero(np.all(npp==wanted,axis=2))
    return result > 10

def crop2(im,Wpart,Hpart):
    parts=[]
    width,height= im.size
    i = 0
    while i < height:
        plus = Hpart
        stopH = min(height,plus +i)
        for j in range(0,width,Wpart):
            stopW = min(width,Wpart +j)
            box = (j,i,stopW,stopH)
            a = im.crop(box)
            parts.append(is_full_or_not(a))
        i+=plus
    return parts


def transform_numbers(text):
    correct = ""
    i = 0
    while i <len(text):
        if text[i] == '#' and i +1 != len(text) and text[i+1] <= 'J' and text[i+1] >= 'A':
            diff = ord(text[i+1])-ord('A')+1
            diff = ord('0') if diff == 10 else ord('0') +diff
            correct += chr(diff)
            i += 2
        else:
            correct += str(text[i])
            i +=1
    return correct

def crop(path,Wpart,Hpart):
    global x
    txt = ""
    im =Image.open(path)
    width,height= im.size
    k = 0
    i = 1
    line_num = 1
    while i < height:

        stopH =min(height,Hpart +i)

        for j in range(7,width,Wpart):

            if k>=1934:
                i = height
                break
            if (k+1)%34 ==0:
                k+=1
                continue
            
            stopW = min(width,Wpart +j)
            box = (j,i,stopW,stopH)
            a = im.crop(box)
            a.save("kkk/pic" + str(k) +".png")
            
            
            parts = crop2(a,15,Hpart/3)
            let = x.get(tuple(parts))
            let = '$' if let == None else let
            if let == '$':
                print(k,parts)
                a.show()
                exit()
                pass
            if let == '$':
                pass
            txt += let
            k +=1
        i+= Hpart

        if line_num % 12 == 0:
            i+=5
        line_num +=1

    return transform_numbers(txt)


txt = crop("pic.png",30,43)
print (txt)
print(txt.count('$') , txt.count('#'),len(txt))
