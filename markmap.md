# Script de Extração de Texto PDF e NER Jurídico com Fabric

## Propósito
- Automatizar extração de texto de PDF
- Executar padrão Fabric de NER jurídico
- Gerar saída em JSON

## Pré‑requisitos
- **Python 3**  
  - `argparse` (builtin)  
- **PyPDF2**  
  - `pip install PyPDF2`  
- **Fabric CLI**  
  - Configurar LLM (OpenAI, Claude, Ollama…)  
- **Pattern ner_juridico**  
  - Arquivo `ner_juridico.md` em `~/.config/fabric/patterns/`

## Instalação
- Salvar script como `extrai_e_ner.py`
- (Opcional) `chmod +x extrai_e_ner.py`

## Uso
- **Sintaxe básica**  
  ```bash
  python3 extrai_e_ner.py <arquivo_pdf> [--txt-dir DIR_TXT] [--json-dir DIR_JSON]
