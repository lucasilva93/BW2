import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
import geopandas as gpd
import humanize as h

file_name_p = "./covid19_italy_province_python.csv"
province = pd.read_csv(file_name_p)
province_clean = province.dropna(how = "all").drop_duplicates() #no nulli o duplicati
print(province_clean)

file_name_r = "./covid19_italy_region_python.csv"
regioni = pd.read_csv(file_name_r)
regioni_clean = regioni.dropna(how = "all").drop_duplicates()
print(regioni_clean)

file_name_c = "./Comuni_python.csv"
comuni = pd.read_csv(file_name_c, encoding = "windows-1252", sep = ",")
comuni['Regione'] = comuni['Regione'].str.lower().str.capitalize() #minuscolo; maiuscola solo la prima lettera di Regione
comuni_clean = comuni.dropna(axis = 1, how = "all").drop(comuni.index[7919]).drop_duplicates() #rimuove ultima riga con la somma
# Rimuove le colonne che contengono solo valori NaN (valori mancanti). axis=1 specifica che l'operazione deve essere eseguita sulle colonne, mentre how="all" specifica di rimuovere le colonne solo se tutti i valori sono NaN.
print(comuni_clean)

file_name_g = "./Ripartizione_geografica_python.csv"
ripartizione = pd.read_csv(file_name_g, sep = ";")
ripartizioni_clean = ripartizione.dropna(how = "all")
print(ripartizioni_clean)


Regione = str(input("Inserisci una specifica Regione : "))
dati_regione = regioni_clean[regioni_clean['RegionName'] == Regione]
print(dati_regione[['RegionName','HospitalizedPatients', 'Recovered', 'Deaths', 'CurrentPositiveCases']]) 
# tutte le info selezionate della Regione scelta, nel mio caso Emilia-Romagna


regioni_clean['Date'] = pd.to_datetime(regioni_clean['Date'], format='%Y-%m-%dT%H:%M:%S').dt.strftime('%d-%m-%y')
print(regioni_clean['Date'])  #T = separatore tra data ed ora  #string format date
#date (senza ora) in giorni, mesi ed anno

# esporto i file puliti
comuni_clean.to_csv("comuni_clean.csv")
province_clean.to_csv("province_clean.csv")
regioni_clean.to_csv("regioni_clean.csv")
ripartizioni_clean.to_csv("ripartizioni_clean.csv")
