import tkinter as tk
import requests
from datetime import datetime, timezone
import threading
import ctypes
from ctypes import wintypes
import time
import os
import sys
import winreg
from pathlib import Path

# --- COULEURS OFFICIELLES ---
# Tu peux ajuster ces codes hexadécimaux pour qu'ils correspondent parfaitement à tes attentes
TEAM_COLORS = {
    "mercedes": "#27F4D2",
    "red_bull": "#3671C6",
    "ferrari": "#E80020",
    "mclaren": "#FF8000",
    "aston_martin": "#229971",
    "alpine": "#0093CC",
    "williams": "#64C4FF",
    "rb": "#6692FF",
    "sauber": "#52E252",
    "haas": "#B6BABD",
    "audi": "#F50537"
}

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# --- CONSTANTES APPBAR WINDOWS ---
ABM_NEW = 0
ABM_REMOVE = 1
ABM_QUERYPOS = 2
ABM_SETPOS = 3
ABE_TOP = 1
ABE_BOTTOM = 3

class APPBARDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.UINT),
        ("hWnd", wintypes.HWND),
        ("uCallbackMessage", wintypes.UINT),
        ("uEdge", wintypes.UINT),
        ("rc", wintypes.RECT),
        ("lParam", wintypes.LPARAM),
    ]

def setup_appbar(hwnd, bar_height):
    """Configure la fenêtre comme une AppBar (Taskbar-like) au dessus de l'écran"""
    try:
        screen_w = ctypes.windll.user32.GetSystemMetrics(0)  # Largeur d'écran
        
        abd = APPBARDATA()
        abd.cbSize = ctypes.sizeof(APPBARDATA)
        abd.hWnd = hwnd
        abd.uEdge = ABE_TOP  # Placer en haut
        abd.rc.top = 0
        abd.rc.left = 0
        abd.rc.right = screen_w
        abd.rc.bottom = bar_height
        
        # Retirer toute AppBar existante
        ctypes.windll.shell32.SHAppBarMessage(ABM_REMOVE, ctypes.byref(abd))
        time.sleep(0.2)
        
        # Ajouter comme nouvelle AppBar
        ctypes.windll.shell32.SHAppBarMessage(ABM_NEW, ctypes.byref(abd))
        
        # Demander la position
        ctypes.windll.shell32.SHAppBarMessage(ABM_QUERYPOS, ctypes.byref(abd))
        
        # Définir la position
        ctypes.windll.shell32.SHAppBarMessage(ABM_SETPOS, ctypes.byref(abd))
        
        print(f"✓ AppBar configurée en haut de l'écran ({screen_w}x{bar_height})")
        return True
    except Exception as e:
        print(f"✗ Erreur lors de la configuration AppBar: {e}")
        return False


# --- GESTION AUTO-START WINDOWS ---
def get_executable_path():
    """Obtient le chemin du programme exécutable (Python ou PyInstaller .exe)"""
    if getattr(sys, 'frozen', False):
        return sys.executable  # PyInstaller .exe
    else:
        return sys.executable + f' "{os.path.abspath(__file__)}"'

def enable_autostart():
    """Ajoute le programme au démarrage automatique de Windows"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                             r"Software\Microsoft\Windows\CurrentVersion\Run", 
                             0, winreg.KEY_SET_VALUE)
        exe_path = get_executable_path()
        winreg.SetValueEx(key, "F1MenubarTicker", 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
        print("✓ Auto-start activé")
        return True
    except Exception as e:
        print(f"✗ Erreur lors de l'activation auto-start: {e}")
        return False

def disable_autostart():
    """Retire le programme du démarrage automatique de Windows"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                             r"Software\Microsoft\Windows\CurrentVersion\Run", 
                             0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "F1MenubarTicker")
        winreg.CloseKey(key)
        print("✓ Auto-start désactivé")
        return True
    except FileNotFoundError:
        print("Auto-start déjà désactivé")
        return True
    except Exception as e:
        print(f"✗ Erreur lors de la désactivation auto-start: {e}")
        return False

def is_autostart_enabled():
    """Vérifie si l'auto-start est activé"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                             r"Software\Microsoft\Windows\CurrentVersion\Run", 
                             0, winreg.KEY_READ)
        winreg.QueryValueEx(key, "F1MenubarTicker")
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False


class F1MenubarTicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg='black')
        self.root.wm_attributes("-transparentcolor", "black")

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        # Hauteur de 40 pixels, modifiable si besoin
        self.bar_height = 40
        self.root.geometry(f"{self.screen_w}x{self.bar_height}+0+0")

        # Configuration AppBar (pousse les fenêtres vers le bas comme une barre Apple)
        self.root.update_idletasks()
        time.sleep(0.1)
        setup_appbar(self.root.winfo_id(), self.bar_height)

        # --- MENU CONTEXTUEL (Clic droit) ---
        self.context_menu = tk.Menu(self.root, tearoff=0, bg='#222', fg='white')
        self.context_menu.add_command(label="⚙️ Toggle Auto-start", command=self.toggle_autostart)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="❌ Quitter", command=self.root.quit)
        
        self.root.bind("<Button-3>", self.show_menu)  # Button-3 = Clic droit
        self.autostart_enabled = is_autostart_enabled()

        # --- UI WIDGETS ---
        
        # 1. CHRONO & HEURE (Gauche - Position relative symétrique)
        self.ticker_text = tk.Label(
            self.root, 
            text="🏎️ SYNC...", 
            font=("Segoe UI Variable Display", 10, "bold"), 
            fg="white", 
            bg="black"
        )
        # Positionné à 0.5 - 0.23 = 0.27
        self.ticker_text.place(relx=0.27, rely=0.5, anchor="center")

        # 2. PODIUM (Centre)
        self.podium_frame = tk.Frame(self.root, bg='black')
        self.podium_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.p1_label = tk.Label(self.podium_frame, text="", font=("Segoe UI Variable Display", 11, "bold"), fg="#FFD700", bg="black")
        self.p1_label.pack(side="left", padx=15) # Espacement interne au podium
        self.p2_label = tk.Label(self.podium_frame, text="", font=("Segoe UI Variable Display", 10, "bold"), fg="#C0C0C0", bg="black")
        self.p2_label.pack(side="left", padx=15)
        self.p3_label = tk.Label(self.podium_frame, text="", font=("Segoe UI Variable Display", 10, "bold"), fg="#CD7F32", bg="black")
        self.p3_label.pack(side="left", padx=15)

        # 3. LEADERS WDC & WCC (Droite - Position relative symétrique)
        self.leaders_frame = tk.Frame(self.root, bg='black')
        # Positionné à 0.5 + 0.23 = 0.73
        self.leaders_frame.place(relx=0.73, rely=0.5, anchor="center")

        self.wdc_label = tk.Label(self.leaders_frame, text="", font=("Segoe UI Variable Display", 10, "bold"), fg="white", bg="black")
        self.wdc_label.pack(side="left", padx=15) # Espacement entre WDC et WCC
        self.wcc_label = tk.Label(self.leaders_frame, text="", font=("Segoe UI Variable Display", 10, "bold"), fg="white", bg="black")
        self.wcc_label.pack(side="left", padx=15)

        # Initialisation des données
        self.next_gp_date = None
        self.country = ""
        
        # Lancement des mises à jour
        self.update_api_data()
        self.update_ticker()
        self.check_fullscreen_apps()
        self.root.mainloop()

    # --- FONCTIONS ---

    def check_fullscreen_apps(self):
        """Masque la barre si une application est en plein écran"""
        try:
            foreground_hwnd = ctypes.windll.user32.GetForegroundWindow()
            if foreground_hwnd and foreground_hwnd != self.root.winfo_id():
                rect = wintypes.RECT()
                ctypes.windll.user32.GetWindowRect(foreground_hwnd, ctypes.byref(rect))
                is_fs = (rect.left <= 0 and rect.top <= 0 and 
                         rect.right >= self.screen_w and rect.bottom >= self.screen_h)
                if is_fs:
                    if self.root.attributes("-topmost"):
                        self.root.attributes("-topmost", False)
                        self.root.lower()
                else:
                    if not self.root.attributes("-topmost"):
                        self.root.attributes("-topmost", True)
                        self.root.lift()
        except: pass
        self.root.after(2000, self.check_fullscreen_apps)

    def update_api_data(self):
        """Récupère les données F1 via API toutes les 10 minutes"""
        def fetch():
            try:
                print("Mise à jour des données API...")
                # A. Prochaine course (Calendrier)
                res_next = requests.get("https://api.jolpi.ca/ergast/f1/current/next.json", timeout=10)
                if res_next.status_code == 200:
                    r = res_next.json()['MRData']['RaceTable']['Races'][0]
                    # Formatage date UTC
                    self.next_gp_date = datetime.fromisoformat(f"{r['date']}T{r['time']}".replace('Z', '+00:00'))
                    self.country = r['Circuit']['Location']['country']

                # B. Dernier Podium (Résultats)
                res_last = requests.get("https://api.jolpi.ca/ergast/f1/current/last/results.json", timeout=10)
                if res_last.status_code == 200:
                    results = res_last.json()['MRData']['RaceTable']['Races'][0]['Results']
                    # Mise à jour du texte des labels du podium
                    self.root.after(0, lambda: self.p1_label.config(text=f"🥇 {results[0]['Driver']['familyName'].upper()}"))
                    self.root.after(0, lambda: self.p2_label.config(text=f"🥈 {results[1]['Driver']['familyName'].upper()}"))
                    self.root.after(0, lambda: self.p3_label.config(text=f"🥉 {results[2]['Driver']['familyName'].upper()}"))

                # C. Leader Pilote (WDC - Standings)
                res_wdc = requests.get("https://api.jolpi.ca/ergast/f1/current/driverstandings.json", timeout=10)
                if res_wdc.status_code == 200:
                    leader = res_wdc.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'][0]
                    team_id = leader['Constructors'][0]['constructorId']
                    # Couleur de l'écurie
                    color = TEAM_COLORS.get(team_id, "white")
                    txt = f"WDC: {leader['Driver']['familyName'].upper()} ({leader['points']} PTS)"
                    self.root.after(0, lambda c=color, t=txt: self.wdc_label.config(text=t, fg=c))

                # D. Leader Constructeur (WCC - Standings)
                res_wcc = requests.get("https://api.jolpi.ca/ergast/f1/current/constructorstandings.json", timeout=10)
                if res_wcc.status_code == 200:
                    wcc_leader = res_wcc.json()['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings'][0]
                    team_name = wcc_leader['Constructor']['name'].upper()
                    team_pts = wcc_leader['points']
                    team_id = wcc_leader['Constructor']['constructorId']
                    # Couleur de l'écurie
                    color = TEAM_COLORS.get(team_id, "white")
                    txt = f"WCC: {team_name} ({team_pts} PTS)"
                    self.root.after(0, lambda c=color, t=txt: self.wcc_label.config(text=t, fg=c))
                
                print("Données API mises à jour avec succès.")

            except Exception as e: print(f"Erreur lors de la récupération des données API: {e}")
            # Relancer la requête dans 10 minutes (600 secondes)
            threading.Timer(600, fetch).start()
        
        # Lancer la première requête dans un thread séparé pour ne pas figer l'UI
        threading.Thread(target=fetch, daemon=True).start()

    def update_ticker(self):
        """Met à jour le chronométrage (toutes les secondes)"""
        if self.next_gp_date:
            # Calcul du temps restant (différence UTC)
            diff = self.next_gp_date - datetime.now(timezone.utc)
            
            # Conversion en heure locale française pour l'affichage de l'heure de la course
            # astimezone() sans argument utilise le fuseau horaire du système (ton PC)
            heure_fr = self.next_gp_date.astimezone().strftime("%H:%M")

            if diff.total_seconds() > 0:
                # Formatage du compte à rebours
                d = diff.days
                h, rem = divmod(diff.seconds, 3600)
                m, s = divmod(rem, 60)
                # Texte final : Pays @ Heure_FR FR | JoursD HeuresH MinutesM SecondesS
                txt = f"NEXT: {self.country.upper()} @ {heure_fr} FR | {d}D {h:02d}H {m:02d}M {s:02d}S"
                self.ticker_text.config(text=txt)
            else:
                # Affichage pendant la course
                self.ticker_text.config(text=f"🏎️ {self.country.upper()} : RACE IN PROGRESS !")
        
        # Rappeler cette fonction dans 1 seconde
        self.root.after(1000, self.update_ticker)

    def show_menu(self, event):
        """Affiche le menu contextuel au clic droit"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def toggle_autostart(self):
        """Bascule l'auto-start"""
        if self.autostart_enabled:
            disable_autostart()
            self.autostart_enabled = False
        else:
            enable_autostart()
            self.autostart_enabled = True

if __name__ == "__main__":
    F1MenubarTicker()   