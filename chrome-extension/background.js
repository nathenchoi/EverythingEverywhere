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
    
    if (copyEnabled) {
      copyToClipboard(searchText);
    }
    
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
            // 성공 시 클립보드 복사 알림 (복사 기능이 활성화된 경우에만)
            if (copyEnabled) {
              showClipboardNotification(searchText);
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
function copyToClipboard(text) {
  // Service Worker에서는 navigator.clipboard를 직접 사용할 수 없으므로
  // content script를 통해 클립보드에 복사
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    if (tabs[0]) {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id },
        func: async (textToCopy) => {
          try {
            // 모던 브라우저의 Clipboard API 시도
            if (navigator.clipboard && navigator.clipboard.writeText) {
              await navigator.clipboard.writeText(textToCopy);
              console.log('클립보드 복사 성공 (Clipboard API):', textToCopy);
              return { success: true, method: 'clipboard-api' };
            } else {
              throw new Error('Clipboard API not available');
            }
          } catch (err) {
            console.log('Clipboard API 실패, fallback 시도:', err);
            
            // Fallback: document.execCommand 방식
            try {
              const textarea = document.createElement('textarea');
              textarea.value = textToCopy;
              textarea.style.position = 'fixed';
              textarea.style.opacity = '0';
              document.body.appendChild(textarea);
              textarea.select();
              
              const success = document.execCommand('copy');
              document.body.removeChild(textarea);
              
              if (success) {
                console.log('클립보드 복사 성공 (execCommand):', textToCopy);
                return { success: true, method: 'exec-command' };
              } else {
                throw new Error('execCommand failed');
              }
            } catch (fallbackErr) {
              console.error('클립보드 복사 완전 실패:', fallbackErr);
              return { success: false, error: fallbackErr.message };
            }
          }
        },
        args: [text]
      }, (results) => {
        if (chrome.runtime.lastError) {
          console.error('스크립트 주입 실패:', chrome.runtime.lastError);
        } else if (results && results[0]) {
          const result = results[0].result;
          if (result && result.success) {
            console.log(`클립보드 복사 성공 (${result.method}):`, text);
          } else {
            console.error('클립보드 복사 실패:', result?.error || 'Unknown error');
          }
        }
      });
    } else {
      console.error('활성 탭을 찾을 수 없음');
    }
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