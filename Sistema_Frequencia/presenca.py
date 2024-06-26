import datetime

class Presenca:
    def __init__(self):
        self.arquivo_presenca = 'presenca.csv'

    def registrar_presenca(self, nome):
        with open(self.arquivo_presenca, "a") as f:
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{nome},{timestamp}\n")
