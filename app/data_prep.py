class DataPreparation:
    def __init__(self, df):
        self.df = df
        self.shuffle = True
        self.random_state = 42
        self.removed_cols = []

    def choose_target(self):
        print("\nColunas disponíveis no dataset:")
        for i, col in enumerate(self.df.columns, 1):
            print(f"{i}: {col}")
        while True:
            try:
                idx = int(input("Selecione o número da variável alvo (target): "))
                if 1 <= idx <= len(self.df.columns):
                    return self.df.columns[idx - 1]
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Por favor, introduza um número válido.")

    def choose_split(self):
        while True:
            try:
                test_size = float(input("Percentagem para teste (ex: 0.2 para 20%): "))
                if 0 < test_size < 1:
                    return test_size
                else:
                    print("Introduza um valor entre 0 e 1.")
            except ValueError:
                print("Por favor, introduza um número válido.")

    def choose_columns_to_remove(self):
        print("\nColunas disponíveis para remoção (IDs, nomes, etc):")
        for i, col in enumerate(self.df.columns, 1):
            print(f"{i}: {col}")
        cols_to_remove = input("Introduza os números das colunas a remover separados por vírgula (ou ENTER para nenhuma): ")
        if cols_to_remove.strip():
            indices = [int(i)-1 for i in cols_to_remove.split(",") if i.strip().isdigit()]
            remove_cols = [self.df.columns[i] for i in indices if 0 <= i < len(self.df.columns)]
            self.df = self.df.drop(columns=remove_cols)
            self.removed_cols.extend(remove_cols)
            print(f"Colunas removidas: {remove_cols}")

    def choose_shuffle(self):
        while True:
            resp = input(f"Pretende baralhar (shuffle) os dados antes do split? [s/n] (default: s): ").strip().lower()
            if resp == '' or resp == 's':
                self.shuffle = True
                break
            elif resp == 'n':
                self.shuffle = False
                break
            print("Por favor, responda com 's' ou 'n'.")

    def choose_random_state(self):
        resp = input(f"Definir seed para reprodutibilidade? (default: 42, ENTER para manter): ").strip()
        if resp == "":
            self.random_state = 42
        else:
            try:
                self.random_state = int(resp)
            except ValueError:
                print("Por favor, introduza um número inteiro ou deixe vazio. Seed mantida a 42.")
                self.random_state = 42

    def show_head(self):
        print("\nPrimeiras linhas do dataset:")
        print(self.df.head())

    def show_stats(self):
        print("\nEstatísticas descritivas do dataset:")
        print(self.df.describe(include='all'))

    def interactive_prep(self):
        while True:
            print("\nO que pretende fazer?")
            print("1 - Remover colunas")
            print("2 - Definir shuffle")
            print("3 - Definir random_state")
            print("4 - Ver primeiras linhas dos dados")
            print("5 - Ver estatísticas dos dados")
            print("6 - Continuar para o split")
            choice = input("Escolha uma opção: ").strip()
            if choice == '1':
                self.choose_columns_to_remove()
            elif choice == '2':
                self.choose_shuffle()
            elif choice == '3':
                self.choose_random_state()
            elif choice == '4':
                self.show_head()
            elif choice == '5':
                self.show_stats()
            elif choice == '6':
                break
            else:
                print("Opção inválida.")