"""Núcleo algorítmico da Codificação de Huffman (byte a byte).

Responsável por:
- Contabilizar frequências de cada símbolo do alfabeto de bytes (0 a 255).
- Definir a estrutura de nós da árvore binária (`Node`) com ordenação determinística
  para uso na fila de prioridade (`heapq`).
- Construir a árvore de Huffman de forma reproduzível entre compactador e
  descompactador.
- Gerar a tabela de códigos prefix-free (`dict[int, str]`).
"""

from __future__ import annotations

from collections import Counter
import heapq


class Node:
    """Nó de uma árvore binária de Huffman.

    Um nó folha representa um símbolo do alfabeto (`simbolo` entre 0 e 255, com
    `esquerda` e `direita` iguais a `None`). Um nó interno representa a fusão de
    duas subárvores (`simbolo` é `None`).

    Critério de desempate determinístico:
    Para garantir que compactador e descompactador construam exatamente a mesma
    árvore a partir apenas das frequências do cabeçalho, comparações entre nós de
    mesma `frequencia` desempatam por `menor_simbolo` presente na subárvore do nó.
    Como os conjuntos de folhas dos nós simultaneamente no heap são sempre disjuntos,
    esse critério garante uma ordenação estrita e 100% determinística.

    Attributes:
        frequencia: Frequência acumulada do símbolo ou da subárvore.
        simbolo: Valor do byte (0..255) para folhas, ou `None` para nós internos.
        esquerda: Filho à esquerda (convencionado como bit `'0'`).
        direita: Filho à direita (convencionado como bit `'1'`).
        menor_simbolo: Menor valor de símbolo (0..255) contido nesta subárvore,
            usado como critério determinístico de desempate no `heapq`.
    """

    def __init__(
        self,
        frequencia: int,
        simbolo: int | None = None,
        esquerda: Node | None = None,
        direita: Node | None = None,
    ) -> None:
        """Inicializa um nó folha ou nó interno da árvore de Huffman.

        Contrato:
        - `frequencia` deve ser um inteiro estritamente positivo (`> 0`).
        - Se `simbolo` não for `None`, trata-se de folha (`0 <= simbolo <= 255`) e
          `menor_simbolo` é igual a `simbolo`.
        - Se `simbolo` for `None`, trata-se de nó interno (com ambos os filhos
          presentes) e `menor_simbolo` é `min(esquerda.menor_simbolo, direita.menor_simbolo)`.

        Args:
            frequencia: Contagem positiva de ocorrências associada ao nó.
            simbolo: Byte (0..255) para nó folha, ou `None` para nó interno.
            esquerda: Subárvore à esquerda (bit `'0'`).
            direita: Subárvore à direita (bit `'1'`).

        Raises:
            ValueError: Se a frequência não for positiva, o símbolo estiver fora
                de `0..255` ou um nó interno não tiver ambos os filhos.
        """
        if frequencia <= 0:
            raise ValueError("A frequência de um nó deve ser um inteiro positivo.")

        self.frequencia = frequencia
        self.simbolo = simbolo
        self.esquerda = esquerda
        self.direita = direita

        if simbolo is not None:
            if not (0 <= simbolo <= 255):
                raise ValueError(f"Símbolo fora do intervalo de byte (0..255): {simbolo}")
            self.menor_simbolo = simbolo
        else:
            if esquerda is None or direita is None:
                raise ValueError(
                    "Nó interno deve possuir ambos os filhos (esquerda e direita)."
                )
            self.menor_simbolo = min(esquerda.menor_simbolo, direita.menor_simbolo)

    def eh_folha(self) -> bool:
        """Indica se o nó é uma folha (armazena um símbolo do alfabeto).

        Returns:
            `True` se `self.simbolo is not None`, caso contrário `False`.
        """
        return self.simbolo is not None

    def __lt__(self, outro: Node) -> bool:
        """Define a relação de ordem usada pelo `heapq` na construção da árvore.

        Contrato:
        - Ordena primeiramente por `self.frequencia < outro.frequencia`.
        - Em caso de empate na frequência, desempata deterministicamente usando
          `self.menor_simbolo < outro.menor_simbolo`.

        Args:
            outro: Outro objeto `Node` a ser comparado.

        Returns:
            `True` se `self` tiver prioridade maior (deve sair antes do min-heap)
            do que `outro`.
        """
        if self.frequencia != outro.frequencia:
            return self.frequencia < outro.frequencia
        return self.menor_simbolo < outro.menor_simbolo


def contar_frequencias(dados: bytes) -> dict[int, int]:
    """Conta a frequência absoluta de cada byte presente na sequência de entrada.

    Contrato:
    - Percorre `dados` byte a byte (valores inteiros no intervalo `0..255`).
    - Inclui no dicionário retornado apenas símbolos com frequência > 0.
    - Para entrada vazia (`b""`), retorna um dicionário vazio `{}`.

    Args:
        dados: Conteúdo binário bruto do arquivo.

    Returns:
        Dicionário mapeando cada byte (`int` de 0 a 255) à sua contagem (`int`).
    """
    # Counter percorre a sequência de bytes em C (muito rápido para arquivos de
    # milhões de bytes) e dict() retorna um dicionário padrão {byte: contagem}.
    return dict(Counter(dados))


def construir_arvore(frequencias: dict[int, int]) -> Node | None:
    """Constrói a árvore de Huffman determinística usando uma min-heap (`heapq`).

    Contrato:
    - Caso de borda (0 símbolos): se `frequencias` estiver vazio, retorna `None`.
    - Caso de borda (1 símbolo): retorna um único nó folha contendo esse símbolo.
    - Caso geral (>= 2 símbolos):
      1. Insere todas as folhas no heap (`heapq.heapify`), respeitando a ordem
         determinística definida em `Node.__lt__`.
      2. Enquanto houver mais de um nó no heap, remove os dois menores nós
         (`no_esquerda`, `no_direita`), cria um nó interno com frequência igual à
         soma de ambos e o reinsere no heap.
      3. Retorna o único nó restante (raiz da árvore).

    Args:
        frequencias: Dicionário `{byte: frequencia}` com contagens positivas.

    Returns:
        Nó raiz (`Node`) da árvore de Huffman, ou `None` se não houver símbolos.
    """
    if not frequencias:
        return None

    # Ordenamos os itens por símbolo por clareza e legibilidade; mesmo sem isso,
    # Node.__lt__ já garante determinismo total na extração do min-heap.
    heap: list[Node] = [
        Node(frequencia=freq, simbolo=simbolo)
        for simbolo, freq in sorted(frequencias.items())
    ]
    heapq.heapify(heap)

    # Se houver apenas 1 símbolo (K = 1), o laço não executa e retornamos a folha única.
    while len(heap) > 1:
        no_esquerda = heapq.heappop(heap)
        no_direita = heapq.heappop(heap)

        no_pai = Node(
            frequencia=no_esquerda.frequencia + no_direita.frequencia,
            simbolo=None,
            esquerda=no_esquerda,
            direita=no_direita,
        )
        heapq.heappush(heap, no_pai)

    return heap[0]


def gerar_tabela_codigos(raiz: Node | None) -> dict[int, str]:
    """Gera a tabela de códigos prefix-free a partir da raiz da árvore de Huffman.

    Contrato:
    - Se `raiz` for `None` (arquivo vazio), retorna `{}`.
    - Se `raiz` for uma única folha (arquivo composto por apenas 1 símbolo distinto),
      associa esse símbolo ao código `"0"` (comprimento de 1 bit) para garantir que
      cada ocorrência produza bits graváveis no fluxo.
    - Para árvores com dois ou mais símbolos, percorre a árvore atribuindo `"0"`
      ao ramo esquerdo e `"1"` ao ramo direito.

    Args:
        raiz: Nó raiz da árvore de Huffman, ou `None`.

    Returns:
        Dicionário mapeando cada símbolo (`int` de 0 a 255) ao seu código binário
        em formato de string composta por `'0'` e `'1'`.
    """
    if raiz is None:
        return {}

    # Caso degenerado (K = 1): apenas 1 símbolo distinto recebe código "0" de 1 bit.
    if raiz.eh_folha():
        assert raiz.simbolo is not None
        return {raiz.simbolo: "0"}

    tabela: dict[int, str] = {}

    def _percorrer(no: Node, prefixo: str) -> None:
        if no.eh_folha():
            assert no.simbolo is not None
            tabela[no.simbolo] = prefixo
            return

        if no.esquerda is not None:
            _percorrer(no.esquerda, prefixo + "0")
        if no.direita is not None:
            _percorrer(no.direita, prefixo + "1")

    _percorrer(raiz, "")
    return tabela
