# LogLab

<img src="docs/_static/loglab.png" width="128" height="128" />

[![Tests](https://github.com/haje01/loglab/actions/workflows/test.yml/badge.svg)](https://github.com/haje01/loglab/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

JSON Lines 로그 형식을 설계하고 검증하기 위한 Python 툴

## ✨ 주요 기능

- 로그를 객체지향적이며 재활용 가능한 형태로 설계
- 설계된 로그에 관한 문서 자동 생성
- 실제 출력된 로그가 설계에 맞게 작성되었는지 검증
- Python, C#, C++ 로그 객체 코드 생성

## ⚡ 빠른 시작

### 설치

**빌드된 실행 파일 (권장)**
```bash
# GitHub Releases에서 OS에 맞는 파일 다운로드
# https://github.com/haje01/loglab/releases
```

**소스 코드 설치**
```bash
git clone https://github.com/haje01/loglab
cd loglab
uv venv
uv pip install -e .
```

### 기본 사용법

```bash
# 로그 스키마 확인
loglab show example/foo.lab.json

# 로그 파일 검증
loglab verify example/foo.lab.json example/foo.jsonl

# HTML 문서 생성
loglab html example/foo.lab.json -o docs.html
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

- **[전체 문서](https://loglab.readthedocs.io/)** - LogLab 의 상세한 가이드와 튜토리얼
- **[생성 문서 예](https://htmlpreview.github.io/?https://raw.githubusercontent.com/haje01/loglab/master/example/rpg.html)** - 가상의 RPG 게임을 위한 로그 문서 사례

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
uv pip install -e .[dev]

# 테스트 실행
pytest tests/

# 빌드
./tools/build.sh
```

## 📄 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일 참조

## 🤝 기여

버그 리포트와 기능 제안은 [Issues](https://github.com/haje01/loglab/issues)에서 환영합니다.

---

> 로그랩은 Windows, Linux, macOS에서 사용할 수 있습니다.
