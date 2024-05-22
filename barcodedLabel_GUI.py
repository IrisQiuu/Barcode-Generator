import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm, inch

def generate_pdf(numLabel, ncol, nrow, ids):
    c = canvas.Canvas("barcodeFile.pdf", pagesize=A4)
    
    codes = []
    for id in ids:
        codes.extend([code128.Code128(id, humanReadable=True, barWidth=0.4, barHeight=20) for _ in range(numLabel)])

    x_positions = [10 * mm, 38 * mm, 65 * mm, 92 * mm, 119 * mm, 146 * mm, 173 * mm]
    y_positions = [266 * mm] * 7
    
    if 1 <= ncol <= 7:
        y_positions[ncol - 1] = 266 * mm - (15.8 * mm) * nrow

    n = 17 * (ncol - 1) + nrow

    for code in codes:
        col = (n // 17) % 7
        row = n % 17
        if col < len(x_positions):
            code.drawOn(c, x_positions[col], y_positions[col])
            y_positions[col] -= 15.8 * mm
            n += 1

    c.setPageSize([8.5 * inch, 11.0 * inch])
    c.showPage()
    c.save()

def on_generate():
    try:
        numLabel = int(numLabel_entry.get())
        ncol = int(ncol_entry.get())
        nrow = int(nrow_entry.get())
        ids = id_entry.get().split(',')

        if not (1 <= ncol <= 7):
            raise ValueError("ncol must be between 1 and 7")
        
        generate_pdf(numLabel, ncol, nrow, ids)
        messagebox.showinfo("Success", "PDF generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

#main application window
root = tk.Tk()
root.title("Barcode Generator")
root.geometry("350x200")

tk.Label(root, text="Number of Labels per ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
numLabel_entry = tk.Entry(root)
numLabel_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Starting Column (1-7):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
ncol_entry = tk.Entry(root)
ncol_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Used Labels in Column:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
nrow_entry = tk.Entry(root)
nrow_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="IDs (comma-separated):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
id_entry = tk.Entry(root)
id_entry.grid(row=3, column=1, padx=10, pady=5)

generate_button = tk.Button(root, text="Generate PDF", command=on_generate, width=20, height=2)
generate_button.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
