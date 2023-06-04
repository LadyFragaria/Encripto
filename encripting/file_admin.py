# ─────────█▄██▄█─────────        V 1.0        ─────────█▄██▄█─────────
# █▄█▄█▄█▄█▐█┼██▌█▄█▄█▄█▄█ App de encriptacion █▄█▄█▄█▄█▐██┼█▌█▄█▄█▄█▄█
# ███┼█████▐████▌█████┼███  Manejo de archivos ███┼█████▐████▌█████┼███
# █████████▐████▌█████████   de Fragaria DEV   █████████▐████▌█████████
"""File managing for the Encripto desktop app
"""


#┎୨♡୧┈┈┈┈ imports ┈┈┈┈୨♡୧┒
import os
from encripting.cripto_works import CriptoText, PT_Encrip, DB_Encrip, ML_Encrip, random_str
from random import choice, randint

class FileAdmin:
    def __init__(self,wd:str):
        self.bf = os.path.join(wd,"work_files")
        self.quotes = ["Pack my box with five dozen liquor jugs",
                       "Jackdaws love my big sphinx of quartz",
                       "The five boxing wizards jump quickly",
                       "How quickly daft jumping zebras vex!",
                       "Sphinx of black quartz, judge my vow",
                       "Glib jocks quiz nymph to vex dwarf",
                       "Waltz, bad nymph, for quick jigs vex"]
        if not os.path.exists(self.bf):
            os.makedirs(self.bf)

    #┎୨♡୧┈┈┈┈ pull data ┈┈┈┈୨♡୧┒
    def profile_data(self,profile:str):
        sub_files = [x[:-4] for x in os.listdir(os.path.join(self.bf,profile)) if ".png" in x]

        return [True if "test" in sub_files else False,
                [x[4:] for x in sub_files if x[:4] == "txt_"],
                [x[4:] for x in sub_files if x[:4] == "bds_"], 
                [x[4:] for x in sub_files if x[:4] == "tml_"]]

    def pull_profiles(self):
        return [x for x in os.listdir(self.bf) if "." not in x]
    
    def get_file(self,profile:str,file:str):
        return os.path.join(self.bf,profile,f"{file}.png")
    
    #┎୨♡୧┈┈┈┈ create works ┈┈┈┈୨♡୧┒
    def create_test_file(self, profile:str, pass_w:str):
        secret = choice(self.quotes)
        diff = 49 - len(secret)
        fill,cut = random_str(diff), randint(0,diff-1)
        p = PT_Encrip(pass_w, fill[:cut] + secret + fill[cut:], 
                      self.get_file(os.path.join(self.bf,profile),"test"))
        p.create_img()

    def create_profile(self, profile:str, pass_w:str):
        new_folder = os.path.join(self.bf,profile)
        if os.path.exists(new_folder):
            return True
        os.mkdir(new_folder)
        self.create_test_file(profile, pass_w)

    def check_passw(self,profile:str,pass_w:str):
        secret = PT_Encrip(pass_w, "x", self.get_file(profile,"test")).deciph_img()
        
        for i in self.quotes:
            if i in secret:
                return True
        return False
    
    #┎୨♡୧┈┈┈┈ write works ┈┈┈┈୨♡୧┒

    def check_name_dispo(self, profile:str, name:str,num:int):
        taken_names= self.profile_data(profile)[num]
        if name not in taken_names:
            return name
        
        counter=1
        corr_name = name

        while corr_name == name:
            if f"{name}_{counter}" in taken_names:
                counter += 1
            else:
                corr_name= f"{corr_name}_{counter}"
                return corr_name


    def save_pt(self,profile:str, name:str, pass_w:str, mess:str):
        PT_Encrip(pass_w, mess, 
                  self.get_file(profile, f"txt_{self.check_name_dispo(profile,name,1)}")).create_img()

    def save_bd(self,profile:str, name:str, pass_w:str, mess:str):
        DB_Encrip(pass_w, mess, 
                  self.get_file(profile, f"bds_{self.check_name_dispo(profile,name,2)}")).create_img()

    def save_ml(self,profile:str, name:str, pass_w:str, mess:str):
        ML_Encrip(pass_w, mess, 
                  self.get_file(profile, f"tml_{self.check_name_dispo(profile,name,3)}")).create_img()

    #┎୨♡୧┈┈┈┈ read works ┈┈┈┈୨♡୧┒
    def read_pt(self,profile:str, name:str, pass_w:str):
        return PT_Encrip(pass_w, " ", self.get_file(profile, f"txt_{name}")).deciph_img()

    def read_bd(self,profile:str, name:str, pass_w:str):
        return DB_Encrip(pass_w, " ", self.get_file(profile, f"bds_{name}")).deciph_img()
    
    def read_ml(self,profile:str, name:str, pass_w:str):
        return ML_Encrip(pass_w, " ", self.get_file(profile, f"tml_{name}")).deciph_img()
    
    #┎୨♡୧┈┈┈┈ delete works ┈┈┈┈୨♡୧┒
    def del_prof(self,profile:str):
        data = self.profile_data(profile)
        names = [f"txt_{i}" for i in data[1]]+ [f"bds_{i}" for i in data[2]]
        if data[0]:
            names.append("test")
        for i in names:
            path = self.get_file(profile,i)
            if os.path.isfile(path):
                os.remove(path)

        os.rmdir(os.path.join(self.bf,profile))

    def del_file(self,profile,file):
        path = self.get_file(profile, file)
        if os.path.isfile(path):
                os.remove(path)

def ciph(rkey,mess,tipe):
        return CriptoText(rkey,mess).readable_ciph(tipe)