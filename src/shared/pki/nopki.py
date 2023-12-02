from shared.pki.pki import PKI
import typing as t


class NoPKI(PKI):

    """
    Class to use when not using HTTPS

    ---
    FIELDS
    ---
        certificate_path : None
            Set to `None`
        private_key_path : None
            Set to `None`
        certificate_authority_path : bool
            Set to `False`

    """

    def __init__(self):
        """
        Constructor to NoPKI

        Args:
            certificate_path (None): Set to `None`
            private_key_path (None): Set to `None`
            certificate_athority_path (bool): Set to `False`
        """
        super().__init__(None, None, None)

        self.certificate_authority_path = False

    def get_ssl_context(self) -> t.Tuple[str, str]:
        """
        Overloads get_ssl_context to return `None`

        Returns:
            None
        """
        return None
