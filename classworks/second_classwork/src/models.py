from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

from sklearn.tree import DecisionTreeClassifier, DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier




class Model:
    def __init__(self, modelname, random_state = 42):
        self.modelname = modelname
        self.random_state = random_state
        self.pipeline = None
        self.paramgrid = None
        self.grid = None
        self._buildmodel()

    def _buildmodel(self):
        if self.modelname == "decisiontree":
            self.pipeline = Pipeline(
                [("clf",
                 DecisionTreeClassifier(random_state=self.random_state)
                 )])
            self.paramgrid = {
                "clf__max_depth": [None, 5, 10, 20],
                "clf__min_samples_split": [2, 5, 10]
            }
        elif self.modelname == "randomforest":
            self.pipeline = Pipeline([(
                "clf",
                RandomForestClassifier(random_state=self.random_state)
                )])
            self.paramgrid = {
                "clf__n_estimators" : [50,100],
                "clf__max_depth" : [None, 10, 20]
            }
        elif self.modelname == "svc":
            self.pipeline = Pipeline([
                ("scaler", StandardScaler()),
                ("clf",SVC())
                ])
            self.paramgrid = {
                "clf__C" : [0.1, 1, 10],
                "clf__kernel" : ["linear", "rbf"]
            }
        elif self.modelname == "knn":
            self.pipeline = Pipeline([
                ("scaler", StandardScaler()),
                ("clf", KNeighborsClassifier())
            ])

            self.paramgrid = {
                "clf__n_neighbors" : [3, 5, 7],
                "clf__weights": ["uniform", "distance"]
            }
        else:
            raise ValueError("Model not founded")
        
    def train(self, Xtrain, ytrain):
        self.grid = GridSearchCV(
            self.pipeline,
            self.paramgrid,
            cv = 5,
            scoring="accuracy",
            n_jobs=-1
        )
        self.grid.fit(Xtrain, ytrain)
    
    def evaluate(self, Xtest, ytest):
        return self.grid.score(Xtest,ytest)
    
    def bestparams(self):
        return self.grid.best_params_
    

def bagging_decisiontree(Xtrain, ytrain, Xtest, ytest):
    bagg = BaggingClassifier(
        estimator=DecisionTreeClassifier(random_state=42),
        n_estimators=100,
        max_samples=0.8,
        max_features=1.0,
        random_state=42
    )
    bagg.fit(Xtrain,ytrain)
    return bagg.score(Xtest,ytest)

def boosting_decisiontree(Xtrain, ytrain, Xtest, ytest):
    ada = AdaBoostClassifier(
        estimator= DecisionTreeClassifier(max_depth=3),
        n_estimators = 100,
        learning_rate = 0.5,
        random_state = 42
    )
    ada.fit(Xtrain,ytrain)
    return ada.score(Xtest,ytest)


def bagging_knn(Xtrain, ytrain, Xtest, ytest):
    bagg = BaggingClassifier(
        estimator= KNeighborsClassifier(n_neighbors=5),
        n_estimators= 50,
        max_samples = 0.8,
        random_state = 42 
    )
    bagg.fit(Xtrain,ytrain)
    return bagg.score(Xtest, ytest)

def bagging_knn(Xtrain, ytrain, Xtest, ytest):
    bagg = BaggingClassifier(
        estimator= KNeighborsClassifier(n_neighbors=5),
        n_estimators= 50,
        max_samples = 0.8,
        random_state = 42 
    )
    bagg.fit(Xtrain,ytrain)
    return bagg.score(Xtest, ytest)


def bagging_svc(Xtrain, ytrain, Xtest, ytest):
    bagg = BaggingClassifier(
        estimator= SVC(C=1, kernel= "rbf", probability=True),
        n_estimators= 10,
        max_samples= 0.8,
        random_state= 42
    )
    bagg.fit(Xtrain,ytrain)
    return bagg.score(Xtest, ytest)