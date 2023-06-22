import android_clean_data
import pandas as pd
import ANDROID_ASDI


data = pd.read_csv(r"D:\securelayer7\devicefingerprinting\logs\iosjune.csv")
dataobj = android_clean_data.android_clean_data()
new_data = dataobj.clean_dataset(data) 

new_data.to_csv("cleaned.csv")

#new_data = pd.read_csv("clearned.csv") 

obj = ANDROID_ASDI.ANDROID_ASDI()
print(obj.get_asdi(new_data))