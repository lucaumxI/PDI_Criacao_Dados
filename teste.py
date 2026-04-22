# arquivo: teste.py
import numpy as np
from PIL import Image

# Importa funções específicas do arquivo pipeline.py
from main import equalizacaoHistograma


def testar_funcao_individual():
    # Carrega uma única imagem para teste
    img_original = np.array(Image.open("Imagens/Abyssinian_96.jpg"))
    # Testa apenas a função gamma
    img_resultado = equalizacaoHistograma(img_original)
    
    # Exibe o resultado na tela (útil para testes rápidos)
    Image.fromarray(img_resultado).show()
    
    # Ou salva se preferir ver o arquivo
    Image.fromarray(img_resultado).save("teste_saida1.png")

if __name__ == "__main__":
    testar_funcao_individual()