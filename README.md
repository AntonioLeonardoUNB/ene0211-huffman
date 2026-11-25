# ENE0211 — Compactador e Descompactador de Huffman

Projeto da disciplina **ENE0211 — Teoria da Informação** (Universidade de Brasília — UnB): implementação de um compactador e descompactador de arquivos via linha de comando baseado em **Codificação de Huffman** em Python puro (utilizando exclusivamente a biblioteca padrão do Python 3.10+).

## Integrantes da Dupla

| Integrante | Matrícula | GitHub |
| :--- | :--- | :--- |
| Antonio Leonardo Souto Gomes | `211027607` | [@AntonioLeonardoUNB](https://github.com/AntonioLeonardoUNB) |
| Victor Girão | `170164446` | [@victorgiraoc](https://github.com/victorgiraoc) |

## Estrutura do Projeto

```text
ene0211-huffman/
├── meucompactador           # Executável CLI (./meucompactador -c / -d)
├── src/
│   ├── __init__.py
│   ├── cli.py               # Parse de argumentos (-c / -d) e exibição de métricas (H_hat, L, taxa)
│   ├── huffman.py           # Contagem de frequências, Node, árvore com heapq determinístico e códigos
│   ├── bitstream.py         # BitWriter, BitReader e cabeçalho binário com struct
│   └── gerador.py           # Fonte sintética (5.000.000 bytes, geométrica truncada) e entropia H(X)
├── tests/
│   ├── __init__.py
│   └── test_integridade.py  # Testes unittest dos 4 casos de borda com validação SHA-256
├── docs/                    # Rascunhos do relatório analítico e anexo de uso de IA
├── .gitignore
└── README.md
```

## Requisitos

- **Python 3.10+**
- Nenhuma dependência externa (somente biblioteca padrão: `argparse`, `heapq`, `struct`, `hashlib`, `math`, `random`, `unittest`, `pathlib`, etc.).

## Instruções de Uso

### Compactar um arquivo

```bash
./meucompactador -c caminho/para/arquivo
```

Gera o arquivo `caminho/para/arquivo.huff` e exibe no terminal:
- Entropia empírica estimada ($\hat{H}$) em bits/símbolo;
- Comprimento médio ($L$) em bits/símbolo;
- Taxa de compressão.

### Descompactar um arquivo

```bash
./meucompactador -d caminho/para/arquivo.huff
```

Restaura o arquivo original a partir do cabeçalho binário (`b'HUFF'`) e da tabela de frequências embarcada.

### Executar os testes de integridade

```bash
python3 -m unittest discover -s tests -v
```

Os testes cobrem os 4 casos de borda obrigatórios comparando o hash **SHA-256** entre o arquivo original e o descompactado:
1. Arquivo vazio (`0` bytes);
2. Arquivo com `1` byte;
3. Arquivo com `1.000.000` de bytes de um único símbolo;
4. Arquivo com `256` bytes equiprováveis (`0x00` a `0xFF`).

## Fluxo de Branches

- `main`: branch principal estável (entregas e marcos consolidados).
- `develop`: branch base de integração para desenvolvimento contínuo da dupla.
