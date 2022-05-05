import re

from graia.ariadne.message.element import Plain


def getargs(messages):
    s = []
    for message in messages:
        if isinstance(message, Plain):
            # 拆分空格或换行
            matches = re.split('\\s+', str(message))
            for match in matches:
                if match.isspace() or len(match) == 0:
                    continue
                s.append(Plain(match))
        else:
            s.append(message)
    
    args = s[1:]
    
    return args
