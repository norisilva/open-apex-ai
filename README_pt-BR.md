# OpenApex AI

**Engenheiro de Corrida com IA e Hub de Telemetria Open-Source para Simuladores de F1**

O OpenApex AI (anteriormente F1 Setups Assist) é uma ferramenta moderna e de código aberto projetada para sim racers que querem elevar sua gameplay. Ele fornece previsões inteligentes de desgaste de pneus, overlays de setups ao vivo e ajustes de acessibilidade orientados por telemetria para F1 24 e F1 25.

## 🚀 Funcionalidades

- **HUD Inteligente de Pneus (IA):** Rastreamento de degradação de pneu em tempo real com previsões matemáticas de desgaste para estimar a janela ideal de pit stops.
- **Overlay de Setups ao Vivo:** Detecta automaticamente a pista atual e exibe seu setup predefinido diretamente na tela como um HUD transparente.
- **Zero Roubo de Foco:** Manipulação avançada de geometria de interface (OS) garante que os overlays apareçam sem nunca roubar o foco ou minimizar o seu jogo.
- **Transformador de Acessibilidade:** Ajusta os arquivos de configuração de hardware do jogo dinamicamente (XML) para fornecer estabilidade máxima para jogadores de controle/gamepad.
- **Multilíngue (i18n):** Suporte nativo para Português, Inglês, Espanhol, Alemão, Hindi e Árabe.
- **Hotkeys Customizáveis:** Mapeie facilmente os controles do HUD para o seu volante ou pedais usando o gerenciador de hotkeys embutido.

## 📥 Instalação

**A maneira mais fácil de usar o OpenApex AI é baixando o Executável:**
1. Acesse a página de [Releases](https://github.com/norisilva/open-apex-ai/releases).
2. Baixe o arquivo `OpenApexAI.exe` mais recente.
3. Coloque em uma pasta de sua escolha e execute-o.

*Nota: Você pode precisar autorizar o aplicativo no Windows Defender, já que o `.exe` é gerado via PyInstaller sem um certificado digital empresarial.*

## 🔧 Rodando a partir do Código-Fonte

Se você prefere rodar o código Python diretamente:

1. Clone o repositório:
   ```cmd
   git clone https://github.com/norisilva/open-apex-ai.git
   ```
2. Instale as dependências:
   ```cmd
   pip install -r requirements.txt
   ```
3. Execute o aplicativo:
   ```cmd
   python main.py
   ```

## 🤝 Como Contribuir

Contribuições são bem-vindas! Se você tiver ideias para novos módulos de IA/telemetria, suporte a novos jogos ou melhorias de interface, fique à vontade para abrir uma issue ou enviar um Pull Request.

## 📄 Licença

Este projeto é de código aberto e está disponível sob a Licença MIT.
