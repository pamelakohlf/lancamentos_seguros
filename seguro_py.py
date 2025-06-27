# -*- coding: utf-8 -*-

import streamlit as st
import unicodedata
import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
import io

def remove_acentos(texto):
    nfkd = unicodedata.normalize('NFKD', texto)
    texto_sem_acentos = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    texto_sem_simbolos = ''.join([c for c in texto_sem_acentos if c.isalnum() or c.isspace() or c in ['.', '/', '-', '(', ')']])
    return texto_sem_simbolos.upper()

def gerar_lancamentos(dados):
    lancamentos = []
    meses = (dados['data_fim'].year - dados['data_inicio'].year) * 12 + (dados['data_fim'].month - dados['data_inicio'].month) + 1

    valor_mensal_seguro = round(dados['valor_seguro'] / meses, 2)
    valor_mensal_iof = round(dados['valor_iof'] / meses, 2)
    valor_mensal_outra = round(dados['valor_outra'] / meses, 2) if dados['valor_outra'] > 0 else 0.0

    data_parcela = dados['data_inicio']

    for i in range(meses):
        parcela_atual = i + 1
        parcela_total = meses
        parc_str = f"PARC. {parcela_atual:02d}/{parcela_total:02d}"

        h_seguro = f"APROPRIACAO PREMIO DE SEGURO - APOLICE N {dados['numero_apolice']} - {dados['seguradora']} - {parc_str}"
        h_iof = f"VALOR IOF SEGURO - APOLICE {dados['numero_apolice']} - {dados['seguradora']} - {parc_str}"
        h_outra = f"VALOR {dados['descricao_outra']} SEGURO - APOLICE {dados['numero_apolice']} - {dados['seguradora']} - {parc_str}"

        h_seguro = remove_acentos(h_seguro)
        h_iof = remove_acentos(h_iof)
        h_outra = remove_acentos(h_outra) if dados['valor_outra'] > 0 else ""

        if i < meses - 1:
            data_lanc = data_parcela.strftime("%d/%m/%Y")
        else:
            data_lanc = dados['data_fim'].strftime("%d/%m/%Y")

        lancamentos.append([
            f"{valor_mensal_seguro:.2f}".replace('.', ','),
            data_lanc,
            dados['conta_despesa_seguro'],
            dados['conta_apropriar'],
            h_seguro
        ])

        if valor_mensal_iof > 0:
            lancamentos.append([
                f"{valor_mensal_iof:.2f}".replace('.', ','),
                data_lanc,
                dados['conta_despesa_iof'],
                dados['conta_apropriar'],
                h_iof
            ])

        if dados['valor_outra'] > 0:
            lancamentos.append([
                f"{valor_mensal_outra:.2f}".replace('.', ','),
                data_lanc,
                dados['conta_despesa_outra'],
                dados['conta_apropriar'],
                h_outra
            ])

        data_parcela += relativedelta(months=1)

    return lancamentos

def salvar_csv_em_memoria(lancamentos):
    cabecalho = ["VALOR", "DATA", "CONTA DEBITO", "CONTA CREDITO", "HISTORICO"]
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=';')
    writer.writerow(cabecalho)
    writer.writerows(lancamentos)
    buffer.seek(0)

    # Convertendo para binário
    return buffer.getvalue().encode('utf-8')


# === Streamlit App ===

st.title("Gerador de Lançamentos de Seguro")

with st.form("formulario"):
    numero_apolice = st.text_input("Número da apólice:", key="numero_apolice")
    seguradora = st.text_input("Seguradora:", key="seguradora")
    valor_seguro = st.number_input("Valor total do seguro (R$):", min_value=0.0, format="%.2f", key="valor_seguro")
    valor_iof = st.number_input("Valor total do IOF (R$):", min_value=0.0, format="%.2f", key="valor_iof")
    valor_outra = st.number_input("Valor de juros/outra despesa (R$):", min_value=0.0, format="%.2f", key="valor_outra")
    descricao_outra = ""
    if valor_outra > 0:
        descricao_outra = st.text_input("Descrição da outra despesa (ex: JUROS):", value="JUROS", key="descricao_outra")

    data_inicio = st.date_input("Data de início da vigência:", key="data_inicio")
    data_fim = st.date_input("Data de fim da vigência:", key="data_fim")

    conta_apropriar = st.text_input("Número da conta de Prêmios de Seguros a Apropriar:", key="conta_apropriar")
    conta_despesa_seguro = st.text_input("Número da conta de despesa do Seguro:", key="conta_despesa_seguro")
    conta_despesa_iof = st.text_input("Número da conta de despesa de IOF:", key="conta_despesa_iof")
    conta_despesa_outra = st.text_input("Número da conta de Juros ou outra despesa a ser lançada:", key="conta_despesa_outra")

    gerar = st.form_submit_button("Gerar Lançamentos")

if gerar:
    dados = {
        "numero_apolice": numero_apolice,
        "seguradora": seguradora,
        "valor_seguro": valor_seguro,
        "valor_iof": valor_iof,
        "valor_outra": valor_outra,
        "descricao_outra": descricao_outra,
        "data_inicio": datetime.combine(data_inicio, datetime.min.time()),
        "data_fim": datetime.combine(data_fim, datetime.min.time()),
        "conta_apropriar": conta_apropriar,
        "conta_despesa_seguro": conta_despesa_seguro,
        "conta_despesa_iof": conta_despesa_iof,
        "conta_despesa_outra": conta_despesa_outra
    }

    lancamentos = gerar_lancamentos(dados)
    csv_binario = salvar_csv_em_memoria(lancamentos)

    st.success("✅ Arquivo gerado com sucesso!")
    st.download_button("📥 Baixar Arquivo CSV", data=csv_binario, file_name="lancamentos_seguro.csv", mime="text/csv")

