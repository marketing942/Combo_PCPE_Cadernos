# Combo Bizurado Digital — PCPE

Página de venda do combo da Polícia Civil de Pernambuco (Resumo Bizurado +
Caderno Tático de Questões + Vade Mecum Tático), lançada com o edital da PCPE.
É um clone do combo PMPE (`../comboPMPE`): mesma estrutura, mesmo preço, mesmo
tracking. O destaque passou do vermelho para o azul das capas da PCPE; o preço
da parcela continua no vermelho de promoção (`--promo`).

**Fluxo:** clique no CTA → checkout direto, sem formulário.

## O que muda em relação ao PMPE

| | Valor |
|---|---|
| Checkout | `https://checkout.cppem.com.br/pay/combo-curso-apostila-caderno-de-questoes-vade-mecum-pcpe` |
| Preço | De R$ 189,00 · 12x de R$ 14,60 · ou R$ 139,90 à vista (-26%) |
| `utm_campaign` de fallback | `combo_pcpe` |
| Evento `iniciar_checkout` | `produto: combo_bizurado_pcpe`, `valor: 139.9` |
| Chave de origem no storage | `cppem_origem_combo_pcpe` |
| Exit popup | `prefix: cppem_combo_pcpe`, `origem: exit_popup_combo_pcpe` (aba `APOSTILA_COMUNIDADE`) |

O botão do hero mantém o id `IPEyzyfmJhKQEYIXAlZH` da regra de clique da PixelX.

## Assets

As capas originais ficam em `_src/` (800×800, tablet centralizado). Tudo o que a
página usa é gerado delas:

```
python _build_assets.py
```

- `combo.webp`: os três tablets em leque (hero e oferta)
- `combo-resumo.webp`, `combo-questoes.webp`, `combo-vade.webp`: capas dos cards
- `og-combo.jpg`: 1200×630 para compartilhamento
- `brasao-pcpe.png`: brasão recortado da capa do Caderno, fundo transparente, 240px de altura

Para trocar uma capa: substitua o arquivo em `_src/` (`resumo.png`,
`questoes.png`, `vade.png`) e rode o script de novo. Se uma faltar, o script
gera uma capa provisória escrita "capa pendente".

## Checklist antes do disparo

- [ ] Checkout abrindo com UTMs e `external_id`
- [ ] Preço conferido: 12x R$ 14,60 · R$ 139,90 à vista (topo, oferta, barra fixa e rodapé)
- [ ] Regra de clique da PixelX disparando neste domínio
- [ ] Popup de saída testado com `ExitPopup.show()`
