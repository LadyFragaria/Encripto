import os
import eel
from encripting.file_admin import FileAdmin, ciph

print("Iniciando")

eel.init("web")

f = FileAdmin(os.getcwd())

#┎୨♡୧┈┈┈┈ non exposed works ┈┈┈┈୨♡୧┒
def button_maker(txt, onclick, classi=False, idi=False):
    return f"""<button {f"class='{classi}'" if classi!=False else ""} {f"id='{idi}'" if idi!=False else ""} {f"onclick='{onclick}'"}> {txt} </button>"""

def simple_cover(fill, tag):
    return f"<{tag}>" + fill + f"</{tag}>"

def form_table(listy):
    html = ""
    treated = [[simple_cover(i,"th") for i in listy.pop(0)]]
    for i in listy:
        treated.append([simple_cover(x,"td") for x in i])
    for i in treated:
        html += simple_cover("".join(i),"tr")
    return simple_cover(html,"table")

#┎୨♡୧┈┈┈┈ testing ┈┈┈┈୨♡୧┒
@eel.expose
def testing_pyfunc():
    print("Conectado")

#┎୨♡୧┈┈┈┈ create menus ┈┈┈┈୨♡୧┒
@eel.expose
def form_profiles():
    html = ""

    for i in f.pull_profiles():
        html += button_maker(i,f'charge_profile("{i}")')

    return html

@eel.expose
def charge_profile(profile):
    data = f.profile_data(profile)

    html = f"<h2 id='profile_name'>{profile}</h2>"
    if data[0]:
        html += '<p>Todo listo</p>' + button_maker("Borrar perfil",'showdiv("del_prof_menu")') + '<div class="file_menus"> <div class="file_menu"> <h3>Texto</h3><div class="buttoner">'

        for i in data[1]:
            html += button_maker(i,f'read_pt("{i}")')

        html += button_maker("+",'showdiv("pt_writer")') + '</div></div> <div class="file_menu"> <h3>Tablas</h3><div class="buttoner">'

        for i in data[2]:
            html += button_maker(i,f'read_bd("{i}")')

        html += button_maker("+",'showdiv("bd_writer")') + '</div></div> <div class="file_menu"> <h3>Texto multilinea</h3><div class="buttoner">'

        for i in data[3]:
            html += button_maker(i,f'read_ml("{i}")')

        html +=  button_maker("+",'showdiv("ml_writer")') +"</div></div></div>"

    else:
        html += "<p>No se encontro test, por favor escribe la contraseña y despues presiona el boton solucionar</p>" + button_maker("Solucionar",f'create_test()')

    return html

@eel.expose
def create_test(profile,pass_w):
    try:
        f.create_test_file(profile,pass_w)
        return "Archivo creado"
    except:
            return "<p>Se presento un problema</p>"

@eel.expose
def create_bd_wb(cols,rows,fname):
    if cols != "" and rows != "" and fname != "":
        listi = [["#"]+[str(i+1) for i in range(int(cols))]]
        for i in range(int(rows)):
            listi.append( [simple_cover(f"{i+1}","p")]+ [f'<input type="text" id="cell{i}_{x}"' for x in range(int(cols))])
        listi = form_table(listi)
        return listi + button_maker("Guardar",f'save_bd({cols},{rows},"{fname}")') 
    return simple_cover("Debes rellenar todos los datos correctamente","p")

#┎୨♡୧┈┈┈┈ read works ┈┈┈┈୨♡୧┒
@eel.expose
def read_pt(profile,pass_w,file):
    if f.check_passw(profile,pass_w):
        return f'<h3 id="file_name">txt_{file}</h3>' + simple_cover(f.read_pt(profile,file,pass_w),"p")
    else:
        return "<p> Contraseña incorrecta </p>"

@eel.expose
def read_bd(profile,pass_w,file):
    if f.check_passw(profile,pass_w):
        return f'<h3 id="file_name">bds_{file}</h3>' + form_table(f.read_bd(profile,file,pass_w))
    else:
        return "<p> Contraseña incorrecta </p>"
    
@eel.expose
def read_ml(profile,pass_w,file):
    if f.check_passw(profile,pass_w):
        mess = [f"{simple_cover(i,'p')}" for i in f.read_ml(profile,file,pass_w)]
        return   f'<h3 id="file_name">tml_{file}</h3>' + "".join(mess)
    else:
        return "<p> Contraseña incorrecta </p>"

#┎୨♡୧┈┈┈┈ save works ┈┈┈┈୨♡୧┒
@eel.expose
def save_profile(profile,pass_w):
    if profile in f.pull_profiles():
        return "<p>Este perfil ya existe</p>"
    else:
        f.create_profile(profile,pass_w)
        return "<p>Perfil creado</p>"

@eel.expose
def save_pt(profile,pass_w,file,mess):
    if f.check_passw(profile,pass_w):
        try:
            f.save_pt(profile,file,pass_w,mess)
            return "<p>Archivo guardado</p>"
        except:
            return "<p>Se presento un problema</p>"
    else:
        return "<p> Contraseña incorrecta </p>"
    
@eel.expose
def save_bd(profile,pass_w,file,mess):
    if f.check_passw(profile,pass_w):
        try:
            f.save_bd(profile,file,pass_w,mess)
            return "<p>Archivo guardado</p>"
        except:
            return "<p>Se presento un problema</p>"
    else:
        return "<p> Contraseña incorrecta </p>"
    
@eel.expose
def save_ml(profile,pass_w,file,mess):
    if f.check_passw(profile,pass_w):
        try:
            f.save_ml(profile,file,pass_w,mess)
            return "<p>Archivo guardado</p>"
        except:
            return "<p>Se presento un problema</p>"
    else:
        return "<p> Contraseña incorrecta </p>"

#┎୨♡୧┈┈┈┈ delete works ┈┈┈┈୨♡୧┒
@eel.expose
def del_prof(profile,pass_w):
    if f.check_passw(profile,pass_w):
        try:
            f.del_prof(profile)
            return "<p>Perfil eliminado</p>"
        except:
            return "<p>Se presento un problema</p>"
    else:
        return "<p> Contraseña incorrecta </p>"

@eel.expose 
def del_file(profile,file,pass_w):
    if f.check_passw(profile,pass_w):
        try:
            f.del_file(profile,file)
            return f"<p>Archivo {file} eliminado</p>"
        except:
            return "<p>Se presento un problema</p>"
    else:
        return "<p> Contraseña incorrecta </p>"

@eel.expose
def ciph_text(rkey,mess):

    return ciph(rkey,mess.replace("\n",""),True)

@eel.expose
def deciph_text(rkey,mess):
    return ciph(rkey,mess,False)

eel.start("home.html")