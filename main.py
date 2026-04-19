import numpy as np
from pathlib import Path
from PIL import Image

def aumentoDados(imagem):
    num = np.random.randint(0,5)

    match num:
        case 0:
            gamma(imagem)
        case 1:
            equalizacaoHistograma(imagem)
        case 2:
            suavizacaoGaussiana(imagem)
        case 3:
            translacao(imagem)
        case 4:
            rotacao(imagem)

def gamma(imagem):
    print("implemente o gamma")

def equalizacaoHistograma(imagem):
    print("implemente o histograma")

def suavizacaoGaussiana(imagem):
    print("implemente a suavizacao")

def translacao(imagem):
    print("implemente a translacao")

def rotacao(imagem):
    print("implemente a rotacao")

def main():
    caminho_pasta = Path("Imagens/")

    # Itera sobre os itens da pasta
    for arquivo in caminho_pasta.iterdir():
        # Verifica se o item é realmente um arquivo (ignora subpastas)
        if arquivo.is_file():
            # Obtém o caminho completo/absoluto do arquivo
            caminho_completo = arquivo.resolve()
            img = np.array(Image.open(caminho_completo))
            for _ in range(9):
                aumentoDados(img)


if __name__ == "__main__":
    main()