# 3. Plano de testes

## Pirâmide de testes

| Nível | Quantidade de casos | O que cobre |
|---|---|---|
| **Unidade** | Maioria (~70%) | Cobre as regras de negócio puras (cálculos de crédito, verificação de tetos, faixas de tempo de atraso, tipos de cliente). São testes rápidos, determinísticos e não dependem de banco de dados ou infraestrutura externa. |
| **Integração** | Média (~20%) | Cobre a persistência no banco de dados (ex: testar a idempotência de pedido único), a comunicação com filas de mensageria (ex: retentativas de notificação) e a integração com APIs (ex: Telemetria e parceiro de WhatsApp). |
| **Ponta a ponta** | Minoria (~10%) | Cobre o fluxo crítico completo: desde a emissão da confirmação do frete, passando pelo cálculo de crédito, até a emissão da nota fiscal e atualização do saldo no Portal do Cliente (WebSocket). |

## Casos de teste

| ID | Requisito | Pré-condição | Entrada | Resultado esperado | Nível | Dublê | Justificativa do dublê |
|---|---|---|---|---|---|---|---|
| CT01 | RF02 | Cliente Varejo, frete de R$ 100,00 | Atraso de 2h00 | Crédito de R$ 0,00 | Unidade | Nenhum | Regra de negócio pura e matemática. O limite inferior não gera crédito. |
| CT02 | RF02 | Cliente Varejo, frete de R$ 100,00 | Atraso de 2h01 | Crédito de R$ 10,00 | Unidade | Nenhum | Regra pura. Testa o primeiro minuto da faixa de 10%. |
| CT03 | RF02 | Cliente Varejo, frete de R$ 100,00 | Atraso de 24h00 | Crédito de R$ 10,00 | Unidade | Nenhum | Regra pura. Testa o limite superior exato da faixa de 10%. |
| CT04 | RF02 | Cliente Varejo, frete de R$ 100,00 | Atraso de 24h01 | Crédito de R$ 25,00 | Unidade | Nenhum | Regra pura. Testa a mudança exata para a faixa de 25%. |
| CT05 | RF02 | Cliente Varejo, frete de R$ 2.500,00 | Atraso de 73h00 | Crédito de R$ 500,00 | Unidade | Nenhum | Regra pura. O crédito seria R$ 1.250 (50%), mas valida a aplicação do teto de R$ 500. |
| CT06 | RF03 | Cliente Corporativo, frete R$ 100,00 | Atraso de 2h01 | Crédito de R$ 20,00 | Unidade | Nenhum | Regra pura. Valida o percentual dobrado (20% ao invés de 10%). |
| CT07 | RF03 | Cliente Corporativo, frete R$ 5.000,00 | Atraso de 73h00 | Crédito de R$ 2.000,00 | Unidade | Nenhum | Regra pura. Valida a aplicação do teto corporativo (limita os R$ 5.000 teóricos a R$ 2.000). |
| CT08 | RF03 | Cliente Cortesia, frete R$ 0,00 | Atraso de 48h00 | Crédito R$ 0,00, Evento de desculpa emitido | Unidade | Spy | Usa *Spy* no serviço de notificação para confirmar que foi chamado, já que não há retorno financeiro. |
| CT09 | RF05 | Cliente Varejo, elegível a crédito | Retorno da Telemetria = TRUE (ausência 10 min a 200m) | Crédito de R$ 0,00 | Integração | Stub | O *Stub* simula uma resposta positiva de ausência da Telemetria, isolando o teste sem depender da rede real. |
| CT10 | RF08 | Atraso gera crédito (necessita notificar) | Retorno HTTP 500 da API Externa 3 vezes | Mensagem enviada para Dead Letter Queue (DLQ) | Integração | Mock | O *Mock* da API força 3 erros sucessivos, permitindo verificar a lógica de *retry* e enfileiramento na DLQ. |
| CT11 | RF09 | Pedido ID 123 já processado com crédito | Nova confirmação de entrega do Pedido 123 | Recusa em silêncio, não gera novo crédito | Integração | Banco em memória | Testa a restrição de chave única (Unique Constraint) da tabela sem precisar subir um SGBD pesado. |
| CT12 | RF06, RNF03 | Sistema pronto para emissão | 1.000 requisições simultâneas para gerar nota | 1.000 notas geradas com números sequenciais únicos | Integração | Nenhum (DB Real / Testcontainers) | Exige um banco real gerenciando a *sequence* transacional para garantir que não haja concorrência (*race condition*). |

## Mutante que o plano detecta

| Mutante | Caso que o detecta | Por quê |
|---|---|---|
| Alterar a regra do Varejo de `if (atraso > 2)` para `if (atraso >= 2)` | CT01 | O mutante faria com que um atraso de exatas 2 horas (limite da tolerância) gerasse crédito indevido (ex: R$ 10,00). O plano detecta a falha porque o CT01 insere exatas 2h00 e exige que o retorno seja estritamente R$ 0,00. O teste passaria a quebrar, revelando o bug no código. |
