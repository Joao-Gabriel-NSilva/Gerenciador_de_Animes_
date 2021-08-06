from uteis import *

sg.theme('darkAmber')  # DarkPurple7

# layouts.

menu_def = [['Tabelas', ['Todos os animes', 'Animes em lançamento', 'Animes assistidos', 'Assistindo atualmente', 'Não assistidos']],
            ['Quantidade assistidos',
            ['Animes']],
            ['Escolher aleatoriamente', ['Sortear Anime']]]

aba1_layout = [
    [sg.T('')],
    [sg.Text('*Nome:', font=('Mrs Eaves', 12)), sg.Text('      '), sg.InputText(key='anime_name', size=(50, 1), tooltip='Nome do anime.')],
    [sg.T('')],
    [sg.Text('*Status:', font=('Mrs Eaves', 12)), sg.Text(' '), sg.Radio('Assistido', 'RADIO1', key='radio1_assistido'),
     sg.Radio('Assistindo', 'RADIO1', key='radio1_assistindo'), sg.Radio('Em lançamento', 'RADIO1', key='radio1_em_lançamento',
     default=True), sg.Radio('Não assistido', 'RADIO1', key='radio1_não_assistido')],
    [sg.T('')],
    [sg.Text('*Temporadas:', font=('Mrs Eaves', 12)), sg.InputText(key='temporadas', size=(50, 1), tooltip='Total de temporadas.')],
    [sg.T('')],
    [sg.Text('                                      '), sg.Button('Adicionar Anime', font=('Mrs Eaves', 12), size=(20, 2))],
    [sg.Text('')]
]

aba2_layout = [
    [sg.Text('')],
    [sg.Text('      '), sg.InputText(key='nome_anime_alterar', size=(64, 1), tooltip='Nome do anime que será alterado.')],
    [sg.Text('                                             '), sg.Button('Buscar', size=(12, 2), key='buscar_anime', font=('Mrs Eaves', 12))],
    [sg.Text('')],
    [sg.Text('                                      '), sg.Text('Selecione o novo status:', font=('Mrs Eaves', 12))],
    [sg.Radio('Assistido', 'RADIO3', key='assistido', default=False), sg.Radio('Assistindo', 'RADIO3', key='assistindo', default=False),
     sg.Radio('Em lançamento', 'RADIO3', key='em lançamento', default=False), sg.Radio('Não assistido', 'RADIO3', key='não assistido', default=False),
     sg.Radio('Dropado', 'RADIO3', key='dropado', default=False)],
    [sg.Text('')],
    [sg.Text('                                             '), sg.Text('Temporadas: ', font=('Mrs Eaves', 12))],
    [sg.Text('      '), sg.InputText(key='novo_n_de_temporadas', tooltip='Novo número de temporadas', size=(64, 1))],
    [sg.Text('                                   '), sg.Button('Atualizar', size=(20, 2), key='atualizar_anime', font=('Mrs Eaves', 12))],
    [sg.Text('')]
]

aba3_layout = [
    [sg.Text('                   '), sg.Text('Digite o nome do anime que será deletado:', font=('Mrs Eaves', 13))],
    [sg.Text('     '), sg.InputText(key='nome_anime_deletar', size=(64, 1))],
    [sg.Text('                                         '), sg.Button('Deletar', key='deletar_anime', size=(20, 2), font=('Mrs Eaves', 12), button_color=('black', 'crimson'))],
    [sg.Text('')]
]

layout_principal = [
    [sg.Menu(menu_def, background_color='white', text_color='black')],
    [sg.TabGroup([[sg.Tab('Adicionar Novo Anime', aba1_layout), sg.Tab('Atualizar Anime', aba2_layout), sg.Tab('Deletar Anime', aba3_layout)]], border_width=1)]
]


# janela
janela = sg.Window('Gerenciador', layout_principal, use_default_focus=False, border_depth=5, icon='dados/icones/FMA-logo.ico', finalize=True)

# eventos
while True:
    try:
        anime = Anime()
        status_anime = None
        novo_status_anime = None
        eventos, valores = janela.read()

        if eventos == sg.WIN_CLOSED:
            break

        # eventos da aba inicial.
        elif eventos == 'Adicionar Anime':

            if valores['anime_name'].strip() == '':
                sg.popup_error('Nenhum nome foi informado!!', title='ERROR',  background_color='snow3', font=('Mrs Eaves', 11), text_color='black',
                               icon='dados/icones/FMA-logo.ico')
            else:
                if valores['radio1_assistido']:
                    status_anime = 'assistido'
                elif valores['radio1_não_assistido']:
                    status_anime = 'não assistido'
                elif valores['radio1_em_lançamento']:
                    status_anime = 'em lançamento'
                elif valores['radio1_assistindo']:
                    status_anime = 'assistindo'

                try:
                    anime_ja_existe = anime.buscar(valores['anime_name'].lower())
                    if not anime_ja_existe.empty:
                        sg.popup_error(f"O anime '{valores['anime_name']}' já esta na lista.", title='ERROR', background_color='snow3',
                                       font=('Mrs Eaves', 11), text_color='black', icon='dados/icones/FMA-logo.ico')

                except NameError:
                    try:
                        # adiciona o novo anime com os parâmetros recebidos do InputText.
                        anime.adicionar_novo_anime(nome=valores['anime_name'], status=status_anime,
                                                   temporadas=valores['temporadas'])
                        sg.popup_quick_message('Anime adicionado!!', background_color='snow3', font=('Mrs Eaves', 11),
                                               text_color='black')
                        janela['anime_name'].update('')
                        janela['temporadas'].update('')
                    except ValueError:
                        sg.popup_error("Todos os campos marcados com asterisco devem ser preenchidos!", title='ERROR', background_color='snow3',
                                       font=('Mrs Eaves', 11), text_color='black', icon='dados/icones/FMA-logo.ico')
                except IndexError:
                    anime.mostra_tabela(nome=valores['nome_anime_alterar'], title='Mais de um anime encontado')

        elif eventos == 'Sortear Anime':
            a = 10/0
            try:
                a, sep = anime.sorteia()
                sg.popup_no_buttons('O anime escolhido foi: ' + a, no_titlebar=True, icon='dados/icones/FMA-logo.ico', auto_close=True, auto_close_duration=3,
                                    background_color='black', text_color='white')

            except ValueError:
                sg.popup_error('Não há nenhum anime marcado como "não assistido" nos arquivos!!', title='ERROR', background_color='snow3',
                               font=('Mrs Eaves', 11), text_color='black', icon='dados/icones/FMA-logo.ico')

        # eventos da barra de menu
        elif eventos == 'Todos os animes':
            anime.mostra_tabela()
        elif eventos == 'Animes em lançamento':
            anime.mostra_tabela(status='em lançamento', title='Animes em lançamento')
        elif eventos == 'Animes assistidos':
            anime.mostra_tabela(status='assistido', title='Animes assistidos')
        elif eventos == 'Assistindo atualmente':
            anime.mostra_tabela(status='assistindo', title='Animes sendo assistidos atualmente', status2='em lançamento')
        elif eventos == 'Não assistidos':
            anime.mostra_tabela(status='não assistido', title='Animes não assistidos')

        elif eventos == 'Animes':
            sg.popup_quick_message('Animes assistidos:  ' + str(anime.mostra_quantidade_assistidos()), no_titlebar=True, background_color='snow3',
                                   text_color='black', font=('Mrs Eaves', 11))

        # eventos da segunda aba
        elif eventos == 'buscar_anime':
            if valores['nome_anime_alterar'].strip() == '':
                sg.popup_error('Nenhum nome foi informado!!', title='ERROR',  background_color='snow3', font=('Mrs Eaves', 11), text_color='black',
                               icon='dados/icones/FMA-logo.ico')
            else:
                try:
                    anime_info = anime.mostra_anime_buscado(valores['nome_anime_alterar'].strip().lower())

                    sg.popup_ok(f"Nome:              {anime_info['nome'].values[0]}",
                                f"Status:             {anime_info['status'].values[0]}",
                                f"Temporadas:   {anime_info['temporadas'].values[0]}",
                                title='Anime Buscado', background_color='snow3', font=('Mrs Eaves', 11), text_color='black',
                                icon='dados/icones/FMA-logo.ico')
                except IndexError:
                    anime.mostra_tabela(nome=valores['nome_anime_alterar'], title='Mais de um anime encontado')

                except NameError:
                    if valores['nome_anime_alterar'].strip() == '':
                        sg.popup_error('Nenhum nome foi informado!!', title='ERROR', background_color='snow3',
                                       font=('Mrs Eaves', 11), text_color='black',
                                       icon='dados/icones/FMA-logo.ico')
                    else:
                        sg.popup_error('O nome "{}" não pôde ser encontrado. Verifique se o nome digitado está correto.'.format(valores['nome_anime_alterar']),
                                       title='ERROR', background_color='snow3', font=('Mrs Eaves', 11), text_color='black',
                                       icon='dados/icones/FMA-logo.ico')

        elif eventos == 'atualizar_anime':

            if valores['nome_anime_alterar'].strip() == '':
                sg.popup_error('Nenhum nome foi informado!!', title='ERROR',  background_color='snow3', font=('Mrs Eaves', 11), text_color='black',
                               icon='dados/icones/FMA-logo.ico')
            else:

                # verifica o novo status marcado no radio.
                if valores['assistido']:
                    novo_status_anime = 'assistido'
                elif valores['assistindo']:
                    novo_status_anime = 'assistindo'
                elif valores['em lançamento']:
                    novo_status_anime = 'em lançamento'
                elif valores['não assistido']:
                    novo_status_anime = 'não assistido'
                elif valores['dropado']:
                    novo_status_anime = 'dropado'

                # tenta atualizar o anime informado no InputText.
                try:
                    anime.atualizar_anime(nome=valores['nome_anime_alterar'].strip().lower(), novo_status=novo_status_anime,
                                          novo_n_de_temporadas=valores['novo_n_de_temporadas'])
                    sg.popup_quick_message('Anime Atualizado!!', no_titlebar=True, background_color='snow3', font=('Mrs Eaves', 11), text_color='black')
                    janela['nome_anime_alterar'].update('')
                    janela['novo_n_de_temporadas'].update('')

                except IndexError:
                    anime.mostra_tabela(nome=valores['nome_anime_alterar'], title='Mais de um anime encontado')

                except NameError:
                    if valores['nome_anime_alterar'].strip() == '':
                        sg.popup_error('Nenhum nome foi informado!!', title='ERROR', background_color='snow3',
                                       font=('Mrs Eaves', 11), text_color='black', icon='dados/icones/FMA-logo.ico')
                    else:
                        sg.popup_error(f"O nome '{valores['nome_anime_alterar']}' não pôde ser encontrado. Verifique se o nome digitado está correto.",
                                       title='ERROR', background_color='snow3', font=('Mrs Eaves', 11), text_color='black',
                                       icon='dados/icones/FMA-logo.ico')

        # eventos da terceira aba

        elif eventos == 'deletar_anime':
            if valores['nome_anime_deletar'].strip() == '':
                sg.popup_error('Nenhum nome foi informado!!', title='ERROR',  background_color='snow3', font=('Mrs Eaves', 11), text_color='black',
                               icon='dados/icones/FMA-logo.ico')
            else:
                try:
                    nome_anime = anime.dataset[anime.buscar(valores['nome_anime_deletar'].lower())]['nome'].values[0]
                    tem_certeza = sg.popup_yes_no(f"Tem certeza que deseja deletar {nome_anime}?", no_titlebar=True, background_color='snow3',
                                                  font=('Mrs Eaves', 11), text_color='black')

                    if tem_certeza == 'Yes':
                        anime.deletar_anime(nome_anime.lower())
                        sg.popup_ok('Anime deletado!!', no_titlebar=True, background_color='snow3', font=('Mrs Eaves', 11), text_color='black')
                        janela['nome_anime_deletar'].update('')
                    else:
                        janela['nome_anime_deletar'].update('')

                except IndexError:
                    anime.mostra_tabela(nome=valores['nome_anime_deletar'], title='Mais de um anime encontado')

                except NameError:
                    sg.popup_error('O nome "{}" não pôde ser encontrado. Verifique se o nome digitado está correto.'.format(valores['nome_anime_deletar']),
                                   title='ERROR', background_color='snow3', font=('Mrs Eaves', 11), text_color='black',
                                   icon='dados/icones/FMA-logo.ico')

    except Exception as e:
        sg.popup_error(str(e.__class__)[str(e.__class__).find("'") + 1: str(e.__class__).find(">") - 1] + '\n' +
                       str(e.with_traceback(e.__traceback__)), no_titlebar=True, background_color='snow3', font=('Mrs Eaves', 11), text_color='black')

janela.close()
