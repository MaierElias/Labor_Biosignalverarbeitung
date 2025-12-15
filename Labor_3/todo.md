# Vorbereitung
Messelektroden sollten einen Abstand von 2 cm von Elektrodenmitte zu Elektrodenmitte aufweisen
entlang des Muskels auf dem Muskelbauch
Referenzelektrode sollte wie bei der Elektrokardiografie an einem sehr knöchernen Körperteil mit wenig Muskelaktivität

http://www.seniam.org/ -> Recommendations → Sensor Locations

http://www.velamed.com/wp-content/uploads/EMG-FIBEL-V1.1.pdf

Gleicher Code wie beim Elektrokardiografie

# 12 bit ADC Anschließen
1.- Verbinden Sie das vierfache Kabel (schwarz/rot/weiß/gelb) mit dem EMG/EKG-Sensor

2.- Anstelle der direkten Verbindung der Jumper-Kabel, werden diese nun in den ADC über Schraubklemmen befestigt. Rot ist mit VCC, schwarz mit GND und gelb mit A0 zu verbinden und mit einem Schraubenzieher festzuziehen (siehe Abbildung 1.3).

3.- Den ADC über ein Qwiic Kabel mit dem Mikrocontroller verbinden

4.- Installieren Sie nun folgende Bibliothek in der Arduino IDE: SparkFun ADS1015 Arduino Library

5.- Öffnen Sie nun über Datei → Beispiele → SparkFun ADS1015 Arduino Library → Example1 ReadBasic den Code und laden Sie diesen auf den Mikrocontroller. Ändern Sie den analogen Kanal im Code auf A0 - dort wird bisher A3 verwendet .

6.- Öffnen Sie den seriellen Plotter und sehen Sie sich die neuen Messdaten an.

von 80 auf 300 Schritte

Achtung: Für alle Experimente sollten Sie mindestens 1-2 Sekunden vor und nach der geplanten Muskelkontraktion eine Pause einlegen und den Muskel nicht anspannen. Dadurch können Sie bei der Analyse Ihrer Daten besser die Zeitpunkte der Kontraktion identifizieren.

# Experiment 1
Bei der Messung soll der Muskel zu 100 % angespannt werden. Die Messung für die MVC muss wiederholt werden, sobald die Elektroden neu angebracht wurden.

1. Bauen Sie die gesamte Hardware auf und laden Sie den Code Lab3Code1 auf Ihren Mikrocontroller

2. Starten Sie das Python-Skript serialReadEMG.ipynb

3. Greifen Sie z.B. den Tisch mit Ihrer Hand, während der Oberarmvertikal und der Unterarm um 90° gebeugt ist. Versuchen Sie den Tisch hochzuheben, ohne dabei den Winkel von 90° zu verändern (Lassen Sie Ihre Kommilitonen auf dem Tisch sitzen, falls der Tisch sich dabei bewegen sollte). Führen Sie dieses Heben für etwa 5 Sekunden aus, wobei Sie mit maximaler Kraft heben möchten. Versuchen Sie dabei die Kabel so wenig wie möglich zu bewegen.

4. Machen Sie eine Pause von mindestens 60 Sekunden und wieder holen Sie den Versuch weitere zwei Male, um drei Datensätze für die MVC zu erhalten. Benennen Sie diese ordentlich (MVC1,…).

# Experiment 2: Relative Muskelaktivität
In diesem Experiment werden Sie ähnlich zum Experiment 1 vorgehen, jedoch mit drei verschiedenen Gewichten, welche bei etwa 25 %, 50 % und 75 % liegen des MVC liegen sollten. Suchen Sie sich also drei unterschiedliche Gewichte und dokumentieren Sie diese. Nutzen Sie folgende Vorgehensweise:

1. Starten Sie das Python-Skript serialReadEMG.ipynb

2. Halten Sie das leichteste Gewicht in derselben Position wie in Experiment 1 (90° Winkel)für 10 Sekunden

3. Machen Sie eine Pause von mind. 40 Sekunden und wiederholen Sie die Messung mit dem mittleren und schweren Gewicht. Benennen Sie diese ordentlich (Weight1,…).

# Experiment 3: Ermüdung
In diesem Experiment werden Sie eine Ermüdung des Muskels messen, indem Sie ein ähnliches Setup wie in Experiment 1 verwenden. Gehen Sie folgendermaßen vor:

1. Gehen Sie zurück zum Tisch, welchen Sie zum heben verwendet haben

2. Starten Sie das Python-Skript serialReadEMG.ipynb.

3. Messen Sie die maximale Kontraktion (so stark wie möglich!) über volle 10-15 Sekunden.

4. Machen Sie eine Pause von mind. 60 Sekunden und wiederholen Sie die Messung zweimal, sodass Sie drei Datensätze der Ermüdung erhalten. Benennen Sie diese ordentlich (Fatigue1,…).


# Notizen
- Daten die der Code ausgibt ist ungefilter!
- Lab3Function führt 3 Daten zusammen -> Variablennamen müssen dafür stimmen