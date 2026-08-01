# F1 Setups Assist - Assistente Universal de Setups

*[Read in English / Ler em Inglês (README.md)](README.md)*

Aplicativo local para **F1 25** projetado como um Assistente Universal de Setups. O sistema extrai automaticamente os melhores setups competitivos online e permite que o jogador aplique **Perfis de Conducao** (Esports, Gamepad ou Acessibilidade para Distonia Focal). Ele também exibe um HUD flutuante no jogo que le sua telemetria para saber em qual pista você está.

## 📦 Como Usar (Para Jogadores)

**A maneira mais fácil de usar o F1 Setups Assist é baixando o Executável:**

1. Vá na aba **[Releases](https://github.com/norisilva/f1-setups-assist/releases)** deste repositório.
2. Baixe o arquivo `F1SetupsAssist.exe`.
3. Coloque em sua área de trabalho e dê um duplo clique nele.
4. Uma Janela de Controle aparecerá!

### Usando o Painel de Controle
- **Baixar Setups:** Clique no primeiro botão para que o sistema baixe os setups mais recentes da nuvem (Usa F1Laps, com fallback para SimRacingSetup caso seja bloqueado pelo Cloudflare).
- **Configurar Perfil de Condução:** Clique na Engrenagem para escolher o seu modo. Você pode usar os setups "Esports" crus, suavizá-los para quem joga no "Gamepad", ou usar o modo máximo de "Acessibilidade" se você tiver dificuldades motoras (como Distonia Focal).
- **HUD no Jogo:** Clique em Iniciar HUD. Uma telinha transparente vai aparecer sobre o seu jogo!

## 🏎️ Configuracao no F1 25

Para que o Overlay identifique em qual pista você está correndo, a telemetria do jogo precisa estar ativa:
1. Abra o F1 25
2. Vá em **Settings** > **Telemetry Settings**
3. **UDP Telemetry**: On
4. **UDP Port**: `20777`
5. **UDP Send Rate**: 10Hz a 20Hz é suficiente (para não sobrecarregar a rede)
6. **UDP Format**: `2025`

> [!CAUTION]
> **Cuidado com outros softwares de telemetria!**
> Se você possui o aplicativo oficial do F1Laps instalado no seu computador, **ele precisa estar fechado** antes de abrir o nosso HUD. O aplicativo F1Laps original monopoliza a porta 20777 do Windows, impedindo que os dados cheguem até o nosso Assistente.

## 💻 Para Desenvolvedores (Como compilar)

Se você quer modificar o código e rodar a partir do Python:

1. Clone o repositório
2. Instale as dependências: 
```bash
pip install -r requirements.txt
playwright install chromium
```
3. Execute `python main.py` para abrir o painel.
4. Para compilar você mesmo o arquivo executável final, dê um duplo clique no `build.bat`! (O script usará o PyInstaller para empacotar a aplicação).

## Estrutura do Projeto
* `scraper/`: Scripts do Playwright responsáveis por navegar, driblar anti-bots e extrair setups.
* `transformer/`: O "cérebro" das regras de acessibilidade e suavização matemática.
* `overlay/`: Servidor UDP e Janela Always-on-top em Tkinter.
* `data/`: Onde os arquivos JSON resultantes e as suas regras pessoais (`rules.json`) ficam salvos.
