from data_loader import DataLoader
from data_prep import DataPreparation

if __name__ == "__main__":

    # 1. Importar dataset (DataLoader)
    loader = DataLoader(folder_path="Data")
    filename = loader.choose_csv_file()
    if not filename:
        exit()
    df = loader.load_csv(filename)
    if df is None:
        exit()

    print("\nPrimeiras linhas do dataset:")
    print(df.head())

    # 2. Preparação dos dados (DataPreparation)
    prep = DataPreparation(df)
    prep.interactive_prep()
    target_col = prep.choose_target()
    test_size = prep.choose_split()

    print(f"\nVariável alvo selecionada: {target_col}")
    print(f"Percentagem para teste: {test_size*100:.0f}%")
    print(f"Shuffle: {prep.shuffle}")
    print(f"Random state: {prep.random_state}")
    print(f"Colunas removidas: {prep.removed_cols}")

    # 3. Separar X e y (usar o DataFrame atualizado!)
    X = prep.df.drop(columns=[target_col])
    y = prep.df[target_col]

    # 4. Escolher modelo (continua o teu fluxo aqui)