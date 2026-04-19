import numpy as np
from pathlib import Path
from PIL import Image

rng = np.random.default_rng()
qntImagens = 0

def aumentoDados(imagem):
    global qntImagens
    qntImagens = qntImagens + 1

    num = np.random.randint(0,5)

    match num:
        case 0:
            img = gamma(imagem)
        case 1:
            img = equalizacaoHistograma(imagem)
        case 2:
            img = suavizacaoGaussiana(imagem)
        case 3:
            img = translacao(imagem)
        case 4:
            img = rotacao(imagem)

    imagem_salvar = Image.fromarray(img)
    imagem_salvar.save(f"imagens_sinteticas/{qntImagens}.png")

def gamma(imagem):
    rand = np.random.randint(0, 2)
    if rand:
        gamma = rng.random()
    else:
        gamma = rng.uniform(low=1, high=10)
   
    c = 255 / (255 ** gamma)
    
    # Vetorização: Aplica a fórmula na matriz inteira de uma vez
    img_gamma = c * (imagem.astype(float) ** gamma)
    
    # Garante que os valores não ultrapassem os limites do uint8
    img_gamma = np.clip(img_gamma, 0, 255).astype(np.uint8)
    
    # Recomendo retornar img_gamma em vez de salvar aqui
    return img_gamma
    
    
def equalizacaoHistograma(imagem):
    print("implemente o histograma")

    return imagem

def suavizacaoGaussiana(imagem):
    print("implemente a suavizacao")

    return imagem

def translacao(imagem):
    print("implemente a translacao")

    return imagem

def rotacao(imagem):
    print("implemente a rotacao")

    return imagem

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