import pandas as pd
import numpy as np
import json
from pandas.io.json import json_normalize
from IPython.display import Image
import re
import string
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
from sklearn.cluster import KMeans
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
from sklearn.metrics import roc_auc_score
from sklearn.neighbors import NearestNeighbors
from sklearn.svm import OneClassSVM
from csv import writer
import sys
if sys.version_info[:2] >= (3, 8):
    from collections.abc import MutableMapping
else:
    from collections import MutableMapping

import warnings
warnings.filterwarnings('ignore')

class ANDROID_ASDI:
    def __init__(self):        
        self.centroids_df = pd.DataFrame
        self.data = pd.DataFrame()       
        self.df = pd.DataFrame()     
        self.pid = ""
        self.asdi_kmeans = ""
        self.centroids = pd.DataFrame()
        self.uID = []
        self.final_table_columns = []
        self.sr_flag = []        

    

    def perform_kmeans(self):
        '''
        Perform kmeans clustering and form centroids  
        Args:
            None
        Returns:
            None
        '''        
        #ios_mobile_fp/
        self.centroids_df = pd.read_csv('./android_asdi_centroids.csv')
        self.centroids_df.drop(columns=[col for col in self.centroids_df if col not in self.final_table_columns], inplace=True)        
        centroids = self.centroids_df.values.tolist()
        l = len(centroids)        
        for i in range (l):
            centroids[i] = np.array(centroids[i])            
        common_params = {
            "init": "k-means++",
            "n_init": 1,
            "init" : centroids,
            "algorithm": "elkan"
        }                     
        self.asdi_kmeans = KMeans(n_clusters=len(self.centroids_df), **common_params).fit(self.centroids_df)        
        self.centroids = pd.DataFrame(self.asdi_kmeans.cluster_centers_, columns = self.asdi_kmeans.feature_names_in_)          
          
    def get_asdi(self, new_data):    
        '''
        Indentify decive, register new devices, update kmeans, generate ASDI 
        Args:
            new_data (dataframe) : Data Logs used to identify a device
        Returns:
            asdi (string) : ASDI for the given input
        '''  
             
        asdi = []
        score = []
        pred = []
        decision = []    
        self.final_table_columns = ["d_name", "core", "mean", "median", "memory", "model", "sr_height", "s_name","sr_width", "sc"]           
        self.sr_flag = 0
        self.perform_kmeans()        
        lof =  OneClassSVM(gamma='auto') 
        lof.fit(self.centroids)        
        new_data.drop(columns =[col for col in new_data if col not in self.final_table_columns], inplace=True)
        new_data["mean"] = new_data.mean(axis=1)
        new_data["median"] = new_data.median(axis=1)
        new_data.sort_index(axis=1, inplace=True)
        print(new_data.loc[0])
        for i in range (len(new_data)):
            score.append(lof.score_samples([new_data.loc[i]]))
            pred.append(lof.predict([new_data.loc[i]]))
            decision.append(lof.decision_function([new_data.loc[i]]))            
            predict = lof.score_samples([new_data.loc[i]])
            predict = np.round(predict,decimals = 2)
            if predict >0:
                    cluster = int(self.asdi_kmeans.predict([new_data.loc[i]]))                
                    asdi.append("AD"+ "_" + str(cluster))
            elif predict == 0:                         
                    cluster = len(self.centroids) 
                    asdi.append("AD"+ "_" + str(cluster))
                    centroid = list( new_data.loc[i].values)
                    centroid.insert(0, cluster)      
                    #ios_mobile_fp/          
                    with open('./android_asdi_centroids.csv', 'a',newline='') as f_object: 
                        # Pass this file object to csv.writer()
                        # and get a writer object
                        writer_object = writer(f_object)                
                        # Pass the list as an argument into
                        # the writerow()
                        writer_object.writerow(centroid)                
                        # Close the file object
                        f_object.close()                                        
                    
                    self.perform_kmeans()
                    lof.fit(self.centroids)
                
            else:                        
                    asdi.append("device not found" + str(predict))#str(lof.score_samples([new_data.loc[i]])))         
        new_data["new_asdi"] = asdi       
        new_data["score"] = score    
        new_data["predict"] = pred       
        new_data["decision"] = decision 
        asdi.append("AD_0") 
        return asdi[0] 
    


