def read_file(file_path: str):

    """
    reads content from the file
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        return f"file content :\n{content}"
    except Exception as e:
        return f"error reading file:{str(e)}"
    

