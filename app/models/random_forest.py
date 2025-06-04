from sklearn.ensemble import RandomForestClassifier
from .base_model import BaseModel
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import matplotlib.pyplot as plt

class RandomForestModel(BaseModel):
    DEFAULT_PARAMS = {
            **BaseModel.DEFAULT_PARAMS,  # herda os do base
            "n_estimators": 1000,           # mais árvores 
            "criterion": "entropy",         # melhor que gini para este caso
            "max_depth": 20,                # limita o tamanho das árvores
            "min_samples_split": 10,       # mínimo de amostras para dividir um nó
            "min_samples_leaf": 5,          # mínimo de amostras por folha
            "class_weight": "balanced",     # essencial para compensar classe majoritária
            "n_jobs": -1,                   # usa todos os núcleos do CPU
            
        }

    def __init__(self, **params):
        super().__init__()
        # Usa os predefinidos e atualiza com os fornecidos
        self.params = self.DEFAULT_PARAMS.copy()
        self.params.update(params)
        self.model = RandomForestClassifier(**self.params)

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def set_params(self, **params):
        """
        Altera os parâmetros do modelo e re-instancia.
        """
        self.params.update(params)
        self.model = RandomForestClassifier(**self.params)

    @staticmethod
    def ask_params():
        """
        Pergunta ao utilizador os parâmetros principais do RandomForest.
        """
        print("\n--- Parâmetros do RandomForest ---")
        params = {}
        # n_estimators
        n_estimators = input("n_estimators (ENTER para 1000): ").strip()
        params["n_estimators"] = int(n_estimators) if n_estimators else 1000
        # criterion
        crit = input("criterion (gini/entropy/log_loss, ENTER para 'entropy'): ").strip().lower()
        params["criterion"] = crit if crit in ["gini", "entropy", "log_loss"] else "entropy"
        # max_depth
        max_depth = input("max_depth (ENTER para 20): ").strip()
        params["max_depth"] = int(max_depth) if max_depth else 20
        # min_samples_split
        min_split = input("min_samples_split (ENTER para 10): ").strip()
        params["min_samples_split"] = int(min_split) if min_split else 10
        # min_samples_leaf
        min_leaf = input("min_samples_leaf (ENTER para 5): ").strip()
        params["min_samples_leaf"] = int(min_leaf) if min_leaf else 5
        # class_weight
        cw = input("class_weight (None/balanced/balanced_subsample, ENTER para 'balanced'): ").strip().lower()
        if cw in ["balanced", "balanced_subsample"]:
            params["class_weight"] = cw
        elif cw == "none":
            params["class_weight"] = None
        else:
            params["class_weight"] = "balanced"
        # n_jobs
        n_jobs = input("n_jobs (ENTER para -1): ").strip()
        params["n_jobs"] = int(n_jobs) if n_jobs else -1
        # random_state
        rs = input("random_state (ENTER para 42): ").strip()
        params["random_state"] = int(rs) if rs else 42
        return params


    def plot_feature_importance(self, feature_names):
        """Grafico com a importância de cada feature (variável) para o modelo Random Forest(exclusivo)."""
        importances = pd.Series(self.model.feature_importances_, index=feature_names)
        importances = importances.sort_values()
        importances.plot(kind='barh', figsize=(8, 5))
        plt.title("Importância das Variáveis")
        plt.tight_layout()
        plt.show()
