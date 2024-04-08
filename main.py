import pandas as pd
import numpy as np
import numpy_financial as npf
import streamlit as st
from bcb import sgs

st.title('Juros Abusivos - Beta')

tipo = st.radio(
    "Modalidade de Contrato",
    ["Pessoa Fisica (PF)", "Pessoa Juridica (PJ)"],
    index=None)

number = st.number_input('Valor Tomado') * -1
payflow = st.data_editor(data = {'Fluxo de Pagamentos': []}, num_rows="dynamic", hide_index=True)
payflow = payflow['Fluxo de Pagamentos']

try:
    if st.button('Processar'):
        payflow.insert(0, number)
        payflow = [float(valor) for valor in payflow]
        taxa_contrato = npf.irr(payflow)
        #taxa_contrato = (((1 + taxa_contrato)**12) - 1) * 100

        if tipo == "Pessoa Fisica (PF)":
            taxa_mercado = sgs.get({'IPCA': 25435}, start='2023-12-01')
            taxa_mercado = taxa_mercado['IPCA'].iloc[-1]
            taxa_mercado = (((1+(taxa_mercado/100))**12) - 1) * 100

        elif tipo == "Pessoa Juridica (PJ)":
            taxa_mercado = sgs.get({'IPCA': 25434}, start='2023-12-01')
            taxa_mercado = taxa_mercado['IPCA'].iloc[-1]
            taxa_mercado = (((1+(taxa_mercado/100))**12) - 1) * 100

        st.text(f"Taxa do Contrato: {round(taxa_contrato, 2)} %a.a | Taxa Média do Mercado: {round(taxa_mercado, 2)} %a.a")

        if taxa_contrato*100 >= 1.2 * taxa_mercado:
            st.warning("A taxa do seu contrato é considerada potencialmente abusiva.")
        else:
            st.success("A taxa do seu contrato não é considerada potencialmente abusiva.")
    
except:
    st.warning("Preencha as informações do contrato.")
