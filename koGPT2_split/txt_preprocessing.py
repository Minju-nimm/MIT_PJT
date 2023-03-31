import os
import re
import argparse
from tqdm import tqdm
from kss import split_sentences

def preprocessing(dir,filename):
    """경로 내 txt 파일을 전처리하는 함수
    input| dir: 파일 경로"""

    filelist = os.listdir(dir)
    print(f"preprocessing {len(filelist)} files..")

    i = 1
    filename_list = open(os.path.join(dir,'filenames.txt'),'w', encoding='utf-8')
    for file in tqdm(filelist,total=len(filelist)):
        f,ext = os.path.splitext(os.path.join(dir,file))
        if ext == '.txt':
            # txt file --> sentences list
            result = []
            file = open(os.path.join(dir,file),'r', encoding='cp949')
            lines = file.readlines()

            # 전처리
            for line in lines:
                line = re.sub(r'\n','',line).strip() # 줄바꿈 제거, 양족 공백 제거
                # 문자열이 비어있지 않을 경우에만 코드 실행
                if line: 
                    line = re.sub(r"\s+"," ",line).strip() # 공백 문자(\s)가 1개 이상 반복되는 패턴을 찾아 1개의 공백 문자로 대체
                    line = re.sub(r"ㅋ|ㅎ|ㅠ|ㅜ","",line) # 한글 이모티콘인 'ㅋ', 'ㅎ', 'ㅠ', 'ㅜ'를 제거
                    line = re.sub(r"\(.*\)|\s-\s.*","",line) # 괄호(()) 안의 내용과, 공백-공백(-) 사이의 내용을 제거
                    line = re.sub(r"(http|https)?:\/\/\S+\b|www\.(\w+\.)+\S*","",line).strip() # URL 주소를 제거
                    # line = re.sub(r"\..",".",line).strip()
                    # line = re.sub(r"\??","?",line)
                    # line = re.sub(r"\!!","!",line)
                    # line = re.sub(r"\,,",",",line).strip()
                    # line = re.sub(r"\“|\”","\"",line)
                    # line = re.sub(r"\‘|\’|\`","\'",line).strip()
                    # 문장 분리
                    # line_list = split_sentences(line,use_heuristic=True,use_quotes_brackets_processing=True)
                    line_list = split_sentences(line)
                    for line in line_list:
                        line = '</s>' + line.strip() + '</s>'
                        result.append(line)
        
            new_file = open(os.path.join(dir,filename+str(i)+ext),'w', encoding='utf-8')
            for line in result:
                new_file.write(line+'\n')
            new_file.close()

            filename_list.write(f+ext+'\t'+filename+str(i)+ext+'\n')
            i += 1
    filename_list.close()

    return "Complete !"



def main(args):
    preprocessing(args.dir,args.filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--dir', type=str, default='./koGPT2/datasets', help='data dir(default: ./koGPT2/datasets')
    parser.add_argument('--filename', type=str, default='folk', help='data filename(default: folk)')

    args = parser.parse_args()

    main(args)