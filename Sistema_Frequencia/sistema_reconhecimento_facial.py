import cv2
import face_recognition
import os
import numpy as np
from presenca import Presenca

class SistemaReconhecimentoFacial:
    def __init__(self):
        self.rostos_conhecidos_encodings = []
        self.rostos_conhecidos_nomes = []
        self.rostos_conhecidos_dir = 'rostos_conhecidos'
        self.garantir_diretorio_existe(self.rostos_conhecidos_dir)
        self.carregar_rostos_conhecidos()
        self.presenca = Presenca()

    def garantir_diretorio_existe(self, diretorio):
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)

    def carregar_rostos_conhecidos(self):
        for filename in os.listdir(self.rostos_conhecidos_dir):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                image = face_recognition.load_image_file(f'{self.rostos_conhecidos_dir}/{filename}')
                face_encodings = face_recognition.face_encodings(image)
                if face_encodings:
                    face_encoding = face_encodings[0]
                    self.rostos_conhecidos_encodings.append(face_encoding)
                    self.rostos_conhecidos_nomes.append(os.path.splitext(filename)[0])

    def capturar_video(self):
        face_locations = []
        face_encodings = []
        face_names = []
        processar_este_frame = True

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Não é possível abrir a câmera")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Não é possível receber o frame (fim do stream?). Saindo ...")
                break

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            if processar_este_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(self.rostos_conhecidos_encodings, face_encoding)
                    name = "Desconhecido"

                    face_distances = face_recognition.face_distance(self.rostos_conhecidos_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.rostos_conhecidos_nomes[best_match_index]

                    face_names.append(name)

                    if name != "Desconhecido":
                        self.presenca.registrar_presenca(name)
                        print(f"Presença confirmada para {name}")
                    else:
                        print("Rosto não reconhecido")

            processar_este_frame = not processar_este_frame

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.putText(frame, "Pressione 'q' para sair", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

            cv2.imshow('Vídeo', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
