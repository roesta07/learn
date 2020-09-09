import os
import pandas as pd
from sklearn import ensemble
from sklearn import preprocessing
from sklearn import metrics
import joblib

# TRAINING_DATA=os.environ.get("TRAINING_DATA")
# FOLD=os.environ.get("FOLD")
TRAINING_DATA="input/train_folds.csv"
FOLD=0
FOLD_MAPPING={
    0:[1,2,3,4],
    1:[0,2,3,4],
    2:[0,1,3,4],
    3:[0,1,2,3]
}
print(TRAINING_DATA)


if __name__=="__main__":
    df=pd.read_csv(TRAINING_DATA)
    train_df=df[df.kfold.isin(FOLD_MAPPING.get(FOLD))]
    valid_df=df[df.kfold==FOLD]
    ytrain=train_df.target.values
    yvalid=valid_df.target.values

    train_df=train_df.drop(["id","target","kfold"],axis=1)
    valid_df=valid_df.drop(["id","target","kfold"],axis=1)

    valid_df=valid_df[train_df.columns]

    label_encoders=[]
    for c in train_df.columns:
        lbl=preprocessing.LabelEncoder()
        lbl.fit(train_df[c].values.tolist()+valid_df[c].values.tolist())
        train_df.loc[:,c]=lbl.transform(train_df[c].values.tolist())
        valid_df.loc[:,c]=lbl.transform(valid_df[c].values.tolist())
        label_encoders.append((c,lbl))

    print(label_encoders)

    ## use dispatcher But for now 
# data is ready to train
    clf=ensemble.RandomForestClassifier(n_estimators=100,n_jobs=5,verbose=2)
    clf.fit(train_df,ytrain)
    preds=clf.predict_proba(valid_df)[:,1]
    print(metrics.roc_auc_score(yvalid,preds))
# use joblib to save pkl file
# joblib.dumb(label_encoders,f"modles/{MODEL}")
