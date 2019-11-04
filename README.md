# loglab
Design &amp; Apply Log Schema.

![diagram](images/diagram.png)

LogLab은 로그를 쉽고 효율적으로 설계하고 활용할 수 있는 툴입니다.

- LogLab은 **메타파일**로 불리는 파일에 내용을 기술합니다.
- 메타파일은 확장자가 `.meta.json`입니다.

## 빠르게 시작하기

아래와 같은 메타파일로 간단한 로그를 설계할 수 있습니다.

```json
{
    "project": {
        "name": "단순 로그 예제",
        "desc": "단순한 로그 사용예를 보여줍니다."
    },
    "events": {
        "Login": {
            "desc": "로그인"
        },
        "Logout": {
            "desc": "로그 아웃"
        }
    }
}
```
앞으로 json 요소의 설명은 `/project/name` 식의 경로 형태로 지정해서 하겠습니다:

- `/project` 로그를 사용할 프로젝트 정보 객체
- `/project/name` 프로젝트 이름
- `/project/desc` 프로젝트 설명
- `/events` 이 아래 *이벤트 이름* + *정보 객체* 식으로 로그 이벤트를 선언합니다.
- `/events/Login` 로그인 이벤트 이름
- `/events/Login/desc` 로그인 이벤트의 설명


위 내용을 `simple.meta.json` 파일로 저장하면, 다음처럼 이 메타파일에 기반한 **샘플 로그**를 생성할 수 있습니다.
```bash
$ loglab sample simple.meta.json

{
    "Logout": {
        "datetime": "20191109-11-13T20:17:39+00:00"
    }
}
{
    "Login": {
        "datetime": "20191109-11-13T20:17:40+00:00"
    }
}
{
    "Login": {
        "datetime": "20191109-11-13T20:17:41+00:00"
    }
}
{
    "Logout": {
        "datetime": "20191109-11-13T20:17:42+00:00"
    }
}
```
샘플 로그는 로그의 모습을 확인하기 위해 메타파일 기반으로 생성하는 가짜 로그입니다. 4개의 임의 이벤트가 기본 형식인 `json`으로 출력되고 있습니다.

출력 형식은 `csv`나 `tsv`로도 가능합니다.

```bash
$ loglab sample simple.meta.json --format csv

"20191109-11-13T20:17:39+00:00", "Logout"
"20191109-11-13T20:17:40+00:00", "Login"
"20191109-11-13T20:17:41+00:00", "Login"
"20191109-11-13T20:17:42+00:00", "Logout"
```

### 이벤트에 속성 추가하기

로그 이벤트별로 다양한 속성(property)를 추가할 수 있습니다. 메타파일을 아래처럼 수정해 서버번호 속성을 추가합니다.

```json
{
    "project": {
        "name": "단순 로그 예제",
        "desc": "단순한 로그 사용예를 보여줍니다."
    },
    "events": {
        "Login": {
            "desc": "로그인",
            "props": [
                [ServerNo, "number"]
            ]
        },
        "Logout": {
            "desc": "로그 아웃",
            "props": [
                [ServerNo, "number"]
            ]
        }
    }
}
```
예제에서는 이벤트와 속성이름은 각 단어를 대문자로 시작하는 `PascalCase` 표기를 따르나, 원하는대로 자유롭게 선택하실 수 있습니다.

- 가능한 속성의 타입은 `string`, `number`, `boolean`, `array`의 네 가지입니다.
- `/events/Login/props` 이 아래 로그인 이벤트의 속성을 기술합니다.
- 각 속성은 `[속성_이름, 속성_타입]` 형태의 리스트로 선언합니다.
- 샘플 로그에서 출력된 이벤트 일시와 이름도 사실 속성이며, 이것은 LogLab에 의해 기본으로 추가되었습니다.

샘플 로그를 출력해보면:
```bash
$ loglab sample simple.meta.json

{
    "Logout": {
        "datetime": "20191109-11-13T20:17:39+00:00",
        "ServerNo": 394801
    }
}
{
    "Login": {
        "datetime": "20191109-11-13T20:17:40+00:00",
        "ServerNo": -9849
    }
}
{
    "Login": {
        "datetime": "20191109-11-13T20:17:41+00:00",
        "ServerNo": 10390
    }
}
{
    "Logout": {
        "datetime": "20191109-11-13T20:17:42+00:00",
        "ServerNo": 791
    }
}
```

임의의 `ServerID`가 추가된 것이 보입니다.

### 이벤트 속성 값의 범위 지정하기

서버의 번호 속성에 - 값이 나오고 있어 좀 이상합니다. 속성 값의 범위를 지정하면 로그의 엄격한 검증이 가능하고, 샘플 생성도 자연스러워집니다. 위에서 사용한 **리스트형 속성 선언**은 간략해서 보기가 좋지만, 기술 내용에 한계가 있습니다. 범위 지정을 위해서는 **객체형 속성 선언**이 필요합니다.

```json
{
    "project": {
        "name": "단순 로그 예제",
        "desc": "단순한 로그 사용예를 보여줍니다."
    },
    "events": {
        "Login": {
            "desc": "로그인",
            "props": {
                "ServerNo": {
                    "type": "number",
                    "minimum": 1,
                    "exclusiveMaximum": 10
                }
            }
        },
        "Logout": {
            "desc": "로그 아웃",
            "props": {
                "ServerNo": {
                    "type": "number",
                    "minimum": 1,
                    "exclusiveMaximum": 10
                }
            }
        }
    }
}
```

좀 더 복잡해졌지만, 이렇게 하면 서버 번호 속성을 1 이상 10 이하로 제한할 수 있습니다. 다시 샘플을 출력해보면:

```bash
$ loglab sample simple.meta.json

{
    "Logout": {
        "datetime": "20191109-11-13T20:17:39+00:00",
        "ServerNo": 7
    }
}
{
    "Login": {
        "datetime": "20191109-11-13T20:17:40+00:00",
        "ServerNo": 3
    }
}
{
    "Login": {
        "datetime": "20191109-11-13T20:17:41+00:00",
        "ServerNo": 1
    }
}
{
    "Logout": {
        "datetime": "20191109-11-13T20:17:42+00:00",
        "ServerNo": 10
    }
}
```
범위가 잘 적용되었습니다.

## 로그 도메인 만들기

