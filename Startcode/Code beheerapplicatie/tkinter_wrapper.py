import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Scherm:
    def __init__(self, titel, breedte, hoogte):
        """
        Initialiseren van het hoofdvenster van de GUI.
        
        Parameters:
        - titel (str): De titel van het venster.
        - breedte (int): De breedte van het venster in pixels.
        - hoogte (int): De hoogte van het venster in pixels.
        """
        self.root = tk.Tk()
        self.root.title(titel)
        self.root.geometry(f"{breedte}x{hoogte}")
        self.tabellen = {}    

    def voeg_tekst_toe(self, tekst, x, y):
        """
        Voegt een tekstlabel toe aan het hoofdvenster.
        
        Parameters:
        - tekst (str): De tekst die op het label moet verschijnen.
        - x (int): De x-positie in het venster.
        - y (int): De y-positie in het venster.
        """
        label = tk.Label(self.root, text=tekst)
        label.place(x=x, y=y)

    def voeg_invoerveld_toe(self, x, y):
        """
        Voegt een invoerveld toe aan het hoofdvenster en geeft ingevulde waarde in het veld terug
        
        Parameters:
        - x (int): De x-positie in het venster.
        - y (int): De y-positie in het venster.
        
        Returns:
        - tk.StringVar: Ingevulde waarde in het invoerveld.
        """
        invoerveld_var = tk.StringVar()
        invoerveld = tk.Entry(self.root, textvariable=invoerveld_var)
        invoerveld.place(x=x, y=y)
        return invoerveld_var

    def voeg_knop_toe(self, tekst, x, y, functie):
        """
        Voegt een knop toe aan het hoofdvenster.
        
        Parameters:
        - tekst (str): De tekst die op de knop moet verschijnen.
        - x (int): De x-positie in het venster.
        - y (int): De y-positie in het venster.
        - functie (callable): De functie die aangeroepen wordt wanneer de knop wordt ingedrukt.
        """
        knop = tk.Button(self.root, text=tekst, command=functie)
        knop.place(x=x, y=y)


    def voeg_nieuwe_voorziening_knop_toe(self, tekst, x, y, voorziening_attributen, opslaan_callback):
        """
        Voegt een gespecialiseerde knop toe die een dialoogvenster opent voor het toevoegen van voorzieningen.
        
        Parameters:
        - tekst (str): De tekst die op de knop moet verschijnen.
        - x (int): De x-positie in het venster.
        - y (int): De y-positie in het venster.
        - voorziening_attributen (list): Een lijst met informatie over de attributen van de nieuwe voorziening.
        - opslaan_callback (callable): De functie die aangeroepen wordt om de gegevens op te slaan.
        """
        knop = tk.Button(self.root, text=tekst, command=lambda: self.open_bewerk_toevoeg_scherm(voorziening_attributen, tekst, opslaan_callback, bewerk_callback=None))
        knop.place(x=x, y=y)
    
    def open_bewerk_toevoeg_scherm(self, voorziening_attributen, titel, toevoeg_callback, bewerk_callback, rij=None):
        """
        Opent een dialoogvenster voor het toevoegen of bewerken van een voorziening.
        
        Parameters:
            voorziening_attributen (list): Lijst van attributen van de voorziening.
            titel (str): Titel van het dialoogvenster.
            toevoeg_callback (function): Callback-functie voor het toevoegen van een voorziening.
            bewerk_callback (function): Callback-functie voor het bewerken van een voorziening.
            rij (list, optional): Bestaande waarden van de voorziening (voor bewerken).
        """

        dialoog_window = tk.Toplevel(self.root)
        dialoog_window.title("Voorziening bewerken" if rij is not None else titel)

        variabelen = {}

        for i, attribuut in enumerate(voorziening_attributen):
            naam = attribuut['naam']
            datatype = attribuut['type']
            is_verplicht = attribuut.get('verplicht', False)
            label_tekst = f"{naam} {'*' if is_verplicht else ''}"
            bestaande_waarde = self._format_value(rij[i], datatype) if rij is not None else ""
            
            # Toon veld alleen als voorziening bewerkt wordt of het veld niet readonly is.
            if (rij is not None or not attribuut.get('read-only', False)) :
                label = tk.Label(dialoog_window, text=label_tekst)
                label.grid(row=i, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
            
                # Voeg velden toe 
                if datatype == "boolean":
                    self._maak_radiobuttons(dialoog_window, i, naam, bestaande_waarde, variabelen)
                elif datatype == "options":
                    self._maak_dropdown(dialoog_window, i, naam, attribuut["opties"], bestaande_waarde, variabelen)
                else:
                    self._maak_inputveld(dialoog_window, i, naam, attribuut, bestaande_waarde, variabelen)

        # Actieknop voor bewerken of toevoegen
        if rij is not None:
            actie_button = tk.Button(dialoog_window, text="Bewerken", command=lambda: self.attractie_opslaan(dialoog_window, voorziening_attributen, variabelen, bewerk_callback))
        else:
            actie_button = tk.Button(dialoog_window, text="Toevoegen", command=lambda: self.attractie_opslaan(dialoog_window, voorziening_attributen, variabelen, toevoeg_callback))
        actie_button.grid(row=len(voorziening_attributen), column=0, columnspan=2, padx=5, pady=5,sticky=tk.E+tk.W)
        
        # Annuleerknop
        annuleren_button = tk.Button(dialoog_window, text="Annuleren", command=dialoog_window.destroy)
        annuleren_button.grid(row=len(voorziening_attributen), column=2, columnspan=2, padx=5, pady=5, sticky=tk.E+tk.W)
        dialoog_window.grab_set()

    def _maak_radiobuttons(self, window, rij, naam, waarde, variabelen):
        """
        Maakt radioknoppen voor boolean-waarden.
        
        Parameters:
            window (tk.Toplevel): Het dialoogvenster waarin de radioknoppen worden gemaakt.
            rij (int): De rij in de grid waar de radioknoppen moeten worden geplaatst.
            naam (str): De naam van het attribuut.
            waarde (str): De huidige waarde van het attribuut.
            variabelen (dict): Dictionary waarin de variabelen worden opgeslagen.
        """

        var = tk.BooleanVar(window, value=(waarde == "Ja"))
        tk.Radiobutton(window, text="Ja", variable=var, value=True).grid(row=rij, column=2, padx=5, pady=5)
        tk.Radiobutton(window, text="Nee", variable=var, value=False).grid(row=rij, column=3, padx=5, pady=5)
        variabelen[naam] = var

    def _maak_dropdown(self, window, rij, naam, opties, waarde, variabelen):
        """
        Maakt een dropdown-menu voor selectie opties.
        
        Parameters:
            window (tk.Toplevel): Het dialoogvenster waarin de dropdown wordt gemaakt.
            rij (int): De rij in de grid waar de dropdown moet worden geplaatst.
            naam (str): De naam van het attribuut.
            opties (dict): De beschikbare opties.
            waarde (str): De huidige waarde van het attribuut.
            variabelen (dict): Dictionary waarin de variabelen worden opgeslagen.
        """
        var = tk.StringVar(window, value=waarde)
        ttk.Combobox(window, textvariable=var, values=opties, state="readonly").grid(row=rij, column=2, columnspan=2, padx=5, pady=5)
        variabelen[naam] = var

    def _maak_inputveld(self, window, rij, naam, attribuut, waarde, variabelen): 
        """
        Maakt een invoerveld voor tekst-, int- en float-waarden.
        
        Parameters:
            window (tk.Toplevel): Het dialoogvenster waarin het invoerveld wordt gemaakt.
            rij (int): De rij in de grid waar het invoerveld moet worden geplaatst.
            naam (str): De naam van het attribuut.
            attribuut (dict): Het attribuut met de configuratie voor het invoerveld.
            waarde (str): De huidige waarde van het attribuut.
            variabelen (dict): Dictionary waarin de gemaakte variabelen worden opgeslagen.
        """
        tekst = tk.StringVar(window, value=waarde)
        entry = tk.Entry(window, textvariable=tekst, state="readonly" if attribuut.get('read-only', False) else "normal")
        entry.grid(row=rij, column=2, columnspan=2, padx=5, pady=5)
        if attribuut["type"] in ["int", "float"]:
             # controleer of het een geldig nummer is.
            entry.config(validate='key', validatecommand=(window.register(self._is_geldig_nummer), '%P'))
        variabelen[naam] = entry

    def attractie_opslaan(self, window, voorziening_attributen, variabelen, callback):
        """
        Slaat de ingevoerde waarden op en roept de callback-functie aan.
        
        Parameters:
            window (tk.Toplevel): Het dialoogvenster dat moet worden gesloten na het opslaan.
            voorziening_attributen (list): Lijst van attributen van de voorziening.
            variabelen (dict): De ingevoerde waarden
            callback (function): Callback-functie die wordt aangeroepen met de ingevoerde waarden.
        """
        gewijzigde_waarden = {}
        fouten_gevonden = False

        for attribuut in voorziening_attributen:
            kolom_naam = attribuut['naam']
            widget = variabelen.get(kolom_naam, None)
            if widget is not None:
                nieuwe_waarde = widget.get() if widget.get() != "" else None
                gewijzigde_waarden[kolom_naam] = nieuwe_waarde
                
                # check of verplichte velden zijn ingevuld
                if attribuut.get('verplicht', False) and nieuwe_waarde is None:
                    fouten_gevonden = True
                    window.update()
                    messagebox.showerror("Verplicht veld", f"Het veld '{kolom_naam}' is verplicht en mag niet leeg zijn.", parent=window )
                    break

        if not fouten_gevonden:
            window.destroy()
            callback(gewijzigde_waarden)

    def voeg_tabel_toe(self, titel, kolom_namen, rijen, x, y, breedte, hoogte, bewerk_callback=None, verwijder_callback=None):
        """
        Voegt een nieuwe tabel toe aan het hoofdvenster.
        
        Parameters:
            titel (str): De titel van de tabel.
            kolom_namen (list): Lijst van kolomnamen.
            rijen (list): Lijst van rijen met gegevens.
            x (int): De x-coördinaat voor de plaatsing van de tabel.
            y (int): De y-coördinaat voor de plaatsing van de tabel.
            breedte (int): De breedte van de tabel.
            hoogte (int): De hoogte van de tabel.
            bewerk_callback (function, optional): Callback-functie voor het bewerken van een rij.
            verwijder_callback (function, optional): Callback-functie voor het verwijderen van een rij.
        """
        titel_label = tk.Label(self.root, text=titel + ":", font=("Arial", 14))
        titel_label.place(x=x, y=y)

        return self._maak_tabel(titel, kolom_namen, rijen, x,y, breedte, hoogte, bewerk_callback, verwijder_callback)

       
    def _maak_tabel(self, titel, voorziening_attributen, rijen, x, y, breedte, hoogte, bewerk_callback=None, verwijder_callback=None):
        """
        Maakt een tabel met gegeven attributen en rijen.
        
        Parameters:
            titel (str): De titel van de tabel.
            voorziening_attributen (list): Lijst van attributen van de voorziening.
            rijen (list): Lijst van rijen met gegevens.
            x (int): De x-coördinaat voor de plaatsing van de tabel.
            y (int): De y-coördinaat voor de plaatsing van de tabel.
            breedte (int): De breedte van de tabel.
            hoogte (int): De hoogte van de tabel.
            bewerk_callback (function, optional): Callback-functie voor het bewerken van een rij.
            verwijder_callback (function, optional): Callback-functie voor het verwijderen van een rij.
        """
        # maak de tabel scrollbare
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        tabel = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=tabel, anchor='nw')

        tabel.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.bind("<MouseWheel>", on_mousewheel)
        tabel.bind("<MouseWheel>", on_mousewheel)
        
        canvas.place(x=x, y=y + 30, width=breedte, height=hoogte)  
        scrollbar.place(x=x + breedte, y=y + 30, height=hoogte)
        
        tabel.titel = titel
        
        self.tabellen[tabel] = {
            "kolom_namen" : voorziening_attributen,
            "x" : x,
            "y" : y,
            "breedte": breedte,
            "hoogte": hoogte,
            "bewerk_callback" : bewerk_callback,
            "verwijder_callback" : verwijder_callback
        }
        

        # Rijen
        if rijen is None:
            self.voeg_tekst_toe(f"Er zijn geen {titel.lower()} gevonden", x, y+30)
        else :
            for i, kolom in enumerate(voorziening_attributen):
                kolom_naam = kolom["naam"]
                label = tk.Label(tabel, text=kolom_naam, relief=tk.RIDGE)
                label.grid(row=0, column=i, sticky="nsew")

            for i, rij in enumerate(rijen):
                for j, item in enumerate(rij):
                    item = self._format_value(item, voorziening_attributen[j]['type'])
                    label = tk.Label(tabel, text=item, relief=tk.RIDGE)
                    label.grid(row=i+1, column=j, sticky="nsew")
                    label.bind("<MouseWheel>", on_mousewheel)  # Zorg ervoor dat elk label ook scrollt


                # Bewerk knop
                if bewerk_callback:
                    bewerk_button = tk.Button(tabel, text="Bewerk", command=lambda row=rij: self.open_bewerk_toevoeg_scherm(voorziening_attributen, titel=None, toevoeg_callback=None, bewerk_callback= bewerk_callback, rij=row))
                    bewerk_button.grid(row=i+1, column=len(voorziening_attributen), sticky="nsew")

                # Verwijder knop
                if verwijder_callback:
                    verwijder_button = tk.Button(tabel, text="Verwijder", command=lambda row=i: self.verwijder_rij(tabel, voorziening_attributen, row, verwijder_callback))
                    verwijder_button.grid(row=i+1, column=len(voorziening_attributen)+1, sticky="nsew")
        
        return tabel

    def verwijder_rij(self, tabel, kolom_namen, rij_index, verwijder_callback):
        """
        Verwijdert een rij uit de tabel en roept de verwijder_callback aan met de verwijderde voorziening.
        
        Parameters:
            tabel (ttk.Frame): De tabel waaruit de rij verwijderd wordt.
            kolom_namen (list): Lijst van kolomnamen.
            rij_index (int): De index van de rij die verwijderd moet worden.
            verwijder_callback (function): Callback-functie die wordt aangeroepen met de verwijderde verzoening en de rij-index.
        """
        verwijderde_waarden = {}
        for i, kolom in enumerate(kolom_namen):
            kolom_naam = kolom['naam']  
            nieuwe_waarde = tabel.grid_slaves(row=rij_index+1, column=i)[0].cget("text")
            verwijderde_waarden[kolom_naam] = nieuwe_waarde

        verwijder_callback(verwijderde_waarden, rij_index)


    def herlaad_tabel(self, tabel, rijen):
        """
        Herlaadt de tabel met nieuwe rijen.
        
        Parameters:
            tabel (ttk.Frame): De tabel die herladen wordt.
            rijen (list): Lijst van nieuwe rijen met gegevens.
        """
        for tabel1 in list(self.tabellen.keys()):
            if tabel1.titel == tabel.titel:
                tabel_info = self.tabellen[tabel1]
                del self.tabellen[tabel1]
                tabel1.destroy()
                self._maak_tabel(tabel1.titel, tabel_info["kolom_namen"], rijen, tabel_info["x"], 
                                    tabel_info["y"], tabel_info["breedte"], tabel_info["hoogte"], tabel_info["bewerk_callback"], tabel_info["verwijder_callback"])


    def voeg_filters_toe(self, filter_options, start_x, start_y, maximale_breedte, callback):
        """
        Voegt filteropties toe aan het hoofdvenster.
        
        Parameters:
            filter_options (dict): Een dictionary met filternamen en opties.
            start_x (int): De start x-coördinaat voor de filters.
            start_y (int): De start y-coördinaat voor de filters.
            maximale_breedte (int): De maximale breedte beschikbaar voor de filters.
            callback (function): Callback-functie die wordt aangeroepen met de geselecteerde filterwaarden.
        """
        x, y = start_x, start_y
        max_height = 0
        filters = {}
        
        for naam, opties in filter_options.items():
            label = tk.Label(self.root, text=f"{naam}:")
            label_width = label.winfo_reqwidth()
            combo_var = tk.StringVar()
            combo = ttk.Combobox(self.root, textvariable=combo_var, values=opties, width=15)
            combo_width = combo.winfo_reqwidth() + 20 
            
            if x + label_width + combo_width > start_x + maximale_breedte:
                x = start_x  
                y += max_height + 5  
                max_height = 0
            
            label.place(x=x, y=y)
            combo.place(x=x + label_width + 5, y=y)  
            
            x += label_width + combo_width + 5
            
            max_height = max(max_height, label.winfo_reqheight(), combo.winfo_reqheight())
            filters[naam] = combo_var

            
        button_width = 100
        if x + button_width <= start_x + maximale_breedte:
            button_x = x + 5
        else:
            button_x = start_x
            y += max_height + 5
        
        # Plaats de filter knop
        filter_button = tk.Button(self.root, text="Filter toepassen", command=lambda: callback({k: (v.get() == "Ja") if v.get() in ["Ja", "Nee"] else v.get() for k, v in filters.items() if v.get()}))
        filter_button.place(x=button_x, y=y-3)

    def toon_vraag_ja_nee_venster(self, titel, bericht):
        """
        Toont een dialoogvenster met een Ja/Nee vraag.
        
        Parameters:
            titel (str): De titel van het dialoogvenster.
            bericht (str): Het bericht in het dialoogvenster.
        
        Returns:
            bool: True als de gebruiker 'Ja' heeft gekozen, anders False.
        """
        return messagebox.askyesno(titel, bericht)
    
    def toon_informatie_bericht(self, titel, bericht):
        """
        Toont een informatie dialoogvenster.
        
        Parameters:
            titel (str): De titel van het dialoogvenster.
            bericht (str): Het bericht in het dialoogvenster.
        """
        messagebox.showinfo(titel, bericht)

    def toon_fout_bericht(self, titel, bericht):
        """
        Toont een foutmelding dialoogvenster.
        
        Parameters:
            titel (str): De titel van het dialoogvenster.
            bericht (str): Het bericht in het dialoogvenster.
        """
        messagebox.showerror(titel, bericht)
    
    def open(self):
        """
        Open de GUI
        """
        self.root.mainloop()

    # *** Hulp functies ***
    def _format_value(self, item, type):
        """
        Formateert een boolean van 0/1 naar de tekst "Ja"/"Nee"
        
        Parameters:
            item (any): De waarde om te formatteren.
            type (str): Het datatype van de waarde.
        
        Returns:
            any: De geformatteerde waarde.
        """
        if type == "boolean":
            if item == 0:
                return "Nee"
            else: 
                return "Ja"
        return item
    
    def _is_geldig_nummer(self, P):
        """
        Controleert of de gegeven string een geldig nummer is.
        
        Parameters:
            P (str): De te controleren string.
        
        Returns:
            bool: True als het een geldig nummer is, anders False.
        """
        if P== "" or P.isdigit() or (P.startswith('-') and P[1:].isdigit()): 
            return True
        try:
            float(P)
            return True
        except ValueError:
            return False