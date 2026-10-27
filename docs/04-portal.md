# 4. Tela do Portal do Cliente (RF10)

## Estados da tela

<!-- A tela é uma função do estado. Liste os estados possíveis da tela de
acompanhamento de um pedido e o que o cliente vê em cada um. -->

## Estados da tela

| Estado | Dados disponíveis | O que a tela exibe |
|---|---|---|
| **Em rota, no prazo** | Posição do veículo (lat/lng), previsão de chegada original. | Mapa com o ícone do veículo atualizado, cronograma de entrega na cor verde e texto de previsão de chegada normal. |
| **Em rota, atrasado** | Posição do veículo, previsão de chegada atualizada, tempo de atraso. | Mapa com alerta visual (ex: ícone do veículo amarelo/vermelho), banner informando o atraso e cronômetro de tempo excedido rodando. |
| **Entregue (Apurando)** | Status de entrega confirmado, horário exato de chegada. | Mensagem de "Pedido Entregue" e um *loader/spinner* na área de Garantia informando "Apurando elegibilidade de crédito..." (cobrindo o tempo do RNF02). |
| **Entregue (Com Crédito)** | Saldo calculado de crédito, número da nota fiscal gerada. | Banner de desculpas pelo atraso, valor do crédito concedido em destaque e o número sequencial da nota de crédito para conferência. |

## Árvore de componentes

```jsx
<AcompanhamentoPedido pedidoId="{id}" tipoCliente="{tipo}">
  <MapaInterativo coordenadas="{geo}" statusAtraso="{status}"/>
  <PainelPrevisao previsaoChegada="{data}" tempoAtraso="{horas}"/>
  <CardGarantia numeroNota="{numero}" saldoCredito="{valor}" statusProcessamento="{status}"/>
</AcompanhamentoPedido>

| Componente | Props recebidas | Responsabilidade |
|---|---|---|
| `<AcompanhamentoPedido>` | `pedidoId`, `tipoCliente` | Container raiz. Responsável por iniciar a conexão WebSocket/SSE, manter o estado global da tela e distribuir os dados aos componentes filhos. |
| `<MapaInterativo>` | `coordenadas`, `statusAtraso` | Renderizar o mapa interativo e plotar o pino do veículo que se move ao vivo, alterando o estado visual caso haja atraso. |
| `<PainelPrevisao>` | `previsaoChegada`, `tempoAtraso` | Exibir o horário estimado de entrega e, se o prazo original for rompido, exibir o alerta com o tempo de atraso acumulado. |
| `<CardGarantia>` | `saldoCredito`, `numeroNota`, `statusProcessamento` | Gerenciar a UI da garantia. Exibe um *loader* enquanto aguarda o cálculo e, após concluído, exibe o saldo do crédito e a nota fiscal. |

## Origem dos dados

* **Posição do veículo:** Chega ao vivo (a cada 30s) diretamente do serviço de **Telemetria** via conexão persistente (*WebSocket* ou *Server-Sent Events - SSE*), sem necessidade de *polling*.
* **Previsão de chegada:** Consumida na montagem da tela via chamada REST (HTTP GET) ao serviço de **Frete**, podendo ser atualizada por eventos push (SSE/WS) caso a rota do motorista mude.
* **Saldo de créditos e Nota:** Assim que a entrega é confirmada, o serviço de **Garantia de Prazo** processa a regra e envia um evento via WebSocket/SSE para o navegador contendo o valor final do crédito e o número da nota gerada pelo Faturamento, atualizando o `<CardGarantia>` reativamente ao vivo na tela do cliente.

<!-- De onde vem cada dado da tela e como a atualização ao vivo chega ao navegador. -->
