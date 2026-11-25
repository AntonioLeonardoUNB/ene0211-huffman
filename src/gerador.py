"""Gerador de fonte sintética discreta sem memória e cálculo de entropia teórica.

Gera um arquivo binário de 5.000.000 de bytes seguindo a distribuição geométrica
truncada no alfabeto de bytes {0, 1, ..., 255}, parametrizada pelas matrículas da
dupla da disciplina ENE0211 (Teoria da Informação - UnB):
- Antonio Leonardo Souto Gomes: 211027607
- Victor Girão: 170164446
"""

from pathlib import Path

MATRICULA_INTEGRANTE_1: int = 211027607
MATRICULA_INTEGRANTE_2: int = 170164446
TAMANHO_FONTE_PADRAO: int = 5_000_000
TAMANHO_ALFABETO: int = 256


def derivar_parametros_matriculas(
    matricula_1: int = MATRICULA_INTEGRANTE_1,
    matricula_2: int = MATRICULA_INTEGRANTE_2,
) -> tuple[float, int]:
    """Deriva o parâmetro `p` da distribuição geométrica e a semente aleatória.

    Contrato:
    - Utiliza as matrículas da dupla conforme a especificação da disciplina ENE0211
      para determinar:
      1. O parâmetro `p` (0 < p < 1) da distribuição geométrica truncada;
      2. A semente (`seed`) inteira para o gerador pseudoaleatório (`random.Random`),
         garantindo reprodutibilidade experimental.

    Args:
        matricula_1: Matrícula UnB do primeiro integrante.
        matricula_2: Matrícula UnB do segundo integrante.

    Returns:
        Tupla `(p, seed)` com o parâmetro da distribuição e a semente reprodutível.
    """
    raise NotImplementedError("Implementar derivação de (p, seed) a partir das matrículas.")


def calcular_distribuicao_geometrica_truncada(
    p: float,
    tamanho_alfabeto: int = TAMANHO_ALFABETO,
) -> list[float]:
    """Calcula a função massa de probabilidade (FMP) da geométrica truncada.

    Contrato:
    - Para cada símbolo k em {0, 1, ..., M - 1} (com M = `tamanho_alfabeto`):
        P(X = k) = ((1 - p) ** k * p) / (1 - (1 - p) ** M)
    - Valida que `0 < p < 1` e `tamanho_alfabeto >= 1`.
    - Garante que as probabilidades sejam positivas e somem 1.0 (dentro da precisão
      de ponto flutuante).

    Args:
        p: Parâmetro de sucesso da distribuição geométrica (0 < p < 1).
        tamanho_alfabeto: Cardinalidade M do alfabeto (padrão: 256).

    Returns:
        Lista de `tamanho_alfabeto` probabilidades ordenadas por símbolo k = 0..M-1.
    """
    raise NotImplementedError("Implementar cálculo da distribuição geométrica truncada.")


def calcular_entropia_teorica(probabilidades: list[float]) -> float:
    """Calcula a entropia teórica de Shannon H(X) em bits por símbolo.

    Contrato:
    - Calcula:
        H(X) = -sum(p_k * log2(p_k)) para todo p_k > 0.
    - Ignora termos com probabilidade igual a 0 (convenção 0 * log2(0) = 0).

    Args:
        probabilidades: Distribuição de probabilidades discreta da fonte.

    Returns:
        Valor da entropia teórica H(X) em bits/símbolo.
    """
    raise NotImplementedError("Implementar cálculo da entropia teórica H(X).")


def gerar_fonte_sintetica(
    caminho_saida: Path,
    tamanho_bytes: int = TAMANHO_FONTE_PADRAO,
    matricula_1: int = MATRICULA_INTEGRANTE_1,
    matricula_2: int = MATRICULA_INTEGRANTE_2,
) -> dict[str, float | int]:
    """Gera o arquivo binário da fonte sintética e retorna os parâmetros teóricos.

    Contrato:
    - Obtém `(p, seed)` a partir das matrículas da dupla.
    - Calcula a distribuição geométrica truncada para os 256 símbolos e a entropia
      teórica `H(X)`.
    - Amostra `tamanho_bytes` símbolos independentes e identicamente distribuídos
      (i.i.d.) usando apenas a biblioteca padrão (`random.Random(seed)`), gravando
      os bytes resultantes em `caminho_saida`.
    - Retorna um resumo contendo `p`, `seed`, `tamanho_bytes` e `entropia_teorica`.

    Args:
        caminho_saida: Caminho do arquivo binário a ser criado.
        tamanho_bytes: Quantidade de bytes a gerar (padrão: 5.000.000).
        matricula_1: Matrícula UnB do primeiro integrante.
        matricula_2: Matrícula UnB do segundo integrante.

    Returns:
        Dicionário com os metadados da fonte gerada (`p`, `seed`, `tamanho_bytes`,
        `entropia_teorica`).
    """
    raise NotImplementedError("Implementar geração da fonte sintética de 5.000.000 bytes.")
