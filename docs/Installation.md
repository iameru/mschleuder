
Zur Installation braucht es als Mindestanforderungen ein __aktuelles Linuxbetriebssystem__, `python (ver 3.7+)`, `git` und `pip` sowie `python3-venv` sowie `pango` fürs pdf erstellen.

## Installation


install zbsp:

```bash
sudo apt install -y git python3 python3-venv python3-pip libpangocairo-1.0-0
git clone https://github.com/iameru/mschleuder # download the tool
cd mschleuder # navigate inside the downloaded

# When bash is available
chmod +x ./install.sh
./install.sh
```


## Start

### Aus dem Ordner

```bash
source venv/bin/activate
gunicorn -w 2 "ms:create_app()"
```
### Mit systemd

bearbeite die Datei `mschleuder.service` (gegebenenfalls frag um hilfe wenn du nicht weisst was du eintragen sollst)
dann:

```bash
cp mschleuder.service /etc/systemd/system/mschleuder.service
```


## Updates

Die `möhrenschleuder` plant im "CI" verfahren konstant Updates erhalten zu können. Das heisst ihr könnt euch, solltet ihr euch selber um das Tool kümmern, einfach per `pull` von `main` das neueste verfügbare Update ziehen. Es ist wichtig dabei die Datenbank migrationen laufen zu lassen falls sich strukturell etwas am Code geändert hat!

beispiel bei systemd nutzung (ihr seid im Ordner, also `mschleuder` nach obiger Installation):

```bash
sudo systemctl stop mschleuder.service # möhrenschleuder anhalten
git pull # die neue version ziehen
source venv/bin/activate # in virtual environment gehen
flask db upgrade # Eventuelle datenbankmigrationen starten
sudo systemctl start mschleuder.service # möhrenschleuder wieder starten
```

## Brauchst du Hilfe?

Melde dich gerne bei mir falls Interesse besteht und wir können einen Termin machen bei dem ich dir dabei helfe das Tool zu [installieren, zu nutzen oder ob es für dich taugt](Zukunft.md)
