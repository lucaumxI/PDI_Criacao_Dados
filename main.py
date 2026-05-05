"""Aumento de dados de imagens em escala de cinza.

Este script lê imagens de entrada em Imagens/, aplica transformações
aleatórias e salva imagens sintéticas em imagens_sinteticas/.

Transformações disponíveis:
- gamma com 0 < gamma < 1
- gamma com 1 < gamma < 10
- equalização de histograma
- suavização gaussiana
- translação
- rotação
"""

import numpy as np
from pathlib import Path
from PIL import Image

rng = np.random.default_rng()
qntImagens = 0

def aumentoDados(imagem, output_dir):
    global qntImagens
    qntImagens += 1

    num = np.random.randint(0, 6)

    match num:
        case 0:
            img = gamma(imagem, 0.001, 0.999)
        case 1:
            img = gamma(imagem, np.nextafter(1.0, 10.0), 10.0)
        case 2:
            img = equalizacaoHistograma(imagem)
        case 3:
            img = suavizacaoGaussiana(imagem)
        case 4:
            img = translacao(imagem)
        case 5:
            img = rotacao(imagem)

    imagem_salvar = Image.fromarray(img)
    imagem_salvar.save(output_dir / f"{qntImagens}.png")

def gamma(imagem, low, high):
    """Aplica transformação gama à imagem.

    low e high definem o intervalo de gamma a ser sorteado.
    """
    gamma_value = rng.uniform(low, high)
    c = 255 / (255 ** gamma_value)

    # usa numpy pra fazer a operação gamma
    img_gamma = c * (imagem.astype(float) ** gamma_value)

    # Garante que os valores não ultrapassem os limites do uint8
    img_gamma = np.clip(img_gamma, 0, 255).astype(np.uint8)

    return img_gamma.astype(np.uint8)
    
    
def equalizacaoHistograma(imagem):
    """Realiza equalização de histograma em uma imagem em escala de cinza.

    O método calcula o histograma dos níveis de intensidade, normaliza a
    distribuição cumulativa e aplica a transformação para redistribuir
    intensidades de forma mais uniforme.
    """
    bins = range(0, 257)
    hist, bins = np.histogram(imagem, bins)    # Calcula quantos pixels possuem cada nível de intensidade

    # Calcula a transformação para cada nível de intensidade
    mn = sum(hist)
    c = 255.0 / mn                         # O valor de (L-1)/MN
    out_intensity = np.zeros(256)
    for k in range(256):
        sum_vals = 0
        for j in range(0, k + 1):
            sum_vals += hist[j]
        out_intensity[k] = c * sum_vals

    # Aplica a transformação usando o mapeamento pelo histograma cumulativo
    img_eq = np.zeros(imagem.shape)
    num_rows, num_cols = imagem.shape
    for row in range(num_rows):
        for col in range(num_cols):
            img_eq[row, col] = out_intensity[imagem[row, col]]

    return img_eq.astype(np.uint8)

def suavizacaoGaussiana(imagem):
    """Aplica suavização gaussiana à imagem.

    O sigma é sorteado entre 1 e 5 e o kernel resultante é usado para
    suavizar a imagem por meio de convolução 2D.
    """
    sigma = rng.uniform(1, 5)
    radius = int(3 * sigma)
    size = 2 * radius + 1

    # Gera o kernel gaussiano normalizado
    ax = np.arange(-radius, radius + 1, dtype=float)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    kernel /= kernel.sum()

    # Aplica convolução 2D com padding reflect
    padded = np.pad(imagem, radius, mode="reflect")
    img_smooth = np.zeros_like(imagem, dtype=float)

    for row in range(imagem.shape[0]):
        for col in range(imagem.shape[1]):
            window = padded[row:row + size, col:col + size]
            img_smooth[row, col] = np.sum(window * kernel)

    return np.clip(img_smooth, 0, 255).astype(np.uint8)

def translacao(imagem):
    """Desloca a imagem horizontalmente e verticalmente.

    O deslocamento é sorteado entre -50 e 50 pixels em cada direção.
    Pixels fora do quadro são descartados e as novas áreas recebem valor zero.
    """
    deltax = rng.integers(-50, 51)
    deltay = rng.integers(-50, 51)
    num_rows, num_cols = imagem.shape
    
    img_transl = np.zeros(imagem.shape)
    for row in range(num_rows):
        for col in range(num_cols):
            y_original = row - deltay
            x_original = col - deltax
            if 0 <= y_original < num_rows and 0 <= x_original < num_cols:
                img_transl[row, col] = imagem[y_original, x_original]

    return img_transl.astype(np.uint8)

def rotacao(imagem):
    """Roda a imagem em um ângulo aleatório.
    
    O ângulo é sorteado entre -180 e 180 graus. A rotação é realizada em torno do centro da imagem, e os pixels fora
    do quadro resultante são descartados. As áreas vazias são preenchidas com valor zero.
    
    """

    angle = rng.uniform(-180, 180)  # Sorteia um ângulo entre -180 e 180 graus
    radians = np.deg2rad(angle)
    cos_angle = np.cos(radians)
    sin_angle = np.sin(radians)

    num_rows, num_cols = imagem.shape
    center_y, center_x = num_rows / 2, num_cols / 2 # Centro da imagem
    img_rot = np.zeros(imagem.shape)
    for row in range (num_rows):
        for col in range (num_cols):
            y_original = int(cos_angle * (row - center_y) + sin_angle * (col - center_x) + center_y)
            x_original = int(-sin_angle * (row - center_y) + cos_angle * (col - center_x) + center_x)
            if 0 <= y_original < num_rows and 0 <= x_original < num_cols:
                    img_rot[row, col] = imagem[y_original, x_original]

    return img_rot.astype(np.uint8)

def main():
    """Executa o pipeline de aumento de dados.

    Lê imagens de entrada de `Imagens/`, converte para escala de cinza
    e gera 10000 imagens sintéticas em `imagens_sinteticas/`.
    """
    caminho_pasta = Path("Imagens/")
    output_dir = Path("imagens_sinteticas")
    output_dir.mkdir(parents=True, exist_ok=True)

    imagens = [arquivo.resolve() for arquivo in caminho_pasta.iterdir() if arquivo.is_file()]
    if not imagens:
        raise SystemExit("Nenhuma imagem encontrada em Imagens/")

    imagens_np = [np.array(Image.open(path).convert("L")) for path in imagens]
    total = 10000

    for i in range(total):
        img = imagens_np[i % len(imagens_np)]
        aumentoDados(img, output_dir)


if __name__ == "__main__":
    main()