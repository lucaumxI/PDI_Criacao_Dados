# arquivo: teste.py
import numpy as np
from PIL import Image

# Importa funções específicas do arquivo pipeline.py
from main import translacao
from main import suavizacaoGaussiana


def testar_funcao_individual():
    # Carrega uma única imagem para teste
    img_original = np.array(Image.open("Imagens/Abyssinian_96.jpg"))
    # Testa apenas a função gamma
    img_resultado = translacao(img_original)
    
    # Exibe o resultado na tela (útil para testes rápidos)
    Image.fromarray(img_resultado).show()
    
    # Ou salva se preferir ver o arquivo
    Image.fromarray(img_resultado).save("teste_saida1.png")


    img_origin = np.array(Image.open("Imagens/Persian_4.jpg"))
    img_result = suavizacaoGaussiana(img_origin)
    Image.fromarray(img_result).show()
    Image.fromarray(img_result).save("teste_saida2.png")    

if __name__ == "__main__":
    testar_funcao_individual()