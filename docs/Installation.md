
Zur Installation braucht es als Mindestanforderungen ein __aktuelles Linuxbetriebssystem__, `python (ver 3.7+)`, `git` und `pip` sowie `python3-venv`.

install:
```bash
sudo apt install -y git python3 python3-venv python3-pip
git clone https://github.com/iameru/mschleuder # download the tool
cd mschleuder/ # navigate inside the downloaded

# When bash is available
chmod +x ./install.sh
./install.sh
```


## Weiterbetrieb des Tools

start des tools danach aus dem Ordner

```bash
source venv/bin/activate
gunicorn -w 2 "ms:create_app()"
```

> noch nicht dokumentiert:
> gunicorn kann auch per systemd gestartet werden was die bevorzugte variante wäre

### Updates

Die `möhrenschleuder` plant im "CI" verfahren konstant Updates erhalten zu können. Das heisst ihr könnt euch, solltet ihr euch selber um das Tool kümmern, einfach per `pull` von `main` das neueste verfügbare Update ziehen. Es ist wichtig dabei die Datenbank migrationen laufen zu lassen falls sich strukturell etwas am Code geändert hat!

beispiel (ihr seid im Ordner, also `mschleuder` nach obiger Installation):
```bash
# gunicorn abbrechen ! (noch nicht dokumentiert)
git pull
flask db upgrade
# gunicorn wieder starten !
```

#### Brauchst du Hilfe?

Melde dich gerne bei mir falls Interesse besteht und wir können einen Termin machen bei dem ich dir dabei helfe das Tool zu [installieren, zu nutzen oder ob es für dich taugt](Zukunft.md)
