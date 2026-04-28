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
    rand = np.random.randint(0, 2)  # sorteia se o gamma sera maior ou menor que 1
    if rand:
        gamma = rng.random()
    else:
        gamma = rng.uniform(low=1, high=10)
   
    c = 255 / (255 ** gamma)
    
    # usa numpy pra fazer a operação gamma
    img_gamma = c * (imagem.astype(float) ** gamma)
    
    # Garante que os valores não ultrapassem os limites do uint8
    img_gamma = np.clip(img_gamma, 0, 255).astype(np.uint8)
    
    # Retorna a imagem para ser salva
    return img_gamma.astype(np.uint8)
    
    
def equalizacaoHistograma(imagem):  # TODO: usar numpy na equalizacao
    bins = range(0, 257)
    hist, bins = np.histogram(imagem, bins)    # Calcula quantos pixels possuem cada nível de intensidade

    # Calcula a transformação para cada nível de intensidade
    mn = sum(hist)
    c = 255./mn                           # O valor de (L-1)/MN
    out_intensity = np.zeros(256)
    for k in range(256):
        sum_vals = 0
        for j in range(0, k+1):
            sum_vals += hist[j]
        out_intensity[k] = c*sum_vals
    
    # Aplica a transformação
    img_eq = np.zeros(imagem.shape)
    num_rows, num_cols = imagem.shape
    for row in range(num_rows):
        for col in range(num_cols):
            img_eq[row, col] = out_intensity[imagem[row, col]]
    
    return img_eq.astype(np.uint8)

def suavizacaoGaussiana(imagem):
    print("implemente a suavizacao")

    return imagem

def translacao(imagem):
    deltax = rng.integers(-50, 51)
    deltay = rng.integers(-50, 51)
    num_rows, num_cols = imagem.shape
    
    img_transl = np.zeros(imagem.shape)
    for row in range(num_rows):
        for col in range(num_cols):
            y_original = row - deltay
            x_original = col - deltax
            if 0 <= y_original < num_rows and 0 <= x_original < num_cols:
                img_transl[row, col] = imagem[row - deltay, col - deltax]

    return img_transl.astype(np.uint8)

def rotacao(imagem):
    print("implemente a rotacao")

    return imagem

def main():
    caminho_pasta = Path("Imagens/")

    # Itera sobre os itens da pasta
    for arquivo in caminho_pasta.iterdir():
        # Verifica se o item é realmente um arquivo (ignora subpastas)
        if arquivo.is_file():
            # Obtém o caminho absoluto do arquivo
            caminho_completo = arquivo.resolve()
            img = np.array(Image.open(caminho_completo))
            for _ in range(9):
                aumentoDados(img)


if __name__ == "__main__":
    main()