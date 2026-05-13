# LogLab

<img src="docs/_static/loglab.png" width="128" height="128" />

[![Tests](https://github.com/haje01/loglab/actions/workflows/test.yml/badge.svg)](https://github.com/haje01/loglab/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

LogLab (로그랩) 은 JSON Lines 로그 형식을 설계, 문서화 및 검증하기 위한 툴입니다.

## ✨ 주요 기능

- 로그를 객체지향적이며 재활용 가능한 형태로 설계
- 설계된 로그에 관한 문서 자동 생성
- 실제 출력된 로그가 설계에 맞게 작성되었는지 검증
- Python, C#, C++, TypeScript 및 Java 로그 객체 코드 생성
- Windows, Linux, macOS 에서 사용할 수 있습니다.

## ⚡ 빠른 시작

### 설치

**uv 기반 설치 (권장)**

먼저 Python 용 패키지 매니저인 `uv` 의 설치가 필요합니다. [uv 설치 페이지](https://docs.astral.sh/uv/getting-started/installation/) 를 참고하여 사용자의 환경에 맞게 설치하도록 합니다.

이제 다음과 같은 `uv` 명령으로 LogLab 을 설치합니다.

```sh
uv tool install --from git+https://github.com/haje01/loglab.git loglab
```

설치가 잘 되었다면 로그랩의 커맨드라인 명령인 `loglab` 을 이용할 수 있습니다. 다음과 같이 입력하여 버전을 확인해봅시다.

```sh
loglab version
0.3.5
```

> 만약 기존에 설치된 loglab 을 최신 버전으로 업그레이드하고 싶다면, 다음과 같은 `uv` 명령을 내리면 됩니다.
> ```sh
> uv tool upgrade loglab
> ```

**소스 코드로 설치**

최신 소스 코드를 기반으로 다음처럼 개발용으로 설치도 가능합니다.

```bash
git clone https://github.com/haje01/loglab
cd loglab
uv venv
source .venv/bin/activate
uv pip install -e .
```

### 기본 사용법 예시

```bash
# 로그 스키마 확인
loglab show example/foo.lab.json

# 로그 파일 검증
loglab verify example/foo.lab.json example/foo.jsonl

# HTML 문서 생성
loglab html example/foo.lab.json -o docs.html

# 로그 객체 코드 생성 (TypeScript)
loglab object example/foo.lab.json ts -o loglab_foo.ts
```

### 스키마와 로그 예제

LogLab 은 지정된 JSON 형식으로 로그 스키마를 정의합니다.

```json
{
  "domain": {
    "name": "foo",
    "desc": "최고의 모바일 게임"
  },
  "events": {
    "Login": {
      "desc": "계정 로그인",
      "fields": [
          ["ServerNo", "integer", "서버 번호"],
          ["AcntId", "integer", "계정 ID"]
      ]
    }
  }
}
```

LogLab 으로 설계된 로그는 [JSON Lines](https://jsonlines.org/) 형식으로 출력됩니다:

```json
{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "Login", "ServerNo": 1, "AcntId": 1000}
{"DateTime": "2021-08-13T20:21:01+09:00", "Event": "Logout", "ServerNo": 1, "AcntId": 1000}
```

## 📖 문서

- **[로그랩 문서](https://loglab.readthedocs.io/)** - 로그랩의 상세한 가이드와 튜토리얼
- **[생성된 문서 예제](https://raw.githack.com/haje01/loglab/master/example/rpg.html)** - 로그랩으로 가상의 RPG 게임을 위한 로그를 설계한 후 자동 생성된 로그 명세 문서

## 🎯 대상 사용자

- 서비스를 위한 로그 설계가 필요한 개발자
- 로그를 처리하고 분석하는 데이터 엔지니어/분석가
- 조직에서 생성되는 로그의 형식을 일관되게 유지/공유하고 싶은 관리자

## 🛠 개발

```bash
# 개발 환경 설정
git clone https://github.com/haje01/loglab.git
cd loglab
uv venv
uv pip install -e . -r requirements-dev.txt

# 테스트 실행
pytest tests/
```

## 📄 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일 참조

## 🤝 기여

버그 리포트와 기능 제안은 [Issues](https://github.com/haje01/loglab/issues)에서 환영합니다.

---
