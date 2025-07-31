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
    # 저장된 사용자 설정 경로 확인
    config_file = Path(__file__).parent / "everything_config.json"
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                custom_path = config.get('everything_path')
                if custom_path and os.path.exists(custom_path):
                    logging.info(f"Using saved custom path: {custom_path}")
                    return custom_path
        except Exception as e:
            logging.warning(f"Failed to read config: {e}")
    
    # 일반적인 Everything 설치 경로들 (더 포괄적으로)
    possible_paths = []
    
    # Program Files 경로들 - 다양한 버전 지원
    program_files_paths = [
        os.environ.get('PROGRAMFILES', r'C:\Program Files'),
        os.environ.get('PROGRAMFILES(X86)', r'C:\Program Files (x86)'),
        os.environ.get('PROGRAMW6432', r'C:\Program Files')
    ]
    
    # 다양한 Everything 버전과 설치 형태
    everything_patterns = [
        r"Everything\Everything.exe",
        r"Everything 1.4\Everything.exe", 
        r"Everything 1.5a\Everything.exe",
        r"Everything 1.5b\Everything.exe",
        r"Everything64\Everything.exe",
        r"Everything32\Everything.exe",
        r"VoidTools\Everything\Everything.exe",
    ]
    
    # Program Files 조합
    for pf_path in program_files_paths:
        if pf_path:
            for pattern in everything_patterns:
                possible_paths.append(os.path.join(pf_path, pattern))
    
    # 추가 일반적인 경로들
    additional_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Everything\Everything.exe"),
        os.path.expandvars(r"%APPDATA%\Everything\Everything.exe"),
        os.path.expandvars(r"%USERPROFILE%\Everything\Everything.exe"),
        os.path.expandvars(r"%USERPROFILE%\Desktop\Everything\Everything.exe"),
        os.path.expandvars(r"%USERPROFILE%\Downloads\Everything\Everything.exe"),
        r"C:\Everything\Everything.exe",
        r"D:\Everything\Everything.exe",
        r"C:\Tools\Everything\Everything.exe",
        r"D:\Tools\Everything\Everything.exe",
        r"C:\Portable\Everything\Everything.exe",
        r"D:\Portable\Everything\Everything.exe",
    ]
    
    possible_paths.extend(additional_paths)
    
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

def save_everything_path(path):
    """Everything 경로를 설정 파일에 저장"""
    config_file = Path(__file__).parent / "everything_config.json"
    try:
        config = {}
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        config['everything_path'] = path
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Saved Everything path: {path}")
        return True
    except Exception as e:
        logging.error(f"Failed to save config: {e}")
        return False

def validate_everything_path(path):
    """Everything 경로가 유효한지 확인"""
    if not path or not os.path.exists(path):
        return False
    
    # 파일명이 Everything.exe인지 확인
    if not path.lower().endswith('everything.exe'):
        return False
    
    # 실행 가능한지 확인
    try:
        result = subprocess.run([path, '-help'], 
                              capture_output=True, 
                              timeout=5)
        return True
    except:
        return False

def search_in_everything(query):
    """Everything에서 검색 실행"""
    everything_exe = find_everything_exe()
    
    if not everything_exe:
        return {
            'success': False,
            'error': 'Everything.exe not found',
            'available_paths': get_potential_everything_paths()
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
            'message': f'Searching for: {query}',
            'everything_path': everything_exe
        }
        
    except Exception as e:
        logging.error(f"Error launching Everything: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def get_potential_everything_paths():
    """잠재적인 Everything 경로들을 반환 (진단용)"""
    everything_exe = find_everything_exe()
    if everything_exe:
        return [everything_exe]
    
    # 존재하지 않는 경로들도 포함해서 반환 (사용자 참고용)
    potential_paths = [
        r"C:\Program Files\Everything\Everything.exe",
        r"C:\Program Files (x86)\Everything\Everything.exe",
        r"C:\Everything\Everything.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Everything\Everything.exe"),
    ]
    
    return [p for p in potential_paths if os.path.exists(p)]

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
            action = message.get('action')
            
            if action == 'search':
                query = message.get('query', '')
                if query:
                    result = search_in_everything(query)
                else:
                    result = {
                        'success': False,
                        'error': 'No search query provided'
                    }
            
            elif action == 'get_status':
                everything_exe = find_everything_exe()
                result = {
                    'success': True,
                    'everything_found': everything_exe is not None,
                    'everything_path': everything_exe,
                    'available_paths': get_potential_everything_paths()
                }
            
            elif action == 'set_path':
                path = message.get('path', '')
                if validate_everything_path(path):
                    if save_everything_path(path):
                        result = {
                            'success': True,
                            'message': 'Everything path saved successfully'
                        }
                    else:
                        result = {
                            'success': False,
                            'error': 'Failed to save path'
                        }
                else:
                    result = {
                        'success': False,
                        'error': 'Invalid Everything.exe path'
                    }
            
            elif action == 'validate_path':
                path = message.get('path', '')
                is_valid = validate_everything_path(path)
                result = {
                    'success': True,
                    'valid': is_valid,
                    'path': path
                }
            
            else:
                result = {
                    'success': False,
                    'error': f'Unknown action: {action}'
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