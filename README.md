# 📊 Saúde Cobertura App

[![Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Um **dashboard interativo** desenvolvido em **Python + Streamlit** para explorar dados de cobertura de planos de saúde no Brasil.  
O projeto faz parte do meu aprendizado em **Ciência de Dados** e foi construído do zero, com foco em boas práticas de versionamento, deploy e visualização de dados.

---

## ✨ Funcionalidades

- **Filtros dinâmicos**: selecione UF, sexo, faixa etária e municípios.  
- **KPIs principais**:
  - Total de beneficiários
  - Beneficiários com assistência médica
  - Beneficiários exclusivos odontológicos
  - Percentuais méd./odonto
- **Visualizações**:
  - 📍 **Por UF**: comparação entre estados.
  - 👥 **Por Faixa Etária**: ordenação automática (ex.: “Até 1 ano” sempre primeiro).
  - 🏙️ **Top Municípios**: ranking dos 20 maiores.
- **Dados filtrados**: tabela interativa com preview de até 1000 linhas.  
- **Exportação**: botão para baixar CSV com os filtros aplicados.  
- **Layout customizado**: KPIs em cards, abas, CSS personalizado.  

---

## 📂 Estrutura do projeto

```
saude_cobertura_app/
├─ data/
│  └─ dados-planos.csv     # Arquivo CSV de exemplo
├─ streamlit_app.py        # Código principal do dashboard
├─ requirements.txt        # Dependências do projeto
└─ README.md               # Este arquivo
```

---

## 🛠️ Tecnologias utilizadas

- [Python 3.10+](https://www.python.org/)  
- [Streamlit](https://streamlit.io/) → framework de dashboard interativo  
- [Pandas](https://pandas.pydata.org/) → manipulação e análise de dados  
- [Plotly Express](https://plotly.com/python/) → gráficos dinâmicos e interativos  

---

## 🚀 Instalação e execução local

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/saude-cobertura-app.git
cd saude-cobertura-app
```

### 2. Crie e ative um ambiente virtual (opcional mas recomendado)
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute o app
```bash
streamlit run streamlit_app.py
```

📍 Acesse em [http://localhost:8501](http://localhost:8501)

---

## 🌐 Deploy no Streamlit Cloud

1. Crie um repositório no GitHub e suba o código.  
2. Vá em [Streamlit Cloud](https://streamlit.io/cloud) e clique em **New app**.  
3. Conecte sua conta GitHub.  
4. Selecione:
   - Repositório: `seu-usuario/saude-cobertura-app`
   - Branch: `main`
   - Arquivo principal: `streamlit_app.py`
5. Clique em **Deploy** 🚀  
6. Seu dashboard ficará disponível em um link público (exemplo: `https://seu-usuario-saude-cobertura-app.streamlit.app`).

---

## 📦 Requisitos (requirements.txt)

```txt
streamlit==1.37.0
pandas==2.2.2
plotly==5.24.0
```

> Usei versões fixas para evitar problemas de compatibilidade ao fazer o deploy.

---

## 📸 Preview

Adicione aqui uma imagem ou gif do seu dashboard rodando:

```markdown
![preview](./screenshot.png)
```

Para gerar um gif, você pode usar [ScreenToGif](https://www.screentogif.com/) (Windows) ou [Peek](https://github.com/phw/peek) (Linux).

---

## 🎯 Objetivos do projeto

- Consolidar conhecimentos de **Ciência de Dados**.  
- Praticar **versionamento com GitHub**.  
- Criar um **dashboard interativo** do zero.  
- Aprender a realizar **deploy em produção** com Streamlit Cloud.  

---

## 🤝 Como contribuir

Contribuições são muito bem-vindas!  
Para contribuir:

1. Faça um fork do projeto.  
2. Crie uma branch (`git checkout -b minha-feature`).  
3. Commit suas alterações (`git commit -m "Minha nova feature"`).  
4. Push para a branch (`git push origin minha-feature`).  
5. Abra um Pull Request.  

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT.  
Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
