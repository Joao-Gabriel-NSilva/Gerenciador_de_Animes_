import sys
import os
import pandas as pd
import numpy as np
import PySimpleGUI as sg
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QIcon

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


class Anime:

    def __init__(self):
        self._dataset = pd.read_csv(self.verificar_arquivo(), encoding='UTF-8', sep=';')

    @staticmethod
    def verificar_arquivo():
        caminho = 'dados/arquivos'

        arquivo = caminho + '/animes.csv'
        colunas_label = 'nome;status;temporadas'

        if not os.path.exists(caminho):
            os.makedirs(caminho)

        if not os.path.exists(arquivo):
            with open(arquivo, 'w') as f:
                f.write(colunas_label)

        return arquivo

    @property
    def dataset(self):
        return self._dataset

    def sorteia(self):
        indexes = []
        for index in self.dataset[self.dataset['status'] == 'não assistido'].index:
            indexes.append(index)

        index = np.random.choice(indexes, 1)
        nome = self.dataset.iloc[index]['nome'].values[0]
        self.dataset.loc[index, 'status'] = 'assistindo'
        self.dataset.to_csv('dados/arquivos/animes.csv', index=False, encoding='UTF-8', sep=';')

        return nome

    def adicionar_novo_anime(self, nome, temporadas, status):

        if temporadas == '':
            raise ValueError

        self._dataset = self.dataset.append({'nome': nome.title(), 'status': status, 'temporadas': int(temporadas)}, ignore_index=True)

        self.dataset.sort_values(by=['nome'], inplace=True)
        self.dataset.index = [x for x in range(self.dataset.shape[0])]
        self.dataset.to_csv('dados/arquivos/animes.csv', index=False, encoding='UTF-8', sep=';')

    def atualizar_anime(self, nome, novo_status, novo_n_de_temporadas):
        selecao = self.buscar(nome)

        if novo_n_de_temporadas == '':
            novo_n_de_temporadas = self.dataset.loc[self.dataset[selecao].index[0], ['temporadas']]
        if novo_status is None:
            novo_status = self.dataset.loc[self.dataset[selecao].index[0], ['status']]

        self.dataset.loc[self.dataset[selecao].index[0], ['temporadas']] = int(novo_n_de_temporadas)
        self.dataset.loc[self.dataset[selecao].index[0], ['status']] = novo_status
        self.dataset.to_csv('dados/arquivos/animes.csv', index=False, encoding='UTF-8', sep=';')

    def deletar_anime(self, nome):
        selecao = self.buscar(nome)

        self.dataset.drop(index=self.dataset[selecao].index[0], inplace=True)
        self.dataset.to_csv('dados/arquivos/animes.csv', index=False, encoding='UTF-8', sep=';')

    def buscar(self, anime_buscado):
        selecao = self.dataset['nome'].str.lower().str.startswith(anime_buscado)

        if self.dataset[selecao].shape[0] > 1:
            raise IndexError
        elif self.dataset[selecao].empty:
            nomes = self.dataset['nome'].str.lower().values
            for nome in nomes:
                if anime_buscado in nome.split():
                    selecao = self.dataset['nome'].str.lower() == nome
            if self.dataset[selecao].empty:
                raise NameError

        return selecao

    def mostra_anime_buscado(self, anime_buscado):

        selecao = self.buscar(anime_buscado)

        informacoes = {"nome": self.dataset.loc[self.dataset[selecao].index[0], ['nome']].values[0],
                       "status": self.dataset.loc[self.dataset[selecao].index[0], ['status']].values[0],
                       "temporadas": self.dataset.loc[self.dataset[selecao].index[0], ['temporadas']].values[0]}

        return pd.DataFrame(informacoes, index=[len(informacoes.values())])

    def mostra_quantidade_assistidos(self):
        selecao = self.dataset['status'] == 'assistido'
        return self.dataset[selecao]['nome'].count()

    def mostra_tabela(self, status=None, status2=None, nome=None, title=None):
        try:
            if title is None:
                title = 'Animes'

            app = QApplication(sys.argv)
            model = Tabela(self.dataset, status, status2, nome)
            view = QTableView()
            view.setModel(model)
            view.resize(535, 800)
            view.setColumnWidth(0, 300)
            view.setWindowTitle(title)
            view.setWindowIcon(QIcon('dados/icones/FMA logo.png'))
            view.show()
            return app.exec_()

        except IndexError:
            sg.popup_ok("A tabela da categoria selecionada está vazia!", no_titlebar=True, background_color='snow3',
                        text_color='black', font=('Mrs Eaves', 11))


class Tabela(QAbstractTableModel):

    def __init__(self, data, status, status2, nome):
        QAbstractTableModel.__init__(self)

        if status is not None:
            if status2 is not None:
                self.data = (data.query(f"status == '{status}' | status == '{status2}'"))
            else:
                self.data = data.query(f"status == '{status}'")
        elif nome is not None:
            selecao = data['nome'].str.lower().str.startswith(nome)
            self.data = data[selecao]

            if self.data.empty:
                nomes = self.data['nome'].str.lower().values
                for name in nomes:
                    if nome in name.split():
                        selecao = self.df_animes['nome'].str.lower() == name
                        self.data = data[selecao]
        else:
            self.data = data

        if self.data.empty:
            raise IndexError

    def rowCount(self, parent=None):
        return self.data.shape[0]

    def columnCount(self, parnet=None):
        return self.data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self.data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.data.columns[col]
        return None
