
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import requests
import os
import progressbar
from PIL import Image

def seletor():
    type_selector = input('Selecione um elemento(id, classe):\n').lower()

    if type_selector == 'id':
        print('[INFO]: Selecionando elemento pelo id...\n')
    elif type_selector == 'class':
        print('[INFO]: Selecionando elemento pela classe...\n')
    else:
        print('[ERRO]: Elemento inválido. Por favor, digite "id" ou "class".\n')
        return selector()
    
    return tipo_seletor

def Append_Directory():
    i = 1
    while True:
        name = f'Images {i}'
        if not os.path.exists(name):
            os.makedirs(name)
            return name
        i += 1

def show_menu():
    print('Comandos:\n\n')
    
    print('=====================================================================================================================================\n')
    print('Image_Downloader:\n')
    print('Digite o endereco do site')
    print('Selecione o modo de funcionamento do programa por id ou classe.')
    print('Digite o nome da classe ou id selecionado, lembrando, para pegar o ID/classe de um site, basta ir no seu navegador e apertar CTRL + I')
    print('E pronto, as imagens serão baixadas automaticamente!\n')
    print('=====================================================================================================================================\n')


def init():

    show_menu()
    url = input('URL: ')
    type_selector = selector()
    selector_name = input('Nome do elemento(classe/id):')
    print('\n')
    os.system('cls')
    Output = criar_pasta_destino()
    url = f'{url}'
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', {f'{tipo_seletor}': f'{nome_seletor}'})
    if div is None:
        print('[ERRO]: Elemento não encontrado!\n')
        input('Pressione qualquer tecla para continuar')
        os.system('cls')
        return init()
    imgs = div.find_all('img')
    widgets = ['Download: ', progressbar.Percentage(), progressbar.Bar(marker='#', left='[', right=']')]
    bar = progressbar.ProgressBar(maxval=len(imgs), widgets=widgets)
    bar.start()

    for i, imagem in enumerate(imgs):
        try:
            src = imagem.get('src')

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(src, headers=headers, stream=True)

            content_type = response.headers.get('content-type')

            if 'image' not in content_type:
                print(f'[ERRO]:{i}. O elemento selecionado não é uma imagem.')
                continue

            nome_arquivo, tipo_arquivo = os.path.splitext(os.path.basename(src))
            imagem_pil = Image.open(response.raw)
            imagem_pil = imagem_pil.convert('RGB')
            nome_arquivo = f'Imagem {i}.png'
            imagem_pil.save(os.path.join(pasta_saida, nome_arquivo), 'PNG')

        except Exception as e:
            print(f'\nNão foi possível baixar a imagem {i}: {e}')
        bar.update(i+1)

    bar.finish()

    print('\nDownloads concluídos com sucesso!\n')
    resposta = input('Deseja sair? (y/n): ').lower()
    if resposta == 'y':
        os.system('cls')
        return init()
    else:
        print('\nExit...\n')

if __name__ == '__main__':
    init()
    input('Pressione qualquer tecla para sair')
