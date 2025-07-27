#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import struct
import subprocess
import os
import logging
from pathlib import Path

# 로깅 설정
log_file = Path(__file__).parent / "native_host.log"
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def send_message(message_dict):
    """크롬으로 메시지 전송"""
    message = json.dumps(message_dict).encode('utf-8')
    sys.stdout.buffer.write(struct.pack('I', len(message)))
    sys.stdout.buffer.write(message)
    sys.stdout.buffer.flush()

def read_message():
    """크롬에서 메시지 읽기"""
    raw_length = sys.stdin.buffer.read(4)
    if not raw_length:
        return None
    
    message_length = struct.unpack('I', raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode('utf-8')
    return json.loads(message)

def find_everything_exe():
    """Everything.exe 경로 찾기"""
    # 일반적인 Everything 설치 경로들
    possible_paths = [
        r"C:\Program Files (x86)\Everything 1.5a\Everything.exe",
        r"C:\Program Files\Everything\Everything.exe",
        r"C:\Program Files (x86)\Everything\Everything.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Everything\Everything.exe"),
    ]
    
    # 환경 변수에서 Everything 경로 확인
    everything_path = os.environ.get('EVERYTHING_PATH')
    if everything_path:
        possible_paths.insert(0, everything_path)
    
    # 각 경로 확인
    for path in possible_paths:
        expanded_path = os.path.expandvars(path)
        if os.path.exists(expanded_path):
            logging.info(f"Found Everything at: {expanded_path}")
            return expanded_path
    
    # PATH에서 Everything 찾기
    try:
        result = subprocess.run(['where', 'Everything.exe'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            path = result.stdout.strip().split('\n')[0]
            logging.info(f"Found Everything in PATH: {path}")
            return path
    except:
        pass
    
    logging.error("Everything.exe not found")
    return None

def search_in_everything(query):
    """Everything에서 검색 실행"""
    everything_exe = find_everything_exe()
    
    if not everything_exe:
        return {
            'success': False,
            'error': 'Everything.exe not found'
        }
    
    try:
        # Everything 명령줄 옵션:
        # -s : 검색어 지정
        # -newwindow : 새 창에서 열기
        cmd = [everything_exe, '-newwindow', '-s', query]
        
        logging.info(f"Executing: {' '.join(cmd)}")
        
        # Everything 실행
        subprocess.Popen(cmd, shell=False)
        
        return {
            'success': True,
            'message': f'Searching for: {query}'
        }
        
    except Exception as e:
        logging.error(f"Error launching Everything: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def main():
    """메인 함수"""
    logging.info("Native host started")
    
    while True:
        try:
            # 크롬에서 메시지 읽기
            message = read_message()
            if not message:
                break
            
            logging.info(f"Received message: {message}")
            
            # 메시지 처리
            if message.get('action') == 'search':
                query = message.get('query', '')
                if query:
                    result = search_in_everything(query)
                else:
                    result = {
                        'success': False,
                        'error': 'No search query provided'
                    }
            else:
                result = {
                    'success': False,
                    'error': 'Unknown action'
                }
            
            # 응답 전송
            send_message(result)
            logging.info(f"Sent response: {result}")
            
        except Exception as e:
            logging.error(f"Error in main loop: {str(e)}")
            send_message({
                'success': False,
                'error': str(e)
            })
    
    logging.info("Native host ended")

if __name__ == '__main__':
    main()