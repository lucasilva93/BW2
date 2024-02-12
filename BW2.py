#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
import geopandas as gpd
import humanize as h

file_comuni ='./comuni_clean.csv'  #file già puliti
file_rip ='./ripartizioni_clean.csv'
file_prov ='./province_clean.csv'
file_reg ='./regioni_clean.csv'
comuni_clean =pd.read_csv(file_comuni)
ripartizioni_clean  =pd.read_csv(file_rip)
province_clean =pd.read_csv(file_prov)
regioni_clean =pd.read_csv(file_reg)
print(comuni_clean)
print(ripartizioni_clean)
print(province_clean)
print(regioni_clean)


# In[2]:


#Regione = str(input("Inserisci una specifica Regione : "))
#dati_regione = regioni_clean[regioni_clean['RegionName'] == Regione]
#print(dati_regione[['RegionName','HospitalizedPatients', 'Recovered', 'Deaths', 'CurrentPositiveCases']]) 
# tutte le info selezionate della Regione scelta, nel mio caso Emilia-Romagna


# In[3]:


# unire regioni e comuni, al posto della def ho provato una try
#Regione = input("Inserisci una Regione: ")

#try:
    # Non valori nulli
    #comuni_regione = comuni_clean.loc[comuni_clean['Regione'].str.contains(Regione, case=False, na = False), 'Denominazione'].drop_duplicates().tolist()
    
    #if comuni_regione:
        #print(f"I comuni della regione '{Regione}' sono: {comuni_regione}")
    #else:
        #print(f"Nessun comune trovato per la regione '{Regione}'.")
#except KeyError:
    #print("Dati non corretti")


# In[3]:


totali_positivi = regioni_clean.tail(21)["TotalPositiveCases"].sum()
print("Totali Casi Positivi durante l'ultimo giorno nelle regioni", totali_positivi) 


# In[5]:


# Mappa Italia
map = "./italy-with-regions_1458.geojson"
italy = gpd.read_file(map)


italy.plot(color = 'lightgreen', edgecolor = 'brown', figsize = (11, 11)) #confini regioni marroni, sfondo verde chiaro

#  heat maps
sns.scatterplot(data = regioni_clean, x ='Longitude', y ='Latitude', hue ='Deaths', palette='viridis', s = 400)
             
#s = size dei markers           #hue = colori in base ai morti
import matplotlib.colors as mcolors
plt.title('Distribuzione Decessi per Covid in Italia')
plt.legend(title = 'Decessi per regione', loc = 'best')
plt.savefig('Distribuzione Decessi Covid in Italia.png')
plt.show()


# In[6]:


#CONTAGI Massimi
import matplotlib.pyplot as plt
import geopandas as gpd

regioni_somma_contagi = regioni_clean.groupby('RegionName')['TotalPositiveCases'].max().reset_index()
print("regioni_somma_contagi", regioni_somma_contagi)
italy_with_cases = italy.merge(regioni_somma_contagi, left_on='name', right_on='RegionName', how='left')
italy_with_cases.plot(column='TotalPositiveCases', cmap='viridis', edgecolor='brown', legend=True, figsize=(10, 10))
plt.title('Distribuzione dei contagi COVID-19 per regione in Italia')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig('Italia1.png')
plt.show()


# In[7]:


# Decessi massimi
import matplotlib.pyplot as plt
import geopandas as gpd
regioni_decessi = regioni_clean.groupby('RegionName')['Deaths'].max().reset_index()
print("regioni_decessi", regioni_decessi)
italy_with_cases = italy.merge(regioni_decessi, left_on='name', right_on='RegionName', how='left')
italy_with_cases.plot(column='Deaths', cmap='Reds', edgecolor='brown', legend=True, figsize=(10, 10))
plt.title('Distribuzione Decessi Covid in Italia')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig('Italia2.png')
plt.show()


# In[8]:


# Pazienti guariti massimi
import matplotlib.pyplot as plt
import geopandas as gpd
regioni_guariti = regioni_clean.groupby('RegionName')['Recovered'].max().reset_index()
print("regioni_guariti", regioni_guariti)
italy_with_cases = italy.merge(regioni_guariti, left_on='name', right_on='RegionName', how='left')
italy_with_cases.plot(column='Recovered', cmap='Greens', edgecolor='brown', legend=True, figsize=(10, 10))
plt.title('Distribuzione Pazienti Covid Guariti  in Italia')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig('Italia3.png')
plt.show()


# In[9]:


#top tre regioni per pazienti guariti

total_Recovered_by_region = regioni_clean.groupby('RegionName')['Recovered'].max()
sorted_regions = total_Recovered_by_region.sort_values(ascending=False)
top_3_regions = sorted_regions.head(3)
print("Le tre regioni con il maggior tasso di pazienti guariti sono:")
print(top_3_regions)
region_names = top_3_regions.index
total_hospitalized_counts = top_3_regions.values

plt.bar(region_names, total_hospitalized_counts, color='#008080')

plt.ylabel('Totale Pazienti Guariti', color = "b")
plt.title('Top 3 Regioni per Pazienti guariti in Italia', color = "g" )

plt.savefig('Top 3 Regioni Guariti.png', dpi = 100)
plt.tight_layout()
plt.show()


# In[10]:


#3 Regioni con il maggior numero di Ospedalizzazioni

totale_osped_regione = regioni_clean.groupby('RegionName')['TotalHospitalizedPatients'].sum() #raggruppo e somma
classi_regioni = totale_osped_regione.sort_values(ascending = False)
top_tre_regioni = classi_regioni.head(3) #Le prime tre Regioni
print("Le tre regioni con il maggior tasso di pazienti ospedalizzati totali sono:", top_tre_regioni)


import matplotlib.pyplot as plt
region_names = top_tre_regioni.index #ascisse
total_hospitalized_counts = top_tre_regioni.values
plt.bar(region_names, total_hospitalized_counts, color ='skyblue') #grafico a barre 
plt.xlabel('Regioni', color = 'r') 
plt.ylabel('Totale Pazienti Ospedalizzati', color = 'y')
plt.title('Top 3 Regioni per Pazienti Ospedalizzati in Italia')
plt.savefig('Top 3 Regioni per Pazienti Ospedalizzati in Italia.png')
plt.xticks(rotation = 55)
plt.tight_layout()
plt.show()


# In[11]:


# top 10 province per casi positivi

Total_Positive_Cases_province = province_clean.groupby('ProvinceName')['TotalPositiveCases'].max()
sorted_province = Total_Positive_Cases_province.sort_values(ascending=False)
top_10_province = sorted_province.head(10)
print("Le dieci province con il maggior tasso di pazienti positivi sono:")
print(top_10_province)
province = top_10_province.index
total_cases = top_10_province.values

plt.figure(figsize=(10, 6))
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown'] #ogni colore, ogni provincia
for i in range(len(province)):
    plt.bar(province[i], total_cases[i], color=colors[i], label=province[i], align='edge')
plt.title("Top 10 Province per Casi Positivi")
plt.xlabel("Provincia")
plt.ylabel("Casi Positivi")
plt.xticks(rotation = 35)
plt.savefig('Top 10 Province.png', dpi = 100)
plt.legend(loc  = "best")
plt.grid(True)
plt.legend()
plt.show()





# In[14]:


# CORRELAZIONE

regioni_corr = regioni_clean.select_dtypes(include=['float64', 'int64'])
corr_matrix = regioni_corr.corr()  #mettiamo in correlazione le regioni includendo float ed int
corr_matrix = corr_matrix.iloc[5:, 5:] #solo le righe e colonne che ci servono, no le prime 4 colonne
plt.figure(figsize=(10, 10))
sns.heatmap(corr_matrix, annot = True, cmap = 'coolwarm', fmt ='.1f', linewidths= .2) 
#1 decimale float, invece annot mostra i valori nelle celle


plt.title('Matrice di Correlazione tra le varie Regioni ')
plt.savefig('Matrice di Correlazione tra le varie Regioni.png')
plt.xticks(rotation = 20)
plt.yticks(rotation = 20)
plt.show()


# In[15]:


#BOXPLOT 
import matplotlib.pyplot as plt
import seaborn as sns

regioni_somma_decessi = regioni_clean.groupby('RegionName')['Deaths']
print(regioni_somma_decessi.describe())
# Plot del boxplot
plt.figure(figsize=(9, 9))
sns.boxplot(data=regioni_clean, x='RegionName', y='Deaths', color = 'orange')
plt.xlabel('Regioni', color = 'r')
plt.ylabel('Picco dei decessi')
plt.title('Box Plot Decessi Covid in Italia per Regione')
plt.xticks(rotation = 80) 
#plt.savefig('Boxplot Decessi.png', dpi = 100)
plt.show()


# In[16]:


file_reg='./regioni_clean.csv'
regioni_clean=pd.read_csv(file_reg)
regioni_clean = regioni_clean.dropna(how = "all").drop_duplicates()

regioni_clean['Date'] = pd.to_datetime(regioni_clean['Date'], format='%d-%m-%y')  #modifico il formato Date
regioni_clean.set_index('Date', inplace=True) 
#modifica il DataFrame regioni_pulite direttamente anziché restituire una copia del DataFrame con l'operazione applicata.
contagi_mezzo_mese = regioni_clean.resample('SME')['TotalPositiveCases'].sum().reset_index()  #resetta l'indice del df basato su mezzo mese
print(contagi_mezzo_mese)



# In[17]:


#contagi SEMESTRALI
plt.figure(figsize=(11, 11))
plt.plot(contagi_mezzo_mese['Date'], contagi_mezzo_mese['TotalPositiveCases'], marker ='x', linewidth = 2 ,linestyle = "--")
plt.grid(True) #griglia di sottofondo
plt.title('Contagi nel 2020')
plt.xlabel('Ogni mese e mezzo', color = "m")
plt.ylabel('Numero di contagi', color = "y")
plt.savefig('Contagi ogni mezzo mese.png', dpi = 100)
plt.show()


# In[18]:


#ripartizione geografica affiancata a regione (colonne selezionate)
import pandas as pd

risultato = pd.merge(regioni_clean, ripartizioni_clean, left_on ='RegionCode', right_on ='Codice Regione', how ='inner')
colonne_interessanti = ["Ripartizione geografica" , "Regione"]
risultato_s = risultato[colonne_interessanti]
print(risultato_s)


# In[19]:


import matplotlib.pyplot as plt

# andamento morti giornalieri 
contagimorti_giornalieri =regioni_clean.resample('D')[['NewPositiveCases','Deaths']].sum().reset_index()
contagimorti_giornalieri['nuovi_morti']=0
for i in range(0, 287):
        if i==0:
                contagimorti_giornalieri.iloc[0,3]=contagimorti_giornalieri.iloc[0,2]
        else:
                contagimorti_giornalieri.iloc[i,3]=contagimorti_giornalieri.iloc[i,2]-contagimorti_giornalieri.iloc[(i-1),2]
    
print(contagimorti_giornalieri)
#print(contagimorti_giornalieri[['Date','TotalPositiveCases','Deaths']])
#contagimorti_giornalieri['letalita']=(contagimorti_giornalieri['Deaths']/contagimorti_giornalieri['TotalPositiveCases'])*100
#letalita=contagimorti_giornalieri['letalita'].round(decimals=3)
plt.figure(figsize=(15, 10))
plt.plot(contagimorti_giornalieri.iloc[:,0],contagimorti_giornalieri.iloc[:,3])
plt.grid(True)
plt.title('Decessi giornalieri covid nel paese (2020)')
plt.xlabel('Scala temporale giornaliera')
plt.ylabel('Decessi')
plt.savefig('Giornalieri.png', dpi = 100)
plt.show()


# In[23]:


# RELAZIONE TRA INDICE POVERTA E DECESSI PER IL COVID

poveri = './poveri_regione_clean.csv'
poveri_regione=pd.read_csv(poveri, sep = ",")
poveri_regione=poveri_regione.drop(['Unnamed: 0'], axis=1)
regioni_raggruppate=regioni_clean.groupby('RegionName', as_index=False)['Deaths'].max()
join_poveri_covidcase = pd.merge(poveri_regione, regioni_raggruppate, left_on='Territorio', right_on='RegionName', how='inner')


print(join_poveri_covidcase)
plt.figure(figsize=(11,11))
plt.plot(join_poveri_covidcase['Territorio'],(join_poveri_covidcase['Deaths']/join_poveri_covidcase['Deaths'].sum())*100, color='red',linewidth=5, label='Percentuale di morti')
plt.bar(join_poveri_covidcase['Territorio'],join_poveri_covidcase['Osservazione'], color='darkgreen', label='Indice percentuale di povertà')
plt.xticks(rotation=75)
plt.title('Essere povero ti fa morire?')
plt.ylabel('Indice % di povertà vs Numero di morti')
plt.savefig('Povertà', dpi = 100)
plt.legend()
plt.show()




# In[24]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL del sito Wikipedia

url = 'https://it.wikipedia.org/wiki/Regioni_d%27Italia#Dati_demografici_e_geografici'

# Effettua una richiesta GET al sito
response = requests.get(url)
# Verifica se la richiesta è andata a buon fine (200)
if response.status_code == 200:
    # Utilizza BeautifulSoup per analizzare il contenuto HTML della pagina
    soup = BeautifulSoup(response.content, 'html.parser')
    # Trova la tabella delle regioni
    table = soup.find('table', {'class': 'wikitable'})
    # Inizializza una lista per memorizzare i dati
    data = []
    # Estrai i dati dalla tabella
    rows = table.find_all('tr')
    for row in rows[1:]:  # Salta la riga delle intestazioni
        cells = row.find_all(['th', 'td'])
        regione = cells[0].text.strip()
        superficie = cells[3].text.strip()  # Assumendo che la superficie sia nella quarta colonna
        data.append([regione, superficie])

# Crea un DataFrame pandas
    dataframe = pd.DataFrame(data, columns=['Regione', 'Superficie(km^2)'])
    dataframe = dataframe.drop(dataframe.index[-1])
    # Stampa il DataFrame
    print(dataframe)
else:
    print('Errore nella richiesta HTTP')

print(ripartizioni_clean, regioni_clean['RegionName'].unique(), "dataframe", dataframe)



# Densità comparata con i morti
abitanti_regione=comuni_clean.groupby('Regione')['Popolazione2011'].sum().reset_index()
abitanti_regione['Regione']= abitanti_regione['Regione'].str.lower()
abitanti_regione['Regione'] = abitanti_regione['Regione'].replace('trentino-alto adige/sudtirol', 'trentino-alto adige')
dataframe['Regione']= dataframe['Regione'].str.lower()
dataframe['Superficie(km^2)'] = dataframe['Superficie(km^2)'].str.replace(',', '.').str.replace(r'\s+', '', regex=True).astype(float)
calcolo_densita= pd.merge(abitanti_regione, dataframe, left_on='Regione', right_on='Regione')
calcolo_densita['Superficie(km^2)']= calcolo_densita['Superficie(km^2)'].astype(float)
calcolo_densita['densita']= calcolo_densita['Popolazione2011']/calcolo_densita['Superficie(km^2)']
regioni_raggruppate['RegionName']=regioni_raggruppate['RegionName'].str.lower()
regioni_raggruppate['RegionName'] = regioni_raggruppate['RegionName'].replace('trentino-alto adige/sudtirol', 'trentino-alto adige')
print(regioni_raggruppate.columns)
morti_densita=pd.merge(calcolo_densita, regioni_raggruppate, left_on='Regione', right_on='RegionName')
print(morti_densita)
#grafico a barre
plt.figure(figsize=(11,11))
plt.bar(morti_densita['Regione'],morti_densita['densita']*100, color='orange',linewidth =6, label='densita popolazione')
plt.bar(morti_densita['Regione'],morti_densita['Deaths'], color='red', label='morti')
plt.xticks(rotation=60)
plt.title("I morti stanno dove c'è più densità?")
plt.ylabel('Morti vs densità')
plt.legend(loc = "best")
plt.savefig('Densità', dpi = 150)
plt.show()


# In[ ]:




