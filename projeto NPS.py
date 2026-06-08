
# ============================================================
# IMPORTAÇÕES
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# CARREGAMENTO DA BASE
# ============================================================

arquivo = r"C:\Users\a.lima\OneDrive - Purcom Quimica Ltda\NPS Fatec\NPS Dados 2026.xlsx"

df = pd.read_excel(arquivo)

# Remove primeira linha (descrição)
df = df.iloc[1:].copy()

# ============================================================
# TRATAMENTO DOS DADOS
# ============================================================

df["DATA_RESPOSTA"] = pd.to_datetime(df["DATA_RESPOSTA"])

df["ANO"] = df["DATA_RESPOSTA"].dt.year

df["RESPOSTA_NPS"] = pd.to_numeric(
    df["RESPOSTA_NPS"],
    errors="coerce"
)

# ============================================================
# DIAGNÓSTICO
# ============================================================

print("\nSETORES ENCONTRADOS:")
print(df["SETOR"].unique())

print("\nEMPRESAS ENCONTRADAS:")
print(df["EMPRESA"].unique())

# ============================================================
# FUNÇÃO PARA CÁLCULO DO NPS
# ============================================================

def calcular_nps(base):

    total = len(base)

    if total == 0:
        return 0

    promotores = len(
        base[base["RESPOSTA_NPS"] >= 9]
    )

    detratores = len(
        base[base["RESPOSTA_NPS"] <= 6]
    )

    perc_promotores = (
        promotores / total
    ) * 100

    perc_detratores = (
        detratores / total
    ) * 100

    return round(
        perc_promotores - perc_detratores,
        2
    )

# ============================================================
# FILTROS PRINCIPAIS
# ============================================================

setor = df[
    df["SETOR"] == "Cia Aérea"
]

empresa = setor[
    setor["EMPRESA"] == "Company327"
]

print("\nREGISTROS DO SETOR:")
print(len(setor))

print("\nREGISTROS DA COMPANY327:")
print(len(empresa))

# ============================================================
# PARTE 1 - NPS DO SETOR
# ============================================================

print("\nNPS DO SETOR\n")

anos_setor = sorted(
    setor["ANO"].unique()
)

nps_setor = []

for ano in anos_setor:

    dados_ano = setor[
        setor["ANO"] == ano
    ]

    nps = calcular_nps(
        dados_ano
    )

    nps_setor.append(nps)

    print(f"{ano}: {nps}")

# ============================================================
# GRÁFICO - NPS DO SETOR
# ============================================================

plt.figure(figsize=(10,5))

plt.plot(
    anos_setor,
    nps_setor,
    marker="o"
)

plt.title(
    "NPS do Setor de Companhias Aéreas"
)

plt.xlabel("Ano")
plt.ylabel("NPS")
plt.grid(True)

plt.show()

# ============================================================
# PARTE 2 - NPS DA EMPRESA
# ============================================================

print("\nNPS DA COMPANY327\n")

anos_empresa = sorted(
    empresa["ANO"].unique()
)

nps_empresa = []

for ano in anos_empresa:

    dados_ano = empresa[
        empresa["ANO"] == ano
    ]

    nps = calcular_nps(
        dados_ano
    )

    nps_empresa.append(nps)

    print(f"{ano}: {nps}")

# ============================================================
# GRÁFICO - NPS DA COMPANY327
# ============================================================

plt.figure(figsize=(10,5))

plt.plot(
    anos_empresa,
    nps_empresa,
    marker="o"
)

plt.title(
    "NPS da Company327"
)

plt.xlabel("Ano")
plt.ylabel("NPS")
plt.grid(True)

plt.show()

# ============================================================
# COMPARAÇÃO EMPRESA X SETOR
# ============================================================

comparacao_setor = []
comparacao_empresa = []

for ano in anos_setor:

    dados_setor = setor[
        setor["ANO"] == ano
    ]

    dados_empresa = empresa[
        empresa["ANO"] == ano
    ]

    comparacao_setor.append(
        calcular_nps(dados_setor)
    )

    comparacao_empresa.append(
        calcular_nps(dados_empresa)
    )

plt.figure(figsize=(10,5))

plt.plot(
    anos_setor,
    comparacao_setor,
    marker='o',
    label='Setor'
)

plt.plot(
    anos_setor,
    comparacao_empresa,
    marker='s',
    label='Company327'
)

plt.title(
    "Comparação NPS - Setor x Company327"
)

plt.xlabel("Ano")
plt.ylabel("NPS")
plt.legend()
plt.grid(True)

plt.show()

# ============================================================
# PARTE 3 - CRITÉRIOS QUALITATIVOS
# ============================================================

criterios = [
    "CRITERIO1",
    "CRITERIO2",
    "CRITERIO3",
    "CRITERIO4",
    "CRITERIO5",
    "CRITERIO6",
    "CRITERIO7",
    "CRITERIO8",
    "CRITERIO9",
    "CRITERIO10",
    "CRITERIO11"
]

nomes = {
    "CRITERIO1":"Satisfação Geral",
    "CRITERIO2":"Comunicação",
    "CRITERIO3":"Especialização no Setor",
    "CRITERIO4":"Inovação",
    "CRITERIO5":"Parceria com Clientes",
    "CRITERIO6":"Proatividade",
    "CRITERIO7":"Qualidade dos Serviços",
    "CRITERIO8":"Prontidão e Adaptação",
    "CRITERIO9":"Qualidade dos Colaboradores",
    "CRITERIO10":"Especialização Técnica",
    "CRITERIO11":"Pontualidade"
}

media_empresa = empresa[
    criterios
].mean()

media_empresa.rename(
    index=nomes,
    inplace=True
)

plt.figure(figsize=(12,6))

media_empresa.sort_values().plot(
    kind="bar"
)

plt.title(
    "Fatores Qualitativos - Company327"
)

plt.ylabel("Média")

plt.xticks(rotation=45, ha='right')

plt.tight_layout()

plt.show()

# ============================================================
# COMPARAÇÃO DOS CRITÉRIOS
# COMPANY327 X DEMAIS EMPRESAS
# ============================================================

outras_empresas = setor[
    setor["EMPRESA"] != "Company327"
]

media_company = empresa[
    criterios
].mean()

media_outras = outras_empresas[
    criterios
].mean()

x = np.arange(
    len(criterios)
)

largura = 0.4

plt.figure(figsize=(15,6))

plt.bar(
    x - largura/2,
    media_company,
    largura,
    label="Company327"
)

plt.bar(
    x + largura/2,
    media_outras,
    largura,
    label="Demais Companhias"
)

plt.xticks(
    x,
    list(nomes.values()),
    rotation=45,
    ha="right"
)

plt.title(
    "Comparação dos Critérios Qualitativos"
)

plt.ylabel("Média")

plt.legend()

plt.tight_layout()

plt.show()

# ============================================================
# PARTE 4 - MELHOR E PIOR PAÍS
# ============================================================

resultado_paises = []

for pais in empresa["PAIS"].unique():

    dados_pais = empresa[
        empresa["PAIS"] == pais
    ]

    nps = calcular_nps(
        dados_pais
    )

    resultado_paises.append(
        [pais, nps]
    )

resultado_paises = pd.DataFrame(
    resultado_paises,
    columns=[
        "PAIS",
        "NPS"
    ]
)

resultado_paises = resultado_paises.sort_values(
    "NPS",
    ascending=False
)

print("\nTOP 5 PAÍSES")
print(
    resultado_paises.head()
)

print("\nPIORES 5 PAÍSES")
print(
    resultado_paises.tail()
)

