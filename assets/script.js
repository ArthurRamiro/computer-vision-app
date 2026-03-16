// Função principal para inicializar a aplicação
function initApp() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    if (!video || !canvas) return;

    const ctx = canvas.getContext('2d');
    const tempCanvas = document.createElement('canvas');
    const tempCtx = tempCanvas.getContext('2d');
    let ws;

    // Solicita acesso à webcam
    navigator.mediaDevices.getUserMedia({
        video: {
            width: { ideal: 1280 },
            height: { ideal: 720 }
        }
    }).then(stream => {
        video.srcObject = stream;
        video.onloadedmetadata = () => {
            video.play().then(() => {
                if (video.videoWidth > 0 && video.videoHeight > 0) {
                    canvas.width = tempCanvas.width = video.videoWidth;
                    canvas.height = tempCanvas.height = video.videoHeight;
                    console.log("Câmera inicializada com sucesso:", video.videoWidth, "x", video.videoHeight);
                    initWS(); 
                } else {
                    console.error("Câmera retornou dimensões inválidas (0x0)");
                }
            }).catch(err => {
                console.error("Erro ao iniciar reprodução do vídeo:", err);
            });
        };
    }).catch(err => {
        console.error("Erro ao acessar a webcam:", err);
        const statusText = document.getElementById('status-text');
        if (statusText) statusText.textContent = "Erro: Acesso à câmera negado";
    });

    // Função para inicializar a conexão WebSocket
    function initWS() {
        const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
        ws = new WebSocket(`${protocol}//${location.host}/ws`);
        console.log("Conectando ao WebSocket...");
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const img = new Image();
            img.onload = () => {
                ctx.drawImage(img, 0, 0);

                // Atualiza o contador de FPS
                const fpsCounter = document.getElementById('fps-counter');
                if (fpsCounter && data.fps !== undefined) {
                    fpsCounter.textContent = `FPS: ${data.fps}`;
                }

                // Atualiza o texto de status do reconhecimento
                const statusText = document.getElementById('status-text');
                if (statusText) {
                    statusText.textContent = data.labels.length > 0 ? "Gesto Detectado" : "Aguardando Gesto...";
                }

                // Atualiza a lista de gestos detectados (labels)
                const labelContainer = document.getElementById('gesture-container');
                if (labelContainer) {
                    if (data.labels.length === 0) {
                        labelContainer.innerHTML = '<div class="label-item"><span class="name">Nenhum gesto detectado</span></div>';
                    } else {
                        labelContainer.innerHTML = data.labels.map(l =>
                            `<div class="label-item">
                                <span class="name">${l.hand}: ${l.gesture}</span>
                                <span class="prob">${(l.probability * 100).toFixed(1)}%</span>
                             </div>`
                        ).join('');
                    }
                }

                // Atualiza a imagem demonstrativa do gesto
                const gestureImg = document.getElementById('gesture-image');
                if (gestureImg) {
                    if (data.gesture_image) {
                        gestureImg.src = `/assets/images/gestures/${data.gesture_image}`;
                        gestureImg.style.display = 'block';
                        gestureImg.classList.add('active-gesture');
                    } else {
                        gestureImg.style.display = 'none';
                        gestureImg.classList.remove('active-gesture');
                    }
                }

                sendFrame(); // Envia o próximo frame após processar o anterior
            };
            img.src = data.image;
        };

        ws.onopen = () => {
            console.log("Conexão WebSocket aberta");
            sendFrame();
        };

        ws.onclose = () => {
            console.warn("Conexão WebSocket fechada. Tentando reconectar...");
            setTimeout(initWS, 1000);
        };

        ws.onerror = (err) => {
            console.error("Erro no WebSocket:", err);
        };
    }

    // Controles de qualidade e configurações
    const qualitySlider = document.getElementById('quality-slider');
    const qualityValue = document.getElementById('quality-value');
    const drawLandmarksCb = document.getElementById('draw-landmarks-cb');
    
    if (!drawLandmarksCb) console.warn("Aviso: Checkbox 'draw-landmarks-cb' não encontrado no DOM");
    
    let currentQuality = 0.6;

    if (qualitySlider && qualityValue) {
        qualitySlider.oninput = function () {
            currentQuality = parseFloat(this.value);
            qualityValue.textContent = Math.round(currentQuality * 100) + '%';
        };
    }

    // Função para capturar e enviar frames da câmera
    function sendFrame() {
        if (ws && ws.readyState === WebSocket.OPEN) {
            tempCtx.drawImage(video, 0, 0);
            const drawLandmarks = (drawLandmarksCb && drawLandmarksCb.checked !== undefined) ? drawLandmarksCb.checked : true;
            ws.send(JSON.stringify({
                image: tempCanvas.toDataURL('image/jpeg', currentQuality),
                draw_landmarks: drawLandmarks
            }));
        }
    }

    // Lógica para destacar o item ativo no menu ao rolar a página
    const sections = ['vision', 'gestures', 'how-it-works'].map(id => document.getElementById(id));
    const navItems = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            if (section) {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                if (window.pageYOffset >= (sectionTop - 200)) {
                    current = section.getAttribute('id');
                }
            }
        });

        navItems.forEach(item => {
            item.classList.remove('active');
            if (item.getAttribute('href') === `#${current}`) {
                item.classList.add('active');
            }
        });
    });
}

// Inicializa a aplicação quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}

