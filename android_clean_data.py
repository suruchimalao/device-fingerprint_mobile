import pandas as pd
import numpy as np
import json
from pandas.io.json import json_normalize
from IPython.display import Image
import re
import string
import warnings
warnings.filterwarnings('ignore')

class android_clean_data:
    def __init__(self):
        self.X = pd.DataFrame()        
        self.data = pd.DataFrame()       
        self.df = pd.DataFrame()  

    def convAlph2Num(self,sent):
        '''
        Normalize strings to numeric value 
        Args:
            sent (string) : string value to be normalized
        Returns:
            x (int) : normalized numeric value
        '''    
        if(sent == 0):
            return 0
        else:
            alphArray = list(string.ascii_lowercase)
            alphSet = set(alphArray)
            sentArray = list(sent.lower())
            x = []
            for u in sentArray:
                if u in alphSet:
                    u = alphArray.index(u) + 1
                    x.append(u)
                
            return(sum(x))
        
    def convVersion(self, sent):
        '''
        Normalize version number to numeric value 
        Args:
            sent (string) : version number to be normalized
        Returns:
            sent (int) : normalized version number
        ''' 
        sent = str(sent)
        sent = sent.replace(".","")
        sent = sent.replace("-","")
        sent = sent.replace("_","")            
        if type(sent) == type("abc"):
            if len(sent) > 0:
                s=0
                for i in sent:
                    s = s +  (ord(i))                     
                return(int(s))
            else:
                return(0)
        elif len(sent) > 0:
            sent = int(sent)
        else:
            sent = 0
        return(sent)        
    
    def clean_dataset(self,filtered):
        '''
        Clean dataset 
        Args:
            data (dict) : Data Logs to be cleaned
        Returns:
            df (dataframe) : Cleaned Data Logs
        '''   
        '''data = pd.DataFrame.from_dict(json_normalize(filtered))
        data.columns = data.columns.str.replace('_source.', '')'''    
        data = filtered
        data = data.dropna(subset = [ 's_size']) 
        data = data.drop(data.index[data["s_size"]=="undefined"])
        data = data.drop(data.index[data["s_size"]==""])
        data = data.drop(data.index[data["s_size"]=="(empty)"])
        data = data.drop(data.index[data["s_size"]=="0x0"])        
        df2 = data
        dfx = df2
        dfx.fillna(0, inplace = True)
        dfx = dfx.replace('',0)
        dfx = dfx.replace('(empty)',0)        
        dfx_copy = dfx
        df3 = df2
        df = dfx
        #Filling missing values        
        df = df.fillna(0)
        df = df.replace('(empty)',"")
        df = df.replace('undefined',"")              
        df = df.replace(to_replace=r"[^\w\s]",value="",regex=True) 
        #Device Information
        if 'model' in df.columns:
            df['model'] = df['model'].apply(self.convVersion)
        else: 
            df['model'] = 0
        
        if 'd_name' in df.columns:
            df['d_name'] = df['d_name'].apply(self.convVersion)
        else: 
            df['d_name'] = 0
        
        #System(OS) Information
        if 's_name' in df.columns:
            df['s_name'] = df['s_name'].apply(self.convAlph2Num)
        else: 
            df['s_name'] = 0    

        #storage information
        if 'sc' in df.columns:
            df['sc'] = df['sc'].apply(self.convVersion)
        else: 
            df['sc'] = 0    

        #CPU Information       
        if 'core' in df.columns:
            df['core'] = pd.to_numeric(df['core'], errors ='coerce')
        else:
            df['core'] = 0
                        
        #Display Information      
        #to be tested
        df["s_size"] =  df["s_size"].replace(0, "0")
        dfsr = pd.DataFrame(df["s_size"].str.split(' X ',1).tolist(), columns = ['sr_height','sr_width'])
        dfsr.index = df.index
        df['sr_height'] = dfsr['sr_height']
        df['sr_width'] = dfsr['sr_width']
        if 'sr_height' in df.columns:
            df['sr_height'] = pd.to_numeric(df['sr_height'], errors ='coerce')
        else:
            df['sr_height'] = 0
        if 'sr_width' in df.columns:
            df['sr_width'] = pd.to_numeric(df['sr_width'], errors ='coerce')
        else:
            df['sr_width'] = 0
        
        ''' #App Information app_info.app_package_name
        if 'app_info.app_package_name' in df.columns:
            df['app_info.app_package_name'] = df['app_info.app_package_name'].apply(self.convAlph2Num)
        else: 
            df['app_info.app_package_name'] = 0'''

        #Memory Information
        if 'memory' in df.columns:
            df['memory'] = pd.to_numeric(df['memory'], errors ='coerce')
        else:
            df['memory'] = 0

        df = df.fillna(0)        
        #drop unwanted columns
        df = df.select_dtypes(exclude=['object'])

        df.reset_index(inplace = True)
        return df