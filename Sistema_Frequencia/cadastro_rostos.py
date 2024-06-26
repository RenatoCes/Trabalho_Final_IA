import cv2
import face_recognition
import os
import numpy as np

class CadastroRostos:
    def __init__(self):
        self.rostos_conhecidos_dir = 'rostos_conhecidos'
        self.garantir_diretorio_existe(self.rostos_conhecidos_dir)

    def garantir_diretorio_existe(self, diretorio):
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)

    def cadastrar_rosto_por_imagem(self, caminho_imagem, nome):
        image = face_recognition.load_image_file(caminho_imagem)
        face_encodings = face_recognition.face_encodings(image)
        if face_encodings:
            face_encoding = face_encodings[0]
            face_filename = f"{self.rostos_conhecidos_dir}/{nome}.jpg"
            cv2.imwrite(face_filename, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            print(f"Rosto registrado para {nome}")
        else:
            print("Nenhum rosto encontrado na imagem fornecida.")

    def cadastrar_rosto_ao_vivo(self, nome):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Não é possível abrir a câmera")
            return

        print("Pressione 'c' para capturar a imagem e registrar o rosto, ou 'q' para sair.")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Não é possível receber o frame (fim do stream?). Saindo ...")
                break

            cv2.putText(frame, "Pressione 'c' para capturar, 'q' para sair", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

            cv2.imshow('Vídeo', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])
                face_locations = face_recognition.face_locations(rgb_frame)
                if face_locations:
                    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                    if face_encodings:
                        face_encoding = face_encodings[0]
                        top, right, bottom, left = face_locations[0]
                        face_image = frame[top:bottom, left:right]
                        face_filename = f"{self.rostos_conhecidos_dir}/{nome}.jpg"
                        cv2.imwrite(face_filename, face_image)
                        print(f"Rosto registrado para {nome}")
                        break
                    else:
                        print("Nenhum rosto encontrado na captura ao vivo.")
                else:
                    print("Nenhum rosto encontrado na captura ao vivo.")

        cap.release()
        cv2.destroyAllWindows()
