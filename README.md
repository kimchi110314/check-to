# 러끼 팔로워 10만 명 알림 시스템

치지직 스트리머 '러끼'의 팔로워 수를 1시간마다 확인해서, 10만 명을 넘으면
지정한 이메일로 알림을 보내는 시스템입니다. GitHub Actions로 자동 실행되므로
컴퓨터를 켜둘 필요가 없습니다.

## 1. GitHub 저장소 만들기

1. GitHub에 로그인 후 새 저장소(Repository)를 하나 만듭니다. (Private 추천)
2. 이 폴더(`chzzk-follower-alert`) 안의 파일들을 그대로 그 저장소에 업로드합니다.
   - 방법 A: GitHub 웹사이트에서 "Add file → Upload files"로 전체 업로드
   - 방법 B: git으로 push
     ```
     git init
     git add .
     git commit -m "초기 설정"
     git branch -M main
     git remote add origin <저장소 주소>
     git push -u origin main
     ```

## 2. Gmail 앱 비밀번호 만들기

일반 Gmail 로그인 비밀번호는 사용할 수 없고, 별도의 "앱 비밀번호"가 필요합니다.

1. 구글 계정 → 보안 → **2단계 인증을 먼저 켭니다** (앱 비밀번호는 2단계 인증이 켜져 있어야 생성 가능)
2. https://myaccount.google.com/apppasswords 접속
3. 앱 이름을 아무거나 입력(예: "chzzk-alert") 후 생성
4. 나오는 16자리 비밀번호를 복사해둡니다 (다시 볼 수 없으니 꼭 저장)

## 3. GitHub 저장소에 비밀 값(Secrets) 등록

저장소 페이지 → **Settings → Secrets and variables → Actions → New repository secret**
에서 아래 3개를 각각 등록합니다.

| Name | Value |
|---|---|
| `GMAIL_ADDRESS` | 알림을 보낼 발신용 Gmail 주소 |
| `GMAIL_APP_PASSWORD` | 2번 단계에서 만든 16자리 앱 비밀번호 |
| `NOTIFY_EMAIL` | `kimchi110201@gmail.com` (알림 받을 주소) |

## 4. 자동 실행 확인

- 별도 설정 없이 업로드하는 순간부터 매시 정각에 자동 실행됩니다.
- 저장소의 **Actions** 탭에서 실행 기록과 로그(현재 팔로워 수 등)를 확인할 수 있습니다.
- 지금 바로 테스트하고 싶다면 Actions 탭 → "Check CHZZK Follower Count" 워크플로우 →
  **Run workflow** 버튼으로 수동 실행해볼 수 있습니다.

## 동작 방식 요약

- `check_followers.py`가 치지직 API에서 러끼 채널의 팔로워 수를 가져옵니다.
- 10만 명 이상이고 아직 알림을 보낸 적이 없으면(`state.json`의 `notified: false`)
  이메일을 발송하고 `notified: true`로 기록합니다.
- 한 번 알림을 보내면 이후에는 다시 보내지 않습니다.
