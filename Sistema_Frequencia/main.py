from sistema_reconhecimento_facial import SistemaReconhecimentoFacial
from cadastro_rostos import CadastroRostos

def main():
    print("Escolha uma opção:")
    print("1. Iniciar sistema de presença")
    print("2. Cadastrar novo rosto por imagem")
    print("3. Cadastrar novo rosto ao vivo")
    escolha = input("Digite sua escolha: ")

    sr_facial = SistemaReconhecimentoFacial()
    cadastro_rostos = CadastroRostos()

    if escolha == '1':
        sr_facial.capturar_video()
    elif escolha == '2':
        caminho_imagem = input("Digite o caminho para a imagem: ")
        nome = input("Digite o nome da pessoa: ")
        cadastro_rostos.cadastrar_rosto_por_imagem(caminho_imagem, nome)
    elif escolha == '3':
        nome = input("Digite o nome da pessoa: ")
        cadastro_rostos.cadastrar_rosto_ao_vivo(nome)
    else:
        print("Escolha inválida")

if __name__ == "__main__":
    main()
