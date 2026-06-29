# Clone Flappy Bird

Projeto com fins educacionais para estudo de **game design** e **Pygame**.
Implementa um clone do Flappy Bird com física, colisão pixel-perfeita e
máquina de estados.

## Instalação

Requer [Python 3](https://python.org) e [Pygame](https://pygame.org).

```bash
pip install -r requirements.txt
python main.py
```

## Como jogar

| Tecla       | Ação        |
|-------------|-------------|
| Espaço / ↑  | Bater asas  |
| Esc         | Sair        |

## Arquitetura

```
src/
├── engine/
│   ├── jogo.py                    # Loop principal (init, eventos, update, render)
│   └── gerenciador_de_recursos.py # Carrega e gerencia imagens, sons, máscaras
├── entities/
│   ├── base.py                    # Chao — scroll infinito do chão
│   ├── pipe.py                    # Geração de pares de tubos
│   └── player.py                  # Jogador — física, animação, rotação
├── states/
│   ├── state_machine.py           # Estado (ABC) + MaquinaEstado
│   ├── welcome_state.py           # Tela inicial com pássaro oscilante
│   ├── play_state.py              # Gameplay: input, pontuação, colisão
│   └── gameover_state.py          # Tela de fim com queda do pássaro
└── systems/
    ├── collision.py               # Colisão pixel-perfeita via máscara alpha
    └── score.py                   # Renderiza pontuação com sprites de dígitos
```

**Fluxo de execução:**

1. `Jogo.executar()` inicia a `MaquinaEstado` no `EstadoBoasVindas`
2. A cada frame: processa eventos → atualiza estado atual → renderiza na tela
3. `EstadoBoasVindas` → (Espaço/↑) → `EstadoJogo` → (colisão) → `EstadoFimDeJogo`
4. Em `EstadoFimDeJogo`, Espaço/↑ após cair no chão reinicia em `EstadoBoasVindas`
