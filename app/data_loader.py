import pandas as pd
import os

class DataLoader:
    def __init__(self, folder_path="Data"):
        self.folder_path = folder_path

    def list_csv_files(self):
        """Lista todos os ficheiros CSV na pasta definida."""
        try:
            files = [f for f in os.listdir(self.folder_path) if f.endswith('.csv')]
            return files
        except Exception as e:
            print(f"Erro ao listar ficheiros: {e}")
            return []

    def choose_csv_file(self):
        """Mostra os ficheiros CSV e pede ao utilizador para escolher um pelo número."""
        files = self.list_csv_files()
        if not files:
            print("Nenhum ficheiro CSV encontrado na pasta Data.")
            return None
        print("Ficheiros CSV disponíveis:")
        for i, fname in enumerate(files, 1):
            print(f"{i}: {fname}")
        while True:
            try:
                choice = int(input("Selecione o número do ficheiro que pretende carregar: "))
                if 1 <= choice <= len(files):
                    return files[choice - 1]
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Por favor, introduza um número válido.")

    def load_csv(self, filename):
        """Carrega um ficheiro CSV da pasta para um DataFrame pandas."""
        filepath = os.path.join(self.folder_path, filename)
        try:
            df = pd.read_csv(filepath)
            print(f"Ficheiro carregado: {filename} ({df.shape[0]} linhas, {df.shape[1]} colunas)")
            return df
        except Exception as e:
            print(f"Erro ao carregar o ficheiro '{filename}': {e}")
            return None

