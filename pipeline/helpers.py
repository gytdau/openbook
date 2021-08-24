
def join_path(path, filename):
    """
    epub path are unix based, we require this method for this to work correctly on windows
    """
    return '/'.join([path, filename])