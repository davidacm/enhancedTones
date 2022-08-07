# Extra de tons aprimorados para o NVDA.

Este extra muda a maneira como  os tons no NVDA são gerados.
Para estar em contexto. Quando o NVDA emite um tom, ele faz o seguinte:

1. abre o player.
2. gera o tom.
3. envia o tom gerado para o player.
4. fecha o player.

Isso pode ser problemático em algumas placas de som, apresentando alta latência ao reproduzir os tons ou não reproduzindo os primeiros tons.
Eu tive esse problema no passado com um dos meus computadores. E essa foi a razão para criar este extra.

Se usar este extra, mesmo que não tenha problemas com a forma original, poderá ver que os tons são mais fluidos, especialmente em tons que se repetem rapidamente.

Este extra usa uma thread para enviar os tons para o player, e o player nunca fecha.
Além disso, este extra implementa um gerador de tom personalizado, que é definido por padrão. Mas pode trocá-lo pelo gerador de tons do NVDA.
O meu gerador de tons personalizado é escrito puramente em Python. Portanto, é menos eficiente que o gerador de tons do NVDA, mas a diferença não é perceptível.

Decidi manter meu gerador de tons porque algumas pessoas gostaram, inclusive eu. Um utilizador com perda auditiva relatou que estava mais confortável com meu gerador de tons.

Nota. A geração de tons não é o mesmo que a função para emitir os tons. Portanto, mesmo se usar o gerador de tons nativo do NVDA, poderá observar as melhorias.

## Faça o download.
\tA versão mais recente está disponível em
[este link] (https://davidacm.github.io/getlatest/gh/davidacm/EnhancedTones)

## Requisitos
  Precisa do NVDA 2018.3 ou posterior.

## Instalação
  Basta instalá-lo como um extra do NVDA.

## Utilização
  A funcionalidade do extra será activada assim que o instalar.  
  Para activá-la ou desactivá-la, acesse as configurações do NVDA e seleccione "tons aprimorados". Nessa categoria, pode definir os seguintes parâmetros:

* Activar o extra. Se desactivado, a função original será usada em seu lugar.
* Biblioteca para geração de tons.

## contribuições, relatórios e doações

Se gosta do meu projecto ou este softWare é útil na sua vida diária e quer contribuir de alguma forma, pode doar através dos seguintes métodos:

* [PayPal.] (https://paypal.me/davicm)
* [Ko-fi.] (https://ko-fi.com/davidacm)
* [criptomoedas e outros métodos.] (https://davidacm.github.io/donations/)

Se quiser corrigir bugs, relatar problemas ou novos recursos, entre em contato comigo em: <dhf360@gmail.com>.

  Ou no repositório github deste projeto:
  [Enhanced tones no GitHub](https://github.com/davidacm/enhancedtones)

    Pode obter a versão mais recente deste extra nesse repositório.

## Tradução:
  Equipa Portuguesa do NVDA: Ângelo Abrantes <ampa4374@gmail.com> e Rui Fontes <Rui Fontes <rui.fontes@tiflotecnia.com>
  Cascais, 6 de Agosto de 2022