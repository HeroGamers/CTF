import os

def main():
    with open("copypasta.pdf", "rb") as f:
        pdf_data = f.read()
    
    # Remove last object
    m1 = pdf_data.split(b"\x0A1 0 obj")[0]
    # Put XREF and startxref at the end
    m2 = m1.split(b"44 0 obj")[0] + m1.split(b"%%EOF")[1] + b"\x0A44 0 obj" + m1.split(b"44 0 obj")[1].split(b"%%EOF")[0] + b"%%EOF\x0A"
    
    # Get offset of 44 0 obj
    offset = m2.find(b"44 0 obj")
    # Set the startxref to the offset of 44 0 obj
    m3 = m2.replace(b"startxref\x0A0\x0A", b"startxref\x0A" + str(offset).encode() + b"\x0A")

    # m4 = m3.replace(b"  ", b"")  # Remove double spaces
    # m4 = m4.replace(b"\x0A \x0A", b"\x0A")  # Remove double newlines
    # m4 = m4.replace(b"\x0A\x0A", b"\x0A")  # Remove double newlines
    # m4 = m4.replace(b"\x0A\x0A", b"\x0A")  # Remove double newlines

    final = m3

    # Write the fixed PDF to a new file
    with open("copypasta_fixed.pdf", "wb") as f:
        f.write(final)

    


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()