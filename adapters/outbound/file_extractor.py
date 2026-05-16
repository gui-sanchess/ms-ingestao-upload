import PyPDF2
import io
import pdf2image
import pytesseract
from domain.ports import FileExtractorPort


class PDFExtractorAdapter(FileExtractorPort):
    def extrair_texto(self, conteudo_bytes: bytes, nome_arquivo: str) -> str:
        # 1. TENTATIVA PADRÃO (Ler texto nato)
        leitor = PyPDF2.PdfReader(io.BytesIO(conteudo_bytes))
        texto = ""
        for pagina in leitor.pages:
            extraido = pagina.extract_text()
            if extraido:
                texto += extraido

        # 2. TENTATIVA OCR (Se o PDF for escaneado, o texto virá quase vazio)
        if len(texto.strip()) < 50:
            print("PDF parece ser uma imagem escaneada. Tentando OCR...")
            try:
                # No Windows, você precisará apontar o caminho do executável do Tesseract instalado.
                # Exemplo: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

                imagens = pdf2image.convert_from_bytes(conteudo_bytes)
                texto_ocr = ""
                for img in imagens:
                    texto_ocr += pytesseract.image_to_string(img, lang='por')  # 'por' para português

                if texto_ocr.strip():
                    return texto_ocr
            except Exception as e:
                print(f"Erro no OCR (Você instalou o Tesseract/Poppler no Windows?): {e}")
                return "Documento escaneado. Para extrair conteúdo, configure o Tesseract OCR no servidor."

        return texto