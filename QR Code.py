import qrcode

def generate_contact_qr():
    print("--- Enter Your Information ---")
    
    # 1. Taking Inputs (Updated)
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    phone_number = input("Enter Phone Number: ")
    email_address = input("Enter Email Address: ")
    company_name = input("Enter Company Name: ")
    designation = input("Enter Designation: ")

    # 2. Creating vCard Data Format (Standard for Contact Info)
    # N = Structured Name (Last;First) - Used for sorting in contacts
    # FN = Full Name (First Last) - Used for display on screen
    vcard_data = (
        "BEGIN:VCARD\n"
        "VERSION:3.0\n"
        f"N:{last_name};{first_name};;;\n"
        f"FN:{first_name} {last_name}\n"
        f"ORG:{company_name}\n"
        f"TITLE:{designation}\n"
        f"TEL:{phone_number}\n"
        f"EMAIL:{email_address}\n"
        "END:VCARD"
    )

    # 3. Generating the QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(vcard_data)
    qr.make(fit=True)

    # 4. Creating and Saving the Image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Filename includes the name so you don't overwrite others
    filename = f"QR_{first_name}_{last_name}.png"
    img.save(filename)
    
    print(f"\nSuccess! QR code generated as '{filename}'")
    print("Scan it with your phone to test.")

if __name__ == "__main__":
    generate_contact_qr()