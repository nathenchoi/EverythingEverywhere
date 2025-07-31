// Native Messaging Host 이름
const NATIVE_HOST_NAME = 'com.everythingeverywhere.host';

// 확장 프로그램이 설치되거나 업데이트될 때
chrome.runtime.onInstalled.addListener(() => {
  // 컨텍스트 메뉴 생성
  chrome.contextMenus.create({
    id: 'searchInEverything',
    title: '로컬에서 Everything으로 검색하기: "%s"',
    contexts: ['selection']
  });
  
  console.log('EverythingEverywhere extension installed');
});

// 컨텍스트 메뉴 클릭 시
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'searchInEverything' && info.selectionText) {
    searchInEverything(info.selectionText);
  }
});

// Everything에서 검색 실행
function searchInEverything(searchText) {
  console.log('Searching for:', searchText);
  
  // 클립보드 설정 확인 후 복사
  chrome.storage.sync.get(['copyToClipboard'], (result) => {
    const copyEnabled = result.copyToClipboard !== undefined ? result.copyToClipboard : true;
    
    // Native Messaging Host로 메시지 전송
    chrome.runtime.sendNativeMessage(
      NATIVE_HOST_NAME,
      { 
        action: 'search',
        query: searchText 
      },
      (response) => {
        if (chrome.runtime.lastError) {
          console.error('Native messaging error:', chrome.runtime.lastError);
          // 사용자에게 오류 알림
          chrome.notifications.create({
            type: 'basic',
            iconUrl: 'icon48.png',
            title: 'Everything 검색 오류',
            message: 'Everything 검색을 실행할 수 없습니다. Native Host가 설치되어 있는지 확인해주세요.'
          });
        } else {
          console.log('Native response:', response);
          if (response && response.success) {
            console.log('Everything search launched successfully');
            
            // 검색 성공 후 클립보드 복사 실행 (설정에 따라)
            if (copyEnabled) {
              performClipboardCopy(searchText);
            } else {
              // 복사 기능이 비활성화된 경우 간단한 성공 알림
              chrome.notifications.create({
                type: 'basic',
                iconUrl: 'icon48.png',
                title: '✅ Everything 검색 완료',
                message: `"${searchText.length > 20 ? searchText.substring(0, 20) + '...' : searchText}" 검색이 실행되었습니다.`
              });
            }
          }
        }
      }
    );
  });
}

// 클립보드에 텍스트 복사 (Service Worker 환경에서 작동)
function performClipboardCopy(text) {
  console.log('클립보드 복사 시작:', text);
  
  // 활성 탭 찾기
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    if (chrome.runtime.lastError) {
      console.error('탭 쿼리 오류:', chrome.runtime.lastError);
      showSimpleNotification('클립보드 복사 실패', '활성 탭을 찾을 수 없습니다.');
      return;
    }
    
    if (!tabs || !tabs[0]) {
      console.error('활성 탭이 없음');
      showSimpleNotification('클립보드 복사 실패', '활성 탭을 찾을 수 없습니다.');
      return;
    }
    
    const activeTab = tabs[0];
    console.log('활성 탭 찾음:', activeTab.id, activeTab.url);
    
    // content script 주입하여 클립보드 복사
    chrome.scripting.executeScript({
      target: { tabId: activeTab.id },
      func: (textToCopy) => {
        console.log('Content script 실행, 복사할 텍스트:', textToCopy);
        
        // Method 1: 모던 Clipboard API 시도
        if (navigator.clipboard && window.isSecureContext) {
          return navigator.clipboard.writeText(textToCopy)
            .then(() => {
              console.log('Clipboard API 성공');
              return { success: true, method: 'clipboard-api' };
            })
            .catch((err) => {
              console.log('Clipboard API 실패:', err);
              // Method 2: execCommand fallback
              return new Promise((resolve) => {
                try {
                  const textarea = document.createElement('textarea');
                  textarea.value = textToCopy;
                  textarea.style.position = 'fixed';
                  textarea.style.left = '-9999px';
                  textarea.style.top = '-9999px';
                  document.body.appendChild(textarea);
                  textarea.focus();
                  textarea.select();
                  
                  const success = document.execCommand('copy');
                  document.body.removeChild(textarea);
                  
                  console.log('execCommand 결과:', success);
                  resolve({ 
                    success: success, 
                    method: success ? 'exec-command' : 'failed',
                    error: success ? null : 'execCommand returned false'
                  });
                } catch (execErr) {
                  console.error('execCommand 오류:', execErr);
                  resolve({ success: false, method: 'failed', error: execErr.message });
                }
              });
            });
        } else {
          console.log('Clipboard API 불가능, execCommand 시도');
          // Clipboard API가 없으면 바로 execCommand 시도
          try {
            const textarea = document.createElement('textarea');
            textarea.value = textToCopy;
            textarea.style.position = 'fixed';
            textarea.style.left = '-9999px';
            textarea.style.top = '-9999px';
            document.body.appendChild(textarea);
            textarea.focus();
            textarea.select();
            
            const success = document.execCommand('copy');
            document.body.removeChild(textarea);
            
            console.log('execCommand 결과 (직접):', success);
            return Promise.resolve({ 
              success: success, 
              method: success ? 'exec-command-direct' : 'failed',
              error: success ? null : 'execCommand returned false'
            });
          } catch (execErr) {
            console.error('execCommand 오류 (직접):', execErr);
            return Promise.resolve({ success: false, method: 'failed', error: execErr.message });
          }
        }
      },
      args: [text]
    }, (results) => {
      if (chrome.runtime.lastError) {
        console.error('스크립트 주입 실패:', chrome.runtime.lastError);
        showSimpleNotification('클립보드 복사 실패', '스크립트 주입에 실패했습니다.');
        return;
      }
      
      if (!results || !results[0]) {
        console.error('스크립트 실행 결과 없음');
        showSimpleNotification('클립보드 복사 실패', '스크립트 실행 결과를 받지 못했습니다.');
        return;
      }
      
      const result = results[0].result;
      console.log('클립보드 복사 결과:', result);
      
      if (result && result.success) {
        console.log(`클립보드 복사 성공 (${result.method}):`, text);
        showClipboardNotification(text);
      } else {
        console.error('클립보드 복사 실패:', result?.error || 'Unknown error');
        showSimpleNotification('클립보드 복사 실패', result?.error || '알 수 없는 오류가 발생했습니다.');
      }
    });
  });
}

// 간단한 알림 표시
function showSimpleNotification(title, message) {
  chrome.notifications.create({
    type: 'basic',
    iconUrl: 'icon48.png',
    title: title,
    message: message
  }, (notificationId) => {
    setTimeout(() => {
      chrome.notifications.clear(notificationId);
    }, 4000);
  });
}

// 클립보드 복사 알림 표시
function showClipboardNotification(text) {
  const shortText = text.length > 20 ? text.substring(0, 20) + '...' : text;
  
  chrome.notifications.create({
    type: 'basic',
    iconUrl: 'icon48.png',
    title: '✅ Everything 검색 및 복사 완료',
    message: `"${shortText}"가 클립보드에 복사되었습니다.`
  }, (notificationId) => {
    // 3초 후 알림 자동 제거
    setTimeout(() => {
      chrome.notifications.clear(notificationId);
    }, 3000);
  });
}

// 확장 프로그램 아이콘 클릭 시 간단한 정보 표시를 위한 메시지 리스너
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getStatus') {
    sendResponse({ 
      status: 'active',
      hostName: NATIVE_HOST_NAME 
    });
  }
});