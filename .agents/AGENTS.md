<RULE>
Ao trabalhar com o parser de telemetria (especialmente F1 24 e F1 25), sempre consulte a documentacao oficial em `docs/Data Output from F1 25 v3 (1).txt` para verificar estruturas de pacotes e offsets.

Lembre-se especificamente que, devido a adicao da parte de minutos nos tempos delta (F1 24/F1 25), a estrutura `LapData` mudou de tamanho. O offset para `m_currentLapNum` agora e 33 (antes era 31), e para `m_lapDistance` agora e 20 (antes era 18).
</RULE>
