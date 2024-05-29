import zipfile
import io
import qrcode
import requests

def get_ngrok_url():
    try:
        res = requests.get("http://localhost:4040/api/tunnels")
        res_dict = res.json()
        return res_dict['tunnels'][0]['public_url']
    except:
        return None

def generador_pdf(endpoint: str):
    pass
def generador_excel(endpoint: str):
    pass
def generador_word(endpoint: str):
    pass
def generador_mysql(endpoint: str):
    pass
def generador_qr(endpoint: str):
    ngrok_url = get_ngrok_url()
    ngrok_url = ngrok_url if ngrok_url else endpoint
    exactas_url = 'https://campus.exactas.uba.ar/'
    
    url = f"{ngrok_url}/redirect?final_url={exactas_url}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    png_buffer = io.BytesIO()
    img.save(png_buffer, 'PNG')
    png_buffer.seek(0)
    return png_buffer.getvalue()

def generador_epub(endpoint: str):
    # Create a new ZIP file in memory
    epub_buffer = io.BytesIO()
    with zipfile.ZipFile(epub_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Set the metadata for the book
        mimetype = 'application/epub+zip'
        zipf.writestr("mimetype", mimetype)
        
        container = '''<?xml version="1.0"?>
        <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
        <rootfiles>
            <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
        </rootfiles>
        </container>'''
        zipf.writestr("META-INF/container.xml", container)
        
        metadata = '''<?xml version="1.0"?>
        <package version="3.0" xml:lang="en" xmlns="http://www.idpf.org/2007/opf" unique-identifier="book-id">
        <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
            <dc:identifier id="book-id">urn:uuid:B9B412F2-CAAD-4A44-B91F-A375068478A0</dc:identifier>
            <meta refines="#book-id" property="identifier-type" scheme="xsd:string">uuid</meta>
            <meta property="dcterms:modified">2000-03-24T00:00:00Z</meta>
            <dc:language>en</dc:language>
            <dc:title>My Book</dc:title>
            <dc:creator>John Smith</dc:creator>
        </metadata>
        <manifest>
            <item id="text" href="text.xhtml" media-type="application/xhtml+xml"/>
            <item id="toc" href="../OEBPS/toc.ncx" media-type="application/x-dtbncx+xml"/>
        </manifest>
        <spine toc="toc">
            <itemref idref="text"/>
        </spine>
        </package>'''
        zipf.writestr("OEBPS/content.opf", metadata)
        
        toc = '''<?xml version="1.0"?>
        <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
        <head>
            <meta name="dtb:uid" content="urn:uuid:B9B412F2-CAAD-4A44-B91F-A375068478A0"/>
            <meta name="dtb:depth" content="1"/>
            <meta name="dtb:totalPageCount" content="0"/>
            <meta name="dtb:maxPageNumber" content="0"/>
        </head>
        <docTitle>
            <text>My Book</text>
        </docTitle>
        <navMap>
            <navPoint id="navpoint-1" playOrder="1">
            <navLabel>
                <text>Chapter 1</text>
            </navLabel>
            <content src="text.xhtml#xpointer(/html/body/section[1])"/>
            </navPoint>
            <navPoint id="navpoint-2" playOrder="2">
            <navLabel>
                <text>Chapter 2</text>
            </navLabel>
            <content src="text.xhtml#xpointer(/html/body/section[2])"/>
            </navPoint>
        </navMap>
        </ncx>'''
        zipf.writestr("OEBPS/toc.ncx", toc)
        
        text = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <!DOCTYPE html>
        <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
        <head>
            <link href="{endpoint}" rel="stylesheet" crossorigin="anonymous">
            <title>My Book</title>
        </head>
        <body>
            <section><h1>Chapter 1</h1>
            <p>This is the text for chapter 1.</p>
            </section>
            <section><h1>Chapter 2</h1>
            <p>This is the text for chapter 2.</p>
            </section>
        </body>
        </html>'''
        zipf.writestr("OEBPS/text.xhtml", text)
    return epub_buffer.getvalue()

generadores = {
    "pdf": generador_pdf,
    "excel": generador_excel,
    "word": generador_word,
    "epub": generador_epub,
    "mysql": generador_mysql,
    "qr": generador_qr
}
