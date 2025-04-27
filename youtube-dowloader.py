from tkinter import *
from pytubefix import YouTube
import threading


class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        
        self.container = Frame(master, padx=20, pady=20)
        self.container.pack()

        self.titulo = Label(self.container, text="PH Downloader", font=("Arial", 13, "bold"))
        self.titulo.pack(pady=(0, 10))

        self.urlLabel = Label(self.container, text="Digite a URL:", font=self.fontePadrao)
        self.urlLabel.pack()

        self.url = Entry(self.container, width=40, font=self.fontePadrao)
        self.url.pack(pady=(0, 10))

        self.botao = Button(self.container, text="Baixar MP3", font=self.fontePadrao, command=self.iniciar_download)
        self.botao.pack()

        self.mensagem = Label(self.container, text="", font=self.fontePadrao)
        self.mensagem.pack(pady=(10, 0))

    def iniciar_download(self):
        self.atualizar_mensagem("Carregando", "blue")
        url = self.url.get()
        self.url.delete(0, END)

        if url.strip() == "":
            self.atualizar_mensagem("Nenhuma URL fornecida.", "red")
            return

        thread = threading.Thread(target=self.baixar_em_thread, args=(url,))
        thread.start()

    def baixar_em_thread(self, url):
        try:
            yt = YouTube(url)
            audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()


            if audio_stream:
                audio_stream.download(output_path="pasta_video")
                self.atualizar_mensagem("Download concluído!", "green")
            else:
                self.atualizar_mensagem("Nenhum áudio encontrado.", "red")

        except Exception as e:
            if "regex_search" in str(e):
                self.atualizar_mensagem("URL inválida.", "red")
            else:
                self.atualizar_mensagem(f"Erro: {str(e)}", "red")

    def atualizar_mensagem(self, texto, cor):
        def _atualizar():
            self.mensagem.config(text=texto, fg=cor)
        self.mensagem.after(0, _atualizar)


root = Tk()
root.title("PH Downloader")
Application(root)
root.mainloop()
