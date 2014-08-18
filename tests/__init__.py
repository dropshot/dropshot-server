import dropshot


def setup_package():
    """
    Setup the tests package.

    Do package level setup like creating databases/files.

    Args:
        none

    Returns:
        none
    """
    dropshot.configure_app()


def teardown_package():
    """
    Teardown the tests package.

    Do package level teardown like removing databases/files.

    Args:
        none

    Returns:
        none
    """
    pass
