from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import seaborn as sns
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report

class BaseModel(ABC):
    """Classe base para todos os modelos de machine learning.
    Esta classe define a interface básica que todos os modelos devem implementar.
    Inclui métodos para treinar, prever, alterar parâmetros e mostrar a matriz de confusão.
    """
    DEFAULT_PARAMS = {
        "random_state": 42  # valor padrão para seed de aleatoriedade
    }
    def __init__(self):
        self.model = None
        self.params = {}

    @abstractmethod
    def train(self, X_train, y_train):
        pass

    @abstractmethod
    def predict(self, X_test):
        pass

    @abstractmethod
    def set_params(self, **params):
        """Altera os parâmetros do modelo e instancia modelo novamente."""
        pass

    def show_params(self):
        """Mostra os parametros atuais do modelo."""
        print("Parâmetros atuais do modelo:")
        for k, v in self.params.items():
            print(f"  {k}: {v}")

    def print_classification_report(self, X_test, y_test):
        """Mostra o classification_report macro e weighted (ponderado) para as previsões do modelo."""
        y_pred = self.predict(X_test)
        # Usa os nomes das classes se existirem
        if hasattr(self.model, 'classes_'):
            labels = self.model.classes_
            target_names = [str(c) for c in labels]
        else:
            labels = None
            target_names = None
        print(classification_report(
            y_test,
            y_pred,
            labels=labels,
            digits=3,
            zero_division=0,
            target_names=target_names
        ))

    def plot_confusion(self, y_true, y_pred, labels=None, filename=None, subfolder=None, duplicados=None):
        """
        Mostra a matriz de confusão.
        - y_true: valores reais (Series ou array)
        - y_pred: valores previstos (Series ou array)
        - labels: lista de classes (strings), ordem dos eixos
        - filename, subfolder, duplicados: usados só para o título do gráfico
        """
        # Se labels não for None, converte para string (para garantir nomes nos eixos)
        if labels is not None:
            labels = [str(l) for l in labels]
            matrix = confusion_matrix(y_true, y_pred, labels=labels)
            xticks = yticks = labels
        else:
            matrix = confusion_matrix(y_true, y_pred)
            xticks = yticks = None

        # Plot com seaborn
        sns.heatmap(matrix, annot=True, fmt='d', cmap='Greens', xticklabels=xticks, yticklabels=yticks)

        # Título informativo
        partes = []
        if filename: partes.append(str(filename).replace('.csv', ''))
        if subfolder: partes.append(str(subfolder))
        if duplicados is not None: partes.append("com duplicados" if duplicados else "sem duplicados")
        titulo = " | ".join(partes) + " | Matriz de Confusão" if partes else "Matriz de Confusão"

        plt.xlabel('Previsto')  # eixo x = classes previstas
        plt.ylabel('Real')      # eixo y = classes reais
        plt.title(titulo)
        plt.tight_layout()
        plt.show()

    def plot_confusion_all(self, X_test, y_test, filename=None, subfolder=None, duplicados=None):
        """
        Gera previsões e mostra a matriz de confusão para todas as classes.
        - X_test: dados de teste (features)
        - y_test: classes reais
        - filename, subfolder, duplicados: para o título
        """
        y_pred = self.predict(X_test)
        # Usa as classes do modelo se existirem, senão usa as únicas do y_test
        labels = [str(l) for l in getattr(self.model, "classes_", pd.unique(y_test))]
        self.plot_confusion(y_test, y_pred, labels=labels, filename=filename, subfolder=subfolder, duplicados=duplicados)

