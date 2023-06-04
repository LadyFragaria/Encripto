# ─────────█▄██▄█─────────        V 1.0        ─────────█▄██▄█─────────
# █▄█▄█▄█▄█▐█┼██▌█▄█▄█▄█▄█ API de incriptacion █▄█▄█▄█▄█▐██┼█▌█▄█▄█▄█▄█
# ███┼█████▐████▌█████┼███ Encrip, text to img ███┼█████▐████▌█████┼███
# █████████▐████▌█████████   de Fragaria DEV   █████████▐████▌█████████

""" Text encryption algorithms
Encryption algorithms for plain text, multiline text, csv and text to img
"""

#┎୨♡୧┈┈┈┈ imports ┈┈┈┈୨♡୧┒
from random import randint
from PIL import Image

class CriptoText:
    """ Encryption of simple text
    Encryption and decription of simple text with text key
    """
    #┎୨♡୧┈┈┈┈ init┈┈┈┈୨♡୧┒
    def __init__(self,rkey:str,mess:str):
        self.rkey = rkey
        self.mess = mess
        self.letters="""AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890 .,:;'"¿?¡![](){}#$%&*+-_~^|/ÀàÈèÌìÒòÙùÁáÉéÍíÓóÚúÝýÂâÊêÎîÔôÛûÃãÑñÕõÄäËëÏïÖöÜüŸÿÅåÆæŒœÇçÐðØøß"""

    #┎୨♡୧┈┈┈┈ translate data pos/char ┈┈┈┈୨♡୧┒
    def numerify(self, text:str):
        """numerify Turns text to an numered array

        Turns text to an array with the position of each character in the abc

        Args:
            text (str): string to turn in array

        Returns:
            list: string nummered in array
        """
        return [self.letters.index(i) for i in
                [x if x in self.letters else "?" for x in text]]

    def normalize(self,nums:list):
        """normilize numbers in the range of 0 - 153

        Args:
            nums (list): array to normalize

        Returns:
            list: array normalized
        """
        top_chars,added = [153, 154]
        corrected = []
        for i in nums:
            if i > top_chars:
                corrected.append(i-added)
            elif i < 0:
                corrected.append(i+added)
            else:
                corrected.append(i)
        return corrected

    def letterify(self,nums:list):
        """letterify turns numered array to text

        turns an array of position of characters to their text form

        Args:
            nums (list): array of characters in position form

        Returns:
            str: text of characters
        """
        return "".join([self.letters[i] for i in self.normalize(nums)])


    #┎୨♡୧┈┈┈┈ key related work ┈┈┈┈୨♡୧┒
    def key_maker(self):
        """key_maker creates the basic ciph keys

        creates de basics ciph keys from the raw ciph key given

        Returns:
            dict: basic ciph keys in numerical form
        """
        full= self.numerify(self.rkey)
        key_len = len(self.rkey)

        ckeys={"full":full}

        # ✿ pull pin data ✿
        if key_len % 2 == 0:
            ckeys["pin"] = full[0:4]
        else:
            ckeys["pin"] = full[-4:]

        # ✿ create cesar keys ✿
        if key_len % 5 == 0:
            bited = [full.pop() for i in range(int(key_len/5))][::-1]
            ckeys["main_key"] = full
            ckeys["second_key"] = [0 for i in range(len(full))] + bited
        elif key_len % 3 == 0:
            #se voltea la lista para tomar los primeros numeros al hacer pop
            full = full[::-1]
            bited = [full.pop() for i in range(int(key_len/3))]
            #se voltea el sobrante para regresar al estado normal
            ckeys["main_key"] = full[::-1]
            ckeys["second_key"] = [0 for i in range(len(full))] + bited
        elif key_len % 2 == 0:
            bite = int(key_len/4)
            ckeys["main_key"] = full[:bite]
            ckeys["second_key"] = full[bite:] + [0 for i in range(bite-1)]
        else:
            ckeys["main_key"] = full
            ckeys["second_key"] = [0 for i in range(len(full)-1)] + full[::-1]
        return ckeys

    #┎୨♡୧┈┈┈┈ cesar related work ┈┈┈┈୨♡୧┒
    def cesar_make_keyciph(self,targ_len:int,ciph_key:list):
        """cesar_make_keyciph creates ciph key as long as text

        repeats ciph key to be as long as terget text

        Args:
            targ_len (int): how long the text is
            ciph_key (list): ciph key to be repeated

        Returns:
            list: ciph key thats text-long
        """
        return (ciph_key * (targ_len // len(ciph_key))) + ciph_key[:(targ_len % len(ciph_key))]

    def cesar_double_encrip(self,ck_main:list,ck_second:list,numered:list,encrip:bool):
        """cesar_double_encrip double encripts text on cesar algorithm

        takes the two encryption keys and the text, creates a ciphered texts

        Args:
            ck_main (list): main ciph key
            ck_second (list): secondary ciph key
            numered (list): text to encrypt in numered position form
            encrip (bool): if true encripts, if false decripts

        Returns:
            list: encrypted text
        """
        targ_len = len(numered)
        zipped = list(zip(self.cesar_make_keyciph(targ_len,ck_main),
                          self.cesar_make_keyciph(targ_len,ck_second),
                          numered))
        if encrip:
            return [(a+b+c) for a, b, c in zipped]
        return [(c-a-b) for a, b, c in zipped]

    #┎୨♡୧┈┈┈┈ position ciph related work ┈┈┈┈୨♡୧┒
    def pin_maker(self,pin:list):
        """pin_maker extracts numbers to use from pin

        _extended_summary_

        Args:
            pin (list): position values from pin

        Returns:
            dict: values to use from pin
        """
        # ✿ extract data from pin ✿
        pin_clean_hunds = [i % 100 for i in pin]
        pin_all = [i // 10 for i in pin_clean_hunds] + [i % 10 for i in pin_clean_hunds]
        pin_all = pin_all + [pin_all.count(0),  pin_all.count(1), pin_all.count(2), len(pin_all)]
        pin_set = list(set(pin_all))

        for i in [0,1]:
            if i in pin_set:
                pin_set.remove(i)

        pin_dict = {"rev0": True if 9 and 3 in pin_set else False,
                    "rev-1": True if 7 and 5 in pin_set else False,
                    "pin_len": pin_all[-1],
                    "max_num": pin_set[-1],
                    "min_num": pin_set[0],
                    "col_wid": [i for i in pin_set if i > 4],
                    "bite_size": [i for i in pin_set if i < 5]}

        # ✿ be sure theres data that can be used ✿
        if len(pin_dict["col_wid"]) < 1:
            pin_dict["col_wid"] = [6 if pin_dict["pin_len"] % 2 == 0 else 5,
                                   8 if pin_dict["max_num"] % 2 == 0 else 7]

        if len(pin_dict["col_wid"]) < 1:
            pin_dict["bite_size"] = [2,3 if pin_dict["min_num"] % 2 == 0 else 4]

        return pin_dict

    def trans_ciph(self,numered:list,wcols:int,bite:int,reverse:bool,encrip:bool):
        """trans_ciph encrypts by column transposition

        Args:
            numered (list): text to encrypt in numered position form
            wcols (int): width of columns
            bite (int): bite to be taken from columns
            reverse (bool): if numbers are moved fw of bw
            encrip (bool): if true encripts, if false decripts

        Returns:
            list: list of positions encrypted by displacement
        """
        parted = [numered[i:i + wcols] for i in range(0, len(numered), wcols)]
        if encrip:
            if reverse:
                for i in range(bite):
                    parted = [[x[-1]] + x[:-1] for x in parted]
            else:
                for i in range(bite):
                    parted = [x[1:] + [x[0]] for x in parted]
        else:
            if reverse:
                for i in range(bite):
                    parted = [x[1:] + [x[0]] for x in parted]
            else:
                for i in range(bite):
                    parted = [[x[-1]] + x[:-1] for x in parted]
        return [item for sublist in parted for item in sublist]

    #┎୨♡୧┈┈┈┈ runnin ciphs ┈┈┈┈୨♡୧┒
    def run_cesar_ciph(self,numered:list,encrip:bool):
        """run_cesar_ciph runs cesar ciph with given data

        Args:
            numered (list): text to encrypt in numered position form
            encrip (bool): if true encripts, if false decripts

        Returns:
           list: encripted list
        """
        ciph_keys = self.key_maker()
        cesared = self.cesar_double_encrip(ciph_keys["main_key"],
                                           ciph_keys["second_key"],
                                           numered,
                                           encrip)
        return cesared

    def run_trans_ciph(self,numered:list,encrip:bool):
        """runs position cipher

        Args:
            numered (list): text to encrypt in numered position form
            encrip (bool): if true encripts, if false decripts

        Returns:
            list: ciphered message in numeric form
        """
        pin_data = self.pin_maker(self.key_maker()["pin"])
        mixed_up = self.trans_ciph(numered,
                                   pin_data["col_wid"][0 if len(self.mess) % 2 == 0 else -1],
                                   pin_data["bite_size"][0 if len(self.mess) % 3 == 0 else -1],
                                   [pin_data[f"rev{0 if len(self.mess) % 5 == 0 else -1}"]],
                                   encrip)
        return mixed_up

    #┎୨♡୧┈┈┈┈ ciph easy use ┈┈┈┈୨♡୧┒
    def full_ciph(self,encrip:bool):
        """full cipher in numeric form

        Args:
            encrip (bool): true if is to encript, false to decript

        Returns:
            list: result of ciph/deciph
        """
        ciph = []
        if encrip:
            ciph= self.run_trans_ciph(self.run_cesar_ciph(self.numerify(self.mess), True), True)
        else:
            ciph = self.run_cesar_ciph(self.run_trans_ciph(self.numerify(self.mess), False), False)
        return self.normalize(ciph)

    #┎୨♡୧┈┈┈┈ readable extraction ┈┈┈┈୨♡୧┒
    def readable_ciph(self,encrip:bool):
        """Returns a readable (letterified) ciph/deciph

        Args:
            encrip (bool): true if is to encript, false to decript

        Returns:
            str: result of ciph
        """
        if encrip:
            return self.letterify(self.full_ciph(True))
        return self.letterify(self.full_ciph(False))

class TextToImg:
    
    #┎୨♡୧┈┈┈┈ init┈┈┈┈୨♡୧┒
    def __init__(self,rkey:str,mess:str,name:str):
        self.cript = CriptoText(rkey,mess)
        self.rkey = rkey
        self.name = name

    #┎୨♡୧┈┈┈┈ encription pattern gen ┈┈┈┈୨♡୧┒
    def pattern(self, targ_len:int):
        """Creates the pattern the pixels will ve encripted in

        Args:
            targ_len (int): leng to match 

        Returns:
            list: encription patern as long as the message
        """
        block = []
        for i in self.cript.key_maker()["full"]:
            if i % 3 == 0:
                block.append(3)
            elif i % 2 == 0:
                block.append(2)
            else:
                block.append(1)
        return (block * (targ_len // len(block))) + block[:(targ_len % len(block))]
    
    #┎୨♡୧┈┈┈┈ methods for img creation ┈┈┈┈୨♡୧┒
    def ran_char(self):
        """creates a random integer in the range of cipher

        Returns:
            int: random integer that mimics the format of all other 
        """
        return randint(0,153)

    def size_calc(self,pixels):
        """calculates de needed size of canvas to our img

        Args:
            pixels (int): how many pixels must save

        Returns:
            tuple: tuple with the needed size
        """
        square = int(pixels**(1/2)) 
        #print(f"SQUARE: {square} of {pixels}")
        if (square*square) < pixels:
            square += 1
        return (square,square)

    #┎୨♡୧┈┈┈┈ create img ┈┈┈┈୨♡୧┒
    def create_pixels(self):
        """creates the pixels of the img that will be saved

        Returns:
            list: list with pixel data in rgb format
        """
        all_data = list(zip(self.pattern(len(self.cript.mess)),self.cript.full_ciph(True)))
        pixels = []
        for a,b in all_data:
            if a == 3:
                pixels.append(( self.ran_char(), self.ran_char(), b ))
            elif a == 2:
                pixels.append(( self.ran_char(), b, self.ran_char() ))
            else:
                pixels.append(( b, self.ran_char(), self.ran_char() ))
        return pixels
    
    def save_img(self,pixels:list,name:str):
        im = Image.new("RGB",self.size_calc(len(pixels)),(255,255,255))
        im.putdata(pixels)
        im.save(name)
    
    def create_img(self):
        """creates and saves the img in png format
        """
        self.save_img(self.create_pixels(),self.name)

    #┎୨♡୧┈┈┈┈ pull and decript ┈┈┈┈୨♡୧┒
    def pull_colors(self):
        """pull the pixels from a presaved img

        Returns:
            list: list of pixel data
        """
        colors = []
        with Image.open(self.name,"r") as im:
            im = im.convert("RGB")
            colors = list(im.getdata())
        return [i for i in colors if i != (255,255,255)]
    
    def retrive_cipher(self,colors:list):
        """retrives the cipher hidden in pixels

        Args:
            colors (list): colors to extract from

        Returns:
            list: ciphered message
        """
        num_mess = []
        for a,b in list(zip(self.pattern(len(colors)),colors)):
            if a == 3:
                num_mess.append(b[2])
            elif a == 2:
                num_mess.append(b[1])
            else:
                num_mess.append(b[0])
        return num_mess

    def extract_from_pixels(self):
        """extracts from the image in the given name

        Returns:
            list: message ciphered in img
        """
        return self.retrive_cipher(self.pull_colors())
    
    def deciph_img(self):
        """translates to text message ciphered in img

        Returns:
            str: mesagge deciphered
        """
        return CriptoText(self.rkey, self.cript.letterify(self.extract_from_pixels())).readable_ciph(False)

class PT_Encrip:
    def __init__(self,rkey:str,mess:str,name:str):
        self.rkey = rkey
        self.mess = mess
        self.name = name
        self.ttimg = TextToImg(rkey, mess, name)

    def create_img(self):
        """creates the img for the profile
        """
        self.ttimg.create_img()

    def deciph_img(self):
        """deciphers the img
        """
        return self.ttimg.deciph_img()
    
def random_str(num:int):
    """creates random string of given number of characters

    Args:
        num (int): string leng

    Returns:
        str: random string
    """
    m = TextToImg(" "," "," ")
    x = [m.ran_char() for x in range(num)]
    return CriptoText(" "," ").letterify(x)

class DB_Encrip:
    def __init__(self,rkey:str,mess:str,name:str):
        self.rkey = rkey
        self.mess = mess
        self.name = name
    
    def prepare_data(self):
        """Prepares the data for pixel creation

        Returns:
            list: 0 contains spaces pattern, 1 contains text as a single string
        """
        spaces = []
        all_text = ""
        for i in self.mess:
            spaces.append([len(str(x)) for x in i])
            for y in i:
                all_text += str(y)
        return [spaces,all_text]
    
    def create_img(self):
        """Creates pixels for img

        Returns:
            list: 0 contains pixels, 1 contains size
        """
        data = self.prepare_data()
        img_obj = TextToImg(self.rkey,data[1],"x")
        pixel_basic = img_obj.create_pixels()
        new_pixels = []
        for line in data[0]:
            for point in line:
                new_pixels += [pixel_basic.pop(0) for x in range(point)]
                new_pixels.append((254,254,254))
            new_pixels.append((253,253,253))

        img_obj.save_img(new_pixels,self.name)

    def deciph_img(self):
        """deciphers the saved image

        Returns:
            list: deciphered db, similar to a csv read
        """
        img_obj = TextToImg(self.rkey,"x",self.name)

        spaces, data, tempo_spaces = [[],[],[]]
        counter = 0
        for i in img_obj.pull_colors():
            if i == (254,254,254):
                tempo_spaces.append(counter)
                counter=0
            elif i == (253,253,253):
                spaces.append(tempo_spaces)
                tempo_spaces = []
            else:
                counter += 1
                data.append(i)

        deciph = list(CriptoText(self.rkey, 
                                 CriptoText("0","0").letterify(img_obj.retrive_cipher(data))).readable_ciph(False))
        nested = []

        for i in spaces:
            temp_l = []
            for x in i:
                temp = []
                temp += [deciph.pop(0) for n in range(x)]
                temp_l.append("".join(temp))
            nested.append(temp_l)

        return nested

class ML_Encrip:
    """Encryps and decryps texts with multiple lines
    """
    def __init__(self,rkey:str,mess:str,name:str):
        self.rkey = rkey
        self.mess = mess
        self.name = name

    def create_img(self):
        """creates the pixels and saves the image

        Returns:
            list: array of pixels
        """
        splited = self.mess.split("\n")
        splited = [x for x in splited if x!=""]
        blocks = [len(x) for x in splited]
        img_obj = TextToImg(self.rkey,"".join(splited),"x")
        pixel_basic = img_obj.create_pixels()
        new_pixels = []
        counter =()
        for line in blocks:
            new_pixels += [pixel_basic.pop(0) for x in range(line)]
            new_pixels.append((254,254,254))

        img_obj.save_img(new_pixels,self.name)
        
        return [new_pixels, img_obj.size_calc(len(new_pixels))]
    
    def deciph_img(self):
        """deciphs the image 

        Returns:
            list: list of deciphered lines
        """
        img_obj = TextToImg(self.rkey,"x",self.name)

        spaces,data = [],[]
        counter = 0
        for i in img_obj.pull_colors():
            if i == (254,254,254):
                spaces.append(counter)
                counter=0
            else:
                counter+=1
                data.append(i)

        deciph = list(CriptoText(self.rkey, 
                                 CriptoText("0","0").letterify(img_obj.retrive_cipher(data))).readable_ciph(False))
        lines = []
        for i in spaces:
            lines.append("".join([deciph.pop(0) for n in range(i)]))

        return lines