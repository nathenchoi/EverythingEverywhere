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

// 클립보드에 텍스트 복사
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    console.log('텍스트가 클립보드에 복사됨:', text);
  }).catch(err => {
    console.error('클립보드 복사 실패:', err);
    // Fallback: content script를 통한 복사 시도
    fallbackCopyToClipboard(text);
  });
}

// 클립보드 복사 실패 시 대체 방법
function fallbackCopyToClipboard(text) {
  // content script 주입을 통한 복사
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    if (tabs[0]) {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id },
        func: (textToCopy) => {
          // 임시 textarea 생성
          const textarea = document.createElement('textarea');
          textarea.value = textToCopy;
          document.body.appendChild(textarea);
          textarea.select();
          document.execCommand('copy');
          document.body.removeChild(textarea);
        },
        args: [text]
      });
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