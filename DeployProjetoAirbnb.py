import pandas as pd
import streamlit as st
import joblib

#ler e carregar o modelo
#modelo = joblib.load('modelo.joblib')

x_numericos = {'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bathrooms': 0, 'bedrooms': 0, 'beds': 0, 'extra_people': 0,
               'minimum_nights': 0, 'ano': 0, 'mes': 0, 'n_amenities': 0, 'host_listings_count': 0}

x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}

x_listas = {
    'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite',
                      'Guesthouse', 'Hostel', 'House', 'Loft', 'Outros', 'Serviced apartment'],
    'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
    'cancellation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period'],
    'bed_type': ['Outros', 'Real Bed']
}

dicionario = {}
for item in x_listas:
    for valor in x_listas[item]:
        dicionario[f'{item}_{valor}'] = 0

for item in x_numericos:
    if item in ['latitude', 'longitude']:
        valor = st.number_input(f'{item}', step=0.00001, value=0.0, format="%.5f")
    elif item == 'extra_people':
        valor = st.number_input(f'{item}', step=0.01, value=0.0)
    else:
        valor = st.number_input(f'{item}', step=1, value=0)
        x_numericos[item] = valor

for item in x_tf:
    x_tf[item] = st.selectbox(f'{item}', options=['Sim', 'Não'])
    if x_tf[item] == 'Sim':
        x_tf[item] = 1
    else:
        x_tf[item] = 0

for item in x_listas:
    valor = st.selectbox(item, options=x_listas[item])
    dicionario[f'{item}_{valor}'] = 1
    

butao = st.button('Prever valor do imovel')
if butao:
    dicionario.update(x_numericos)
    dicionario.update(x_tf)
    valores_x = pd.DataFrame(dicionario, index=[0])

    dados = pd.read_csv('dados.csv')
    colunas = list(dados.columns)[1:-1]

    valores_x = valores_x[colunas]
    #ler e carregar o modelo
    modelo = joblib.load('modelo.joblib')
    resultado = modelo.predict(valores_x)
    st.write(f'Previsão do valor do imóvel: R$ {resultado[0]:.2f}')

