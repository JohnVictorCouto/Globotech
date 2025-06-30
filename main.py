from analise.sistema import SistemaAnaliseEngajamento  # Importa a classe principal do sistema
import os  # Para verificar se o arquivo CSV existe no caminho especificado

def exibir_menu():
    """
    Exibe o menu principal de opções para o usuário.
    """

    print("\n--- MENU PRINCIPAL ---")
    print("1. Processar arquivo CSV")
    print("2. Gerar Relatório de Engajamento por Conteúdo")
    print("3. Gerar Relatório de Atividade de Usuários")
    print("4. Top Conteúdos por Tempo Total Consumido")
    print("5. Top Conteúdos Mais Curtidos")
    print("6. Top Conteúdos Mais Visualizados (view_start)")
    print("7. Plataforma com Maior Engajamento")
    print("8. Conteúdos Mais Comentados")
    print("9. Total de Interações por Tipo de Conteúdo")
    print("10. Tempo Médio de Consumo por Plataforma")
    print("11. Comentários por Conteúdo")
    print("12. Ordenar Conteudos de A - Z")
    print("13. Ordenar Conteudos de Z - A")
    print("0. Sair")
    return input("Escolha uma opção: ")

# Instancia o sistema que gerencia o processamento e análise dos dados
sistema = SistemaAnaliseEngajamento()

# Caminho do arquivo CSV com os dados brutos de interações
caminho_csv = "interacoes_globo.csv"

# Flag que indica se os dados foram carregados e processados
dados_processados = False

print("\n\nFase 3: Análise de Engajamento de Mídias Globo com Estruturas de Dados\n")

# Loop principal que exibe o menu e executa as ações escolhidas pelo usuário
while True:
    opcao = exibir_menu()

    if opcao == "1":
        if os.path.exists(caminho_csv):
            sistema.carregar_interacoes_csv(caminho_csv)
            sistema.processar_interacoes_da_fila()
            dados_processados = True
            print("\nDados do arquivo CSV foram processados com sucesso.")
        else:
            print(f"Arquivo CSV não encontrado: {caminho_csv}")

    elif opcao == "2":
        if dados_processados:
            sistema.gerar_relatorio_engajamento_conteudos()
        else:
            print("Primeiro processe o arquivo CSV (Opção 1).")

    elif opcao == "3":
        if dados_processados:
            sistema.gerar_relatorio_atividade_usuarios()
        else:
            print("Primeiro processe o arquivo CSV (Opção 1).")

    elif opcao == "4":
        if dados_processados:
            sistema.gerar_relatorio_top_conteudos_consumidos(5)
        else:
            print("Primeiro processe o arquivo CSV (Opção 1).")
    elif opcao == "5":
        if dados_processados:
            sistema.relatorio_top_conteudos_mais_curtidos()
        else:
            print("Primeiro processe o arquivo CSV (Opção 1).")

    elif opcao == "6":
        if dados_processados:
            sistema.relatorio_top_conteudos_mais_visualizados()
        else:
            print("Primeiro processe o arquivo CSV (Opção 1).")
    elif opcao == "7":
        if dados_processados:
            sistema.relatorio_plataforma_maior_engajamento()
        else:
            print("Primeiro processe o arquivo CSV (Opção 1).")

    elif opcao == "8":
        if dados_processados:
            sistema.relatorio_conteudos_mais_comentados()
        else:
            print("Primeiro processe o arquivo CSV (Opção 1).")

    elif opcao == "9":
        if dados_processados:
            sistema.relatorio_total_interacoes_por_tipo_conteudo()
        else:
            print("Primeiro processe o arquivo CSV (Opção 1).")

    elif opcao == "10":
        if dados_processados:
            sistema.relatorio_tempo_medio_consumo_por_plataforma()
        else:
            print("Primeiro processe o arquivo CSV (Opção 1).")

    elif opcao == "11":
        if dados_processados:
            sistema.relatorio_comentarios_por_conteudo()
        else:
            print("Primeiro processe o arquivo CSV (Opção 1).")

    elif opcao == "12":
        if dados_processados:
            sistema.relatorio_conteudos_ordenados_por_nome(ordem='AZ')  # A → Z
        else:
            print("Primeiro processe o arquivo CSV (Opção 1).")

    elif opcao == "13":
        if dados_processados:
            sistema.relatorio_conteudos_ordenados_por_nome(ordem='ZA')  # Z → A
        else:
            print("Primeiro processe o arquivo CSV (Opção 1).")

    elif opcao == "0":
        print("Encerrando o programa.")
        break

    else:
        print("Opção inválida. Tente novamente.")
