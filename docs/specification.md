# Spezifikation


## Das Tool

Die **Möhrenschleuder** ist ein Werkzeug für Solidarische Landwirtschaften oder ähnlich organisierte Betriebe die ihre Produkte in Stück/Gewicht an eine oder mehrere Verteilstationen mit halben oder ganzen Anteilen der Mitglieder verteilen.

Wichtigste Kernfunktion ist das Verteilen von Produkten.

Dann folgen in der Wichtigkeit, nicht unbedingt in der Reihenfolge:

 - Speichern der Verteilung
 - Generierung von Lieferschienen für eine Verteilung
 - Erstellung von Statistik zur Erntemenge / Stationsverläufe / ...

### / landingpage

Auf der landingpage wird ein kurzüberblick für Nutzer:Innen über die letzte Verteilung geboten. In "zukunft" könnte dort auch ein überblick für alle Mitglieder entstehen, frei zugänglich.

### /settings Einstellungen

Hier können `logo`, `kopfzeile` und `fußzeile` für die Lieferscheine geändert werden sowie `Einheiten` angelegt, geändert und gelöscht werden. **Einheiten** sind notwendige bestandteile von *Produkten*. Einheiten kann es in stück (zbsp Bund, Stück, Kisten) oder in Gewicht (zbsp Gramm, Kilo, Pfund) geben.
Einheitsänderungen werden für die Statistik archiviert.

### /stations Stationen

In der Stationsansicht können Stationen angelegt, geändert, gelöscht werden.
Stationen haben dabei `halbe` und `ganze` Anteile, eine `info` für Adressen/Kontakte beim ausliefern und natürlich einen `namen`. Es gibt auch eine `ordnungsnummer` für stationen (siehe [/distribute Verteilen](#/distribute Verteilen) ).
Bei jeder Änderung wird die Station, wie sie vorher war, für die Statistik archiviert.

### /products Gemüse

In der Produktübersicht können Produkte angelegt, geändert, gelöscht werden.
Produkte haben dabei einen `Namen`, eine oder mehrere `Einheiten` in denen sie verteilt werden, eine `info` für kurze Informationen zum Produkt sowie ein `zuletzt verteilt` feld.
Produktänderungen werden *nicht* für die Statistik archiviert.

Eine Verteilung eines produkts wird hier gestartet durch klick auf das Produkt gelangt man in die *Verteil Detail Seite* des Produkts.

### /history History

In der Historyübersicht gibt es eine Übersicht über vergangene Verteilungen und Lieferscheine.
In zukunft: Es gibt hier auch **Statistiken** zu sehen über den Verlauf von produkten, zum beispiel der Ernte/Verteilmenge von Paprika von Jahr 2021 bis Jahr 2023 Kalenderwoche 13.
Es wird in "zukunft" hier auch eine einfachere Möglichkeit eines kompletten Datenexportes geben.

### /distribute Verteilen

In der Verteilübersicht gibt es Infos zur aktuell gestarteten Verteilung, ähnlich einem Warenkorb beim onlineshopping.

### /distribute/produkt Verteil Detail Seite

Die Detailseite ist die Seite auf der Produkte verteilt werden. Hier kann die Verteilung gestartet werden nachdem eine *Erntemenge* eingegeben wurde.
Es gibt dazu Knöpfe, die die einzelnen Anteile für die halben anteile auf *gleich, halb oder nix* setzen.
Wenn die Verteilung in *Stück* geschieht, kann der Rest verteilt werden. Geschieht die verteilung in *Gewicht* wird einfach geteilt.
Auf der Seite sind die Stationen in ihrer `Ordnungsnummer` geordnet für ein einfacheres Verteilen im Lager.

Es wird **Spezialfälle** geben die selten aber eben manchmal eintreten.
 - es gibt die möglichkeit selber händisch zu verteilen (zbsp bei extrem geringen Produktmengen die nicht sinnvoll verteilbar sind sonst)
 - es gibt die möglichkeit das gleiche Produkt für die selbe Verteilung nochmal zu verteilen, mit anderen Werten. Damit wird der Fall abgedeckt, dass plötzlich nochmal ein schon verteiltes produkt auftaucht.

Die verteilung kann dann gespeichert werden und wird im `Lieferschein` sowie in der `Statistik` verwendet.

### /harvest Mengenrechner

Es soll einen Mengenrechner geben. Mit dem kann recht einfach die Menge des Produkts errechnet werden anhand eines Verteilwunsches. Die Seite ist eine umgekehrter Verteil Detail Seite die Anhand der Stationen und der gewünschten Verteilmenge, zbsp 4 Stück für die ganzen, 2 für die halben Anteile, die Gesamtmenge berechnet. Bei der tatsächlichen Verteilung und zur Berücksichtigung im `Lieferschein` und der `Statistik` **muss** dann dennoch die *Verteil Detail Seite* nochmal genutzt werden!
