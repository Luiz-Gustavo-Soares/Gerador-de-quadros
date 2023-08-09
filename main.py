from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from uteis import Save
from image import Image_calc


def atualizar_photos(img_o, img_p):
    '''
    Atualiza as duas fotos (original e preview) no GUI
    :param img_o: Imagem a ser colocada no quadro Original
    :param img_p: Imagem a ser colocada no quadro Preview
    :return: None 
    '''
    img_original = Image.fromarray(img_o)
    img_original = img_original.resize((200, 200))
    img_original_tk = ImageTk.PhotoImage(image=img_original)

    img_preview = Image.fromarray(img_p)
    img_preview = img_preview.resize((200, 200))
    img_preview_tk = ImageTk.PhotoImage(image=img_preview)

    figure_original.imgtk = img_original_tk
    figure_preview.imgtk = img_preview_tk
    figure_original.configure(image=img_original_tk)
    figure_preview.configure(image=img_preview_tk)


def inicial_img():
    '''
    Cria Imagens em branco para serem colocadas inicialmente nos quadros
    :return: None
    '''
    im_base = Image.new('RGB', (200, 200), color=(255, 255, 255))
    im_base.load()
    im_base = ImageTk.PhotoImage(image=im_base)
    figure_original.imgtk = im_base
    figure_preview.imgtk = im_base
    figure_original.configure(image=im_base)
    figure_preview.configure(image=im_base)


def configurar(cm, pts):
    '''
    Configura a imagem original e o numero de pontos no quadro
    :param cm: caminho da imagem
    :param pts: quantidade de pontos
    :return: None
    '''
    img_calc.ar_config(cm, int(pts))


def select_arq():
    '''
    Seleciona o arquivo de imagem original e atualiza as configuraçoes
    :return: None 
    '''
    global caminho
    cm_img = askopenfilename()

    if cm_img:
        caminho = cm_img
        resetar()
        img_o, img_p = img_calc.img_return()
        atualizar_photos(img_o, img_p)
        rodar_button.configure(state='normal')
    else:
        mensagem['text'] = 'Nenhuma imagem selecionada'
        

def callback_run():
    '''
    Callback que realiza a função de criação da segunda imagem
    :return: None
    '''
    if stop == False:
        img_o, img_p, msg = img_calc.etapa()
        mensagem['text'] = msg
        salvarTxt.adicionar(msg)
        atualizar_photos(img_o, img_p)

        if int(img_calc.linha_atual) < int(max_linhas.get()):
            windows.after(10, callback_run)
        
        else:
            mensagem['text'] = 'Finalizado'
    else:
        mensagem['text'] = 'Pause'


def run():
    '''
    Inicia o processo de criação da imagem
    :return: None
    '''
    global stop
    stop = False
    callback_run()


def parar():
    '''
    Pausa o sistema de criação da imagem
    :return: None
    '''
    global stop
    stop = True


def resetar():
    '''
    Reseta as configurações cadastradas anteriormente
    :return: None
    '''

    parar()
    configurar(caminho, numero_pontos.get())
    salvarTxt.reset()
    inicial_img()
    mensagem['text'] = ''


def salvar():
    '''
    Salva a imagem criada e uma lista de pontos a ser seguida pra criação da imagem
    :return: None
    '''
    salvarTxt.salvar()
    img_calc.save()
    mensagem['text'] = 'Salvo!'


salvarTxt = Save('Ordem de Pontos.txt')
img_calc = Image_calc()
caminho = ''
stop = False


# -- Janela -- 
windows = Tk()
windows.resizable(width=False, height=False)
windows.title('Gerador de quadros')

text_original = Label(windows, text='Imagem Original')
text_original.grid(column=0, row=0, padx=10)

text_preview = Label(windows, text='Imagem Preview')
text_preview.grid(column=1, row=0,  padx=10)

figure_original = Label(windows)
figure_original.grid(column=0, row=1, padx=10)
figure_preview = Label(windows)
figure_preview.grid(column=1, row=1, padx=10)

inicial_img()

Button(windows, text='Selecionar Imagem', command=select_arq).grid(column=0, row=2, pady=5)

mensagem = Label(windows, text='')
mensagem.grid(column=1, row=2)

Label(windows, text='Numero de pontos:').grid(column=0, row=3)
numero_pontos = Spinbox(windows, from_=10, to=600, width=8)
numero_pontos.grid(column=1, row=3, pady=10)

Label(windows, text='Numero de maximo de linhas:').grid(column=0, row=4)
max_linhas = Spinbox(windows, from_=1, to=1000, width=8)
max_linhas.grid(column=1, row=4, pady=10)

rodar_button = Button(windows, text='Rodar', command=run, state='disabled')
rodar_button.grid(column=0, row=5, padx=2, pady=3)

Button(windows, text='Parar', command=parar).grid(column=1, row=5, padx=2, pady=3)
Button(windows, text='Resetar', command=resetar).grid(column=0, row=6, padx=2, pady=3)
Button(windows, text='Salvar', command=salvar).grid(column=1, row=6, padx=2, pady=3)


configurar(caminho, numero_pontos.get())


windows.mainloop()
