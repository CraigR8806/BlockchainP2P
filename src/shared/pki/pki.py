import typing as t


class PKI:

    """
    Class to hold Certificate and Key information to help pass them around specifically for HTTPS support

    ---
    FIELDS
    ---
        certificate_path : str
            Absolute path to the certificate
        private_key_path : str
            Absolute path to the private key
        certificate_authority_path : str
            Absolute path to the CA certificate

    """

    def __init__(
        self,
        certificate_path: str,
        private_key_path: str,
        certificate_athority_path: str,
    ):
        """
        Constructor to PKI

        Args:
            certificate_path (str): Absolute path to the certificate
            private_key_path (str): Absolute path to the private key
            certificate_athority_path (str): Absolute path to the CA certificate
        """
        self.certificate_path = certificate_path
        self.private_key_path = private_key_path
        self.certificate_authority_path = certificate_athority_path

    def get_ssl_context(self) -> t.Tuple[str, str]:
        """
        Returns a `Tuple` containing the `certificate_path` and `private_key_path` field values

        Returns:
            t.Tuple[str, str]: contains the `certificate_path` and `private_key_path` field values
        """
        return (self.certificate_path, self.private_key_path)
