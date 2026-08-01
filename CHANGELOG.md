# Changelog

## [1.1.0] - 2026-08-01
### Added
- Novo modulo de previsao e overlay de desgaste de pneus (TyrePredictor e TyreOverlayApp).

### Fixed
- Removido codigo morto e quebrado (`from_bytes`) dentro da funcao `process_packet` que chamava objeto inexistente.
- Corrigido problema estrutural na leitura UDP do F1 24/25: a variavel `m_currentLapNum` agora e lida corretamente do byte 33 (e `m_lapDistance` do 20), corrigindo o bug onde o overlay de pneus ficava travado em "Aguardando volta completa..." por nao detectar a transicao das voltas.
