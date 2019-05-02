def clean_content(content):
    content = content.replace('ss="">', "")
    content.replace("<br>", "")
    content.replace("</br>", "")
    return_content = ""
    i = 0
    while i < len(content):
        if content[i] == '<':
            while content[i] != '>':
                i = i + 1
        else:
            return_content = return_content + content[i]
        i = i + 1

    return return_content
