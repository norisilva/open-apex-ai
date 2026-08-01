# F1 Setups Assist - Acessibilidade para Distonia Focal

Aplicativo local para **F1 25** projetado especificamente para acessibilidade de jogadores com Distonia Focal no braco direito. O sistema extrai automaticamente os melhores setups online, aplica regras matematicas focadas em conforto e dirigibilidade (evitando snap oversteers e microcorrecoes excessivas), e exibe um Overlay flutuante que le sua telemetria para saber em qual pista voce esta.

## 🛠️ Requisitos

* Python 3.10 ou superior
* O projeto foi testado em ambiente Windows.

### Instalacao

1. Clone ou baixe este repositorio
2. Abra o terminal na pasta do projeto e instale as dependencias Python:
   ```bash
   pip install -r requirements.txt
   ```
3. Instale o navegador do Playwright (necessario para extracao de dados):
   ```bash
   python -m playwright install chromium
   ```

## 🏎️ Configuracao no F1 25

Para que o Overlay identifique em qual pista voce esta correndo, a telemetria do jogo precisa estar ativa:
1. Abra o F1 25
2. Va em **Settings** > **Telemetry Settings**
3. **UDP Telemetry**: On
4. **UDP Port**: `20777`
5. **UDP Send Rate**: 10Hz a 20Hz e suficiente (para nao sobrecarregar a rede)
6. **UDP Format**: `2025`

> [!WARNING]
> **Cuidado com outros softwares de telemetria!**
> Se voce possui o aplicativo oficial do F1Laps instalado no seu computador, **ele precisa estar fechado** antes de abrir o nosso Overlay (Opcao 3). O aplicativo F1Laps original monopoliza a porta 20777 do Windows, impedindo que os dados cheguem ate o nosso Assistente de Acessibilidade. Voce pode continuar logado na sua conta no navegador normalmente.

## 🚀 Como Usar

O projeto possui um menu unificado. No terminal, execute:

```bash
python main.py
```

Voce vera o seguinte menu interativo:
```text
========================================
 F1 SETUPS ASSIST - ACESSIBILIDADE      
========================================
1. Extrair setups do F1Laps (Scrape)
2. Aplicar motor de transformacao
3. Iniciar Telemetria e Overlay
4. Executar fluxo completo (1, 2 e 3)
0. Sair
========================================
```

### O que cada opcao faz?

* **Opcao 1**: Abre um navegador invisivel e extrai os setups da categoria "Race" mais rapidos do site F1Laps. Salva os dados brutos no arquivo `data/setups_originais.json`.
* **Opcao 2**: Le o arquivo original e aplica o fator de suavizacao matematico (ex: Suspensao fica 25% mais macia, Diferencial travado). O resultado e salvo em `data/setups_acessibilidade.json`.
* **Opcao 3**: Abre a janela transparente flutuante. Ao entrar na pista (Modo Time Trial ou Grand Prix), o sistema le a porta UDP e mostra imediatamente o setup macio calculado.
* **Opcao 4**: Faz todos os 3 passos acima de forma automatizada.

## 🔧 Como ajustar sua Acessibilidade (Tuning)

Se achar que o carro ainda esta agressivo ou que ficou macio demais, **nao e necessario alterar codigo complexo**.

1. Abra o arquivo `transformer/rules.py`
2. Modifique os valores desejados. Por exemplo:
   * Para suspensao mais agressiva: mude `"factor": 0.75` para `0.85`
   * Para limitar mais a saida de traseira: mude o on-throttle `"clamp_max": 52` para `50`
3. Salve o arquivo.
4. Execute `python main.py` e escolha a **Opcao 2**. O seu JSON sera recalculado instantaneamente.

## Estrutura do Projeto
* `scraper/`: Scripts do Playwright responsaveis por navegar, driblar anti-bots e extrair setups.
* `transformer/`: O "cérebro" das regras de acessibilidade e suavizacao matemática.
* `overlay/`: Servidor UDP e Janela Always-on-top em Tkinter.
* `data/`: Onde os arquivos JSON resultantes ficam salvos.
