#Libraries to pre-process the variables
from sklearn.preprocessing import LabelEncoder,MinMaxScaler
from sklearn.model_selection import train_test_split

#Define the features and the target
col_features = df.columns[6:-3]
X = df[col_features]
Y = df['mood']
#Normalize the features
X= MinMaxScaler().fit_transform(X)
#Encode the labels (targets)
encoder = LabelEncoder()
encoder.fit(Y)
encoded_y = encoder.transform(Y)
#Split train and test data with a test size of 20%
X_train,X_test,Y_train,Y_test = train_test_split(X,encoded_y,test_size=0.2,random_state=15)