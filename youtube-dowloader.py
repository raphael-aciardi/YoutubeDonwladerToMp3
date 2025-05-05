import shutil
from pathlib import Path
import threading

from tkinter import *
from pytubefix import YouTube
from moviepy import AudioFileClip

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
        self.atualizar_mensagem("Baixando...", "blue")
        try:
            yt = YouTube(url)
            audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()


            if audio_stream:
                path = Path(".", "dist", "temp")
                path.mkdir(exist_ok=True)
                audio_stream.download(output_path=path)
                self.atualizar_mensagem("Download concluído!", "green")
            else:
                self.atualizar_mensagem("Nenhum áudio encontrado.", "red")

        except Exception as e:
            if "regex_search" in str(e):
                self.atualizar_mensagem("URL inválida.", "red")
            else:
                self.atualizar_mensagem(f"Erro: {str(e)}", "red")

        else:
            self.converter_video()
            
    def converter_video(self):
        self.atualizar_mensagem("Convertendo...", "blue")
        path_in = Path(".", "dist", "temp")
        path_out = Path(".", "dist", "pasta_video")
        for file in path_in.iterdir():
            if file.name.endswith((".mp4", ".m4a", ".mkv", ".avi")):
                audio_clip = AudioFileClip(file)
                file_out_name = "_".join(file.name.split(".")[:-1]) + ".mp3"
                audio_clip.write_audiofile(path_out / file_out_name)
                audio_clip.close()
                if path_in.exists():
                    shutil.rmtree(path_in)
                    
                self.atualizar_mensagem("Conversão concluida!", "green")
                break
        else:
            self.atualizar_mensagem("Nenhum áudio encontrado.", "red")

    def atualizar_mensagem(self, texto, cor):
        def _atualizar():
            self.mensagem.config(text=texto, fg=cor)
        self.mensagem.after(0, _atualizar)


root = Tk()
root.title("PH Downloader")
Application(root)
root.mainloop()
