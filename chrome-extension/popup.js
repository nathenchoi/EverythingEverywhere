document.addEventListener('DOMContentLoaded', () => {
  const statusDiv = document.getElementById('status');
  const pathInfoDiv = document.getElementById('pathInfo');
  const settingsToggle = document.getElementById('settingsToggle');
  const settingsSection = document.getElementById('settingsSection');
  const pathInput = document.getElementById('pathInput');
  const testBtn = document.getElementById('testBtn');
  const saveBtn = document.getElementById('saveBtn');
  const pathValidation = document.getElementById('pathValidation');
  const suggestions = document.getElementById('suggestions');
  const suggestionsList = document.getElementById('suggestionsList');

  let currentStatus = null;

  // 초기 상태 확인
  checkEverythingStatus();

  // 설정 토글 버튼
  settingsToggle.addEventListener('click', () => {
    if (settingsSection.classList.contains('hidden')) {
      settingsSection.classList.remove('hidden');
      settingsToggle.textContent = '닫기';
      loadSuggestions();
    } else {
      settingsSection.classList.add('hidden');
      settingsToggle.textContent = '설정';
    }
  });

  // 테스트 버튼
  testBtn.addEventListener('click', () => {
    const path = pathInput.value.trim();
    if (!path) {
      showValidation('경로를 입력해주세요.', 'error');
      return;
    }
    
    testBtn.textContent = '테스트 중...';
    testBtn.disabled = true;
    
    sendNativeMessage({ action: 'validate_path', path: path }, (response) => {
      testBtn.textContent = '테스트';
      testBtn.disabled = false;
      
      if (response && response.success) {
        if (response.valid) {
          showValidation('✅ 유효한 Everything.exe 경로입니다!', 'success');
        } else {
          showValidation('❌ 유효하지 않은 경로입니다. Everything.exe 파일이 있는지 확인해주세요.', 'error');
        }
      } else {
        showValidation('❌ 경로 검증 중 오류가 발생했습니다.', 'error');
      }
    });
  });

  // 저장 버튼
  saveBtn.addEventListener('click', () => {
    const path = pathInput.value.trim();
    if (!path) {
      showValidation('경로를 입력해주세요.', 'error');
      return;
    }
    
    saveBtn.textContent = '저장 중...';
    saveBtn.disabled = true;
    
    sendNativeMessage({ action: 'set_path', path: path }, (response) => {
      saveBtn.textContent = '저장';
      saveBtn.disabled = false;
      
      if (response && response.success) {
        showValidation('✅ Everything 경로가 저장되었습니다!', 'success');
        // 상태 다시 확인
        setTimeout(checkEverythingStatus, 500);
      } else {
        showValidation(`❌ 저장 실패: ${response?.error || '알 수 없는 오류'}`, 'error');
      }
    });
  });

  // 추천 경로 클릭
  suggestionsList.addEventListener('click', (e) => {
    if (e.target.classList.contains('suggestion-path')) {
      pathInput.value = e.target.textContent;
    }
  });

  function checkEverythingStatus() {
    statusDiv.textContent = '상태 확인 중...';
    statusDiv.className = 'status';
    
    sendNativeMessage({ action: 'get_status' }, (response) => {
      currentStatus = response;
      
      if (response && response.success) {
        if (response.everything_found) {
          statusDiv.textContent = '✅ Everything 연결됨';
          statusDiv.className = 'status active';
          
          if (response.everything_path) {
            pathInfoDiv.textContent = `경로: ${response.everything_path}`;
            pathInfoDiv.classList.remove('hidden');
          }
        } else {
          statusDiv.textContent = '⚠️ Everything을 찾을 수 없습니다';
          statusDiv.className = 'status warning';
          pathInfoDiv.classList.add('hidden');
        }
      } else {
        statusDiv.textContent = '❌ Native Host 연결 실패';
        statusDiv.className = 'status error';
        pathInfoDiv.classList.add('hidden');
      }
    });
  }

  function loadSuggestions() {
    if (currentStatus && currentStatus.available_paths && currentStatus.available_paths.length > 0) {
      suggestionsList.innerHTML = '';
      currentStatus.available_paths.forEach(path => {
        const pathDiv = document.createElement('div');
        pathDiv.className = 'suggestion-path';
        pathDiv.textContent = path;
        suggestionsList.appendChild(pathDiv);
      });
      suggestions.classList.remove('hidden');
    } else {
      // 일반적인 경로들 제시
      const commonPaths = [
        'C:\\Program Files\\Everything\\Everything.exe',
        'C:\\Program Files (x86)\\Everything\\Everything.exe',
        'C:\\Everything\\Everything.exe'
      ];
      
      suggestionsList.innerHTML = '';
      commonPaths.forEach(path => {
        const pathDiv = document.createElement('div');
        pathDiv.className = 'suggestion-path';
        pathDiv.textContent = path;
        suggestionsList.appendChild(pathDiv);
      });
      suggestions.classList.remove('hidden');
    }
  }

  function showValidation(message, type) {
    pathValidation.textContent = message;
    pathValidation.className = `info status ${type}`;
    pathValidation.classList.remove('hidden');
    
    // 3초 후 자동 숨김
    setTimeout(() => {
      pathValidation.classList.add('hidden');
    }, 3000);
  }

  function sendNativeMessage(message, callback) {
    try {
      chrome.runtime.sendNativeMessage('com.everythingeverywhere.host', message, callback);
    } catch (error) {
      console.error('Native message error:', error);
      if (callback) {
        callback({ success: false, error: 'Native messaging failed' });
      }
    }
  }
});