import { Login, Logout } from './loglab_foo';

// Login 이벤트 생성
const loginEvent = new Login(1, 1001, "ios");
console.log("Login Event:", loginEvent.serialize());

// Logout 이벤트 생성 (옵셔널 필드 포함)
const logoutEvent = new Logout(1, 1001);
logoutEvent.PlayTime = 123.45;  // 옵셔널 필드 설정
console.log("Logout Event:", logoutEvent.serialize());

// 객체 재사용을 위한 리셋
loginEvent.reset(2, 2002, "aos");
console.log("Reset Login Event:", loginEvent.serialize());
