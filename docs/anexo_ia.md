# Anexo de Uso de Inteligência Artificial

**Disciplina:** ENE0211 - Teoria da Informação (UnB)  
**Projeto:** Compactador e descompactador de arquivos via Codificação de Huffman (`ene0211-huffman`)  
**Dupla:** Antonio Leonardo Souto Gomes (211027607) e Victor Girão (170164446)  
**Ferramenta utilizada:** Google Antigravity (agente em linha de comando)

---

## Como estamos usando a ferramenta

Decidimos usar o assistente como apoio de desenvolvimento e revisão, mas sem delegar o projeto inteiro de uma vez. Para conseguir acompanhar cada parte do código e estar preparado para a arguição oral, combinamos de trabalhar por etapas: primeiro montar só o esqueleto do projeto (com assinaturas, docstrings e `NotImplementedError`), depois implementar uma issue de cada vez com explicação detalhada antes de qualquer commit ou PR.

---

## Relato das etapas realizadas até o momento

### 25/11/2026 - Criação do repositório e da estrutura inicial (Antonio Leonardo)

Começamos pedindo ao assistente para inicializar o projeto `ene0211-huffman` em Python 3.10+ usando apenas a biblioteca padrão. A estrutura foi montada com o executável `meucompactador` (com `chmod +x`), os módulos em `src/` (`cli.py`, `huffman.py`, `bitstream.py` e `gerador.py`), o arquivo de testes em `tests/test_integridade.py`, a pasta `docs/`, `.gitignore` e `README.md`.

Nessa etapa nenhuma lógica foi implementada: todas as funções ficaram apenas com o contrato explicado na docstring e `raise NotImplementedError`. Também foram criados o repositório privado no GitHub, o commit inicial na branch `main` (`5cf89c9`), a branch `develop` e o convite de colaborador para o Victor (`@victorgiraoc`). Conferimos a sintaxe dos arquivos com `py_compile` e testamos os imports antes de seguir.

### 25/11/2026 - Organização das issues no GitHub (Antonio Leonardo)

Com o esqueleto pronto, usamos o assistente junto com a CLI do GitHub (`gh`) para criar as quatro labels do projeto (`core`, `io-binario`, `testes-corpus` e `relatorio-ia`), o milestone com o prazo final de 29/11/2026 e as 8 issues do trabalho, sendo 4 para cada integrante. A divisão foi pensada para que os dois mexam tanto na parte principal do compactador quanto nos experimentos e no relatório.

### 25/11/2026 - Implementação da Issue #1 em `src/huffman.py` (Antonio Leonardo)

Criamos a branch `feat/issue-1` a partir de `develop` e implementamos o módulo `src/huffman.py`, que cuida da contagem de frequências, da classe `Node`, da construção da árvore de Huffman com `heapq` e da geração da tabela de códigos.

Durante a revisão do código gerado, analisamos três pontos principais:
- Na função `contar_frequencias`, optamos por `dict(Counter(dados))` porque o `Counter` da biblioteca padrão roda em C e contou 5.000.000 de bytes em cerca de 61 ms, o que ajuda bastante quando formos rodar a fonte sintética.
- No método `Node.__lt__`, o desempate para frequências iguais foi feito usando `menor_simbolo` da subárvore. Como os nós presentes no heap ao mesmo tempo nunca compartilham símbolos, esse valor nunca empata e garante que compactador e descompactador construam exatamente a mesma árvore a partir das frequências do cabeçalho.
- No caso degenerado de apenas um símbolo distinto (`K = 1`), `gerar_tabela_codigos` devolve o código `"0"` de 1 bit em vez de uma string vazia, permitindo gravar bits no arquivo compactado.

Antes de commitar, rodamos verificações em memória cobrindo os casos de borda (0 bytes, 1 byte, 1.000.000 de bytes iguais e 256 bytes equiprováveis), determinismo com entradas em ordens diferentes, propriedade livre de prefixo, igualdade de Kraft e validações de erro na classe `Node`.

---

## Problemas e ajustes encontrados no uso da IA

### 1. Atribuição silenciosa de assignee no `gh` para convite pendente
Ao criar as issues #5 a #8 via `gh issue create --assignee victorgiraoc`, o comando terminou com código de saída `0` como se tudo tivesse funcionado. Porém, ao conferir a lista de issues com `gh issue list`, vimos que o campo `Assignee` das quatro issues tinha ficado vazio porque o Victor ainda não tinha aceito o convite de colaborador no repositório. Mantivemos o nome dele registrado no corpo de cada issue e deixamos o comando `gh issue edit` pronto para atribuir assim que ele aceitar o convite. Serviu de alerta para não confiar só no retorno de sucesso de scripts gerados automaticamente.

### 2. Diferença de nome de função entre o esqueleto e a descrição da Issue #1
No esqueleto inicial de `src/huffman.py`, a função responsável por montar o dicionário de códigos foi criada com o nome `gerar_tabela_codigos`, enquanto no texto da Issue #1 ela aparecia como `gerar_codigos`. Como estamos trabalhando em paralelo na dupla, essa diferença causaria erro de importação quando o `src/cli.py` fosse integrado. Identificamos o desalinhamento antes da implementação, mantivemos o contrato `gerar_tabela_codigos` já definido no arquivo e registramos a correspondência na issue para evitar confusão.
