from tkinter import *
from tkinter import ttk, messagebox
from pymongo import MongoClient

APP = MongoClient(host="localhost", port=27017)
db = APP["PROJETPYMONGO"]
mycollection = db["Production"]

def Affiche():
    tree.delete(*tree.get_children())
    result = mycollection.find()
    for x in result:
        tree.insert(
            "",
            "end",
            values=(
                x["CodeEntreprise"],
                x["nomRegion"],
                x["nombreEmploye"],
                x["Production"],
                x["Performance"],
            ),
        )

def calculer_production_et_performance():
    region = combo_region.get()
    nombre = entry_nombre.get()
    if nombre.isdigit():
        nombre = int(nombre)
        production_par_employe = {"DT": 17, "SM": 35, "TH": 52}.get(region, 0)
        production = production_par_employe * nombre

        if production > 10000:
            performance = "Excellente"
        elif 500 <= production <= 10000:
            performance = "Acceptable"
        else:
            performance = "Insuffisante"

        entry_production.config(state=NORMAL)
        entry_production.delete(0, END)
        entry_production.insert(0, str(production))
        entry_production.config(state="readonly")

        entry_performance.config(state=NORMAL)
        entry_performance.delete(0, END)
        entry_performance.insert(0, performance)
        entry_performance.config(state="readonly")
    else:
        entry_production.config(state=NORMAL)
        entry_production.delete(0, END)
        entry_production.config(state="readonly")
        entry_performance.config(state=NORMAL)
        entry_performance.delete(0, END)
        entry_performance.config(state="readonly")

def ajouter():
    code = entry_code.get()
    region = combo_region.get()
    nombre = entry_nombre.get()
    production = entry_production.get()
    performance = entry_performance.get()

    if code and region and nombre and production and performance:
        try:
            nombre = int(nombre)
            production = int(production)

            productiondata = {
                "CodeEntreprise": code,
                "nomRegion": region,
                "nombreEmploye": nombre,
                "Production": production,
                "Performance": performance,
            }

            mycollection.insert_one(productiondata)
            tree.insert("", "end", values=(code, region, nombre, production, performance))
            effacer_champs()
            messagebox.showinfo("Succès", "Données ajoutées avec succès.")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide pour le nombre d'employés et la production.")
    else:
        messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")

def supprime():
    pro = tree.selection()
    if pro:
        code = tree.item(pro, "values")[0]
        confirmation = messagebox.askyesno("Confirmation", "Voulez-vous supprimer cette production ?")
        if confirmation:
            result = mycollection.delete_one({"CodeEntreprise": code})
            if result.deleted_count > 0:
                tree.delete(pro)
                messagebox.showinfo("Succès", "Donnée supprimée avec succès.")
            else:
                messagebox.showerror("Erreur", "Aucune donnée trouvée avec ce code.")
    else:
        messagebox.showwarning("Attention", "Veuillez sélectionner une ligne à supprimer.")

def effacer_champs():
    entry_code.delete(0, END)
    entry_nombre.delete(0, END)
    combo_region.set("")
    entry_production.config(state=NORMAL)
    entry_production.delete(0, END)
    entry_production.config(state="readonly")
    entry_performance.config(state=NORMAL)
    entry_performance.delete(0, END)
    entry_performance.config(state="readonly")

def confirmer():
    confirmation = messagebox.askyesno("Confirmation", "Voulez-vous vraiment quitter ?")
    if confirmation:
        fenetre.quit()

fenetre = Tk()
fenetre.title("Gestion de la Production")
fenetre.geometry("800x500")
fenetre.config(bg="lightgray")

frame_region = LabelFrame(fenetre, text="Sélectionner la Région", padx=10, pady=10, bg="white")
frame_region.pack(fill="x", padx=20, pady=10)

Label(frame_region, text="Région :", bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
combo_region = ttk.Combobox(frame_region, values=["DT", "SM", "TH"], state="readonly", width=15)
combo_region.grid(row=0, column=1, padx=10, pady=5)

frame_info = LabelFrame(fenetre, text="Information Production", padx=10, pady=10, bg="white")
frame_info.pack(fill="x", padx=20, pady=10)

Label(frame_info, text="Code Entreprise :", bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_code = Entry(frame_info, width=20)
entry_code.grid(row=0, column=1, padx=10, pady=5)

Label(frame_info, text="Nombre Employé :", bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_nombre = Entry(frame_info, width=20)
entry_nombre.grid(row=1, column=1, padx=10, pady=5)

Label(frame_info, text="Production :", bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_production = Entry(frame_info, width=20, state="readonly")
entry_production.grid(row=2, column=1, padx=10, pady=5)

Label(frame_info, text="Performance :", bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_performance = Entry(frame_info, width=20, state="readonly")
entry_performance.grid(row=3, column=1, padx=10, pady=5)

btn_ajouter = Button(frame_info, text="Ajouter", command=ajouter, bg="lightgreen")
btn_ajouter.grid(row=4, column=0, padx=10, pady=10)

btn_supprimer = Button(frame_info, text="Supprimer", command=supprime, bg="tomato")
btn_supprimer.grid(row=4, column=1, padx=10, pady=10)

btn_quitter = Button(frame_info, text="Quitter", bg="lightgray", command=confirmer)
btn_quitter.grid(row=4, column=2, padx=10, pady=10)

entry_nombre.bind("<KeyRelease>", lambda event: calculer_production_et_performance())
combo_region.bind("<<ComboboxSelected>>", lambda event: calculer_production_et_performance())

frame_tableau = Frame(fenetre)
frame_tableau.pack(fill="both", expand=True, padx=20, pady=10)

colonnes = ("Code", "Région", "Nombre Employé", "Production", "Performance")
tree = ttk.Treeview(frame_tableau, columns=colonnes, show="headings")
tree.pack(side="left", fill="both", expand=True)

for col in colonnes:
    tree.heading(col, text=col)
    tree.column(col, width=100)

scrollbar = Scrollbar(frame_tableau, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.config(yscrollcommand=scrollbar.set)

Affiche()

fenetre.mainloop()
