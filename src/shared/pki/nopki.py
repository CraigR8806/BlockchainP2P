from shared.pki.pki import PKI


class NoPKI(PKI):



    def __init__(self):
        super().__init__(None, None, None)

        self.certificate_authority_path = False


    def get_ssl_context(self):
        return None
    
    def get_cert(self):
        return None