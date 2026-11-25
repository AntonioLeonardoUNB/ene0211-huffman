"""Interface de linha de comando (CLI) e orquestração da compactação/descompactação.

Responsável por:
- Interpretar argumentos de linha de comando (`-c` para compactar, `-d` para descompactar)
  utilizando `argparse`.
- Coordenar os módulos `src.huffman` e `src.bitstream` nos fluxos de compressão e
  descompressão.
- Calcular e exibir as métricas exigidas pela disciplina:
  * Entropia empírica estimada (H_hat), em bits/símbolo;
  * Comprimento médio do código (L), em bits/símbolo;
  * Taxa de compressão.
"""

import argparse
from pathlib import Path


def criar_parser() -> argparse.ArgumentParser:
    """Cria e configura o parser de argumentos da linha de comando.

    Contrato:
    - Deve definir um grupo mutuamente exclusivo e obrigatório com as opções:
      * `-c` / `--compactar`: caminho do arquivo de entrada a ser compactado.
      * `-d` / `--descompactar`: caminho do arquivo `.huff` a ser descompactado.
    - Opcionalmente pode aceitar `-o` / `--saida` para sobrescrever o caminho de
      saída padrão (`<arquivo>.huff` na compactação ou remoção do sufixo `.huff`
      na descompactação).

    Returns:
        Instância configurada de `argparse.ArgumentParser`.
    """
    raise NotImplementedError("Implementar configuração do parser argparse.")


def calcular_metricas(
    frequencias: dict[int, int],
    tabela_codigos: dict[int, str],
    tamanho_original: int,
    tamanho_compactado: int,
) -> dict[str, float]:
    """Calcula as métricas de desempenho da codificação de Huffman.

    Contrato:
    - Entropia empírica estimada (H_hat):
        H_hat = -sum(p_i * log2(p_i)), onde p_i = freq_i / tamanho_original.
      Para arquivo vazio (`tamanho_original == 0`), retorna 0.0.
    - Comprimento médio do código (L):
        L = sum(p_i * len(codigo_i)), em bits por símbolo (apenas payload codificado).
      Para arquivo vazio, retorna 0.0.
    - Taxa de compressão:
        Relação percentual ou razão entre `tamanho_compactado` (incluindo cabeçalho)
        e `tamanho_original`, tratando divisão por zero para arquivos vazios.

    Args:
        frequencias: Dicionário `{byte: contagem}` obtido do arquivo original.
        tabela_codigos: Dicionário `{byte: codigo_binario_str}` gerado pela árvore.
        tamanho_original: Tamanho do arquivo original em bytes.
        tamanho_compactado: Tamanho total do arquivo `.huff` gerado em bytes.

    Returns:
        Dicionário contendo as chaves `"entropia_estimada"`, `"comprimento_medio"`
        e `"taxa_compressao"`.
    """
    raise NotImplementedError("Implementar cálculo de H_hat, L e taxa de compressão.")


def exibir_metricas(
    entropia_estimada: float,
    comprimento_medio: float,
    taxa_compressao: float,
    tamanho_original: int,
    tamanho_compactado: int,
) -> None:
    """Imprime no terminal um resumo formatado das métricas da compactação.

    Contrato:
    - Deve exibir de forma legível:
      * Tamanho original (bytes) e tamanho compactado (bytes);
      * Entropia estimada H_hat (bits/símbolo);
      * Comprimento médio L (bits/símbolo);
      * Taxa de compressão.

    Args:
        entropia_estimada: Valor de H_hat em bits/símbolo.
        comprimento_medio: Valor de L em bits/símbolo.
        taxa_compressao: Taxa de compressão calculada.
        tamanho_original: Tamanho do arquivo original em bytes.
        tamanho_compactado: Tamanho do arquivo compactado em bytes.
    """
    raise NotImplementedError("Implementar formatação e impressão das métricas.")


def compactar_arquivo(
    caminho_entrada: Path,
    caminho_saida: Path | None = None,
) -> dict[str, float]:
    """Compacta um arquivo arbitrário para o formato binário `.huff`.

    Contrato:
    - Lê os bytes do arquivo `caminho_entrada` (validando existência).
    - Define `caminho_saida` como `<caminho_entrada>.huff` se não fornecido.
    - Conta frequências, constrói a árvore de Huffman e gera a tabela de códigos.
    - Serializa o cabeçalho binário (`src.bitstream.serializar_cabecalho`) e grava
      os bits codificados com `BitWriter`.
    - Trata corretamente casos de borda (0 bytes e arquivo com apenas 1 símbolo).
    - Calcula e exibe as métricas finais (H_hat, L e taxa de compressão).

    Args:
        caminho_entrada: Caminho do arquivo original.
        caminho_saida: Caminho opcional do arquivo `.huff` de destino.

    Returns:
        Dicionário com as métricas calculadas da compactação.
    """
    raise NotImplementedError("Implementar fluxo completo de compactação.")


def descompactar_arquivo(
    caminho_entrada: Path,
    caminho_saida: Path | None = None,
) -> Path:
    """Descompacta um arquivo `.huff`, restaurando exatamente os bytes originais.

    Contrato:
    - Lê o arquivo compactado `caminho_entrada` e desserializa o cabeçalho
      validando os magic bytes `b'HUFF'`.
    - Define `caminho_saida` removendo o sufixo `.huff` (ou usando padrão seguro)
      caso não seja fornecido.
    - Reconstrói a mesma árvore de Huffman determinística a partir das frequências
      armazenadas no cabeçalho.
    - Lê exatamente `tamanho_original` símbolos usando `BitReader`, descartando
      eventuais bits de preenchimento (padding) do último byte.
    - Trata corretamente arquivos de 0 bytes e arquivos de símbolo único.

    Args:
        caminho_entrada: Caminho do arquivo `.huff`.
        caminho_saida: Caminho opcional do arquivo restaurado.

    Returns:
        Caminho (`Path`) do arquivo descompactado gravado em disco.
    """
    raise NotImplementedError("Implementar fluxo completo de descompactação.")


def main(argv: list[str] | None = None) -> int:
    """Ponto de entrada principal da aplicação CLI.

    Contrato:
    - Faz o parse dos argumentos recebidos em `argv` (ou `sys.argv[1:]`).
    - Direciona para `compactar_arquivo` (`-c`) ou `descompactar_arquivo` (`-d`).
    - Captura erros esperados (arquivo inexistente, cabeçalho inválido) imprimindo
      mensagem clara em `stderr` e retornando código de saída diferente de zero.

    Args:
        argv: Lista opcional de argumentos (útil para testes automatizados).

    Returns:
        Código de saída do processo (`0` em caso de sucesso, não zero em erro).
    """
    raise NotImplementedError("Implementar função main da CLI.")
