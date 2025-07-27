document.addEventListener('DOMContentLoaded', () => {
  const statusDiv = document.getElementById('status');
  
  // 백그라운드 스크립트에서 상태 확인
  chrome.runtime.sendMessage({ action: 'getStatus' }, (response) => {
    if (response && response.status === 'active') {
      statusDiv.textContent = '✅ 확장 프로그램 활성화됨';
      statusDiv.className = 'status active';
    } else {
      statusDiv.textContent = '❌ 확장 프로그램 오류';
      statusDiv.className = 'status error';
    }
  });
});