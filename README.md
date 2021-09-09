# LogLab

LogLab(로그랩) 은 다양한 서비스의 로그를 설계하고 활용하기 위한 툴이다. 크게 다음과 같은 기능을 가지고 있다:

- 로그를 객체지향적으로 설계
- 설계된 로그의 문서 출력
- 설계된 로그에 준하는 더비(가짜) 로그 생성
- 실제 출력된 로그가 설계에 맞게 작성되었는지 검증

로그랩은 윈도우, Linux, MacOS 에서 사용할 수 있다.

## 설치

LogLab의 설치를 위해서는 최소 Python 3.6 이상이 필요하다. 설치되어 있지 않다면 [이곳](https://www.python.org/) 에서 가급적 최신 버전의 파이썬을 설치하도록 하자.

LogLab 의 홈페이지는 https://github.com/haje01/loglab 이다. 다음과 같이 설치하자:

```
$ git checkout https://github.com/haje01/loglab
$ pip install -e .
```

설치가 잘 되었다면 로그랩의 커맨드라인 툴 `loglab` 을 이용할 수 있다. 아래와 같이 입력해보자:

```
$ loglab
Usage: loglab [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  doc      로그 문서 표시.
  dummy    가짜 로그 생성.
  schema   로그 및 플로우 파일용 스키마 생성.
  verify   생성된 로그 파일 검증.
  version  로그랩 버전 표시.
```


위에서 볼 수 있듯 `loglab` 에는 몇 가지 명령어가 있는데, 예제를 통해 하나씩 살펴보도록 하겠다. 여기서는 간단히 버전을 확인해보자:

```
$ loglab version
0.0.1
```

이제 가상의 게임 서비스를 위한 로그를 설계하는 예제를 통해 로그랩의 활용법을 빠르게 살펴보자.

## 최초 랩파일 만들기

로그랩은 **랩(Lab)파일** 로 불리는 JSON 파일에 로그 명세를 기술하는 것으로 로그를 설계한다. 랩파일은 로그랩에서 제공하는 JSON 스키마 형식에 맞추어 작성하며, 확장자는 `.lab.json` 을 사용한다. [VS Code](https://code.visualstudio.com/) 등 JSON 스키마를 지원하는 에디터를 이용하면 인텔리센스(IntelliSense) 기능이 지원되어 편집에 용이할 것이다.

빈 작업 디렉토리를 하나 만들고, 에디터를 사용해 아래와 같은 내용으로 `foo.lab.json` 파일을 만들자.

> 에졔는 /home/ubuntu/loglab_test 디렉토리를 이용하였다.

```js
{
	"events": {
		"Login": {
			"desc": "계정 로그인"
		}
	}
}
```

로그랩에서는 로깅의 대상이 되는 각 사건을 **이벤트(event)** 라고 한다. 각 이벤트에는 관련된 하나 이상의 **필드(field)**를 기술할 수 있는데, 위 예에서는 아직 필드 정보는 없다.

랩파일의 `events` 항목 아래에 다양한 이벤트 요소를 기술할 수 있다. 여기서는 계정 로그인 이벤트를 위한 `Login` 요소를 만들고, 그 아래의 `desc` 요소에 이 이벤트에 대한 설명을 기입하였다.


이제 작업 디텍토리에서 `doc` 명령을 내려보자:

```
$ loglab doc

[사용할 랩파일 : /home/ubuntu/loglab_test/foo.lab.json]

Event : Login
Description : 계정 로그인
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
+----------+----------+---------------+
```

`doc` 명령은 로그랩 파일에 기술된 내용을 참고해 로그 이벤트에 대한 문서를 텍스트 형식으로 출력한다. 랩파일에 기술된 이벤트 이름 및 설명이 출력되는 것을 알 수 있다.

그런데, 아직 아무런 필드를 명시하지 않았음에도 `DateTime` 이라는 필드가 보인다. 이것은 *모든 로그에 이벤트 발생 일시는 꼭 필요하기에 로그랩에서 자동으로 생성*해준 것이다.

> 앞의 `Login` 과 `DateTime` 에서 알 수 있듯, 로그랩의 이벤트 및 필드 이름은 단어의 시작을 대문자로 (Pascal Case) 한다.

### 랩파일의 선택

`loglab` 은 실행시 현재 디렉토리에서 확장자가 `.lab.json` 인 파일을 찾아보고, 만약 하나의 랩파일만 발견된다면 그것을 이용한다.

> 출력의 [사용할 랩파일:~] 부분에서 `loglab` 이 어떤 랩파일을 이용하는지 확인할 수 있다.

먄약 랩파일이 없거나, 하나 이상의 랩파일이 존재한다면 다음과 같이 사용할 랩파일을 구체적으로 명시할 것을 요구한다.

```
Error: 현재 디렉토리에 랩파일이 하나 이상 있습니다. 사용할 랩파일을 명시적으로 지정해 주세요.
```

다음처럼 `doc` 명령의 도움말을 출력해보자:

```
$ loglab doc --help
Usage: loglab doc [OPTIONS]

  로그 문서 표시.

Options:
  -l, --labfile TEXT  사용할 랩파일의 위치를 명시적으로 지정
  --help              Show this message and exit.
```

`loglab` 의 모든 명령에는 위와 같이 `-l` 또는 `--labfile` 옵션이 있는데, 이것을 이용해 이용할 랩파일의 경로를 명시적으로 지정할 수 있다.

### 스키마와 도메인 정보 지정하기

복잡한 구조의 JSON 파일을 편집하다보면 어떤 내용이 기술될 수 있는지 기억하기도 어려워 틀리기 쉽다. 이에 JSON 스키마를 이용하면 편리하다. `foo.lab.json` 파일에 다음처럼 `$schema` 요소를 추가해 보자.

```js
{
	"$schema": "https://raw.githubusercontent.com/haje01/loglab/master/schema/lab.schema.json",
	"events": {
		"Login": {
			"desc": "계정 로그인."
		}
	}
}
```

사용하는 에디터가 VS Code 와같이 JSON 스키마를 지원한다면, 이제 인텔리센스 기능의 가이드를 받을 수 있다.

추가적으로, 랩파일의 **도메인(Domain) 정보**를 추가하면 도움이 된다. 이것은 이 랩파일이 어떤 서비스를 위한 것인가에 대한 정보이다. 다음과 같이 `domain` 항목 아래 도메인 이름 및 설명을 기술한다.

```js
{
	"$schema": "https://raw.githubusercontent.com/haje01/loglab/master/schema/lab.schema.json",
	"domain": {
		"name": "foo",
		"desc": "위대한 모바일 게임"
	},
	"events": {
		"Login": {
			"desc": "계정 로그인"
		}
    }
}
```

> 스키마가 잘 동작한다면 아래와 같은 가이드를 볼 수 있을 것이다.
> ![스키마 가이드](image/guide.png)

도메인 정보 추가 후 다시 `doc` 명령을 실행하면 아래와 같이 출력된다.

```
[사용할 랩파일 : /home/ubuntu/loglab_test/foo.lab.json]

Domain : foo
Description : 위대한 모바일 게임

Event : Login
Description : 계정 로그인
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
+----------+----------+---------------+
```

## 필드의 추가

필드는 이벤트에 관한 상세 정보를 표현한다. 기본으로 생성된 `DateTime` 외 필드를 추가해보자.

필드 정보는 이벤트 요소 아래 `fields` 항목에 기술한다. 그것은 JSON 리스트 타입인데, 그것의 항목 타입도 3개 항목을 가지는 리스트이다. 각각은 아래와 같은 형식이다.

```
    "fields": [
        ['필드 이름', '필드 타입', '필드 설명']
        ['필드 이름', '필드 타입', '필드 설명']
        .
        .
        .
    ]
```

로그랩에서 사용할 수 있는 필드의 타입은 다음과 같다:

- `datetime` : 일시. [RFC3339](https://json-schema.org/latest/json-schema-validation.html#RFC3339)를 따른다.
- `string` : 문자열
- `integer`: 정수
- `number` : 실수 (`float` 과 일치)
- `boolean` : 불린 (`true` 또는 `false`)

예를 들어, `Login` 이벤트의 경우 로그인한 계정 ID 필드가 필요할 것이다. 아래와 같이 추가한다:

```
"Login": {
    "desc": "계정 로그인",
    "fields": [
        ["AcntId", "integer", "계정 ID"]
    ]
}}
```

이제 `doc` 명령을 내려보면:

```
$ loglab doc
# 생략

Event : Login
Description : 계정 로그인
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
| AcntId   | integer  | 계정 ID       |
+----------+----------+---------------+
```

계정 정보 필드가 추가된 것을 확인할 수 있다.

## 새로운 이벤트의 추가

계정의 로그인 이벤트가 있다면, 로그아웃도 있어야 하지 않을까? 다음과 같이 추가하자.

```js
{
    // 생략

	"events": {
		"Login": {
			"desc": "계정 로그인",
			"fields": [
				["AcntId", "integer", "계정 ID"]
			]
		},
		"Logout": {
			"desc": "계정 로그아웃",
			"fields": [
				["AcntId", "integer", "계정 ID"]
			]
		}
	}
}
```

`doc` 명령을 내려보면:

```
$ loglab doc
# 생략

Event : Login
Description : 계정 로그인
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
| AcntId   | integer  | 계정 ID       |
+----------+----------+---------------+

Event : Logout
Description : 계정 로그인
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
| AcntId   | integer  | 계정 ID       |
+----------+----------+---------------+
```

`Logout` 이 추가된 것을 알 수 있다.

그런데 로그인, 로그아웃 이벤트 모두 `AcntId` 필드을 가지고 있는 것이 보인다. 앞으로 계정에 관한 다른 이벤트를 만든다면 거기에도 이 필드가 필요할 것이다.  이런 중복 기술을 방지할 수 없을까?

## 믹스인을 활용한 리팩토링

**믹스인(mixin)** 은 다른 요소에서 선언한 필드를 가져와서 쓰는 방법이다. 믹스인을 활용하면 다양한 이벤트에서 공통적으로 필요한 필드를 중복없이 재활용할 수 있다.

믹스인을 하기 위해서는 **베이스(base)** 요소 가 필요하다. 베이스는 이벤트와 비슷하나, 그 자체로 직접 사용되지는 않고, 이벤트 요소나 다른 베이스에서 참조되기 위한 용도이다. 베이스는 랩파일의 `bases` 항목 아래 다음과 같은 형식으로 정의한다:

```js
{
	// 생략

	"bases": {
		"Account": {
			"desc": "계정 이벤트",
			"fields": [
				["AcntId", "integer", "계정 ID"]
			]
		}
	},
	"events": {
		"Login": {
			"desc": "계정 로그인",
			"mixins": ["bases.Account"]
		},
		"Logout": {
			"desc": "계정 로그인",
			"mixins": ["bases.Account"]
		}
	}
}

```

위 예에서 `bases` 항목 아래 `Account` 라는 베이스를 만들었다. 여기에 계정 관련 이벤트를 위한 공통 필드를 가지도록 하는데, 일단은 `AcntId` 만 있다.

이제 기존 `Login`, `Logout` 이벤트는 이 베이스를 믹스인하도록 하자. 각 이벤트에 `mixin` 항목을 만들고 `bases.Account` 를 갖는 리스트를 기술한다.

이렇게 하면 각 이벤트는 `Account` 의 필드를 가져다 쓰게 되는 것이다. `doc` 명령으로 확인하면:

```$ loglab doc
# 생략

Event : Login
Description : 계정 로그인
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
| AcntId   | integer  | 계정 ID       |
+----------+----------+---------------+

Event : Logout
Description : 계정 로그인
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
| AcntId   | integer  | 계정 ID       |
+----------+----------+---------------+
```

두 이벤트의 `fields` 항목은 없지만 베이스의 항목을 가져와 원래대로 결과를 유지하는 것을 알 수 있다.

> `doc` 명령으로 출력되는 문서에 베이스는 없는 것을 확인할 수 있다. 베이스는 참조되어 사용되어질 뿐, 그 자체로 이벤트는 아니기 때문이다.


## 게임관련 이벤트와 필드의 추가

이제 기본적인 랩파일 작성 방법을 알게 되었다. 지금까지 배운 것을 활용하여 실제 게임에서 발생할 수 있는 다양한 이벤트를 추가해보겠다.

### 서버 번호 필드

게임 서비스내 대부분 이벤트는 특정 서버에서 발생하기 마련이다. 어떤 서버의 이벤트인지 표시하기 위해 다음과 같은 베이스를 추가한다.

```js
{
	// 생략

	"bases": {
    	// 생략
		"Server": {
			"desc": "서버 이벤트",
			"fields": [
				["ServerNo", "integer", "서버 번호"]
			]
		}
	},

// 생략
}
```

`Login`, `Logout` 이벤트도 당연히 특정 서버에 관한 것이기에, 다음과 같이 믹스인에 추가한다.

```js
{
    // 생략
	"events": {
		"Login": {
			"desc": "계정 로그인",
			"mixins": ["bases.Account", "bases.Server"]
		},
		"Logout": {
			"desc": "계정 로그인",
			"mixins": ["bases.Account", "bases.Server"]
		}
	}
}
```

`doc` 명령으로 `ServerNo` 필드가 추가된 것을 확인할 수 있다.

```
$ loglab doc
# 생략

Event : Login
Description : 계정 로그인
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
| AcntId   | integer  | 계정 ID       |
| ServerNo | integer  | 서버 번호     |
+----------+----------+---------------+

Event : Logout
Description : 계정 로그인
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
| AcntId   | integer  | 계정 ID       |
| ServerNo | integer  | 서버 번호     |
+----------+----------+---------------+
```


만약 서비스에서 계정에 관한 이벤트가 항상 서버 단위로 일어난다면, 계정 이벤트에 서버 이벤트를 포함해 더 간단히 만들 수 있다:

```js
{
	// 생략

	"bases": {
		"Server": {
			"desc": "서버 이벤트",
			"fields": [
				["ServerNo", "integer", "서버 번호"]
			]
		},
        "Account": {
			"desc": "계정 이벤트",
			"mixins": ["bases.Server"],
			"fields": [
				["AcntId", "integer", "계정 ID"]
			]
		}
	},
	"events": {
		"Login": {
			"desc": "계정 로그인",
			"mixins": ["bases.Account"]
		},
		"Logout": {
			"desc": "계정 로그인",
			"mixins": ["bases.Account"]
		}
	}
}
```


`Account` 베이스에 `Server` 를 믹스인하여 계정 로그인/로그아웃 이벤트가 `Account` 만 믹스인 하면 되도록 하였다.

> 믹스인을 할 요소의 `bases` 항목 내 등장 순서는 중요하지 않다. 위의 경우 `Account` 가 `Server` 앞에 오더라도 문제가 없다.


### 믹스인의 처리 순서

 믹스인은 `mixin` 리스트에 등장하는 순서대로 수행된다. 이것을 이용하면 특정 필드의 순서를 조정하거나 타입을 덮어쓸 수 있다. 예를 들어 위 예에서 `ServerNo` 필드가 `AcntId` 보다 먼저 나오게 하고 싶다면 `mixin` 리스트에 다음과 같이 바꿔주면 된다.

 ```js
         "Login": {
 			"desc": "계정 로그인",
 			"mixins": ["bases.Server", "bases.Account"]
 		},
 ```

```
Event : Login
Description : 계정 로그인
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
| ServerNo | integer  | 서버 번호     |
| AcntId   | integer  | 계정 ID       |
+----------+----------+---------------+
```

> 만약 믹스인과  `fields` 에서 같은 이름의 필드가 등장한다면 `fields` 의 것이 선택된다.


### 캐릭터 관련 이벤트

게임에서 실제 플레이를 하는 것은 게임이 속한 캐릭터이다. 이에 캐릭터 관련 이벤트를 추가해보겠다.

한 계정은 하나 이상의 캐릭터를 소유하고 선택하여 플레이할 수 있기에, 캐릭터의 로그인/아웃 이벤트를 다음과 같이 추가한다:

```js
{
	// 생략
	"bases": {
		"Server": {
			"desc": "서버 요소",
			"fields": [
				["ServerNo", "integer", "서버 번호"]
			]
		},
		"Account": {
			"desc": "계정 요소",
			"mixins": ["bases.Server"],
			"fields": [
				["AcntId", "integer", "계정 ID"]
			]
		},
		"Character": {
			"desc": "캐릭터 요소",
			"mixins": ["bases.Account"],
			"fields": [
				["CharId", "integer", "캐릭터 ID"]
			]
		}
	},
	"events": {
		"Login": {
			"desc": "계정 로그인",
			"mixins": ["bases.Account"]
		},
		"Logout": {
			"desc": "계정 로그인",
			"mixins": ["bases.Account"]
		},
		"CharLogin": {
			"desc": "캐릭터 로그인",
			"mixins": ["bases.Character"]
		},
		"CharLogout": {
			"desc": "캐릭터 로그인",
			"mixins": ["bases.Character"]
		}
	}
}
```

캐릭터의 이벤트는 계정에 속한 것이기에 `Account` 베이스를 믹스인하여 `Character` 베이스를 만들고, 이것을 믹스인 하여 `CharLogin`, `CharLogout` 이벤트를 만들었다. `doc` 명령으로 확인하면:

```
$ loglab doc
# 생략

Event : Login
Description : 계정 로그인
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
| ServerNo | integer  | 서버 번호     |
| AcntId   | integer  | 계정 ID       |
+----------+----------+---------------+

Event : Logout
Description : 계정 로그인
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
| ServerNo | integer  | 서버 번호     |
| AcntId   | integer  | 계정 ID       |
+----------+----------+---------------+

Event : CharLogin
Description : 캐릭터 로그인
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
| ServerNo | integer  | 서버 번호     |
| AcntId   | integer  | 계정 ID       |
| CharId   | integer  | 캐릭터 ID     |
+----------+----------+---------------+

Event : CharLogout
Description : 캐릭터 로그인
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
| ServerNo | integer  | 서버 번호     |
| AcntId   | integer  | 계정 ID       |
| CharId   | integer  | 캐릭터 ID     |
+----------+----------+---------------+
```

4가지 이벤트가 잘 생성된 것을 확인할 수 있다.


### 옵션 필드

지금까지 등장한 모든 필드들은 기본적으로 로그에 꼭 필요한(required) 필드들이었다. 만약 나올 수도 있고 안나와도 괜찮은 필드가 있다면 옵션(option) 필드로 만들 수 있다. 이것은 `fields` 리스트의 각 항목별 4번째 항목에 `true` 또는 `false` 로 지정한다 (`false` 면 기본이기에 굳이 기술할 필요가 없겠다).

예를 들어 `AcntLogout` 이벤트에서 로그인 후 플레이한 시간을 다음과 같이 추가할 수 있겠다:

```js
{
    // 생략

        "Logout": {
			"desc": "계정 로그인",
			"mixins": ["bases.Account"],
			"fields": [
				["PlayTime", "number", "플레이 시간 (초)", true]
			]
		},

    // 생략
}
```

`doc` 명령으로 보면 아래와 같다:

```
# 생략

Event : Logout
Description : 계정 로그인
+----------+----------+------------------+------------+
| Field    | Type     | Description      | Optional   |
|----------+----------+------------------+------------|
| DateTime | datetime | 이벤트 일시      |            |
| ServerNo | integer  | 서버 번호        |            |
| AcntId   | integer  | 계정 ID          |            |
| PlayTime | number   | 플레이 시간 (초) | true       |
+----------+----------+------------------+------------+

# 생략
```

지금까지 없던 `Optional` 컬럼이 보이고 `PlayTime` 필드만이 `true`로 표시된다.

### 몬스터와 아이템

좀 더 실제 게임과 가깝게 하기 위해 몬스터와 아이템 관련 이벤트도 추가하겠다. 먼저, 다음과 같은 베이스를 추가한다.

```js
{
    // 생략
		"Position": {
			"desc": "맵상의 위치 요소",
			"fields": [
				["MapNo", "integer", "맵 번호"],
				["PosX", "number", "맵상 X 위치"],
				["PosY", "number", "맵상 Y 위치"],
				["PosZ", "number", "맵상 Z 위치"]
			]
		},
		"Monster": {
			"desc": "몬스터 요소",
			"fields": [
				["MonTypeId", "integer", "몬스터 타입 ID"],
				["MonInstId", "integer", "몬스터 인스턴스 ID"]
			]
		}
    // 생략
}
```

`Position` 베이스는 이벤트가 맵상 특정 위치에서 발생한 경우를 위한 것이다. 몬스터를 잡거나, 아이템을 습득하는 것은 모두 맵상의 위치에서 일어나기에 필요하다. `Monster` 베이스는 특정 몬스터 개체에 관한 것이다.

아래는 몬스터를 잡은 경우 이벤트이다:

```js
{
    // 생략
        "KillMonster": {
			"desc": "몬스터를 잡음",
			"mixins": ["bases.Character", "bases.Position", "bases.Monster"],
		}
}
```

아래는 `doc` 의 결과이다:
```
Event : KillMonster
Description : 몬스터를 잡음
+-----------+----------+--------------------+
| Field     | Type     | Description        |
|-----------+----------+--------------------|
| DateTime  | datetime | 이벤트 일시        |
| ServerNo  | integer  | 서버 번호          |
| AcntId    | integer  | 계정 ID            |
| CharId    | integer  | 캐릭터 ID          |
| MapNo     | integer  | 맵 번호            |
| PosX      | number   | 맵상 X 위치        |
| PosY      | number   | 맵상 Y 위치        |
| PosZ      | number   | 맵상 Z 위치        |
| MonTypeId | integer  | 몬스터 타입 ID     |
| MonInstId | integer  | 몬스터 인스턴스 ID |
+-----------+----------+--------------------+
```


이런 식으로 베이스를 잘 설계하고, 그것을 믹스인하는 것 만으로도 복잡한 이벤트를 간단히 만들 수 있다.

이제 아이템 관련 베이스를 추가해보자:

```js
{
    // 생략
        "Item": {
			"desc": "아이템 요소",
			"fields": [
				["ItemTypeId", "integer", "아이템 타입 ID"],
				["ItemInstId", "integer", "아이템 인스턴스 ID"]
			]
		}
    // 생략
}
```

`Item` 은 특정 아이템 개체를 위한 베이스이다.

이것을 이용해 몬스터가 아이템을 떨어뜨리는 이벤트를 추가한다:

```js
{
    // 생략
        "MonsterDropItem": {
			"desc": "몬스터가 아이템을 떨어뜨림",
			"mixins": ["bases.Monster", "bases.Position", "bases.Item"]
		}
}
```

몬스터가 주체이기에 지금까지와는 달리 계정이나 캐릭터 베이스가 없다. 대신 몬스터 개체의 정보가 먼저 나오도록 믹스인 순서를 조정하였다.  `doc` 의 결과는 다음과 같다:

```
Event : MonsterDropItem
Description : 몬스터가 아이템을 떨어뜨림
+------------+----------+--------------------+
| Field      | Type     | Description        |
|------------+----------+--------------------|
| DateTime   | datetime | 이벤트 일시        |
| MonTypeId  | integer  | 몬스터 타입 ID     |
| MonInstId  | integer  | 몬스터 인스턴스 ID |
| MapNo      | integer  | 맵 번호            |
| PosX       | number   | 맵상 X 위치        |
| PosY       | number   | 맵상 Y 위치        |
| PosZ       | number   | 맵상 Z 위치        |
| ItemTypeId | integer  | 아이템 타입 ID     |
| ItemInstId | integer  | 아이템 인스턴스 ID |
+------------+----------+--------------------+
```

캐릭터의 아이템 습득도 간단히 만들 수 있다.
```js
{
    // 생략
        "GetItem": {
			"desc": "캐릭터의 아이템 습득",
			"mixins": ["bases.Character", "bases.Position", "bases.Item"]
		}
}
```

`doc` 의 결과는 아래와 같다:

```
Event : GetItem
Description : 캐릭터의 아이템 습득
+------------+----------+--------------------+
| Field      | Type     | Description        |
|------------+----------+--------------------|
| DateTime   | datetime | 이벤트 일시        |
| ServerNo   | integer  | 서버 번호          |
| AcntId     | integer  | 계정 ID            |
| CharId     | integer  | 캐릭터 ID          |
| MapNo      | integer  | 맵 번호            |
| PosX       | number   | 맵상 X 위치        |
| PosY       | number   | 맵상 Y 위치        |
| PosZ       | number   | 맵상 Z 위치        |
| ItemTypeId | integer  | 아이템 타입 ID     |
| ItemInstId | integer  | 아이템 인스턴스 ID |
+------------+----------+--------------------+
```

## 필드값의 제약


지금까지 필드를 만들 때 이용했던 타입 정보로는 충분히 실제 로그의 특성을 반영하지 못할 수 있다. 예를 들어 `ServerNo` 필드의 경우 단순히 정수가 아닌 0 이상의 정수가 와야할 것이다. 이렇게 필드에 대한 좀 더 세분화된 정보를 더하는 것을 **필드값을 제약(restrict)** 한다고 표현한다.

> 필드값의 제약은 뒤에 나올 로그 검증 및 더미 로그 생성에 요긴하게 사용된다.

필드값을 제약하기 위해서는 `fields` 항목에서 지금까지 사용하던 리스트 요소 방식은 사용할 수 없고, 아래와 같은 오브젝트 방식으로 기술해야 한다.

```js
```

[TODO]

## 더미 로그의 생성

실제 로그가 어떻게 생겼는지 마리 살펴볼 수 있다면, 로그를 생성하거나 처리하는 쪽 모두 참고가 될 것이다. `loglab` 에서는 이를 위해 `dummy` 명령을 지원한다.

[TODO]

### 플로우 만들기

[TODO]
