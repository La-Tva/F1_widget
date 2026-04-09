# 🏎️ F1 Widget

Affiche les infos Formule 1 en barre en haut de ton écran Windows!

## ⚡ Installation Rapide (30 secondes)

1. **Télécharge** → [F1-Widget.exe (Latest Release)](../../releases)
2. **Double-clique** sur le fichier
3. **Voilà!** 🚀 La barre apparaît en haut

Aucune installation requise. Fonctionne directement!

## 🎯 Features

✅ Compte à rebours jusqu'à la prochaine course  
✅ Podium du dernier GP (🥇 🥈 🥉)  
✅ Leader Championnat Pilotes (WDC)  
✅ Leader Championnat Constructeurs (WCC)  
✅ Mise à jour toutes les 10 minutes  
✅ Auto-start Windows (optionnel)  

## 🎨 À quoi ça ressemble

```
[NEXT: JAPAN (SUZUKA) @ 14:00 FR | 10D 02H 15M 30S] [🥇 RUSSELL] [🥈 LECLERC] [🥉 HAMILTON] [WDC: RUSSELL (51 PTS)] [WCC: FERRARI (120 PTS)]
```

## 🛠️ Détails Techniques

- **Langage** : Python 3.11
- **Build** : PyInstaller 6.19
- **Taille** : 10.75 MB
- **Dépendances** : requests, tkinter (incluses)
- **OS** : Windows 10+

## ⚙️ Utilisation

### Clic Droit sur la Barre

```
⚙️ Toggle Auto-start   → Lancer au démarrage
❌ Quitter            → Fermer le widget
```

### Auto-Start

Pour lancer le widget automatiquement au démarrage :
1. Lance le widget
2. Clic-droit sur la barre
3. Clique "Toggle Auto-start"

Pour désactiver :
- Même process ou
- Supprime `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run\F1MenubarTicker` (Regedit)

## 🔒 Sécurité

✅ **Code source 100% visible** - Lire [f1_widget.pyw](f1_widget.pyw)  
✅ **Pas de virus** - PyInstaller officiel  
✅ **Pas de tracking** - Zéro données personnelles  
✅ **Pas de téléchargements** - Fonctionne standalone  

[Voir la documentation sécurité complète](SECURITE_ET_CONFIANCE.md)

## 📊 Data Source

Les données proviennent de l'**API Ergast F1** (publique, opensource)
- https://api.jolpi.ca/ergast/f1/

Mise à jour toutes les 10 minutes.

## 🐛 Problèmes?

### "Windows Defender avertit"
```
C'est normal pour les .exe auto-créés.
Clique "Plus d'infos" → "Exécuter quand même"
```

### "Mon antivirus détecte un virus"
```
Faux positif courant (PyInstaller ressemble à du malware).
Ajoute le fichier à la whitelist.
```

### "Ça ne s'affiche pas"
```
1. Vérifies que Windows 10+ est installé
2. Redémarre la barre (tâche du gestionnaire)
3. Laisse 10 minutes pour la mise à jour API
```

## 🛎️ Dev

Si tu veux le compiler toi-même :

```bash
# Prérequis : Python 3.9+
pip install pyinstaller requests

# Build
pyinstaller --onefile --name "F1-Widget" f1_widget.pyw

# Résultat : dist/F1-Widget.exe
```

## 📝 License

MIT - Utilise, modifie, partage librement!

## 🙏 Crédits

- **Data** : API Ergast F1
- **Build** : PyInstaller
- **Framework** : Python + Tkinter

---

**Questions?** Crée une [Issue](../../issues) sur GitHub!

**Like?** ⭐ Star le repo! 

---

Dernière mise à jour : 9 Avril 2026  
Status : ✅ Production
