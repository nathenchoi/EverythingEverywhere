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
        }
      }
    }
  );
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