import os
import requests
import pyautogui
from pytube import YouTube
from moviepy.editor import *
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QFrame,
QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QScrollArea, QFormLayout, QGroupBox)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # CONFIGURAÇÕES DA JANELA.
        self.setMinimumSize(QSize(1000, 700))
        self.setWindowIcon(QIcon('.\img\IconeDoPrograma.png'))
        self.setWindowTitle("YouTube To MP3.")

        # WIDGET CENTRAL.
        self.WidgetCentral = QWidget()
        self.LayoutWidgetCentral = QVBoxLayout()
        self.LayoutWidgetCentral.setContentsMargins(0, 0, 0, 0)
        self.WidgetCentral.setLayout(self.LayoutWidgetCentral)
        self.WidgetCentral.setStyleSheet('''QWidget {
            background-color:rgb(20, 20, 20);
        }''')
        self.setCentralWidget(self.WidgetCentral)

        # FRAME BARRA SUPERIOR.
        self.FrameBarraSuperior = QFrame()
        self.LayoutFrameBarraSuperior = QHBoxLayout()
        self.LayoutFrameBarraSuperior.setContentsMargins(60, 0, 0, 0)
        self.FrameBarraSuperior.setLayout(self.LayoutFrameBarraSuperior)
        self.FrameBarraSuperior.setStyleSheet('''QFrame {
            background-color: rgb(30, 30, 30);
            max-height: 60px;
            min-height: 60px;
        }''')
        self.LayoutWidgetCentral.addWidget(self.FrameBarraSuperior)

        # LABEL DO ICONE DO PROGRAMA DA BARRA SUPERIOR.
        self.LabelIconeBarraSuperior = QLabel(self)
        self.IconeBarraSuperior = QPixmap('.\img\IconeBarraSuperior.png')
        self.LabelIconeBarraSuperior.setPixmap(self.IconeBarraSuperior)
        self.LabelIconeBarraSuperior.setStyleSheet('''QLabel {
            max-width: 70px;
        }''')
        self.LayoutFrameBarraSuperior.addWidget(self.LabelIconeBarraSuperior)

        # LABEL COM NOME DO PROGRAMA DA BARRA SUPERIOR.
        self.LabelNomeDoPrograma = QLabel('YouTube To MP3.')
        self.LabelNomeDoPrograma.setStyleSheet('''QLabel {
            color: rgb(255, 255, 255);
            font-size: 20px;
            font-weight: bold;
        }''')
        self.LayoutFrameBarraSuperior.addWidget(self.LabelNomeDoPrograma)

        # SPACER VERTICAL.
        self.VerticalSpacer = QSpacerItem(20, 80, QSizePolicy.Maximum)
        self.LayoutWidgetCentral.addSpacerItem(self.VerticalSpacer)

        # FRAME DO BOTÃO DE COLAR A URL.
        self.FrameBotaoColarUrl = QFrame()
        self.LayoutFrameBotaoColarUrl = QHBoxLayout()
        self.LayoutFrameBotaoColarUrl.setContentsMargins(0, 0, 0, 0)
        self.FrameBotaoColarUrl.setLayout(self.LayoutFrameBotaoColarUrl)
        self.FrameBotaoColarUrl.setStyleSheet('''QFrame {
            max-height: 55px;
        }''')
        self.LayoutWidgetCentral.addWidget(self.FrameBotaoColarUrl)

        # BOTÃO QUE COLA A URL NO PROGRAMA.
        self.BotaoColarUrl = QPushButton(' Colar URL')
        self.BotaoColarUrl.setIcon(QIcon('.\img\IconeBotaoColarUrl'))
        self.BotaoColarUrl.setIconSize(QSize(30, 30))
        self.BotaoColarUrl.clicked.connect(self.ColarUrl)
        self.BotaoColarUrl.setCursor(Qt.PointingHandCursor)
        self.BotaoColarUrl.setStyleSheet('''QPushButton {
            background-color: rgb(255, 50, 50);
            min-height: 50px;
            max-width: 200px;
            border-radius: 25px;
            color: rgb(255, 255, 255);
            font-size: 20px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: rgb(255, 70, 70);
        }
        
        QPushButton:pressed {
            background-color: rgb(255, 90, 90);
        }''')
        self.LayoutFrameBotaoColarUrl.addWidget(self.BotaoColarUrl)

        # ARMAZENA O LINK DO BOTÃO COLAR.
        self.LinkBotaoColar = QLineEdit()
        self.LinkBotaoColar.returnPressed.connect(self.InformacoesDownload)
        self.LinkBotaoColar.setStyleSheet('''QLineEdit {
            max-height: 0px;
            border: none;
        }''')
        self.LayoutWidgetCentral.addWidget(self.LinkBotaoColar)

        # SPACER VERTICAL.
        self.VerticalSpacer = QSpacerItem(20, 60, QSizePolicy.Maximum)
        self.LayoutWidgetCentral.addSpacerItem(self.VerticalSpacer)

        # FRAME ADICIONAR INFORMAÇÕES DO DOWNLOAD.
        self.FrameAddInformacoes = QFrame()
        self.LayoutFrameAddInformacoes = QVBoxLayout()
        self.FrameAddInformacoes.setLayout(self.LayoutFrameAddInformacoes)
        self.LayoutFrameAddInformacoes.setContentsMargins(60, 0, 60, 0)
        self.FrameAddInformacoes.setStyleSheet('''QFrame {
            max-height: 800px;
        }''')
        self.LayoutWidgetCentral.addWidget(self.FrameAddInformacoes)

        self.LabelIconeBackground = QLabel()
        self.IconeBackground = QPixmap('.\img\IconeBackground.png')
        self.LabelIconeBackground.setPixmap(self.IconeBackground)
        self.LabelIconeBackground.setAlignment(Qt.AlignCenter)
        self.LayoutFrameAddInformacoes.addWidget(self.LabelIconeBackground)

        # FRAME DE DOWNLOAD CONCLUIDO.
        self.FrameDownloadConcluido = QFrame()
        self.LayoutFrameDownloadConcluido = QHBoxLayout()
        self.FrameDownloadConcluido.setLayout(self.LayoutFrameDownloadConcluido)
        self.LayoutFrameDownloadConcluido.setContentsMargins(0, 0, 0, 0)
        self.FrameDownloadConcluido.setStyleSheet('''QFrame {
            max-height: 65px;
        }''')
        self.LayoutWidgetCentral.addWidget(self.FrameDownloadConcluido)

        # FRAME ONDE FICA A LABEL DE CONCLUIDO E O BOTÃO PARA LOCALIZAR O ARQUIVO. 
        self.FrameLabelBotaoConcluido = QFrame()
        self.LayoutFrameLabelBotaoConcluido = QHBoxLayout()
        self.FrameLabelBotaoConcluido.setLayout(self.LayoutFrameLabelBotaoConcluido)
        self.LayoutFrameLabelBotaoConcluido.setContentsMargins(30, 0, 30, 0)
        self.FrameLabelBotaoConcluido.setStyleSheet('''QFrame {
            background-color: rgb(20, 20, 20);
            border-radius: 25px;
            max-height: 55px;
            max-width: 330px;
        }''')
        self.LayoutFrameDownloadConcluido.addWidget(self.FrameLabelBotaoConcluido)

        # LABEL DO DOWNLOAD CONCLUIDO.
        self.LabelDownloadConcluido = QLabel()
        self.LabelDownloadConcluido.setAlignment(Qt.AlignCenter)
        self.LayoutFrameLabelBotaoConcluido.addWidget(self.LabelDownloadConcluido)

        # BOTÃO ABRIR LOCAL DO ARQUIVO.
        self.BotaoAbrirLocalArquivo = QPushButton()
        self.BotaoAbrirLocalArquivo.setCursor(Qt.PointingHandCursor)
        self.BotaoAbrirLocalArquivo.clicked.connect(self.Diretorio)
        self.BotaoAbrirLocalArquivo.setStyleSheet('''QPushButton {
            border: none;
        }''')
        self.LayoutFrameLabelBotaoConcluido.addWidget(self.BotaoAbrirLocalArquivo)

        # SPACER VERTICAL.
        self.VerticalSpacer = QSpacerItem(20, 80, QSizePolicy.Maximum)
        self.LayoutWidgetCentral.addSpacerItem(self.VerticalSpacer)

        # FRAME RODA PÉ.
        self.FrameRodaPe = QFrame()
        self.LayoutFrameRodape = QHBoxLayout()
        self.FrameRodaPe.setLayout(self.LayoutFrameRodape)
        self.FrameRodaPe.setStyleSheet('''QFrame {
            background-color: rgb(30, 30, 30);
            max-height: 40px;
        }''')
        self.LayoutWidgetCentral.addWidget(self.FrameRodaPe)

        # LABEL DA MENSAGEM DO RODA PÉ
        self.LabelMenssagemRodaPe = QLabel()
        self.LabelMenssagemRodaPe.setAlignment(Qt.AlignCenter)
        self.LabelMenssagemRodaPe.setStyleSheet('''QLabel {
            color: rgb(255, 255, 255);
            font-size: 16px;
            font-weight: bold;
        }''')
        self.LayoutFrameRodape.addWidget(self.LabelMenssagemRodaPe)

    # FUNÇÃO PARA COLAR O LINK NO ARMAZENAMENTO.
    def ColarUrl(self):
        pyautogui.PAUSE = 0.1
        pyautogui.hotkey('tab')
        pyautogui.PAUSE = 0.1
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.PAUSE = 0.1
        pyautogui.press('enter')
        pyautogui.PAUSE = 0.1

    # FUNÇÃO DO FRAME DAS INFORMAÇÕES DO DOWNLOAD.
    def InformacoesDownload(self):
        
        # SE A URL FOR VÁLIDA.
        if 'https://www.youtube.com/' in self.LinkBotaoColar.text():

            self.BotaoColarUrl.hide()
            self.LabelIconeBackground.hide()

            # FRAME DAS INFORMAÇÕES DO DOWNLOAD.
            self.FrameInformacoesDownload = QFrame()
            self.LayoutFrameInformacoesDownload = QHBoxLayout()
            self.FrameInformacoesDownload.setLayout(self.LayoutFrameInformacoesDownload)
            self.LayoutFrameInformacoesDownload.setContentsMargins(40, 0, 40, 0)
            self.FrameInformacoesDownload.setStyleSheet('''QFrame {
                background-color: rgb(30, 30, 30);
                max-height: 200px;
                border-radius: 40px;
            }''')
            self.LayoutFrameAddInformacoes.addWidget(self.FrameInformacoesDownload)
            
            # PEGA O LINK DO ARQUIVO.
            url_link = YouTube(self.LinkBotaoColar.text())

            # FRAME DO BOTÃO DE CANCELAR O DOWNLOAD.
            self.FrameBotaoCancelar = QFrame()
            self.LayoutFrameBotaoCancelar = QHBoxLayout()
            self.FrameBotaoCancelar.setLayout(self.LayoutFrameBotaoCancelar)
            self.LayoutFrameBotaoCancelar.setContentsMargins(0, 0, 0, 130)
            self.FrameBotaoCancelar.setStyleSheet('''QFrame {
                min-width: 40px;
                max-width: 40px;
            }''')
            self.LayoutFrameInformacoesDownload.addWidget(self.FrameBotaoCancelar)
            
            # BOTÃO DE CANCELAR O DOWNLOAD.
            self.BotaoCancelar = QPushButton()
            self.BotaoCancelar.setIcon(QIcon('.\img\IconeBotaoCancelar.png'))
            self.BotaoCancelar.setIconSize(QSize(18, 18))
            self.BotaoCancelar.setCursor(Qt.PointingHandCursor)
            self.BotaoCancelar.clicked.connect(self.CancelarDownload)
            self.BotaoCancelar.setStyleSheet('''QPushButton {
                background-color: rgb(255, 50, 50);
                border-radius: 20px;
               max-height: 40px;
                max-width: 40px;
            }
            
            QPushButton:hover {
                background-color: rgb(255, 70, 70);
            }
            
            QPushButton:pressed {
                background-color: rgb(255, 90, 90);
            }''')
            self.LayoutFrameBotaoCancelar.addWidget(self.BotaoCancelar)
            
            # FRAME DA IMAGEM DO ARQUIVO.
            self.FrameImagemArquivo = QFrame()
            self.LayoutFrameImagemArquivo = QHBoxLayout()
            self.FrameImagemArquivo.setLayout(self.LayoutFrameImagemArquivo)
            self.LayoutFrameImagemArquivo.setContentsMargins(0, 0, 0, 0)
            self.FrameImagemArquivo.setStyleSheet('''QFrame {
                max-width: 210px;
            }''')
            self.LayoutFrameInformacoesDownload.addWidget(self.FrameImagemArquivo)

            # PEGA A IMAGEM DO ARQUIVO.
            imagem_do_arquivo = url_link.thumbnail_url

            # IMAGEM DO ARQUIVO
            self.ImagemArquivo = QPixmap()
            self.ImagemArquivo.loadFromData(requests.get(imagem_do_arquivo).content)
            self.ImagemArquivo = self.ImagemArquivo.scaled(350, 150, Qt.KeepAspectRatio)

            # LABEL COM A IMAGEM DO ARQUIVO
            self.LabelImagemArquivo = QLabel()
            self.LabelImagemArquivo.setPixmap(self.ImagemArquivo)
            self.LayoutFrameImagemArquivo.addWidget(self.LabelImagemArquivo)

            # FRAME DAS LABELS COM INFORMAÇÕES DO ARQUIVO.
            self.FrameLabelsInformacoesArquivo = QFrame()
            self.LayoutFrameLabelsInformacoesArquivo = QVBoxLayout()
            self.LayoutFrameLabelsInformacoesArquivo.setContentsMargins(10, 30, 10, 30)
            self.FrameLabelsInformacoesArquivo.setLayout(self.LayoutFrameLabelsInformacoesArquivo)
            self.FrameLabelsInformacoesArquivo.setStyleSheet('''QFrame {

            }''')
            self.LayoutFrameInformacoesDownload.addWidget(self.FrameLabelsInformacoesArquivo)

            # LABELS INFORMAÇÕES DO ARQUIVO.
            self.LabelInformacoesArquivo = QLabel('Informações do arquivo')
            self.LabelInformacoesArquivo.setStyleSheet('''QLabel {
                color: rgb(255, 255, 255);
                font-size: 20px;
                font-weight: bold;
            }''')
            self.LayoutFrameLabelsInformacoesArquivo.addWidget(self.LabelInformacoesArquivo)

            # PEGA O NOME DO ARQUIVO.
            nome_do_arquivo = url_link.title

            # LABEL NOME DO ARQUIVO.
            self.LabelNomeArquivo = QLabel(str(nome_do_arquivo))
            self.LabelNomeArquivo.setStyleSheet('''QLabel {
                color: rgb(255, 255, 255);
                font-size: 16px;
                font-weight: bold;
            }''')
            self.LayoutFrameLabelsInformacoesArquivo.addWidget(self.LabelNomeArquivo)

            # PEGA A DURAÇÃO DO ARQUIVO.
            duracao_do_arquivo = url_link.length
            tamanho = int(duracao_do_arquivo)
            minutos = tamanho // 60
            segundos = tamanho % 60

            # LABEL DURAÇÃO DO ARQUIVO.
            self.LabelDuracaoArquivo = QLabel(str(minutos) + ':' + str(segundos))
            self.LabelDuracaoArquivo.setStyleSheet('''QLabel {
                color: rgb(255, 255, 255);
                font-size: 16px;
                font-weight: bold;
            }''')
            self.LayoutFrameLabelsInformacoesArquivo.addWidget(self.LabelDuracaoArquivo)

            # FRAME DO BOTÃO DE DOWNLOAD.
            self.FrameBotaoDownload = QFrame()
            self.LayoutFrameBotaoDownload = QVBoxLayout()
            self.FrameBotaoDownload.setLayout(self.LayoutFrameBotaoDownload)
            self.FrameBotaoDownload.setStyleSheet('''QFrame {
                max-width: 100px;
                min-width: 100px;
            }''')
            self.LayoutFrameInformacoesDownload.addWidget(self.FrameBotaoDownload)

            # BOTÃO DE DOWNLOAD DO ARQUIVO.
            self.BotaoDownload = QPushButton()
            self.BotaoDownload.setIcon(QIcon('.\img\IconeBotaoDownload'))
            self.BotaoDownload.setIconSize(QSize(40, 40))
            self.BotaoDownload.setCursor(Qt.PointingHandCursor)
            self.BotaoDownload.clicked.connect(self.Download)
            self.BotaoDownload.setStyleSheet('''QPushButton {
                background-color: rgb(255, 50, 50);
                border-radius: 40px;
                max-height: 80px;
                max-width: 80px;
            }
            
            QPushButton:hover {
                background-color: rgb(255, 70, 70);
            }
            
            QPushButton:pressed {
                background-color: rgb(255, 90, 90);
            }''')
            self.LayoutFrameBotaoDownload.addWidget(self.BotaoDownload)

        # SE A URL NÃO FOR VÁLIDA.
        else:
            self.LabelMenssagemRodaPe.setText('URL inválida cole uma url válida para baixar.')

    # FUNÇÃO PARA CANCELAR O DOWNLOAD DO ARQUIVO.
    def CancelarDownload(self):
        self.FrameInformacoesDownload.hide()
        self.BotaoColarUrl.show()
        self.LabelIconeBackground.show()

    # FUNÇÃO DO DOWNLOAD.
    def Download(self):

        # BAIXA O AUDIO DO VÍDEO DO YOUTUBE.
        audio = YouTube(self.LinkBotaoColar.text())
        stream = audio.streams.get_highest_resolution()
        download = stream.download(r'C:\Users\Jakson Franceschini\Downloads')

        mp4 = str(download)
        mp3 = str(download[39:-4],) + '.mp3'

        videoclip = VideoFileClip(mp4)

        audioclip = videoclip.audio
        audioclip.write_audiofile(r'C:/Users/Jakson Franceschini/Downloads/' + mp3)

        audioclip.close()
        videoclip.close()

        os.remove(download)

        # FRAME ONDE FICA A LABEL DE CONCLUIDO E O BOTÃO PARA LOCALIZAR O ARQUIVO. 
        self.FrameLabelBotaoConcluido.setStyleSheet('''QFrame {
            background-color: rgb(30, 30, 30);
            border-radius: 25px;
            max-height: 55px;
            max-width: 330px;
        }''')
        
        # LABEL DO DOWNLOAD CONCLUIDO.
        self.LabelDownloadConcluido.setText('Download concluido')
        self.LabelDownloadConcluido.setStyleSheet('''QLabel {
            color: rgb(255, 255, 255);
            font-size: 20px;
            font-weight: bold;
        }''')

        # BOTÃO ABRIR LOCAL DO ARQUIVO.
        self.BotaoAbrirLocalArquivo.setIcon(QIcon('.\img\IconeBotaoAbrirLocalArquivo.png'))
        self.BotaoAbrirLocalArquivo.setIconSize(QSize(25, 25))
        self.BotaoAbrirLocalArquivo.setCursor(Qt.PointingHandCursor)
        self.BotaoAbrirLocalArquivo.setStyleSheet('''QPushButton {
            background-color: rgb(30, 30, 30);
            border: none;
            min-height: 50px;
            min-width: 50px;
        }
        
        QPushButton:hover {
            background-color: rgb(40, 40, 40);
            border-radius: 25px;
            min-height: 50px;
            min-width: 50px;
        }
        
        QPushButton:pressed {
            background-color: rgb(60, 60, 60);
        }''')

        # RETORNA A LABEL COM A MENSAGEM DO RODA PÉ EM BRANCO.
        self.LabelMenssagemRodaPe.setText('')

    # FUNÇÃO PARA ABRIR O LOCAL DO ARQUIVO.
    def Diretorio(self):
        os.startfile(r'C:\Users\Jakson Franceschini\Downloads')

if (__name__ == '__main__'):
    application = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    application.exec()