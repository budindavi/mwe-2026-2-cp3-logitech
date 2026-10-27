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
| | | |

## Origem dos dados

<!-- De onde vem cada dado da tela e como a atualização ao vivo chega ao navegador. -->
