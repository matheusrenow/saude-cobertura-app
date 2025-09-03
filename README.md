# 📊 Saúde Cobertura App

[![Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)

Um dashboard interativo desenvolvido em **Streamlit** para visualizar dados de cobertura de planos de saúde no Brasil.  
Criado como projeto de aprendizado em **Ciência de Dados**, o app permite explorar beneficiários por **UF**, **faixa etária** e **município**, com filtros dinâmicos e gráficos interativos.

---

## ✨ Funcionalidades

- KPIs em tempo real (total de beneficiários, assistência médica, odontológica, proporções).  
- Gráficos comparativos:
  - **📍 Por UF** – beneficiários por estado.
  - **👥 Faixa Etária** – ordenação automática de faixas (ex.: “Até 1 ano” primeiro).
  - **🏙️ Municípios** – ranking Top 20.  
- Filtros dinâmicos por **UF**, **sexo**, **faixa etária** e **município**.  
- Pré-visualização dos dados filtrados.  
- Download do CSV com os dados selecionados.  
- Layout customizado com CSS, KPIs em cards e abas.

---

## 🚀 Como rodar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/saude-cobertura-app.git
cd saude-cobertura-app
