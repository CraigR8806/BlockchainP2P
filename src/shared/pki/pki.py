



class PKI:

    def __init__(self, certificate_path:str, private_key_path:str, certificate_athority_path:str):
        self.certificate_path = certificate_path
        self.private_key_path = private_key_path
        self.certificate_authority_path = certificate_athority_path


    def get_ssl_context(self):
        return (self.certificate_path, self.private_key_path)
    
    def get_cert(self):
        return (self.certificate_path, self.private_key_path)
