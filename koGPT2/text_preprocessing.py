import re
import os

def read_txt_files(path):
    # read specific txt files and join them
    with open(os.path.join(path, 'tale1.txt'), "r", encoding='utf-8') as f1, \
         open(os.path.join(path, 'folk_tale.txt'), "r", encoding='utf-8') as f2, \
         open(os.path.join(path, 'Brothers.txt'), "r", encoding='cp949') as f3, \
         open(os.path.join(path, 'Aesop.txt'), "r", encoding='cp949') as f4:
             
        lines1 = f1.read()
        lines2 = f2.read()
        lines3 = f3.read()
        lines4 = f4.read()
        
    lines1 = " ".join(lines1.split())
    lines2 = " ".join(lines2.split())
    lines3 = " ".join(lines3.split())
    lines4 = " ".join(lines4.split())

    # join lines1, lines2, lines3, lines4 with a space separator
    joined_lines = lines1 + " " + lines2 + " " + lines3 + " " + lines4
    return joined_lines


def clean_text(lines):
    lines = re.sub('\(계속\).*?[●○]', '', lines)
    lines = re.sub('[●○]', '', lines)

    lines = re.sub(r"\s+"," ",lines).strip() # 여러 개의 공백을 하나의 공백으로 대체
    lines = re.sub(r"[~♥]", "", lines) 

    lines = re.sub(r"ㅋ|ㅎ|ㅠ|ㅜ","",lines) 
    lines = re.sub(r'\n','',lines).strip()

    lines = re.sub(r"\(.*\)|\s-\s.*","",lines) # 괄호로 둘러싸인 문자열 또는 공백-공백-문자열 형태를 삭제
    lines = re.sub(r"(http|https)?:\/\/\S+\b|www\.(\w+\.)+\S*","",lines).strip()

    return lines
