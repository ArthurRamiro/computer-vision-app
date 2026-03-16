# Importações necessárias do FastHTML e utilitários do projeto
import json
import time
from fasthtml.common import *
from core.processor import GestureProcessor
from core.utils import decode_image, encode_image

# Configura o caminho estático como '.' para que os diretórios /assets/ funcionem corretamente
app, rt = fast_app(static_path='.', debug=True, hdrs=(
    Link(rel='stylesheet', href='/assets/style.css'),
    Script(src='/assets/script.js'),
))

# Inicializa o processador de gestos
processor = GestureProcessor()

# Classe para rastrear o FPS (Frames Por Segundo) da aplicação
class FPSTracker:
    def __init__(self):
        self.prev_time = time.time()
    def update(self):
        curr = time.time()
        fps = 1 / (curr - self.prev_time) if curr > self.prev_time else 0
        self.prev_time = curr
        return int(fps)

fps_tracker = FPSTracker()

@rt("/")
def get():
    # Estrutura principal da página usando componentes FastHTML
    return Title("Rockit Vision — Reconhecimento de Gestos com IA"), Main(
        Header(
            Div(
                Div(
                    H1("Rockit Vision", cls="main-title"),
                    P("Sistema Inteligente de Reconhecimento de Gestos", cls="subtitle"),
                    Nav(
                        A("Monitoramento", href="#vision", cls="nav-link"),
                        A("Biblioteca", href="#gestures", cls="nav-link"),
                        A("Tecnologia", href="#how-it-works", cls="nav-link"),
                        cls="nav-container"
                    )
                ),
                cls="header-content"
            )
        ),
        Div(
            Div(
                # Card de visualização da câmera
                Div(
                    Span("", cls="status-dot"),
                    Span("Aguardando Gesto...", id="status-text"),
                    cls="vision-status"
                ),
                Video(id="video", autoplay=True, playsinline=True, style="display:none"),
                Canvas(id="canvas"),
                Div("FPS: 0", id="fps-counter", cls="fps-badge"),
                cls="vision-card"
            ),
            Div(
                # Card de controles e configurações
                Div(
                    H3("Controle de Qualidade"),
                    Div(
                        Input(type="range", id="quality-slider", min="0.1", max="1.0", step="0.05", value="0.6"),
                        Span("60%", id="quality-value"),
                        cls="quality-control"
                    ),
                    H3("Configurações"),
                    Div(
                        Label(Input(type="checkbox", id="draw-landmarks-cb", checked=True), " Desenhar Pontos da Mão"),
                        cls="settings-control"
                    ),
                    H3("Dados em Tempo Real"),
                    Div(id="gesture-container"),
                    cls="info-card"
                ),
                # Card de visualização do gesto detectado
                Div(
                    H3("Gesto Detectado"),
                    Div(Img(id="gesture-image"), cls="gesture-preview-box"),
                    cls="info-card"
                ),
                cls="sidebar-info"
            ),
            cls="main-content",
            id="vision"
        ),

        # Seção de Gestos Reconhecidos (Estilo Como Funciona)
        Div(
            H2("Biblioteca de Gestos"),
            P("Conheça os movimentos que nosso APP é capaz de identificar instantaneamente.", cls="section-subtitle"),
            Div(
                Div(
                    Img(src="/assets/images/gestures/ola.png", cls="gesture-card-img"),
                    H4("Saudação"),
                    P("Reconhecimento de 'Olá' ou 'Tchau' baseado na palma aberta e dedos estendidos."),
                    cls="step-card"
                ),
                Div(
                    Img(src="/assets/images/gestures/joinha.png", cls="gesture-card-img"),
                    H4("Positivo"),
                    P("O clássico 'Joinha' detectado pela orientação específica do polegar para cima."),
                    cls="step-card"
                ),
                Div(
                    Img(src="/assets/images/gestures/paz.png", cls="gesture-card-img"),
                    H4("Paz e Amor"),
                    P("Identificação do símbolo de paz através da separação dos dedos indicador e médio."),
                    cls="step-card"
                ),
                Div(
                    Img(src="/assets/images/gestures/rock.png", cls="gesture-card-img"),
                    H4("Metal"),
                    P("Gesto do rock reconhecido pela extensão dos dedos indicador e minguinho."),
                    cls="step-card"
                ),
                Div(
                    Img(src="/assets/images/gestures/hangloose.png", cls="gesture-card-img"),
                    H4("Hang Loose"),
                    P("Mapeamento do sinal surfista com polegar e minguinho em sentidos opostos."),
                    cls="step-card"
                ),
                Div(
                    Img(src="/assets/images/gestures/spock.png", cls="gesture-card-img"),
                    H4("Saudação Spock"),
                    P("Famoso gesto vulcano reconhecido pela divisão binária dos dedos da mão."),
                    cls="step-card"
                ),
                Div(
                    Img(src="/assets/images/gestures/coracao.png", cls="gesture-card-img"),
                    H4("Coração"),
                    P("Gesto bilateral de afeto detectado quando ambos os polegares se tocam em arco."),
                    cls="step-card"
                ),
                cls="steps-grid"
            ),
            cls="how-it-works",
            id="gestures"
        ),

        # Seção de explicação técnica
        Div(
            H2("Tecnologia"),
            P("Uma combinação poderosa de Visão Computacional e Inteligência Artificial para traduzir movimentos em dados.", cls="section-subtitle"),
            Div(
                Div(
                    NotStr('<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="step-icon"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg>'),
                    H4("Captura de Alta Fidelidade"),
                    P("A sequência de frames é capturada via webcam com técnicas de filtragem para garantir clareza visual mesmo em ambientes com pouca luz."),
                    cls="step-card"
                ),
                Div(
                    NotStr('<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="step-icon"><path d="M12 2v8"/><path d="m4.93 10.93 1.41 1.41"/><path d="M2 18h2"/><path d="M20 18h2"/><path d="m19.07 10.93-1.41 1.41"/><path d="M22 22H2"/><path d="m8 22 4-10 4 10"/><path d="M14 18H10"/></svg>'),
                    H4("Rede Neural Avançada"),
                    P("Utilização do MediaPipe para mapear instantaneamente os 21 pontos articulares (landmarks) da mão em um espaço tridimensional."),
                    cls="step-card"
                ),
                Div(
                    NotStr('<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="step-icon"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M7 14h10"/><path d="M10 11h4"/><path d="M8 17h8"/><path d="M12 11V7"/></svg>'),
                    H4("Motor de Inferência"),
                    P("Algoritmos de Machine Learning classificam a orientação dos pontos em gestos específicos com alta precisão."),
                    cls="step-card"
                ),
                Div(
                    NotStr('<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="step-icon"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>'),
                    H4("Feedback Real-Time"),
                    P("Processamento de baixa latência que entrega resultados instantâneos e métricas de performance direto na sua tela."),
                    cls="step-card"
                ),
                cls="steps-grid"
            ),
            cls="how-it-works",
            id="how-it-works"
        ),

        Div(cls="snake-divider"),

        # Rodapé e links sociais
        Div(
            Div(
                P("© 2026 Rockit Vision. Desenvolvido durante a NLW Operator."),
                P("Por Arthur Ramiro Martins"),
                Div(
                    A(
                        NotStr('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>'),
                        href="https://github.com/ArthurRamiro", target="_blank", cls="social-link"
                    ),
                    A(
                        NotStr('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/></svg>'),
                        href="https://www.linkedin.com/in/arthur-ramiro-4011322a1/", target="_blank", cls="social-link"
                    ),
                    cls="social-links"
                ),
                cls="footer-content"
            ),
            cls="app-footer",
            id="footer"
        ),

        cls="app-container"
    )

# Rota WebSocket para processamento em tempo real
@app.ws("/ws")
async def ws(image: str, draw_landmarks: bool, send):
    try:
        # print(f"Frame recebido - Tamanho: {len(image)}")
        img = decode_image(image)
        if img is not None:
            processed_img, labels, gesture_image = processor.process_frame(img, draw_landmarks)
            fps = fps_tracker.update()
            await send(json.dumps({
                "image": encode_image(processed_img),
                "labels": labels,
                "gesture_image": gesture_image,
                "fps": fps
            }))
    except Exception as e:
        print(f"Erro no WebSocket do servidor: {e}")

if __name__ == "__main__":
    serve()
