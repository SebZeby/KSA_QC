import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from datetime import date
import os

################################# PARAMETRES #################################

res_previewX = int(400)             #resolution de la fenetre de preview
res_previewY = int(res_previewX*9/16)

################################# CLASSES ET FONCTIONS #################################

class FluxVideos: 
    
    def __init__(self,index_cam, resolution_X, resolution_Y):
        self.tmp = cv2.VideoCapture(int(index_cam))                   #creation de l'objet flux vidéo
        self.tmp.set(cv2.CAP_PROP_FRAME_WIDTH, resolution_X)     # Largeur de la résolution
        self.tmp.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution_Y)    # Hauteur de la résolution
    def read(self):
        return self.tmp.read()
    def release(self):
        self.tmp.release()
    def isOpened(self):
        return self.tmp.isOpened()

def update(flux_video, label_preview, legende):  # Ajoutez les paramètres flux_video et label_preview
    ret, frame = flux_video.read()
    if ret:
        img =cv2.putText(frame,text=str(legende), org=(10,40), fontFace=cv2.FONT_HERSHEY_COMPLEX,fontScale=1, color=(0,0,255),thickness=2)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)

        ctk_img = ctk.CTkImage(light_image=img,size=(res_previewX, res_previewY))

        label_preview.configure(image=ctk_img)

    Screen.after(1, update, flux_video, label_preview, legende)  # Passez les paramètres pour la prochaine exécution de la fonction update. un delai trop bas = lag de ouf et lenteur au demarrage

def save_photo(source,nom_vue):                               #fonction prise de photo
    OF = tb_OF.get()
    No_Pce = tb_No_Pce.get()

    folder_name = "archives"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    nom_photo = f"{folder_name}/{date.today()} OF-01-{OF}_{No_Pce} {nom_vue}.png"

    ret, frame=source.read()
    if ret:
        cv2.imwrite(nom_photo,frame)
        print("Photo enregistrée")
    else:
        print("Photo non enregistrée")

################################# ACTIONS BOUTONS #################################
def bt_save_click():

    save_photo(top_view, "top")
    #save_photo(secondary_view,"secondary")
    tb_No_Pce.delete(0,'end')

################################# SETUP INTERFACE #################################

##### CREATION DES WIDGETS #####

Screen =ctk.CTk()
Screen.title('Kugler QC')

titre = ctk.CTkLabel(
    Screen,
    text="Archivage photos qualité",
    font=ctk.CTkFont(size=30,weight='bold')
    )
titre.pack(padx=10,pady=(40,20))

frm_input = ctk.CTkFrame(Screen)

frm_previews = ctk.CTkFrame(Screen)

tb_OF = ctk.CTkEntry(frm_input,placeholder_text="12345.1",font=ctk.CTkFont(size=20,weight='bold'),width=100,justify='center')
tb_No_Pce = ctk.CTkEntry(frm_input,placeholder_text="00",font=ctk.CTkFont(size=20,weight='bold'),width=40,justify='center')
lbl_OF = ctk.CTkLabel(frm_input,text="OF-01-",font=ctk.CTkFont(size=20,weight='bold'))
lbl_tiret =ctk.CTkLabel(frm_input,text="-",font=ctk.CTkFont(size=20,weight='bold'))

btn_Save_Images = ctk.CTkButton(
    Screen,
    text="Enregistrer les photos",
    font=ctk.CTkFont(size=20,weight='normal'),
    command=bt_save_click
    )

preview1 = ctk.CTkLabel(frm_previews,text="")                                                      #Init du retour video 1
preview2 = ctk.CTkLabel(frm_previews,text="")
preview3 = ctk.CTkLabel(frm_previews,text="")

##### PLACEMENTS DES WIDGETS #####

frm_input.pack(padx=10,pady=10)
btn_Save_Images.pack()
frm_previews.pack(padx=10,pady=10)

lbl_OF.pack(side=ctk.LEFT)
tb_OF.pack(side=ctk.LEFT)
lbl_tiret.pack(side=ctk.LEFT)
tb_No_Pce.pack(side=ctk.LEFT)

preview1.pack(padx=10,pady=10,side=ctk.LEFT)
preview2.pack(padx=10,pady=10,side=ctk.LEFT)
preview3.pack(padx=10,pady=10,side=ctk.LEFT)

################################# SETUP DES INPUTS #################################

top_view = FluxVideos(0, 1920, 1080)
#secondary_view = FluxVideos(0, 1920, 1080)
#third_view = FluxVideos(0, 1920, 1080)

################################# START DES BOUCLES ET GUI #################################


update(top_view,preview1,"top view")
update(top_view,preview2,"secondary view")
#update(top_view,preview3,"third view")

Screen.mainloop()

top_view.release()
#secondary_view.release()
#third_view.release()

print("Cameras liberées - Fin de programme")