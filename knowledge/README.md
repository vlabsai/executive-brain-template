# Conhecimento revisado

Esta pasta guarda seu perfil e as notas que você conferiu, com origem e pendências.

A entrevista cria perfil.md preenchido com seu papel, objetivo e preferências. As pastas de [empresas](empresas/README.md), [pessoas](pessoas/README.md), [projetos](projetos/README.md), [reuniões](reunioes/README.md) e [temas](temas/README.md) já vêm preparadas. Seus READMEs explicam o uso; as notas são criadas conforme houver conteúdo. Notas anteriores na raiz continuam válidas.

## Convenções das notas

Novas notas revisadas têm duas propriedades simples:

```yaml
---
id: 71422ee1-63af-45d7-9126-e7905bf8f360
domains: [empresa-exemplo]
---
```

O assistente gera o id uma vez e o preserva ao atualizar ou mover a nota. domains é uma lista curta de contextos, como pessoal ou o nome de uma empresa. Reutilize os nomes já usados; uma pessoa pode pertencer a vários contextos. Domínio organiza informações, não controla acesso. O tipo é dado pela pasta; não precisa de outro cadastro.

No corpo: título humano, conteúdo útil, relações, origem e revisão efetivamente realizada. Datas desconhecidas e pendências continuam identificadas; não complete campos com suposições. Uma síntese de reunião guarda as decisões daquele momento; o projeto aponta para ela e mantém o estado atual, sem copiar a transcrição inteira.

Use links Markdown relativos, por exemplo `[Projeto Alfa](../projetos/projeto-alfa.md)`, e ligue apenas notas existentes e relações sustentadas pelas fontes. A origem pode estar em [inbox](../inbox/README.md) ou em uma localização autorizada. Antes de criar, procure a entidade e a origem nas notas existentes. Receber novamente a mesma ata atualiza ou confirma sua nota; não cria outra reunião. Ao renomear, preserve o id e corrija os links que apontam para o destino anterior.

A consulta indexa somente notas revisadas desta pasta, excluindo READMEs. Fontes e propostas em inbox/ ficam fora da busca de conhecimento aceito.
