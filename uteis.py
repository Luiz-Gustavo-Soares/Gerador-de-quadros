class Save():
    def __init__(self, nome_arquivo='arquivo.txt'):
        '''
        Inicializa a classe
        :param nome_arquivo: nome do aquivo a ser salvo (opcional)
        :return: None
        '''
        
        self.nome_arquivo = nome_arquivo
        self.lista_criacao = []
    
    def adicionar(self, item):
        '''
        Adiciona um item na lista de salvamento
        :return: None
        '''

        self.lista_criacao.append(item)
    
    def reset(self):
        '''
        Limpa a lista de salvamento
        :return: None
        '''

        self.lista_criacao = []
        
    def salvar(self):
        '''
        Salva a lista em um arquivo de texto
        :return: nome_arquivo
        '''

        with open(self.nome_arquivo, 'w') as arquivo:
            for i in self.lista_criacao:
                arquivo.write(str(i) + '\n')
        return self.nome_arquivo
