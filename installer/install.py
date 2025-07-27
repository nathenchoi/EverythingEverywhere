#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import winreg
import shutil
import sqlite3
import hashlib
from pathlib import Path

def find_chrome_extensions():
    """설치된 크롬 확장 프로그램에서 EverythingEverywhere 찾기"""
    extensions = []
    
    # 크롬 사용자 데이터 디렉토리들
    chrome_dirs = [
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data"),
        os.path.expandvars(r"%APPDATA%\Google\Chrome\User Data"),
    ]
    
    for chrome_dir in chrome_dirs:
        if not os.path.exists(chrome_dir):
            continue
            
        # Default 프로필과 Profile 1, 2... 확인
        for profile in ["Default", "Profile 1", "Profile 2", "Profile 3"]:
            extensions_dir = os.path.join(chrome_dir, profile, "Extensions")
            if not os.path.exists(extensions_dir):
                continue
                
            # 각 확장 프로그램 디렉토리 확인
            for ext_id in os.listdir(extensions_dir):
                ext_path = os.path.join(extensions_dir, ext_id)
                if not os.path.isdir(ext_path):
                    continue
                    
                # 버전 폴더들 확인
                for version in os.listdir(ext_path):
                    version_path = os.path.join(ext_path, version)
                    manifest_path = os.path.join(version_path, "manifest.json")
                    
                    if os.path.exists(manifest_path):
                        try:
                            with open(manifest_path, 'r', encoding='utf-8') as f:
                                manifest = json.load(f)
                                
                            # EverythingEverywhere 확장인지 확인
                            if (manifest.get('name') == 'EverythingEverywhere' or 
                                'everything' in manifest.get('name', '').lower()):
                                extensions.append({
                                    'id': ext_id,
                                    'name': manifest.get('name', 'Unknown'),
                                    'version': manifest.get('version', 'Unknown'),
                                    'profile': profile
                                })
                        except:
                            continue
    
    return extensions

def get_chrome_extension_id():
    """크롬 확장 프로그램 ID 가져오기 또는 입력받기"""
    print("=" * 60)
    print("EverythingEverywhere 설치 프로그램")
    print("=" * 60)
    
    # 자동으로 확장 프로그램 찾기
    print("\n🔍 설치된 EverythingEverywhere 확장 검색 중...")
    extensions = find_chrome_extensions()
    
    if extensions:
        print(f"\n✅ {len(extensions)}개의 EverythingEverywhere 확장을 발견했습니다:")
        for i, ext in enumerate(extensions, 1):
            print(f"   {i}. ID: {ext['id']}")
            print(f"      이름: {ext['name']}")
            print(f"      버전: {ext['version']}")
            print(f"      프로필: {ext['profile']}")
            print()
        
        if len(extensions) == 1:
            print(f"자동으로 선택됨: {extensions[0]['id']}")
            return extensions[0]['id']
        else:
            while True:
                try:
                    choice = input(f"사용할 확장을 선택하세요 (1-{len(extensions)}): ")
                    choice = int(choice) - 1
                    if 0 <= choice < len(extensions):
                        return extensions[choice]['id']
                    else:
                        print("잘못된 선택입니다.")
                except ValueError:
                    print("숫자를 입력하세요.")
    
    # 자동 감지 실패시 수동 입력
    print("\n⚠️  자동 감지에 실패했습니다. 수동으로 입력해주세요.")
    print("\n1. 먼저 크롬에서 확장 프로그램을 로드하세요:")
    print("   - 크롬에서 chrome://extensions/ 열기")
    print("   - '개발자 모드' 활성화")
    print("   - '압축해제된 확장 프로그램 로드' 클릭")
    print("   - chrome-extension 폴더 선택")
    print("\n2. 로드된 확장 프로그램의 ID를 확인하세요")
    print("   (예: abcdefghijklmnopqrstuvwxyz123456)\n")
    
    extension_id = input("확장 프로그램 ID를 입력하세요: ").strip()
    
    if not extension_id:
        print("오류: 확장 프로그램 ID가 필요합니다!")
        sys.exit(1)
    
    return extension_id

def install_native_host():
    """Native Messaging Host 설치"""
    # 경로 설정
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    native_host_dir = project_dir / "native-host"
    
    # 확장 프로그램 ID 가져오기
    extension_id = get_chrome_extension_id()
    
    # 매니페스트 파일 업데이트
    manifest_file = native_host_dir / "com.everythingeverywhere.host.json"
    with open(manifest_file, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    # Python 실행 파일 경로 설정
    python_exe = sys.executable
    native_host_py = str(native_host_dir / "native_host.py")
    
    # 배치 파일 생성 (Python 스크립트 실행용)
    batch_file = native_host_dir / "native_host.bat"
    with open(batch_file, 'w') as f:
        f.write(f'@echo off\n"{python_exe}" "{native_host_py}" %*')
    
    # 매니페스트에서 경로와 allowed_origins 업데이트
    manifest['path'] = str(batch_file)
    manifest['allowed_origins'] = [f"chrome-extension://{extension_id}/"]
    
    # 업데이트된 매니페스트 저장
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n✅ 매니페스트 파일 업데이트됨")
    print(f"   경로: {batch_file}")
    print(f"   확장 ID: {extension_id}")
    
    # 레지스트리에 Native Messaging Host 등록
    try:
        # HKEY_CURRENT_USER에 등록 (관리자 권한 불필요)
        key_path = r"Software\Google\Chrome\NativeMessagingHosts\com.everythingeverywhere.host"
        
        # 레지스트리 키 생성
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        
        # 매니페스트 파일 경로 설정
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, str(manifest_file))
        winreg.CloseKey(key)
        
        print(f"\n✅ 레지스트리 등록 완료")
        print(f"   키: HKEY_CURRENT_USER\\{key_path}")
        print(f"   값: {manifest_file}")
        
    except Exception as e:
        print(f"\n❌ 레지스트리 등록 실패: {e}")
        sys.exit(1)
    
    # Everything 경로 확인
    print("\n🔍 Everything.exe 경로 확인 중...")
    possible_paths = [
        r"C:\Program Files (x86)\Everything 1.5a\Everything.exe",
        r"C:\Program Files\Everything\Everything.exe",
        r"C:\Program Files (x86)\Everything\Everything.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Everything\Everything.exe"),
        os.path.expandvars(r"%PROGRAMFILES%\Everything\Everything.exe"),
        os.path.expandvars(r"%PROGRAMFILES(X86)%\Everything\Everything.exe"),
    ]
    
    everything_found = False
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Everything 발견: {path}")
            everything_found = True
            break
    
    if not everything_found:
        print("⚠️  Everything이 기본 경로에 없습니다.")
        print("   Everything이 다른 경로에 설치되어 있다면,")
        print("   EVERYTHING_PATH 환경 변수에 경로를 설정하세요.")
        print("\n   일반적인 Everything 설치 경로:")
        for path in possible_paths:
            print(f"   - {path}")
        
        # 수동 경로 입력 옵션
        manual_path = input("\n수동으로 Everything.exe 경로를 입력하시겠습니까? (엔터: 건너뛰기): ").strip()
        if manual_path and os.path.exists(manual_path):
            print(f"✅ 수동 입력 경로 확인됨: {manual_path}")
            everything_found = True
    
    print("\n✅ 설치 완료!")
    print("\n다음 단계:")
    print("1. 크롬을 완전히 종료했다가 다시 시작하세요")
    print("2. 웹페이지에서 텍스트를 선택하고 우클릭하세요")
    print("3. '로컬에서 Everything으로 검색하기' 메뉴를 확인하세요")

def uninstall_native_host():
    """Native Messaging Host 제거"""
    print("\nNative Messaging Host 제거 중...")
    
    try:
        # 레지스트리에서 제거
        key_path = r"Software\Google\Chrome\NativeMessagingHosts\com.everythingeverywhere.host"
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
        print("✅ 레지스트리에서 제거됨")
    except:
        print("⚠️  레지스트리 항목이 없거나 제거할 수 없습니다")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        uninstall_native_host()
    else:
        install_native_host()