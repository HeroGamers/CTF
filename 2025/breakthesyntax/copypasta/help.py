from pypdf import PdfReader, PdfWriter
import os

def fix():
    with open("copypasta.pdf", "rb") as f:
        pdf_data = f.read()
    
    # Remove last object
    m1 = pdf_data.split(b"\x0A1 0 obj")[0]
    # Put XREF and startxref at the end
    m2 = m1.split(b"44 0 obj")[0] + m1.split(b"%%EOF")[1] + b"\x0A44 0 obj" + m1.split(b"44 0 obj")[1].split(b"%%EOF")[0] + b"%%EOF\x0A"
    
    # m2 = m2.replace(b"<<", b"<<\x0A")
    # m2 = m2.replace(b">>", b"\x0A>>\x0A")

    m2 = m2.replace(b"50 0 obj", b"34 0 obj\x0A<<\n/Type /Pages\n/Kids [39 0 R]\n/Count 1\n>>\x0Aendobj\x0A" + b"50 0 obj")
    
    
    # Get offset of 44 0 obj
    offset = m2.find(b"44 0 obj")
    # Set the startxref to the offset of 44 0 obj
    m3 = m2.replace(b"startxref\x0A0\x0A", b"startxref\x0A" + str(offset).encode() + b"\x0A")

    final = m3

    # Write the fixed PDF to a new file
    with open("copypasta_fixed.pdf", "wb") as f:
        f.write(final)


def decrypt():
    reader = PdfReader("copypasta_fixed.pdf")
    if reader.is_encrypted:
        reader.decrypt("pumpkin")
    
    writer = PdfWriter(clone_from=reader)
    with open("copypasta_fixed_py.pdf", "wb") as f:
        writer.write(f)

def main():
    fix()
    decrypt()
    

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()