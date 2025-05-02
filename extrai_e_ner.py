#!/usr/bin/env python3
import sys
import datetime
import subprocess
import argparse
from pathlib import Path

from PyPDF2 import PdfReader

# Default directories (can be overridden by command-line arguments)
DEFAULT_OUTPUT_DIR = Path.home() / "Downloads"

def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extrai todo o texto de um arquivo PDF.

    Args:
        pdf_path (Path): Caminho para o arquivo PDF.
    Returns:
        str: Texto concatenado de todas as páginas do PDF.
    Raises:
        FileNotFoundError: Se o PDF não existir.
        Exception: Para outros erros de leitura.
    """
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")
    try:
        reader = PdfReader(str(pdf_path))
        text = []
        for page in reader.pages:
            text.append(page.extract_text() or "")
        return "\n".join(text)
    except Exception as e:
        raise Exception(f"Erro ao ler PDF {pdf_path}: {e}")

def save_text_to_file(text: str, pdf_path: Path, out_dir: Path) -> Path:
    """
    Salva o texto em um arquivo TXT dentro de out_dir,
    com nome AAAAMMDD_<nome_pdf>_textoextraido.txt.

    Args:
        text (str): O texto a ser salvo.
        pdf_path (Path): Caminho do PDF original para extrair o nome base.
        out_dir (Path): Diretório onde criar o arquivo.
    Returns:
        Path: Caminho completo do arquivo salvo.
    Raises:
        Exception: Se não conseguir escrever no arquivo.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    pdf_stem = pdf_path.stem  # Nome do arquivo sem extensão
    filename = f"{date_str}_{pdf_stem}_textoextraido.txt"
    out_path = out_dir / filename
    try:
        with out_path.open("w", encoding="utf-8") as f:
            f.write(text)
        return out_path
    except Exception as e:
        raise Exception(f"Erro ao salvar texto em {out_path}: {e}")

def run_ner_processing(txt_path: Path, out_json_dir: Path) -> Path:
    """
    Executa o comando `cat {txt_path} | fabric -sp ner_juridico`
    redirecionando a saída para um arquivo JSON nomeado com base no TXT.

    Args:
        txt_path (Path): Caminho do arquivo TXT de entrada.
        out_json_dir (Path): Diretório de saída para o arquivo JSON.
    Returns:
        Path: Caminho completo do arquivo JSON gerado.
    Raises:
        Exception: Se o comando falhar.
    """
    out_json_dir.mkdir(parents=True, exist_ok=True)
    # Derive JSON filename from TXT filename
    json_filename = txt_path.stem.replace('_textoextraido', '_entidades') + ".json"
    out_json_path = out_json_dir / json_filename

    # Monta o comando shell
    # Use f-string para clareza e aspas para caminhos com espaços
    cmd = f"cat '{txt_path}' | fabric -sp ner_juridico > '{out_json_path}'"
    try:
        # Using check=True to raise CalledProcessError on non-zero exit codes
        subprocess.run(cmd, shell=True, check=True, executable="/bin/bash")
        return out_json_path
    except subprocess.CalledProcessError as e:
        # Provide more context in the error message
        raise Exception(f"Erro ao executar comando NER '{cmd}': {e.stderr or e}")
    except FileNotFoundError as e:
        # Handle case where 'fabric' or 'cat' might not be found
        raise Exception(f"Comando não encontrado ao executar NER: {e}")

def main():
    """
    Fluxo principal:
    1. Parseia argumentos da linha de comando.
    2. Extrai texto do PDF.
    3. Salva em TXT.
    4. Executa a extração de entidades jurídicas.
    """
    parser = argparse.ArgumentParser(
        description="Extrai texto de um PDF, salva em TXT e executa NER jurídico com Fabric."
    )
    parser.add_argument(
        "pdf_file",
        metavar="arquivo_pdf",
        type=str,
        help="Caminho para o arquivo PDF de entrada."
    )
    parser.add_argument(
        "--txt-dir",
        dest="output_txt_dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Diretório para salvar o arquivo TXT extraído (padrão: {DEFAULT_OUTPUT_DIR})."
    )
    parser.add_argument(
        "--json-dir",
        dest="output_json_dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Diretório para salvar o arquivo JSON resultante do NER (padrão: {DEFAULT_OUTPUT_DIR})."
    )
    args = parser.parse_args()

    try:
        # Use resolve() for absolute path and basic existence check (handled later too)
        pdf_path = Path(args.pdf_file).resolve()
        output_txt_dir = args.output_txt_dir.resolve()
        output_json_dir = args.output_json_dir.resolve()

        print(f"Processando PDF: {pdf_path}")
        print(f"Diretório de saída TXT: {output_txt_dir}")
        print(f"Diretório de saída JSON: {output_json_dir}")

        print("\n1. Extraindo texto do PDF...")
        text = extract_text_from_pdf(pdf_path)
        if not text.strip():
             print("[AVISO] Nenhum texto extraído do PDF. O arquivo TXT estará vazio.", file=sys.stderr)

        print("2. Salvando texto extraído...")
        txt_path = save_text_to_file(text, pdf_path, output_txt_dir)
        print(f"   Arquivo TXT gerado em: {txt_path}")

        print("3. Executando NER jurídico com Fabric...")
        json_path = run_ner_processing(txt_path, output_json_dir)
        print(f"   Entidades JSON salvas em: {json_path}")

        print("\nProcesso concluído com sucesso!")

    except FileNotFoundError as fnf:
        print(f"\n[ERRO] Arquivo PDF não encontrado: {fnf}", file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        print(f"\n[ERRO] Falha durante o processamento: {err}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()