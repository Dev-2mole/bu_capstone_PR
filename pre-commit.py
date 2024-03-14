#!/usr/bin/env python3

import sys
import re
import os

# 검사할 정규 표현식 패턴 목록
PATTERNS = {
    '전화번호'     : r'`^\d{2,3}-\d{3,4}-\d{4}$',
    '휴대폰번호'   :   r'^[A-Za-z0-9]{6,12}$',
    '주민등록번호'  : r'\d{2}([0]\d|[1][0-2])([0][1-9]|[1-2]\d|[3][0-1])[-]*[1-4]\d{6}',
    'AWS Access Key ID': r'AKIA[0-9A-Z]{16}', 
    'AWS Secret Access Key': r'[0-9a-zA-Z/+]{40}',  
    'ID와 PW': r'(\w+):(\w+)'
}

def check_code_for_sensitive_data(repo_path):
    for root, dir, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for label, pattern in PATTERNS.items():
                        if re.search(pattern, content):
                            print(f'민감한 정보가 발견된 파일: {file_path}, 정보 유형: {label}')
                            return True
    return False

def main():
    repo_path = '.'  
    if check_code_for_sensitive_data(repo_path):
        print("Error: 코드 검사에서 민감한 정보가 발견되었습니다. 커밋을 중단합니다.")
        sys.exit(1)

if __name__ == '__main__':
    main()
