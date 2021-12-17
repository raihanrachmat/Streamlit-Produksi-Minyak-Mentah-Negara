import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

def load_data():
    dataMinyak = pd.read_csv('produksi_minyak_mentah.csv')
    country = pd.read_json('kode_negara_lengkap.json')
    mergeResult = pd.merge(left=country, right=dataMinyak, left_on='alpha-3', right_on='kode_negara')
    data = dataHasil=mergeResult[['name','tahun','produksi','alpha-3','country-code','iso_3166-2','region','sub-region','intermediate-region','region-code','sub-region-code']]
    data2 = data.rename({'name': 'Negara','produksi':'Jumlah Produksi' ,'tahun': 'Tahun','alpha-3':'Kode Negara','region':'Wilayah','sub-region':'Wilayah Bagian'}, axis='columns')
    return data2

dataset=load_data()
datanegara = pd.read_json('kode_negara_lengkap.json')
image = Image.open('Logo ITB.png')
st.sidebar.image(image)
st.sidebar.subheader('''Nama: Raihan Abdurrafi Rachmat
NIM: 12220126''')
select = st.sidebar.selectbox('Pilih negara',datanegara['name'])
state_data = dataset[dataset['Negara'] == select]
select_year = st.sidebar.selectbox('Pilih tahun',dataset['Tahun'])
state_year = dataset[dataset['Tahun'] == select_year]


def get_total_dataframe(dataset):
    total_dataframe = dataset[['Negara','Tahun','Jumlah Produksi']]
    return total_dataframe
def get_total_year(dataset):
    tahun =dataset[dataset["Tahun"] == select_year]
    tahun['Produksi Kumulatif'] = tahun['Jumlah Produksi'].cumsum()
    year_dataframe = tahun[['Negara','Kode Negara','Wilayah',
                            'Wilayah Bagian','Tahun','Jumlah Produksi','Produksi Kumulatif']]
    return year_dataframe
def get_data_info(dataset):
    info_data = dataset[['Negara','Kode Negara','Wilayah','Wilayah Bagian','Tahun','Jumlah Produksi']]
    pd.set_option('display.max_colwidth', 0)
    return info_data


dataset_bersih = dataset[dataset['Jumlah Produksi'] != 0]
state_total = get_total_dataframe(state_data)
menu = st.sidebar.radio("Lihat Berdasarkan:",("Show All","Negara","Tahun"))
if menu=="Show All":
    st.markdown("## **Data Produksi Minyak Mentah**")
    dataset_show = dataset[['Negara','Kode Negara','Wilayah','Wilayah Bagian','Tahun','Jumlah Produksi']]
    st.dataframe(dataset_show, width=None, height=500)
    if st.button("Analisa Data"):
        st.subheader("Produksi minyak paling tinggi:")
        info_data = dataset[['Negara','Tahun','Jumlah Produksi','Kode Negara','Wilayah','Wilayah Bagian']]
        hasil = info_data[info_data['Jumlah Produksi']==info_data['Jumlah Produksi'].max()]
        st.dataframe(hasil)
        
        st.subheader("Produksi minyak paling tinggi secara kumulatif:")
        dataKumulatif = dataset
        allData=dataKumulatif[dataKumulatif['Negara']=='Saudi Arabia']
        allData = allData[['Negara','Tahun','Jumlah Produksi','Kode Negara','Wilayah','Wilayah Bagian']]
        allData['Kumulatif Tertinggi'] = allData['Jumlah Produksi'].cumsum()
        allData = allData[allData['Kumulatif Tertinggi']==allData['Kumulatif Tertinggi'].max()]
        st.dataframe(allData)

        dataset_olah = dataKumulatif[dataKumulatif['Jumlah Produksi'] != 0]
        st.subheader("Produksi minyak paling rendah:")
        info_data = dataset_olah[['Negara','Tahun','Jumlah Produksi','Kode Negara','Wilayah','Wilayah Bagian']]
        hasil = info_data[info_data['Jumlah Produksi']==info_data['Jumlah Produksi'].min()]
        st.dataframe(hasil)

        tidak_produksi = dataKumulatif[dataKumulatif['Jumlah Produksi'] == 0]
        st.subheader("Negara-negara yang tidak berproduksi:")
        hasil = tidak_produksi[['Negara','Tahun','Jumlah Produksi','Kode Negara','Wilayah','Wilayah Bagian']]
        st.dataframe(hasil)
    
if menu=="Negara":
    st.markdown("### Grafik pada negara "+select)
    state_total_graph = px.bar(state_total, x='Tahun',y='Jumlah Produksi',labels={'Negara produsen minyak = %s' % (select)})
    st.plotly_chart(state_total_graph,use_container_width=True)

    if st.button("Analisa Data "):
        dataset_negara = dataset
        st.markdown("Produksi paling tinggi")
        dataset_olah = dataset_negara[dataset_negara['Negara']==select]
        dataset_olah = dataset_olah[['Negara','Tahun','Jumlah Produksi','Kode Negara','Wilayah','Wilayah Bagian']]
        hasil = dataset_olah[dataset_olah['Jumlah Produksi']==dataset_olah['Jumlah Produksi'].max()]
        st.dataframe(hasil)

        st.markdown("Produksi paling rendah")
        dataset_olah=dataset[dataset['Negara']==select]
        info_data = dataset_olah[['Negara','Tahun','Jumlah Produksi','Kode Negara','Wilayah','Wilayah Bagian']]
        hasil = info_data[info_data['Jumlah Produksi']==info_data['Jumlah Produksi'].min()]
        st.dataframe(hasil)

        st.markdown("Produksi paling tinggi secara kumulatif")
        dataset_olah=dataset_negara[dataset_negara['Negara']==select]
        dataset_olah = dataset_olah[['Negara','Tahun','Jumlah Produksi','Kode Negara','Wilayah','Wilayah Bagian']]
        dataset_olah['Kumulatif Tertinggi'] = dataset_olah['Jumlah Produksi'].cumsum()
        hasil = dataset_olah[dataset_olah['Kumulatif Tertinggi']==dataset_olah['Kumulatif Tertinggi'].max()]
        st.dataframe(hasil)

        st.markdown("Produksi paling rendah secara kumulatif")
        dataset_olah=dataset_negara[dataset_negara['Negara']==select]
        dataset_olah = dataset_olah[['Negara','Tahun','Jumlah Produksi','Kode Negara','Wilayah','Wilayah Bagian']]
        dataset_olah['Kumulatif Terendah'] = dataset_olah['Jumlah Produksi'].cumsum()
        hasil = dataset_olah[dataset_olah['Kumulatif Terendah']==dataset_olah['Kumulatif Terendah'].min()]
        st.dataframe(hasil)
       
year_total = get_total_year(state_year)
if menu=="Tahun":
    dataset_bersih = dataset_bersih[['Negara','Tahun','Jumlah Produksi','Kode Negara','Wilayah','Wilayah Bagian']]
    st.markdown("### Grafik negara yang menghasilkan minyak pada " +"tahun %s " % (select_year))
    year_total_graph = px.bar(year_total,x='Jumlah Produksi',y='Negara',labels={'Jumlah':'Produksi tahun %s' % (select_year)})
    st.plotly_chart(year_total_graph,use_container_width=True)

    if st.button("Analisa Data"):
        st.markdown("Negara yang Memproduksi Minyak Terbesar")
        data_tahun =dataset_bersih[dataset_bersih["Tahun"] == select_year]
        data_tahun=data_tahun[data_tahun['Jumlah Produksi']==data_tahun['Jumlah Produksi'].max()]
        st.dataframe(data_tahun)

        st.markdown("Negara yang Memproduksi Minyak Terkecil")
        data_rendah =dataset_bersih[dataset_bersih["Tahun"] == select_year]
        data_rendah=data_rendah[data_rendah['Jumlah Produksi']==data_rendah['Jumlah Produksi'].min()]
        st.dataframe(data_rendah)

        st.markdown("Negara yang Tidak Memproduksi Minyak pada Tahun %s"%(select_year))
        tidak_produksi = dataset[dataset["Tahun"] == select_year]
        tidak_produksi = tidak_produksi[tidak_produksi['Jumlah Produksi'] == 0]
        tidak_produksi = tidak_produksi[['Negara','Tahun','Jumlah Produksi','Kode Negara','Wilayah','Wilayah Bagian']]
        st.dataframe(tidak_produksi)

    if st.checkbox("10 Negara tertinggi produksi minyak pada tahun %s"%(select_year)):
        dataMax = year_total.nlargest(10, 'Jumlah Produksi')
        dataf = dataMax[['Negara','Tahun','Jumlah Produksi']]
        max_data = px.bar(dataf, x='Jumlah Produksi',y='Negara',labels={'Jumlah':'Produksi tahun %s' % (select_year)})
        st.plotly_chart(max_data,use_container_width=True)

st.markdown(" <style>footer {visibility: hidden;}</style> ", unsafe_allow_html=True)
