#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import zipfile
from pathlib import Path

def create_distribution_package():
    """배포용 패키지 생성"""
    
    print("EverythingEverywhere 배포 패키지 생성 중...")
    
    # 프로젝트 루트 디렉토리
    project_dir = Path(__file__).parent
    
    # 배포용 디렉토리 생성 (타임스탬프 추가)
    import time
    timestamp = int(time.time())
    dist_dir = project_dir / "dist"
    package_dir = dist_dir / f"EverythingEverywhere_{timestamp}"
    
    # 배포 디렉토리 생성 (존재하면 덮어쓰기)
    package_dir.mkdir(parents=True, exist_ok=True)
    
    # 복사할 파일/폴더 목록
    items_to_copy = [
        "chrome-extension",
        "native-host", 
        "installer",
        "README.md"
    ]
    
    # 파일/폴더 복사
    for item in items_to_copy:
        src = project_dir / item
        dst = package_dir / item
        
        if src.is_dir():
            shutil.copytree(src, dst)
            print(f"[OK] 폴더 복사: {item}")
        elif src.is_file():
            shutil.copy2(src, dst)
            print(f"[OK] 파일 복사: {item}")
    
    # 간단한 설치 스크립트 생성
    setup_script = package_dir / "setup.bat"
    with open(setup_script, 'w', encoding='utf-8') as f:
        f.write("""@echo off
chcp 65001 > nul
echo.
echo ==========================================
echo  EverythingEverywhere 설치 프로그램
echo ==========================================
echo.
echo 1. 크롬에서 확장 프로그램을 먼저 설치하세요:
echo    - 크롬에서 chrome://extensions/ 열기
echo    - 개발자 모드 활성화
echo    - "압축해제된 확장 프로그램 로드" 클릭
echo    - chrome-extension 폴더 선택
echo.
echo 2. 확장 프로그램이 로드되면 아무 키나 누르세요...
pause > nul
echo.
echo 3. Native Host 설치 중...
cd installer
python install.py
echo.
echo 설치가 완료되었습니다!
echo 크롬을 재시작한 후 사용하세요.
echo.
pause
""")
    
    # 사용 설명서 생성
    guide_file = package_dir / "사용법.txt"
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write("""EverythingEverywhere 사용법
================================

## 설치 방법
1. setup.bat 실행
2. 안내에 따라 크롬 확장 프로그램 설치
3. Native Host 자동 설치
4. 크롬 재시작

## 사용 방법
1. 웹페이지에서 텍스트 선택 (드래그)
2. 마우스 우클릭
3. "로컬에서 Everything으로 검색하기" 클릭
4. Everything이 자동 실행되어 검색 결과 표시

## 요구사항
- Windows OS
- Google Chrome 브라우저
- Everything 앱 설치 (https://www.voidtools.com/)
- Python 3.6 이상

## 문제 해결
- Everything이 실행되지 않는 경우:
  * Everything이 설치되어 있는지 확인
  * native-host/native_host.log 파일에서 오류 확인

- 확장 프로그램이 동작하지 않는 경우:
  * 크롬을 완전히 재시작
  * chrome://extensions/에서 확장 프로그램 활성화 상태 확인

## 제거 방법
installer/uninstall.bat 실행
""")
    
    # ZIP 파일로 압축
    zip_path = dist_dir / "EverythingEverywhere_portable.zip"
    
    print(f"\n[압축] ZIP 파일 생성 중: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(package_dir)
                zipf.write(file_path, arc_path)
                
    file_size = zip_path.stat().st_size / 1024  # KB
    
    print(f"\n[완료] 배포 패키지 생성 완료!")
    print(f"   폴더: {package_dir}")
    print(f"   ZIP: {zip_path} ({file_size:.1f} KB)")
    print(f"\n[사용법] 다른 컴퓨터에서 사용하려면:")
    print(f"   1. {zip_path.name} 파일을 전송")
    print(f"   2. 압축 해제 후 setup.bat 실행")

if __name__ == "__main__":
    create_distribution_package()