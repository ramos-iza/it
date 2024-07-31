import pandas as pd
import datetime
import plotly.express as px
import streamlit as st

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# lendo a base de dados 
base202406 = pd.read_excel('202406AGENCIAS.xlsx')

# filtrando as informações 
base202406 = base202406.iloc[8:,]

# transformar a primeira linha em cabeçalho 
base202406 = base202406.rename(columns=base202406.iloc[0]).drop(base202406.index[0])

# removendo espaços em branco dos nomes das colunas 
base202406.columns = base202406.columns.str.replace(' ', '') 

columns = ['BAIRRO', 'CEP', 'MUNICíPIO', 'UF']
for column in columns:
    print(column)
    base202406[column] =  base202406[column].str.replace(' ', '')
    
# dropa NaN na coluna de endereço 
base202406 = base202406.dropna(subset='ENDEREÇO', axis=0)

# ler as bases de latitude e longitude 
df_lat_backup = pd.read_csv('df_lat.csv')
df_lat = df_lat_backup
df_lat = df_lat.rename(columns={'Unnamed: 0':'CEP', '0': 'LATITUDE'})


df_lon_backup = pd.read_csv('df_lon.csv')
df_lon = df_lon_backup
df_lon = df_lon.rename(columns={'Unnamed: 0':'CEP', '0': 'LONGITUDE'})


# merge com a base 
base202406 = base202406.merge(df_lat, how='outer', on='CEP')

base202406 = base202406.merge(df_lon, how='outer', on='CEP')

# verificando a quantidade de nan
len(base202406)
base202406['LATITUDE'].isna().sum()

base = base202406

# ler a base com a latitude e longitude do google 
df_lon_v2_backup = pd.read_csv('df_lon_v220240718_181034.csv')
df_lon_v2 = df_lon_v2_backup 
df_lon_v2 = df_lon_v2.rename(columns={'Unnamed: 0':'CEP', '0': 'LONGITUDE_v2'})

df_lat_v2_backup = pd.read_csv('df_lat_v220240718_180823.csv')
df_lat_v2 = df_lat_v2_backup
df_lat_v2 = df_lat_v2.rename(columns={'Unnamed: 0':'CEP', '0': 'LATITUDE_v2'})

len(df_lat_v2)

# Merge com a base 
base = base.merge(df_lat_v2, how= 'outer', on='CEP')
base = base.merge(df_lon_v2, how= 'outer', on='CEP')

# verificar a quantidade de ausentes
base['LONGITUDE'].isna().sum()

base['LONGITUDE_v2'].isna().sum()

# preenchendo os valores ausentes nas colunas LATITUDE e LONGITUDE com os respectivos valores de LATITUDE_v2 e LONGITUDE_v2
base['LATITUDE'] = base['LATITUDE'].fillna(base['LATITUDE_v2']) 
base['LONGITUDE'] = base['LONGITUDE'].fillna(base['LONGITUDE_v2']) 

# verificando ausentes que sobraram que decidi ignorar por ora 
len(base[base['LATITUDE'].isna()]['CEP'].unique())
#base_limpa = base.dropna(subset=['LATITUDE'])
#base_limpa.sample(frac=0.005, replace=True, random_state=1)

# tirando espaços em branco da coluna de nome da isntituição e segmento 
base['NOMEINSTITUIÇÃO'] = base['NOMEINSTITUIÇÃO'].str.strip()
base['NOMEINSTITUIÇÃO'].unique()

base['SEGMENTO'] = base['SEGMENTO'].str.strip()
base['SEGMENTO'].unique()

# verificando somente os segmentos que o abanco itau tem 
base[base['NOMEINSTITUIÇÃO'].str.contains('ITAÚ')]['SEGMENTO'].unique()

base[base['NOMEINSTITUIÇÃO'].str.contains('ITAU')]['SEGMENTO'].unique()

# Filtranado a base somente com banco multiplo 
base_multiplo = base[(base['SEGMENTO'] == 'Banco Múltiplo') | (base['SEGMENTO'] == 'Banco do Brasil - Banco Múltiplo')]
#base_multiplo = base.query('SEGMENTO == "Banco Múltiplo"')
base_multiplo.NOMEINSTITUIÇÃO.unique()
len(base_multiplo.NOMEINSTITUIÇÃO.unique())

# dict para unificar o nome das instituições 
fazer_dict = base_multiplo.NOMEINSTITUIÇÃO.unique()
fazer_dict = pd.DataFrame(fazer_dict)
bank = {row[0]: row[0] for index, row in fazer_dict.iterrows()}
print(bank)

bank = {'BANCO DO BRASIL S.A.':'BANCO DO BRASIL',
'BRB - BANCO DE BRASILIA S.A.': 'BANCO DE BRASILIA', 
'BANCO RABOBANK INTERNATIONAL BRASIL S.A.': 'RABOBANK INTERNATIONAL.',
 'BANCO BTG PACTUAL S.A.': 'BTG', 
'BANCO CITIBANK S.A.': 'CITIBANK.', 
'BANCO ANDBANK (BRASIL) S.A.': 'ANDBANK', 
'ITAÚ UNIBANCO S.A.': 'ITAÚ',
 'BANCO BRADESCO S.A.': 'BRADESCO', 
'BANCO SANTANDER (BRASIL) S.A.': 'BANCO SANTANDER',
 'BANCO BMG S.A.': 'BMG', 
'BANCO C6 CONSIGNADO S.A.': 'C6',
 'BANCO DO ESTADO DO RIO GRANDE DO SUL S.A.': 'BANCO DO ESTADO DO RIO GRANDE DO SUL',
 'BANCO SAFRA S.A.': 'SAFRA',
 'BANCO WOORI BANK DO BRASIL S.A.': 'WOORI',
 'BANESTES S.A. BANCO DO ESTADO DO ESPIRITO SANTO': 'BANCO DO ESTADO DO ESPIRITO SANTO', 
'BANCO DO NORDESTE DO BRASIL S.A.': 'BANCO DO NORDESTE ', 
'BANCO PAN S.A.': 'PAN',
 'BANCO J. SAFRA S.A.': ' SAFRA.', 
'BANCO SOCIETE GENERALE BRASIL S.A.': 'SOCIETE GENERALE',
 'BANCO BRADESCO BBI S.A.': 'BRADESCO', 
'OURIBANK S.A. BANCO MÚLTIPLO': 'OURIBANK',
 'DAYCOVAL LEASING - BANCO MÚLTIPLO S.A.': 'DAYCOVAL',
 'BANCO MUFG BRASIL S.A.': 'MUFG.',
 'BANCO DA CHINA BRASIL S.A.': 'BANCO DA CHINA ',
 'BANCO TRICURY S.A.': 'TRICURY', 
'BANCO DAYCOVAL S.A.': ' DAYCOVAL', 
'BANCO SUMITOMO MITSUI BRASILEIRO S.A.': 'SUMITOMO MITSUI', 
'BANCO C6 S.A.': 'C6', 
'BANCO SOFISA S.A.': 'SOFISA', 
'OMNI BANCO S.A.': 'OMNI', 
'BANCOSEGURO S.A.': 'BANCOSEGURO',
 'SCOTIABANK BRASIL S.A. BANCO MÚLTIPLO': 'SCOTIABANK',
 'BANCO PAULISTA S.A.': 'PAULISTA.',
 'BANCO ABC BRASIL S.A.': 'ABC', 
'BANCO IBM S.A.': 'IBM.', 
'BANCO DIGIMAIS S.A.': 'DIGIMAIS ', 
'BANCO RODOBENS S.A.': 'RODOBENS.', 
'BANCO GM S.A.': 'GM.', 
'HIPERCARD BANCO MÚLTIPLO S.A.': 'HIPERCARD.',
 'BANCO ITAUCARD S.A.': 'ITAÚ', 
'BANCO ITAÚ CONSIGNADO S.A.': 'ITAÚ', 
'BANCO ITAUBANK S.A.': 'ITAÚ',
 'ITAÚ UNIBANCO HOLDING S.A.': 'ITAÚ', 
'BANCO ITAÚ VEÍCULOS S.A.': 'ITAÚ', 
'BANCO BRASILEIRO DE CRÉDITO SOCIEDADE ANÔNIMA': 'BRASILEIRO DE CRÉDITO SOCIEDADE ANÔNIMA',
 'BANCO FATOR S.A.': 'FATOR', 
'BANCO MORGAN STANLEY S.A.': 'MORGAN STANLEY', 
'CHINA CONSTRUCTION BANK (BRASIL) BANCO MÚLTIPLO S/A': 'CHINA CONSTRUCTION', 
'BANCO KDB DO BRASIL S.A.': 'KDB', 
'BANCO GENIAL S.A.': 'GENIAL',
 'BANK OF AMERICA MERRILL LYNCH BANCO MÚLTIPLO S.A.': 'BANK OF AMERICA MERRILL LYNCH', 
'DEUTSCHE BANK S.A. - BANCO ALEMAO': 'DEUTSCHE BANK', 
'BANCO CRÉDIT AGRICOLE BRASIL S.A.': 'BANCO CRÉDIT AGRICOLE',
 'BANCO BOCOM BBM S.A.': 'BOCOM BBM',
 'ICBC DO BRASIL BANCO MÚLTIPLO S.A.': 'ICBC',
 'BCV - BANCO DE CRÉDITO E VAREJO S.A.': 'BANCO DE CRÉDITO E VAREJO ',
 'BANCO J.P. MORGAN S.A.': 'J.P. MORGAN', 
'GOLDMAN SACHS DO BRASIL BANCO MULTIPLO S.A.': 'GOLDMAN SACHS',
 'DEUTSCHE SPARKASSEN LEASING DO BRASIL BANCO MÚLTIPLO S.A.': 'DEUTSCHE SPARKASSEN LEASING',
 'BANCO CREDIT SUISSE (BRASIL) S.A.': 'CREDIT SUISSE', 
'BANCO INTER S.A.': 'INTER', 
'BANCO LETSBANK S.A.': 'LETSBANK', 
'BANCO FIBRA S.A.': 'BFIBRA ', 
'BANCO VOITER S.A.': 'VOITER', 
'BANCO CIFRA S.A.': 'CIFRA',
 'BANCO BNP PARIBAS BRASIL S.A.': 'BNP PARIBAS',
 'BANCO INBURSA S.A.': 'INBURSA',
 'BANCO DE LAGE LANDEN BRASIL S.A.': 'BANCO DE LAGE LANDEN', 
'BANCO BANDEPE S.A.': 'BANDEPE',
 'BANCO MODAL S.A.': 'MODAL', 
'INTESA SANPAOLO BRASIL S.A. - BANCO MÚLTIPLO': 'INTESA SANPAOLO',
 'BANCO MIZUHO DO BRASIL S.A.': 'MIZUHO',
 'BANCO BS2 S.A.': 'BS2', 
'BANCO CAIXA GERAL - BRASIL S.A.': 'CAIXA GERAL.',
 'BANCO PINE S.A.': 'PINE', 
'BANCO INDUSTRIAL DO BRASIL S.A.': 'INDUSTRIAL',
 'BANCO ABN AMRO CLEARING S.A.': 'ABN AMRO CLEARING', 
'BANCO HSBC S.A.': 'HSBC',
 'BANCO MASTER MÚLTIPLO S.A.': 'MASTER', 
'BANCO VR S.A.': 'VR.',
 'BANCO ORIGINAL S.A.': 'ORIGINAL', 
'BANCO TOYOTA DO BRASIL S.A.': 'TOYOTA',
 'BANCO LUSO BRASILEIRO S.A.': 'LUSO',
 'BANCO BRADESCO FINANCIAMENTOS S.A.': 'BRADESCO',
 'BANCO CARGILL S.A.': 'CARGILL',
 'BANCO HONDA S.A.': 'HONDA', 
'BANCO CATERPILLAR S.A.': 'CATERPILLAR.', 
'BANCO BV S.A.': ' BV',
 'BANCO HYUNDAI CAPITAL BRASIL S.A.': 'HYUNDAI', 
'BANCO VOTORANTIM S.A.': 'VOTORANTIM', 
'PICPAY BANK - BANCO MÚLTIPLO S.A': 'PICPAY',
 'BANCO KOMATSU DO BRASIL S.A.': 'KOMATSU',
 'BANCO CSF S.A.': 'CSF',
 'BANCO YAMAHA MOTOR DO BRASIL S.A.': 'YAMAHA MOTOR', 
'BANCO BRADESCARD S.A.': 'BRADESCO',
 'BANCO BRADESCO BERJ S.A.': ' BRADESCO',
 'BANCO MERCEDES-BENZ DO BRASIL S.A.': 'MERCEDES-BENZ', 
'SCANIA BANCO S.A.': 'SCANIA',
 'BANCO JOHN DEERE S.A.': 'JOHN DEERE', 
'BANCO RIBEIRAO PRETO S.A.': 'BANCO RIBEIRAO PRETO',
 'BANCO AFINZ S.A. - BANCO MÚLTIPLO': 'AFINZ',
 'BANCO LOSANGO S.A. - BANCO MÚLTIPLO': 'LOSANGO', 
'BANCO CEDULA S.A.': ' CEDULA.', 
'BANCO CLASSICO S.A.': 'CLASSICO.', 
'BANCO GUANABARA S.A.': 'GUANABARA',
 'BANCO XP S.A.': 'XP', 
'BANCO SEMEAR S.A.': 'SEMEAR',
 'BANCO MERCANTIL DO BRASIL S.A.': 'MERCANTIL',
 'BANCO STELLANTIS S.A.': 'STELLANTIS', 
'BANCO XCMG BRASIL S.A.': 'XCMG',
 'BANCO TRIANGULO S.A.': 'BANCO TRIANGULO ',
 'SOCIAL BANK BANCO MÚLTIPLO S/A': 'SOCIAL BANK',
 'BANCO VOLKSWAGEN S.A.': 'VOLKSWAGEN ',
 'BANCO DO ESTADO DE SERGIPE S.A.': 'BANCO DO ESTADO DE SERGIPE', 
'BANCO DIGIO S.A.': 'DIGIO', 
'BANCO DO ESTADO DO PARÁ S.A.': 'BANCO DO ESTADO DO PARÁ',
 'BANCO RNX S.A.': ' RNX', 
'BANCO SENFF S.A.': 'SENFF',
 'BANCO RCI BRASIL S.A.': 'RCI',
 'BANCO BARI DE INVESTIMENTOS E FINANCIAMENTOS S.A.': 'BARI',
 'PARANÁ BANCO S.A.': 'PARANÁ',
 'BANCO VOLVO BRASIL S.A.': 'VOLVO', 
'BANCO CNH INDUSTRIAL CAPITAL S.A.': 'CNH INDUSTRIAL CAPITAL.', 
'BANCO PACCAR S.A.': 'PACCAR', 
'NOVO BANCO CONTINENTAL S.A. - BANCO MÚLTIPLO': 'NOVO BANCO CONTINENTAL',
'BANCO TOPÁZIO S.A.': 'TOPÁZIO', 
'BANCO RANDON S.A.': 'RANDON',
 'BANCO MONEO S.A.': 'MONEO'}



# crinado nova coluna de acordo com o dict acima 
base_multiplo['BANCO_UNIFICADO'] = base_multiplo['NOMEINSTITUIÇÃO'].map(bank)

# Plot com todas as instituições 
import plotly.express as px

fig = px.scatter_geo(base_multiplo, lat='LATITUDE', lon='LONGITUDE', 
                     color='BANCO_UNIFICADO',
                     scope='south america',
                     hover_data=['NOMEINSTITUIÇÃO', 'NOMEAGÊNCIA', 'BAIRRO'],
                     opacity = 0.5,
                     title='Mapa', height = 800)
#fig.show()

# -------- Início da construção do dashboard em astreamlit --------

st.set_page_config(layout="wide")

# Aplica o CSS personalizado ao Streamlit
#st.markdown(container_cs, unsafe_allow_html=True)

with st.sidebar.expander("Dash macro", expanded=False):
    pass

aba = st.sidebar.radio('Escolha a aba', ['Mapas agências'])

if aba == 'Mapas agências':
    
    col1, col2 = st.columns(2)
    with col1: 
        base_palette = px.colors.qualitative.Plotly
        extended_palette = base_palette * (70 // len(base_palette)) + base_palette[:70 % len(base_palette)]
        color_discrete_map = {bank: color for bank, color in zip(base_multiplo['BANCO_UNIFICADO'].unique().tolist(), extended_palette)}
        with st.expander('Agências do Itaú pelo Brasil', expanded=True):
            fig = px.scatter_geo(base_multiplo[base_multiplo['BANCO_UNIFICADO'] == 'ITAÚ'], lat='LATITUDE', lon='LONGITUDE', 
                        color= 'BANCO_UNIFICADO',
                        color_discrete_map=color_discrete_map,
                        scope='south america',
                        hover_data=['NOMEAGÊNCIA', 'BAIRRO', 'NOMEINSTITUIÇÃO'],
                        opacity = 0.5,
                        title='Mapa', height = 800)
            st.plotly_chart(fig, use_container_width=True, responsive=True)  
        

    
    with col2: 
        with st.expander('Comparação entre agências', expanded=True):
            col3, col4 = st.columns(2)
            with col3:
                opcoes = base_multiplo['BANCO_UNIFICADO'].unique().tolist()
                opcoes_selecao1 = st.selectbox('Selecione uma Instituição', opcoes)    
            with col4:
                opcoes_selecao2 = st.selectbox('Selecione outra Instituição', opcoes) 
                     
            dados_filtrados = base_multiplo[(base_multiplo['BANCO_UNIFICADO'] == opcoes_selecao1) | (base_multiplo['BANCO_UNIFICADO'] == opcoes_selecao2)]
            base_palette = px.colors.qualitative.Plotly
            extended_palette = base_palette * (70 // len(base_palette)) + base_palette[:70 % len(base_palette)]
            color_discrete_map = {bank: color for bank, color in zip(opcoes, extended_palette)}
            fig = px.scatter_geo(dados_filtrados, lat='LATITUDE', lon='LONGITUDE', 
                        color= 'BANCO_UNIFICADO',
                        color_discrete_map=color_discrete_map,
                        scope='south america',
                        hover_data=['NOMEAGÊNCIA', 'BAIRRO', 'NOMEINSTITUIÇÃO'],
                        opacity = 0.5,
                        title='Mapa', height = 800)
            st.plotly_chart(fig, use_container_width=True, responsive=True)         

    with st.expander('Mapa com agências de bancos múltiplos em todo o Brasil', expanded=True):    
        fig = px.scatter_geo(base_multiplo, lat='LATITUDE', lon='LONGITUDE', 
                    color='BANCO_UNIFICADO',
                    scope='south america',
                    hover_data=['NOMEAGÊNCIA', 'BAIRRO', 'NOMEINSTITUIÇÃO'],
                    opacity = 0.5,
                    title='Mapa', height = 800)
        st.plotly_chart(fig, use_container_width=True, responsive=True)
        
        
        




