
# Script de Extração de Texto PDF e NER Jurídico com Fabric

Este script Python automatiza o processo de extração de texto de um arquivo PDF, processamento desse texto usando um padrão [Fabric](https://github.com/danielmiessler/fabric) para Reconhecimento de Entidades Nomeadas (NER) focado no domínio jurídico, e salvamento das entidades extraídas em um arquivo JSON.

## Propósito

O objetivo principal é facilitar o uso de padrões Fabric que exigem entrada de texto (como o padrão `ner-juridico`) diretamente a partir de documentos PDF, que são comuns no ambiente jurídico. O script lida com a conversão PDF->TXT e a execução do comando Fabric.

## Pré-requisitos

Antes de executar o script, certifique-se de que você possui:

1.  **Python 3:** Instalado em seu sistema (inclui `argparse`).
2.  **Pip:** O gerenciador de pacotes do Python.
3.  **Biblioteca PyPDF2:** Instale usando pip:
    ```bash
    pip install PyPDF2
    ```
4.  **Fabric CLI:** O framework Fabric instalado e configurado. Siga as instruções de instalação no [repositório oficial do Fabric](https://github.com/danielmiessler/fabric). Isso inclui configurar o acesso a um modelo de linguagem (LLM) suportado (como OpenAI, Claude, Ollama, etc.).
5.  **Pattern `ner_juridico`:** O padrão Fabric específico para NER jurídico (`ner_juridico.md` ou similar) deve estar corretamente instalado no diretório de padrões do Fabric (geralmente `~/.config/fabric/patterns/`). Certifique-se de que o nome do padrão no script (`ner_juridico` no comando `fabric -sp ner_juridico`) corresponde ao nome do arquivo do padrão (sem a extensão `.md`).

## Instalação

1.  Instale o wrapper bash:
    ```bash
    chmod +x extrai_e_ner
    cp extrai_e_ner ~/bin/
    ```
2.  Verifique se ~/bin está no PATH:
    ```bash
    echo $PATH | grep ~/bin
    ```
3.  (Opcional) Para usar o script Python diretamente:
    ```bash
    chmod +x extrai_e_ner.py
    ```

## Uso

Execute o script a partir da linha de comando, passando o caminho para o arquivo PDF como argumento principal. Você pode opcionalmente especificar os diretórios de saída para os arquivos TXT e JSON.

**Sintaxe:**

```bash
extrai_e_ner <arquivo_pdf> [--txt-dir DIRETORIO_TXT] [--json-dir DIRETORIO_JSON]
```

Ou, se executável:

```bash
./extrai_e_ner.py <arquivo_pdf> [--txt-dir DIRETORIO_TXT] [--json-dir DIRETORIO_JSON]
```

**Argumentos:**

*   `<arquivo_pdf>` (Obrigatório): Caminho completo para o arquivo PDF de entrada.
*   `--txt-dir DIRETORIO_TXT` (Opcional): Especifica o diretório onde o arquivo TXT extraído será salvo. Se omitido, o padrão é o diretório `Downloads` do usuário (`~/Downloads`).
*   `--json-dir DIRETORIO_JSON` (Opcional): Especifica o diretório onde o arquivo JSON resultante do NER será salvo. Se omitido, o padrão é o diretório `Downloads` do usuário (`~/Downloads`).

**Exemplos:**

1.  **Uso Básico (Saídas em `~/Downloads`):**
    ```bash
    python3 extrai_e_ner.py /path/to/meu_processo.pdf
    ```
    *   Gerará: `~/Downloads/YYYYMMDD_meu_processo_textoextraido.txt`
    *   Gerará: `~/Downloads/YYYYMMDD_meu_processo_entidades.json`

2.  **Especificando Diretórios de Saída:**
    ```bash
    python3 extrai_e_ner.py /path/to/meu_processo.pdf --txt-dir /path/to/output/txt --json-dir /path/to/output/json
    ```
    *   Gerará: `/path/to/output/txt/YYYYMMDD_meu_processo_textoextraido.txt`
    *   Gerará: `/path/to/output/json/YYYYMMDD_meu_processo_entidades.json`

## Workflow do Script

1.  Parseia os argumentos da linha de comando.
2.  **Extração:** Usa `PyPDF2` para extrair texto de todas as páginas do PDF.
3.  **Salvar TXT:** Salva o texto extraído em um arquivo `.txt` no diretório especificado (ou padrão), com nome baseado na data e no nome do PDF original.
4.  **Executar Fabric NER:** Executa o comando `cat '<arquivo.txt>' | fabric -sp ner_juridico > '<arquivo.json>'` via `subprocess`.
5.  **Saída:** O resultado final é o arquivo JSON no diretório especificado (ou padrão), contendo as entidades extraídas pelo Fabric, com nome baseado no arquivo original.

O script irá imprimir mensagens indicando o progresso e o sucesso ou falha da operação.

## Limitações

*   **Qualidade da Extração de PDF:** A capacidade de extrair texto corretamente depende muito da qualidade e estrutura do PDF de origem. PDFs baseados em imagem (scans sem OCR) ou com layouts muito complexos podem resultar em texto mal extraído ou vazio. O script alerta se nenhum texto for extraído.
*   **Dependência da Configuração do Fabric:** O script depende de uma instalação funcional e configurada do `fabric` e da existência do pattern `ner_juridico`. Erros na configuração do Fabric (chaves de API, acesso ao modelo, localização do pattern) causarão falha na etapa de execução do NER.
