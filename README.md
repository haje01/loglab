# LogLab

LogLab(로그랩) 은 다양한 서비스를 위한 로그를 설계하고 활용하기 위한 툴이다. 다음과 같은 기능을 가지고 있다.

- 로그를 객체지향적이며 재활용 가능한 형태로 설계
- 설계된 로그에 관한 문서 생성
- 설계된 로그에 준하는 더미(가짜) 로그 생성
- 실제 출력된 로그가 설계에 맞게 작성되었는지 검증

로그랩은 윈도우, Linux, MacOS 에서 사용할 수 있다.

- [LogLab](#loglab)
  - [설치](#설치)
  - [최초 랩파일 만들기](#최초-랩파일-만들기)
    - [랩파일의 선택](#랩파일의-선택)
    - [스키마와 도메인 정보 지정하기](#스키마와-도메인-정보-지정하기)
  - [필드의 추가](#필드의-추가)
  - [새로운 이벤트의 추가](#새로운-이벤트의-추가)
  - [믹스인을 활용한 리팩토링](#믹스인을-활용한-리팩토링)
  - [게임관련 이벤트와 필드의 추가](#게임관련-이벤트와-필드의-추가)
    - [서버 번호 필드](#서버-번호-필드)
    - [믹스인의 처리 순서](#믹스인의-처리-순서)
    - [베이스간 믹스인](#베이스간-믹스인)
    - [캐릭터 관련 이벤트](#캐릭터-관련-이벤트)
    - [옵션 필드](#옵션-필드)
    - [몬스터와 아이템](#몬스터와-아이템)
  - [필드값의 제약](#필드값의-제약)
    - [서버 번호 필드에 제약 걸기](#서버-번호-필드에-제약-걸기)
    - [디바이스 플랫폼 필드 추가하기](#디바이스-플랫폼-필드-추가하기)
  - [로그 파일 검증](#로그-파일-검증)
  - [더미 로그의 생성](#더미-로그의-생성)
    - [플로우 만들기](#플로우-만들기)

## 설치

LogLab의 설치를 위해서는 최소 Python 3.6 이상이 필요하다. 설치되어 있지 않다면 [이곳](https://www.python.org/) 에서 최신 버전의 파이썬을 설치하도록 하자.

LogLab 의 홈페이지는 https://github.com/haje01/loglab 이다. 다음과 같이 설치하자.

```
$ git checkout https://github.com/haje01/loglab
$ pip install -e .
```

설치가 잘 되었다면 로그랩의 커맨드라인 툴인 `loglab` 을 이용할 수 있다. 다음과 같이 입력해보자.

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


위에서 볼 수 있듯 `loglab` 에는 몇 가지 명령어가 있는데, 예제를 통해 하나씩 살펴보도록 하겠다. 먼저 간단히 버전을 확인해보자.

```
$ loglab version
0.0.1
```

지금부터는 가상의 게임 서비스를 위한 로그를 설계하는 예제를 통해 로그랩의 활용법을 빠르게 살펴보자.

## 최초 랩파일 만들기

로그랩은 **랩(lab)파일** 로 불리는 JSON 파일에 로그 명세를 기술하는 것으로 로그를 설계한다. 랩파일은 로그랩에서 제공하는 JSON 스키마 형식에 맞추어 작성하며, 확장자는 `.lab.json` 을 사용한다. [VS Code](https://code.visualstudio.com/) 등 JSON 스키마를 지원하는 에디터를 이용하면 인텔리센스(IntelliSense) 기능이 지원되어 편집에 용이할 것이다.

먼저 빈 작업 디렉토리를 하나를 만들고, 에디터를 사용해 아래와 같은 내용으로 `foo.lab.json` 파일을 만들자.

```js
{
  "events": {
    "Login": {
      "desc": "계정 로그인"
    }
  }
}
```

로그랩에서는 로깅의 대상이 되는 각 사건을 **이벤트(event)** 라고 한다. 각 이벤트에는 관련된 하나 이상의 **필드(field)** 를 기술할 수 있는데, 위 예에서는 아직 필드 정보는 없다.

랩파일의 `events` 항목 아래에 다양한 이벤트 요소를 기술할 수 있다. 예제는 계정 로그인 이벤트를 위한 `Login` 요소를 만들었다. 그 아래의 `desc` 요소는 이벤트에 대한 설명을 위한 것이다.


이제 작업 디텍토리에서 `loglab` 의 `doc` 명령을 사용해보자.

> 필자는 /home/ubuntu/loglab_test 디렉토리를 이용하였다.

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

우선 출력의 `[사용할 랩파일: ... ]` 부분에서 `loglab` 이 어떤 랩파일을 이용하는지 확인할 수 있다.

`doc` 명령은 랩파일의 내용을 참고해 로그 이벤트에 대한 문서를 텍스트 형식으로 출력한다. 출력에서 랩파일에 기술된 이벤트 이름, 설명 그리고 필드 정보가 출력되는 것을 확인할 수 있다.

그런데, 아직 `Login` 이벤트에는 아무런 필드를 명시하지 않았음에도 `DateTime` 이라는 필드가 보인다. 이것은 *모든 로그에 이벤트 발생 일시는 꼭 필요하기에 로그랩에서 자동으로 생성* 해준 것이다.

> 앞의 `Login` 과 `DateTime` 에서 알 수 있듯, 로그랩의 이벤트 및 필드 이름은 단어의 시작을 대문자로 (Pascal Case) 한다.

### 랩파일의 선택

`loglab` 은 실행시 현재 디렉토리에서 확장자가 `.lab.json` 인 파일을 찾아보고, 만약 하나의 랩파일만 발견된다면 그것을 이용한다. 먄약 랩파일이 없거나, 하나 이상의 랩파일이 존재한다면 다음과 같이 사용할 랩파일을 구체적으로 명시할 것을 요구한다.

랩파일이 없는 경우
```
Error: 현재 디렉토리에 랩파일이 없습니다. 새 랩파일을 만들거나, 사용할 랩파일을 명시적으로 지정해 주세요.
```
랩파일이 여럿 있는 경우
```
Error: 현재 디렉토리에 랩파일이 하나 이상 있습니다. 사용할 랩파일을 명시적으로 지정해 주세요.
```

이런 경우 사용할 랩파일의 경로 지정이 필요한데, 우선 다음처럼 `doc` 명령의 도움말을 출력해보자.

```
$ loglab doc --help
Usage: loglab doc [OPTIONS]

  로그 문서 표시.

Options:
  -l, --labfile TEXT  사용할 랩파일의 위치를 명시적으로 지정
  --help              Show this message and exit.
```

`loglab` 의 **모든 명령**에는 위와 같이 `-l` 또는 `--labfile` 옵션이 있는데, 이것을 이용해 사용할 랩파일의 경로를 명시적으로 지정할 수 있다.

### 스키마와 도메인 정보 지정하기

복잡한 구조의 JSON 파일을 편집하다보면 어떤 내용이 기술될 수 있는지 기억하기 어렵고 틀리기 쉽다. 이런 경우 해당 형식의 JSON 스키마가 있다면 편리하다. 로그랩에서는 랩파일을 위한 스키마를 제공한다. `foo.lab.json` 파일에 다음처럼 `$schema` 요소를 추가해 보자.

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

사용하는 에디터가 VS Code 처럼 JSON 스키마를 지원한다면, 인텔리센스 기능의 가이드를 받을 수 있다.

추가적으로, 랩파일의 **도메인(Domain) 정보**를 추가하면 도움이 된다. 도메인은 랩파일이 어떤 서비스를 위한 것인가에 대한 정보를 담는다. 다음처럼 `domain` 항목 아래 도메인 이름 및 설명을 입력한다.

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

> 입력 과정에서 스키마가 잘 동작한다면 아래와 같은 가이드를 볼 수 있을 것이다.
> ![스키마 가이드](image/guide.png)

도메인 정보 추가 후 다시 `doc` 명령을 실행하면 아래와 같이 도메인 정보도 출력된다.

```
$ loglab doc
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

> 지금부터는 공간을 아끼기 위해 표준 출력 및 JSON 파일의 맥락상 동일한 부분은 `...` 표시 후 생략하도록 하겠다.

필드는 이벤트에 관한 상세 정보를 표현한다. 기본으로 생성된 `DateTime` 외 필드를 추가해보자.

필드는 이벤트 요소 아래 리스트 타입인 `fields` 항목에 기술하는데, 그것의 항목 타입도 3 개 항목을 가지는 리스트이다. 각각은 아래와 같은 형식이다.

```js
{
  // ...

    "fields": [
      ['필드 이름', '필드 타입', '필드 설명']
    ]

  // ...
}
```

로그랩에서 사용할 수 있는 필드의 타입은 다음과 같다.

- `datetime` : 날짜+시간. [RFC3339](https://json-schema.org/latest/json-schema-validation.html#RFC3339)를 따른다.
- `string` : 문자열
- `integer`: 정수
- `number` : 실수 (`float` 과 일치)
- `boolean` : 불린 (`true` 또는 `false`)

예를 들어, `Login` 이벤트의 경우 로그인한 계정 ID 필드가 필요할 것이다. 아래와 같이 추가한다.

```js
{
  // ...

  "events": {
    "Login": {
      "desc": "계정 로그인",
      "fields": [
          ["AcntId", "integer", "계정 ID"]
      ]
    }
}
```

이제 `doc` 명령을 내려보면,

```
$ loglab doc
# ...

Event : Login
Description : 계정 로그인
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
| AcntId   | integer  | 계정 ID       |
+----------+----------+---------------+
```

계정 정보 `AcntId` 필드가 추가된 것을 확인할 수 있다.

## 새로운 이벤트의 추가

계정의 로그인 이벤트가 있다면, 로그아웃도 있어야 하지 않을까? 다음과 같이 추가해보자.

```js
{
  // ...

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

`doc` 명령을 내려보면,

```
$ loglab doc
# ...

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

그런데 로그인, 로그아웃 이벤트 모두 `AcntId` 필드을 가지고 있는 것이 보인다. 앞으로 계정에 관한 다른 이벤트를 만든다면 거기에도 모두 이 필드를 만들어 주어야 할 것이다. 이런 중복을 방지할 수 없을까?

## 믹스인을 활용한 리팩토링

**믹스인(mixin)** 은 다른 요소에서 선언한 필드를 가져와서 쓰는 방법이다. 믹스인을 활용하면 다양한 이벤트에서 공통적으로 필요한 필드를 중복 기술없이 재활용할 수 있다.

믹스인을 하기 위해서는 **베이스(base)** 요소가 필요하다. 베이스는 이벤트와 비슷하나, 그 자체로 직접 사용되지는 않고, 이벤트 요소나 다른 베이스에서 참조되기 위한 용도이다. 베이스는 랩파일의 `bases` 항목 아래 다음과 같은 형식으로 정의한다.

```js
{
  // ...

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

위 예에서 `bases` 항목 아래 `Account` 라는 베이스를 만들었다. 여기에 계정 관련 이벤트를 위한 공용 필드를 기술하도록 한다. 일단은 `AcntId` 만 있다.

이제 기존 `Login`, `Logout` 이벤트의 필드 요소는 제거하고, `Account` 베이스를 믹스인하도록 하자. 믹스인할 베이스 요소는 `bases.베이스_이름` 형식으로 지정한다. 각 이벤트에 `mixin` 항목을 만들고 `bases.Account` 를 항목으로 가지는 리스트를 만든다.

> 이벤트는 베이스 뿐만 아니라 다른 이벤트도 믹스인할 수 있다. 이 경우 `events.이벤트_이름` 형식으로 지정하면 된다. 베이스는 이벤트를 믹스인할 수 없다.

이렇게 하면 각 이벤트는 `Account` 베이스에 등록된 필드를 모두 가져다 쓰게 된다. `doc` 명령으로 확인하면,

```
$ loglab doc
# ...

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

두 이벤트에 `fields` 항목이 없지만 `Account` 베이스의 필드를 가져와 원래 결과와 같은 것을 알 수 있다.

> `doc` 명령으로 출력되는 문서에 베이스는 출력되지 않는다. 베이스는 참조되어 사용되어질 뿐, 그 자체로 이벤트는 아니기 때문이다.


## 게임관련 이벤트와 필드의 추가

이제 기본적인 랩파일 작성 방법을 알게 되었다. 지금까지 배운 것을 활용하여 실제 게임에서 발생할 수 있는 다양한 이벤트를 추가해보겠다.

### 서버 번호 필드

게임 서비스내 대부분 이벤트는 특정 서버에서 발생하기 마련이다. 몇 번 서버의 이벤트인지 표시하기 위해 다음과 같이 `Server` 베이스를 추가한다.

```js
{
  // ...

  "bases": {

    // ...

    "Server": {
      "desc": "서버 이벤트",
      "fields": [
        ["ServerNo", "integer", "서버 번호"]
      ]
    }
  },

  // ...
}
```

`Login`, `Logout` 이벤트도 당연히 특정 서버에 관한 것이기에, 다음과 같이 믹스인에 추가한다.

```js
{
  // ...

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

`doc` 명령으로 두 이벤트에 `ServerNo` 필드가 추가된 것을 확인할 수 있다.

```
$ loglab doc
# ...

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

### 믹스인의 처리 순서

 믹스인은 `mixin` 리스트에 등장하는 순서대로 수행되며, 앞 항목과 뒤 항목에 일치하는 필드가 있다면 뒤의 것으로 덮어쓰게 된다. 이것을 이용하면 특정 필드의 순서를 조정하거나 재정의 할 수 있다. 예를 들어 위 예에서 `ServerNo` 필드가 `AcntId` 보다 먼저 나오게 하고 싶다면 `mixin` 리스트에 다음과 같이 바꿔주면 된다.

 ```js
 {
    // ...

    "Login": {
      "desc": "계정 로그인",
      "mixins": ["bases.Server", "bases.Account"]
    },

    // ...
 ```

 `doc` 결과는 다음과 같다.

```
$ loglab doc
# ...

Event : Login
Description : 계정 로그인
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
| ServerNo | integer  | 서버 번호     |
| AcntId   | integer  | 계정 ID       |
+----------+----------+---------------+

# ...
```

### 베이스간 믹스인

베이스는 다른 베이스를 믹스인 할 수 있다. 예제의 서비스에서 계정에 관한 이벤트가 항상 서버 단위로 일어난다면, `Account` 베이스에 `Server` 베이스를 포함해 더 간단히 만들 수 있다.

```js
{
  // ...

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

이제 `Account` 베이스 자체가 `Server` 를 믹스인하기에, 계정 로그인/로그아웃 이벤트는 `Account` 만 믹스인하면 된다.

> 믹스인을 할 요소의 `bases` 항목 내 등장 순서는 중요하지 않다. 위의 경우 `Account` 가 `Server` 앞에 오더라도 문제가 없다.


### 캐릭터 관련 이벤트

게임에서 실제 플레이를 하는 것은 게임이 속한 캐릭터이다. 이에 캐릭터 관련 이벤트를 추가해보겠다.

한 계정은 하나 이상의 캐릭터를 소유하고 선택하여 플레이할 수 있기에, 먼저 다음과 같은 `Character` 베이스를 추가한다.

```js
{
  // ...

  "bases": {

    // ...

    "Character": {
      "desc": "캐릭터 정보",
      "mixins": ["bases.Account"],
      "fields": [
        ["CharId", "integer", "캐릭터 ID"]
      ]
    }
  },

  // ...
}
```

다음은 `Character` 베이스를 이용해, 캐릭터의 로그인/아웃 이벤트를 추가한다.

```js
{
  // ...

  "events": {

    // ...

    "CharLogin": {
      "desc": "캐릭터 로그인",
      "mixins": ["bases.Character"]
    },
    "CharLogout": {
      "desc": "캐릭터 로그아웃",
      "mixins": ["bases.Character"]
    }
  }
}
```

`doc` 명령으로 확인하면,

```
$ loglab doc
# ...

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
Description : 캐릭터 로그아웃
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
| ServerNo | integer  | 서버 번호     |
| AcntId   | integer  | 계정 ID       |
| CharId   | integer  | 캐릭터 ID     |
+----------+----------+---------------+
```

`CharLogin`, `CharLogout` 이벤트를 확인할 수 있다.


### 옵션 필드

지금까지 등장한 모든 필드들은 기본적으로 로그 이벤트에 반드시 나와야 하는(required) 필드들이었다. 만약 나올 수도 있고 안 나와도 괜찮은 필드가 있다면, **옵션(option)** 필드로 만들 수 있다. 그것은 `fields` 리스트의 각 항목별 4번째 항목에 `true` 또는 `false` 를 지정하여 만들 수 있다 (`false` 는 기본값이기에 굳이 기술할 필요가 없겠다).

예를 들어 `AcntLogout` 이벤트에서, 로그인 이후 플레이한 시간을 선택적으로 포함하게 하려면 다음과 같이 추가할 수 있다.

```js
{
    // ...

  "events": {

    // ...

    "Logout": {
      "desc": "계정 로그인",
      "mixins": ["bases.Account"],
      "fields": [
        ["PlayTime", "number", "플레이 시간 (초)", true]
      ]
    },

    // ...
}
```

`doc` 명령으로 보면 아래와 같다.

```
$ loglab doc
# ...

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

# ...
```

지금까지 없던 `Optional` 컬럼이 보이고 `PlayTime` 필드만이 `true`로 표시된다.

### 몬스터와 아이템

좀 더 실제 게임과 가깝게 하기 위해 몬스터와 아이템 관련 이벤트도 만들겠다. 먼저, 다음과 같은 베이스를 추가한다.

```js
{
  // ...

  "bases": {

    // ...

    "Position": {
      "desc": "맵상의 위치 정보",
      "fields": [
        ["MapNo", "integer", "맵 번호"],
        ["PosX", "number", "맵상 X 위치"],
        ["PosY", "number", "맵상 Y 위치"],
        ["PosZ", "number", "맵상 Z 위치"]
      ]
    },
    "Monster": {
      "desc": "몬스터 정보",
      "fields": [
        ["MonTypeId", "integer", "몬스터 타입 ID"],
        ["MonInstId", "integer", "몬스터 인스턴스 ID"]
      ]
    }

    // ...
}
```

`Position` 베이스는 이벤트가 맵상의 특정 위치에서 발생한 경우를 위한 것이다. 몬스터를 잡거나, 아이템을 습득하는 것은 모두 맵상의 위치에서 일어나기에 필요하다. `Monster` 베이스는 특정 몬스터 개체에 관한 것이다.

이제 캐릭터가 몬스터를 잡은 경우의 이벤트 `KillMonster` 를 추가한다.

```js
{

  // ...

  "events": {

    // ...

    "KillMonster": {
      "desc": "몬스터를 잡음",
      "mixins": ["bases.Character", "bases.Position", "bases.Monster"],
    }
}
```

아래는 `doc` 의 결과이다.
```
$ loglab doc
# ...

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

# ...
```

믹스인한 베이스의 정보, 즉 계정 및 캐릭터, 지도상의 위치, 몬스터 개체에 관한 정보들이 잘 구성된 것을 확인할 수 있다. 이런 식으로 베이스를 잘 설계하고, 그것을 믹스인하는 것 만으로도 복잡한 로그 이벤트를 간단히 만들 수 있다.

이제 아이템 관련 베이스를 추가해보자.

```js
{
  // ...

  "bases": {

    // ...

    "Item": {
      "desc": "아이템 정보",
      "fields": [
        ["ItemTypeId", "integer", "아이템 타입 ID"],
        ["ItemInstId", "integer", "아이템 인스턴스 ID"]
      ]
    }

    // ...
}
```

`Item` 은 특정 아이템 개체를 위한 베이스이다. 이것을 이용해 몬스터가 아이템을 떨어뜨리는 이벤트를 추가한다.

```js
{
  // ...

  "events": {

    // ...

    "MonsterDropItem": {
      "desc": "몬스터가 아이템을 떨어뜨림",
      "mixins": ["bases.Monster", "bases.Position", "bases.Item"]
    }
}
```

몬스터가 주체이기에 지금까지와는 달리 계정이나 캐릭터 베이스가 믹스인되지 않았다. 또 몬스터 개체의 정보가 먼저 나오도록 믹스인 순서를 조정하였다.  `doc` 의 결과는 다음과 같다.

```
$ loglab doc
# ...

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

# ...
```

비슷하게 캐릭터의 아이템 습득 이벤트도 간단히 만들 수 있다.

```js
{
  // ...

  "events": {

    // ...

    "GetItem": {
      "desc": "캐릭터의 아이템 습득",
      "mixins": ["bases.Character", "bases.Position", "bases.Item"]
    }
}
```

`doc` 의 결과는 아래와 같다.

```
$ loglab doc
# ...

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

# ...
```

## 필드값의 제약

지금까지 필드를 만들 때 사용했던 타입 정보만으로는 실제 로그의 특성을 충분히 반영하지 못할 수 있다. 예를 들어 `Server` 베이스의 `ServerNo` 필드의 경우, 단순히 정수가 아닌 1 이상의 정수가 와야 할 것이다. 이렇게 필드의 값에 관해 더 세분화된 정보를 지정하는 것을 **필드값을 제약(restrict)** 한다고 하겠다.

> 필드값의 제약은 로그 설계 측면에서 꼭 필요한 것은 아니지만, 뒤에 나올 로그 검증 및 더미 로그 생성 기능을 이용하려면 필요하다.

### 서버 번호 필드에 제약 걸기

필드값을 제약하기 위해서는 `fields` 항목에서 지금까지 사용하던 리스트 요소 대신 오브젝트 방식으로 기술해야 한다. 예로 `ServerNo` 필드를 제약해보자.

```js
{
//...
  "bases": {
    "Server": {
      "desc": "서버 정보",
      "fields": [
        {
          "name": "ServerNo",
          "desc": "서버 번호",
          "type": "integer",
          "minimum": 1
        }
      ]
    },
//...
}
```

기존 리스트 `["ServerNo", "integer", "서버 번호"]` 형식에서 오브젝트 형식으로 바뀌었다. 끝에 추가된 `minimum` 은 **제약문** 으로 `ServerNo`의 값을 1 으로 제약한다.

`doc` 을 실행해보자.

```
$ loglab doc
# ...

Event : Login
Description : 계정 로그인
+----------+----------+---------------+------------+
| Field    | Type     | Description   | Restrict   |
|----------+----------+---------------+------------|
| DateTime | datetime | 이벤트 일시   |            |
| ServerNo | integer  | 서버 번호     | 1 이상     |
| AcntId   | integer  | 계정 ID       |            |
+----------+----------+---------------+------------+

Event : Logout
Description : 계정 로그인
+----------+----------+------------------+------------+------------+
| Field    | Type     | Description      | Optional   | Restrict   |
|----------+----------+------------------+------------+------------|
| DateTime | datetime | 이벤트 일시      |            |            |
| ServerNo | integer  | 서버 번호        |            | 1 이상     |
| AcntId   | integer  | 계정 ID          |            |            |
| PlayTime | number   | 플레이 시간 (초) | true       |            |
+----------+----------+------------------+------------+------------+

# ...
```

모든 이벤트의 `ServerNo` 필드에 `1 이상` 이라는 제약이 걸려있는 것을 알 수 있다.

참고로, 제약문은 필드의 타입별로 아래와 같은 것들이 있다.

- `integer`
  - `minimum` : 정수의 포함하는 최소값
  - `maximum` : 정수의 포함하는 최대값
- `number`
  - `minimum` : 실수의 포함하는 최소값
  - `maximum` : 실수의 포함하는 최대값
- `string`
  - `enum` : 허용하는 문자열의 나열값
  - `minLength` : 문자열의 최소 길이
  - `maxLength` : 문자열의 최대 길이
  - `pattern` : 허용하는 문자열의 정규식 패턴
  - `format` : 문자열의 기정의된 포맷
    - `date-time`, `date`, `email`, `hostname`, `ipv4`, `ipv6`, `uri` 중 하나

만약 `ServerNo` 를 100 미만으로 제약하고 싶다면 `maximum` 을 이용한다.

```js
//...
  "bases": {
    "Server": {
      "desc": "서버 정보",
      "fields": [
        {
                    "name": "ServerNo",
                    "desc": "서버 번호",
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 99
                }
      ]
    },
//...
```

`doc` 결과는 아래와 같다.

```
$ loglab doc
# ...

Event : Login
Description : 계정 로그인
+----------+----------+---------------+----------------+
| Field    | Type     | Description   | Restrict       |
|----------+----------+---------------+----------------|
| DateTime | datetime | 이벤트 일시   |                |
| ServerNo | integer  | 서버 번호     | 1 에서 99 까지 |
| AcntId   | integer  | 계정 ID       |                |
+----------+----------+---------------+----------------+

Event : Logout
Description : 계정 로그인
+----------+----------+------------------+------------+----------------+
| Field    | Type     | Description      | Optional   | Restrict       |
|----------+----------+------------------+------------+----------------|
| DateTime | datetime | 이벤트 일시      |            |                |
| ServerNo | integer  | 서버 번호        |            | 1 에서 99 까지 |
| AcntId   | integer  | 계정 ID          |            |                |
| PlayTime | number   | 플레이 시간 (초) | true       |                |
+----------+----------+------------------+------------+----------------+

# ...
```
`1 에서 99 까지` 로 제약이 표시된다.

ID 계열 필드들, 즉 `AcntId`, `CharId`, `MonTypeId`, `MonInstId`, `ItemTypeId`, `ItemInstId` 과 `MapNo` 에도 모두 1 이상이 되도록 제약을 걸어주자 (리스트 형식으로 필드를 기술할 때 보다 꽤 번거롭다).

### 디바이스 플랫폼 필드 추가하기

이번에는 문자열 필드 제약의 예를 위해, 로그인시 게임을 하는 유저 디바이스의 플랫폼(OS) 필드를 추가하겠다.

다음처럼 `Login` 이벤트에 `Platform` 필드를 추가한다.

```js
{
  // ...

  "events": {
    "Login": {
      "desc": "계정 로그인",
      "mixins": ["bases.Account"],
      "fields": [
          {
              "name": "Platform",
              "desc": "디바이스의 플랫폼",
              "type": "string",
              "enum": [
                  "ios", "aos"
              ]
          }
      ]
    },

  // ...
}
```

`doc` 의 결과는 아래와 같다.

```
$ loglab doc
# ...

Event : Login
Description : 계정 로그인
+----------+----------+-------------------+------------------------+
| Field    | Type     | Description       | Restrict               |
|----------+----------+-------------------+------------------------|
| DateTime | datetime | 이벤트 일시       |                        |
| ServerNo | integer  | 서버 번호         | 1 에서 99 까지         |
| AcntId   | integer  | 계정 ID           | 1 이상                 |
| Platform | string   | 디바이스의 플랫폼 | ['ios', 'aos'] 중 하나 |
+----------+----------+-------------------+------------------------+

# ...
```

## 로그 파일 검증

[TODO]

## 더미 로그의 생성

실제 로그가 어떻게 생겼는지 마리 살펴볼 수 있다면, 로그를 생성하거나 처리하는 쪽 모두 참고가 될 것이다. `loglab` 에서는 이를 위해 `dummy` 명령을 지원한다.

[TODO]

### 플로우 만들기

[TODO]
