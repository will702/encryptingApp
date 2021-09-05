from Crypto.Cipher import AES

from kivy.app import App
def enc_image(input_data, key, iv, filepath,image_name):
    cfb_cipher = AES.new(key, AES.MODE_CFB, iv)

    enc_data = cfb_cipher.encrypt(input_data)

    enc_file = open(filepath + f"/{image_name}.enc", "wb")
    enc_file.write(enc_data)
    enc_file.close()


def dec_image(input_data, key, iv, filepath):
    import datetime
    App.get_running_app().name_decrypt_file = datetime.datetime.now()

    cfb_decipher = AES.new(key, AES.MODE_CFB, iv)
    plain_data = cfb_decipher.decrypt(input_data)

    output_file = open(filepath + f"/{App.get_running_app().name_decrypt_file}.png", "wb")
    output_file.write(plain_data)
    output_file.close()