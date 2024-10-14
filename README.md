Wichtige Elemente des Programms:

Spieler
  Rechteck mit Tastatur-Steuerung
  Auto Jump wenn Oberflächen berührt werden

Bricks
  Werden nebeneinander und dann in Reihen übereinander Platziert, 
  ein zufälliger Offset sorgt für Variation

Ground
  Ein Rechteck am unteren Bildschirmrand

Deltatime
  dt wird berechnet um unabhängig der FPS zu programmieren.
  Jede Bewegung wird mit dt multipliziert. Je nachdem ob das Spiel schneller oder langsamer lief, wird die Geschwindigkeit entsprechend angepasst.
  Das Ergebniss ist eine gleichmäßige Bewegung

Gravitation
  

Kollision
  Komplexeste Thema des ganzen Programms
  Wenn der Spieler Boden (Ground oder Brick) berührt, bleibt er stehen (keine Gravitation)


Schüsse
  Sind Rechtecke die an der Position des SPielers erstellt werden und sich nach oben bewegen.

Sprites
  Erstelle wie gewohnt ein Rechteck und setze die Farbe auf Hintergrundfarbe damit es unsichtbar ist.
  Lade das Bild mit pygame.image.load("bild.png") und benutze pygame.transform.scale um es auf die richtige Größe zu bringen
  Zu letzt benutzt du blit zum darstellen an der richtigen Position (gleiche Position wie das Rechteck)
