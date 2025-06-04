from sklearn.dummy import DummyClassifier
from .base_model import BaseModel
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

class DummyModel(BaseModel):
    DEFAULT_PARAMS = {
        "strategy": "most_frequent"
    }

    def __init__(self, **params):
        super().__init__()
        self.params = self.DEFAULT_PARAMS.copy()
        self.params.update(params)
        self.model = DummyClassifier(**self.params)

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def set_params(self, **params):
        self.params.update(params)
        self.model = DummyClassifier(**self.params)

    @staticmethod
    def ask_params():
        print("\n--- Parâmetros do DummyClassifier ---")
        params = {}
        strategy_in = input("strategy (most_frequent/stratified/uniform/constant, default stratified): ").strip().lower()
        if strategy_in in ["most_frequent", "stratified", "uniform", "constant"]:
            params["strategy"] = strategy_in
        else:
            params["strategy"] = "stratified"
        return params





