from abc import ABC, abstractmethod
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

class BaseModel(ABC):
    def __init__(self):
        self.model = None

    @abstractmethod
    def train(self, X_train, y_train):
        pass

    @abstractmethod
    def evaluate(self, X_test, y_test):
        pass

    def plot_confusion(self, y_test, y_pred, labels=None):
        cm = confusion_matrix(y_test, y_pred, labels=labels)
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=False, fmt='d', cmap='Blues',
                    xticklabels=labels, yticklabels=labels)
        plt.xlabel('Predito')
        plt.ylabel('Verdadeiro')
        plt.title('Matriz de Confusão')
        plt.tight_layout()
        plt.show()