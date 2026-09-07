import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from PIL import ImageTk


class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        self.qr_image = None
        self.qr_photo = None

        # Title
        title = tk.Label(
            root,
            text="QR Code Generator",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)

        # Instruction
        instruction = tk.Label(
            root,
            text="Enter text or URL below:",
            font=("Arial", 12)
        )
        instruction.pack(pady=5)

        # Input box
        self.entry = tk.Entry(
            root,
            font=("Arial", 14),
            width=40
        )
        self.entry.pack(pady=10, ipady=8)

        # Generate button
        generate_button = tk.Button(
            root,
            text="Generate QR Code",
            font=("Arial", 12, "bold"),
            command=self.generate_qr,
            width=20
        )
        generate_button.pack(pady=10)

        # QR code display area
        self.qr_label = tk.Label(
            root,
            text="Your QR code will appear here",
            font=("Arial", 12)
        )
        self.qr_label.pack(pady=20)

        # Save button
        self.save_button = tk.Button(
            root,
            text="Save QR Code",
            font=("Arial", 12, "bold"),
            command=self.save_qr,
            width=20,
            state=tk.DISABLED
        )
        self.save_button.pack(pady=10)

        # Clear button
        clear_button = tk.Button(
            root,
            text="Clear",
            font=("Arial", 12),
            command=self.clear,
            width=20
        )
        clear_button.pack(pady=5)

    def generate_qr(self):
        data = self.entry.get().strip()

        if not data:
            messagebox.showwarning(
                "Empty Input",
                "Please enter some text or a URL."
            )
            return

        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )

        qr.add_data(data)
        qr.make(fit=True)

        # Create image
        self.qr_image = qr.make_image(
            fill_color="black",
            back_color="white"
        ).convert("RGB")

        # Resize image for display
        display_image = self.qr_image.copy()
        display_image.thumbnail((300, 300))

        # Convert for Tkinter
        self.qr_photo = ImageTk.PhotoImage(display_image)

        # Display QR code
        self.qr_label.config(
            image=self.qr_photo,
            text=""
        )

        # Enable save button
        self.save_button.config(state=tk.NORMAL)

    def save_qr(self):
        if self.qr_image is None:
            messagebox.showwarning(
                "No QR Code",
                "Please generate a QR code first."
            )
            return

        # Ask user where to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("All Files", "*.*")
            ],
            title="Save QR Code"
        )

        if file_path:
            self.qr_image.save(file_path)

            messagebox.showinfo(
                "Success",
                "QR code saved successfully!"
            )

    def clear(self):
        self.entry.delete(0, tk.END)

        self.qr_label.config(
            image="",
            text="Your QR code will appear here"
        )

        self.qr_image = None
        self.qr_photo = None

        self.save_button.config(state=tk.DISABLED)


# Create application
root = tk.Tk()
app = QRCodeGenerator(root)

root.mainloop()