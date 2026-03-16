# Rockit Vision 🚀 — Reconhecimento de Gestos com Inteligência Artificial

O **Rockit Vision** é uma aplicação de ponta que utiliza **Visão Computacional** e **Machine Learning** para identificar gestos manuais em tempo real através da webcam. Desenvolvido com uma arquitetura moderna e de baixa latência, o projeto transforma movimentos físicos em dados digitais acionáveis.

Este projeto foi desenvolvido durante a **NLW Operator 2026** da Rocketseat.

---

## Funcionalidades

- 🖐️ **Detecção Multi-Mão**: Rastreamento simultâneo de até duas mãos.
- 🎯 **21 Pontos de Referência**: Mapeamento preciso das articulações da mão via MediaPipe Landmarks.
- 🤖 **Classificação Inteligente**: Reconhecimento de diversos gestos customizados:
  - **Saudação**: 👋 Olá / Tchau
  - **Positivo**: 👍 Joinha
  - **Paz e Amor**: ✌️ Símbolo da paz
  - **Metal**: 🤘 Gesto do rock
  - **Hang Loose**: 🤙 Sinal de surfista
  - **Spock**: 🖖 Saudação vulcana
  - **Coração**: 🫶 Gesto de afeto (bilateral)
- ⚡ **Processamento Real-Time**: Comunicação via WebSockets para feedback instantâneo.
- 🎛️ **Controle de Qualidade**: Ajuste dinâmico da resolução e toggle para visualização de landmarks.
- 📊 **Métricas de Performance**: Monitoramento de FPS em tempo real.

---

## 🛠️ Tecnologias Utilizadas

### Backend & IA
- **[Python 3.14+](https://www.python.org/)**: Linguagem base do projeto.
- **[FastHTML](https://fastht.ml/)**: Framework ágil para criação de aplicações web modernas.
- **[MediaPipe](https://google.github.io/mediapipe/)**: Framework do Google para detecção de pose e landmarks.
- **[Scikit-Learn](https://scikit-learn.org/)**: Motor de inferência para os modelos de classificação customizados.
- **[OpenCV](https://opencv.org/)**: Processamento e manipulação de fluxos de vídeo.
- **[Joblib](https://joblib.readthedocs.io/)**: Serialização e carregamento eficiente de modelos de ML.

### Frontend
- **HTML5 & Vanilla CSS**: Estrutura e estilo premium com foco em experiência do usuário.
- **JavaScript (Vanilla)**: Lógica de captura de webcam e comunicação WebSocket.

---

## ⚙️ Como Funciona?

O pipeline de processamento segue quatro etapas fundamentais:

1.  **Captura**: O frame é capturado pela webcam no navegador e enviado via WebSocket.
2.  **Mapeamento**: O **MediaPipe** identifica os 21 pontos (X, Y, Z) de cada mão detectada.
3.  **Inferência**: As coordenadas dos pontos são normalizadas e enviadas para o classificador **Random Forest** (treinado previamente), que identifica o gesto.
4.  **Feedback**: O resultado (rótulo, probabilidade e overlays) é enviado de volta ao frontend para renderização suave no `canvas`.

---

## 🚀 Como Executar

Este projeto utiliza o gerenciador de pacotes **[uv](https://github.com/astral-sh/uv)** para maior velocidade e consistência.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/ArthurRamiro/computer-vision-app.git
    cd computer-vision-app
    ```

2.  **Instale as dependências:**
    ```bash
    uv sync
    ```

3.  **Execute a aplicação:**
    ```bash
    uv run python app_fasthtml.py
    ```

4.  **Acesse no navegador:**
    Abra [http://localhost:5001](http://localhost:5001) (ou a porta indicada no terminal).

---

## 📁 Estrutura do Projeto

```text
computer_vision_app/
├── assets/              # Arquivos estáticos (CSS, JS, Imagens)
├── core/                # Lógica central do sistema
│   ├── models.py        # Configuração e carregamento de modelos
│   ├── processor.py     # Processamento de frames e IA
│   └── utils.py         # Auxiliares de codificação de imagem
├── models/              # Arquivos binários dos modelos (.task, .joblib)
├── app_fasthtml.py      # Ponto de entrada da aplicação
├── pyproject.toml       # Dependências e metadados (uv)
└── README.md            # Documentação (você está aqui)
```

---

## 👨‍💻 Desenvolvedor

**Arthur Ramiro Martins**
- [GitHub](https://github.com/ArthurRamiro)
- [LinkedIn](https://www.linkedin.com/in/arthur-ramiro-4011322a1/)

---

<p align="center">
  Feito durante a NLW Operator 🚀
</p>
