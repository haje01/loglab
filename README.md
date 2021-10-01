# LogLab

<img src="image/loglab.png" width="128" height="128" />

LogLab(로그랩) 은 다양한 서비스를 위한 로그를 설계하고 활용하기 위한 툴이다. 다음과 같은 기능을 가지고 있다.

- 로그를 객체지향적이며 재활용 가능한 형태로 설계
- 설계된 로그에 관한 문서 생성
- 설계된 로그에 준하는 더미(가짜) 로그 생성
- 실제 출력된 로그가 설계에 맞게 작성되었는지 검증

로그랩은 다음과 같은 다양한 입장에서 도움이 될 수 있다.

- 새로운 서비스를 개발하려는 개발자
- 로그를 처리하고 분석하는 데이터 엔지니어/분석가
- 조직에서 생성되는 로그의 형식을 일관되게 유지/공유 하고 싶은 관리자

로그랩은 윈도우, Linux, MacOS 에서 사용할 수 있다.

---

- [LogLab](#loglab)
  - [설치](#설치)
  - [최초 랩 파일 만들기](#최초-랩-파일-만들기)
    - [랩 파일의 선택](#랩-파일의-선택)
    - [스키마와 도메인 정보 지정하기](#스키마와-도메인-정보-지정하기)
  - [필드의 추가](#필드의-추가)
  - [새로운 이벤트의 추가](#새로운-이벤트의-추가)
  - [믹스인을 활용한 리팩토링](#믹스인을-활용한-리팩토링)
  - [게임관련 이벤트와 필드의 추가](#게임관련-이벤트와-필드의-추가)
    - [서버 번호 필드](#서버-번호-필드)
    - [믹스인의 처리 순서](#믹스인의-처리-순서)
    - [베이스간 믹스인](#베이스간-믹스인)
    - [옵션 필드](#옵션-필드)
    - [캐릭터 관련 이벤트](#캐릭터-관련-이벤트)
    - [몬스터와 아이템](#몬스터와-아이템)
  - [필드값의 제약](#필드값의-제약)
    - [서버 번호에 제약 걸기](#서버-번호에-제약-걸기)
    - [커스텀 타입](#커스텀-타입)
    - [나열 이용하기](#나열-이용하기)
  - [로그 파일의 검증](#로그-파일의-검증)
  - [더미 로그의 생성](#더미-로그의-생성)
    - [플로우 파일 만들기](#플로우-파일-만들기)
  - [공용 랩 파일을 통한 로그 표준화](#공용-랩-파일을-통한-로그-표준화)
    - [외부 랩 파일 가져오기](#외부-랩-파일-가져오기)
    - [복잡한 랩 파일 필터링하기](#복잡한-랩-파일-필터링하기)
  - [기타 기능과 팁 소개](#기타-기능과-팁-소개)
    - [HTML 문서 출력](#html-문서-출력)
    - [실행 파일 이용과 빌드](#실행-파일-이용과-빌드)
  - [로그랩을 활용하는 다양한 방법](#로그랩을-활용하는-다양한-방법)
    - [레가시 로그 정리용](#레가시-로그-정리용)

## 설치

LogLab의 설치를 위해서는 최소 Python 3.6 이상이 필요하다. 설치되어 있지 않다면 [이곳](https://www.python.org/) 에서 최신 버전의 파이썬을 설치하도록 하자.

LogLab 의 홈페이지는 https://github.com/haje01/loglab 이다. 다음과 같이 설치하자.

```
$ git clone https://github.com/haje01/loglab
$ pip install -e .
```

설치가 잘 되었다면 로그랩의 커맨드라인 툴인 `loglab` 을 이용할 수 있다. 다음과 같이 입력해보자.

```
$ loglab
Usage: loglab [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  doc      로그 구성 요소 출력.
  dummy    가짜 로그 생성.
  schema   로그 및 플로우 파일용 스키마 생성.
  verify   생성된 로그 파일 검증.
  version  로그랩 버전 표시.
```

위에서 볼 수 있듯 `loglab` 에는 몇 가지 명령어가 있는데, 예제를 통해 하나씩 살펴보도록 하겠다. 먼저 간단히 버전을 확인해보자.

```
$ loglab version
0.1
```

지금부터는 가상의 모바일 게임 `foo` 를 위한 로그를 설계하는 예제를 통해 로그랩의 활용법을 하나씩 살펴보자.

## 최초 랩 파일 만들기

로그랩은 **랩(lab) 파일** 로 불리는 JSON 파일에 로그 명세를 기술하는 것으로 로그를 설계한다. 랩 파일은 로그랩에서 제공하는 JSON 스키마 형식에 맞추어 작성하며, 확장자는 `.lab.json` 을 사용한다. [VS Code](https://code.visualstudio.com/) 등 JSON 스키마를 지원하는 에디터를 이용하면 인텔리센스 (IntelliSense) 기능이 지원되어 편집에 용이할 것이다.

먼저 빈 작업 디렉토리를 하나를 만들고, 에디터를 사용해 아래와 같은 내용으로 `foo.lab.json` 파일을 만들자.

```js
{
  "domain": {
    "name": "foo",
    "desc": "최고의 모바일 게임"
  },
  "events": {
    "Login": {
      "desc": "계정 로그인"
    }
  }
}
```

랩 파일에 첫 번째로 나오는 `domain` 요소는 랩 파일의 **도메인(Domain) 정보**를 기술하는데 사용한다. 도메인 요소는 랩 파일이 어떤 서비스를 위한 것인가에 대한 정보를 담는다.

위 예처럼 `domain` 항목 아래 도메인 이름 및 설명을 입력하면 되는데, 도메인 이름은 나중에 해당 랩 파일을 식별하는 용도로 사용되기에, 알파벳 소문자와 숫자, 그리고 밑줄 문자 `_` 만을 사용해 **식별 가능한 범위에서 간략하게 기술**한다.

> 예제에서 처럼 랩 파일의 이름과 도메인 이름을 같게 하는 것을 추천한다.

로그랩에서는 로깅의 대상이 되는 각 사건을 **이벤트(event)** 라고 하는데, 위 랩  파일에서 두 번째로 나오는 `events` 요소에 하나 이상ㅇ의 이벤트 요소를 기술할 수 있다. 예에서 계정 로그인 이벤트를 위한 `Login` 요소를 만들었다. 그 아래의 `desc` 요소는 이벤트에 대한 설명을 위한 것이다.

각 이벤트에는 관련된 하나 이상의 **필드(field)** 를 기술할 수 있는데, 예에서는 아직 필드 정보는 없다.

이제 작업 디텍토리에서 `loglab` 의 `show` 명령을 사용해보자.

> 필자는 /home/ubuntu/loglab_test 디렉토리를 이용하였다.

```
$ loglab show
[랩 파일 : /home/ubuntu/loglab_test/foo.lab.json]

Domain : foo
Description : 최고의 모바일 게임

Event : Login
Description : 계정 로그인
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
+----------+----------+---------------+
```

`show` 명령은 랩 파일의 내용을 참고해 로그의 구성 요소들을 텍스트 형식으로 출력한다. 출력 첫 번째 줄의 `[랩 파일: ... ]` 부분에서 `loglab` 이 어떤 랩 파일을 이용하는지 확인할 수 있으며, 이어서 랩 파일에 기술된 도메인 정보, 이벤트 이름과 설명 그리고 필드 정보가 출력되는 것을 확인할 수 있다.

> 이렇게 랩 파일이 있는 디렉토리를 *로그랩 작업 디렉토리* 로 부르겠다. 여기에는 하나 이상의 랩 파일이 있을 수 있고, 나중에 설명할 명령을 통해 `.loglab` 디렉토리에 작업 결과가

그런데, 아직 `Login` 이벤트에는 아무런 필드를 명시하지 않았음에도 `DateTime` 이라는 필드가 보인다. 이것은 모든 로그에 이벤트 발생 일시는 꼭 필요하기에 *로그랩에서 자동으로 생성* 해준 것이다.

> 앞의 `Login` 과 `DateTime` 에서 알 수 있듯, 로그랩의 이벤트 및 필드 이름은 단어의 시작을 대문자로 (Pascal Case) 한다.

### 랩 파일의 선택

`loglab` 은 랩 파일이 필요한 명령을 수행할 때 현재 디렉토리에서 확장자가 `.lab.json` 인 파일을 찾아보고, 만약 하나의 랩 파일만 발견된다면 그것을 이용한다. 먄약 랩 파일이 없거나, 하나 이상의 랩 파일이 존재한다면 다음과 같이 사용할 랩 파일을 구체적으로 지정할 것을 요구한다.

랩 파일이 없는 경우
```
Error: 현재 디렉토리에 랩 파일이 없습니다. 새 랩 파일을 만들거나, 사용할 랩 파일을 명시적으로 지정해 주세요.
```
랩 파일이 여럿 있는 경우
```
Error: 현재 디렉토리에 랩 파일이 하나 이상 있습니다. 사용할 랩 파일을 명시적으로 지정해 주세요.
```

이런 경우 사용할 랩 파일의 경로 지정이 필요한데, 우선 다음처럼 `show` 명령의 도움말을 출력해보자.

```
$ loglab show --help
Usage: loglab show [OPTIONS]

  로그 구성 요소 출력.

Options:
  -l, --labfile TEXT  사용할 랩 파일의 위치를 명시적으로 지정
  --help              Show this message and exit.
```

`loglab` 의 **모든 명령**에는 위와 같이 `-l` 또는 `--labfile` 옵션이 있는데, 이것을 이용해 사용할 랩 파일의 경로를 명시적으로 지정할 수 있다.

### 스키마와 도메인 정보 지정하기

복잡한 구조의 JSON 파일을 편집하다보면 어떤 내용이 기술될 수 있는지 기억하기 어렵고 틀리기 쉽다. 이런 경우 해당 형식의 JSON 스키마가 있다면 편리하다. 로그랩에서는 랩 파일을 위한 스키마를 제공한다. `foo.lab.json` 파일에 다음처럼 `$schema` 요소를 추가해 보자.

```js
{
  "$schema": "https://raw.githubusercontent.com/haje01/loglab/master/schema/lab.schema.json",
  "domain": {
    "name": "foo",
    "desc": "최고의 모바일 게임"
  },
  "events": {
    "Login": {
      "desc": "계정 로그인"
    }
  }
}
```

사용하는 에디터가 VS Code 처럼 JSON 스키마를 지원한다면, 인텔리센스 기능의 가이드를 받을 수 있다.

> 입력 과정에서 스키마가 잘 동작한다면 아래와 같은 가이드를 볼 수 있을 것이다.
> ![스키마 가이드](image/guide.png)

## 필드의 추가

> 지금부터는 공간을 아끼기 위해 표준 출력 및 JSON 파일의 맥락상 동일한 부분은 `...` 표시 후 생략하도록 하겠다.

필드는 이벤트에 관한 상세 정보를 표현한다. 기본으로 생성된 `DateTime` 외 필드를 추가해보자.

필드는 이벤트 요소 아래 `fields` 리스트에 기술하는데, 각 필드는 3 개 항목을 가지는 리스트이다. 아래와 같은 형식이다.

```js
{
  // ...

    "fields": [
      [필드_이름, 필드_타입, 필드_설명]
    ]

  // ...
}
```

로그랩에서 사용할 수 있는 필드의 기본 타입은 다음과 같다.

- `string` : 문자열
- `integer`: 정수
- `number` : 실수 (`float` 과 일치)
- `boolean` : 불린 (`true` 또는 `false`)
- `datetime` : 일시(날짜+시간). [RFC3339](https://json-schema.org/latest/json-schema-validation.html#RFC3339) 를 따른다.

> RFC3399 일시의 예로 `2021-09-12T23:41:50.52Z` 은 UTC 기준 2021년 9월 12일 23시 41분 50.52 초이며 `2021-09-14T16:39:57+09:00` 은 한국 표준시 (KST) 로 2021년 9월 14일 16시 39분 57초 이다.

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

이제 `show` 명령을 내려보면,

```
$ loglab show
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

`show` 명령을 내려보면,

```
$ loglab show
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
Description : 계정 로그아웃
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

믹스인을 하기 위해서는 **베이스(base)** 요소가 필요하다. 베이스는 이벤트와 비슷하나, 그 자체로 직접 사용되지는 않고, 이벤트 요소나 다른 베이스에서 참조되기 위한 용도이다. 베이스는 랩 파일의 `bases` 항목 아래 다음과 같은 형식으로 정의한다.

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
      "desc": "계정 로그아웃",
      "mixins": ["bases.Account"]
    }
  }
}

```

위 예에서 `bases` 항목 아래 `Account` 라는 베이스를 만들었다. 여기에 계정 관련 이벤트를 위한 공용 필드를 기술하도록 한다. 일단은 `AcntId` 만 있다. 기존 `Login`, `Logout` 이벤트의 필드 요소는 제거하고, `Account` 베이스를 믹스인하도록 하자. 믹스인할 베이스 요소는 `bases.베이스_이름` 형식으로 지정한다. 각 이벤트에 `mixin` 항목을 만들고 `bases.Account` 를 항목으로 가지는 리스트를 만든다.

> 이벤트는 베이스 뿐만 아니라 다른 이벤트도 믹스인할 수 있다. 이 경우 `events.이벤트_이름` 형식으로 지정하면 된다. 베이스는 이벤트를 믹스인할 수 없다.

이렇게 하면 각 이벤트는 `Account` 베이스에 등록된 필드를 모두 가져다 쓰게 된다. `show` 명령으로 확인하면,

```
$ loglab show
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
Description : 계정 로그아웃
+----------+----------+---------------+
| Field    | Type     | Description   |
|----------+----------+---------------|
| DateTime | datetime | 이벤트 일시   |
| AcntId   | integer  | 계정 ID       |
+----------+----------+---------------+
```

두 이벤트에 `fields` 항목이 없지만 `Account` 베이스의 필드를 가져와 원래 결과와 같은 것을 알 수 있다.

이런 식으로 서로 다른 요소에서 공통 요소를 추출해 내는 것을 **리팩토링(refactoring)** 이라고 한다.

> 리팩토링은 왜 필요할까? 예를 들어 계정에 관한 필드를 가지는 로그 이벤트가 100 개 있다고 하자. 어느날 계정 정보에 필드 하나가 추가되어야 한다는 요청이 들어오면, 리팩토링이 되어 있지 않은 경우 100 개나 되는 이벤트를 모두 수정해야 할 것이다. 미리 계정 관련 베이스를 만들어 리팩토링 해두었다면, 단 한 번의 수정으로 100 개 이벤트 모두에 추가 필드를 적용할 수 있다.


> `show` 명령으로 출력되는 구조에 베이스는 출력되지 않는다. 베이스는 참조되어 사용되어질 뿐, 그 자체로 이벤트는 아니기 때문이다.


## 게임관련 이벤트와 필드의 추가

이제 기본적인 랩 파일 작성 방법을 알게 되었다. 지금까지 배운 것을 활용하여 실제 게임에서 발생할 수 있는 다양한 이벤트를 추가해보겠다.

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
      "desc": "계정 로그아웃",
      "mixins": ["bases.Account", "bases.Server"]
    }
  }
}
```

`show` 명령으로 두 이벤트에 `ServerNo` 필드가 추가된 것을 확인할 수 있다.

```
$ loglab show
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
Description : 계정 로그아웃
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

 `show` 결과는 다음과 같다.

```
$ loglab show
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
      "desc": "계정 로그아웃",
      "mixins": ["bases.Account"]
    }
  }
}
```

이제 `Account` 베이스 자체가 `Server` 를 믹스인하기에, 계정 로그인/로그아웃 이벤트는 `Account` 만 믹스인하면 된다.

> 믹스인을 할 요소의 `bases` 항목 내 등장 순서는 중요하지 않다. 위의 경우 `Account` 가 `Server` 앞에 오더라도 문제가 없다.

### 옵션 필드

지금까지 등장한 모든 필드들은 기본적으로 로그 이벤트에 반드시 나와야 하는(required) 필드들이었다. 만약 나올 수도 있고 안 나와도 괜찮은 필드가 있다면, **옵션(option)** 필드로 만들 수 있다. 그것은 `fields` 리스트의 각 항목별 4번째 항목에 `true` 또는 `false` 를 지정하여 만들 수 있다 (`false` 는 기본값이기에 굳이 기술할 필요가 없겠다).

예를 들어 `Logout` 이벤트에서, 로그인 이후 플레이한 시간을 선택적으로 포함하게 하려면 다음과 같이 추가할 수 있다.

```js
{
    // ...

  "events": {

    // ...

    "Logout": {
      "desc": "계정 로그아웃",
      "mixins": ["bases.Account"],
      "fields": [
        ["PlayTime", "number", "플레이 시간 (초)", true]
      ]
    },

    // ...
}
```

`show` 명령으로 보면 아래와 같다.

```
$ loglab show
# ...

Event : Logout
Description : 계정 로그아웃
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
      "mixins": ["bases.Character", "events.Logout"]
    }
  }
}
```

`CharLogin` 은 캐릭터 베이스만을 사용해서 구현하였으나, `CharLogout` 은 캐릭터 베이스에 더해 계정 로그아웃 이벤트인 `Logout` 을 믹스인 해보았다.

``show` 명령으로 확인하면 `CharLogin` 과 `CharLogout` 이벤트를 확인할 수 있다.

```
$ loglab show
# ...

Event : CharLogin
Description : 캐릭터 로그인
+----------+----------+---------------+-----------------+
| Field    | Type     | Description   | Restrict        |
|----------+----------+---------------+-----------------|
| DateTime | datetime | 이벤트 일시   |                 |
| ServerNo | integer  | 서버 번호     | 1 이상 100 미만 |
| AcntId   | types.Id | 계정 ID       |                 |
| CharId   | types.Id | 캐릭터 ID     |                 |
+----------+----------+---------------+-----------------+

Event : CharLogout
Description : 캐릭터 로그아웃
+----------+----------+------------------+------------+-----------------+
| Field    | Type     | Description      | Optional   | Restrict        |
|----------+----------+------------------+------------+-----------------|
| DateTime | datetime | 이벤트 일시      |            |                 |
| ServerNo | integer  | 서버 번호        |            | 1 이상 100 미만 |
| AcntId   | types.Id | 계정 ID          |            |                 |
| CharId   | types.Id | 캐릭터 ID        |            |                 |
| PlayTime | number   | 플레이 시간 (초) | True       |                 |
+----------+----------+------------------+------------+-----------------+

# ...
```

`CharLogout` 에는 `Login` 이벤트의 필드인 `PlayTime` 도 잘 포함된 것을 알 수 있다.

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
        ["MapId", "integer", "맵 번호"],
        ["PosX", "number", "맵상 X 위치"],
        ["PosY", "number", "맵상 Y 위치"],
        ["PosZ", "number", "맵상 Z 위치"]
      ]
    },
    "Monster": {
      "desc": "몬스터 정보",
      "mixins": ["bases.Server"],
      "fields": [
        ["MonTypeId", "integer", "몬스터 타입 ID"],
        ["MonInstId", "integer", "몬스터 인스턴스 ID"]
      ]
    }

    // ...
}
```

`Position` 베이스는 이벤트가 맵상의 특정 위치에서 발생한 경우를 위한 것이다. 몬스터를 잡거나, 아이템을 습득하는 것은 모두 맵상의 위치에서 일어나기에 필요하다. `Monster` 베이스는 특정 몬스터 개체에 관한 것이다. 몬스터도 서버 내에서만 존재할 수 있기에 `bases.Server` 를 믹스인 하였다.

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

아래는 `show` 의 결과이다.
```
$ loglab show
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
| MapId     | integer  | 맵 번호            |
| PosX      | number   | 맵상 X 위치        |
| PosY      | number   | 맵상 Y 위치        |
| PosZ      | number   | 맵상 Z 위치        |
| MonTypeId | integer  | 몬스터 타입 ID     |
| MonInstId | integer  | 몬스터 인스턴스 ID |
+-----------+----------+--------------------+

# ...
```

믹스인한 베이스의 정보, 즉 계정 및 캐릭터, 지도상의 위치, 몬스터 개체에 관한 정보들이 잘 결합된 것을 확인할 수 있다. 이런 식으로 베이스를 잘 설계하고 그것을 믹스인하는 것 만으로, 복잡한 로그 이벤트를 쉽게 만들 수 있다.

이제 아이템 관련 베이스를 추가해보자.

```js
{
  // ...

  "bases": {

    // ...

    "Item": {
      "desc": "아이템 정보",
      "mixins": ["bases.Server"],
      "fields": [
        ["ItemTypeId", "integer", "아이템 타입 ID"],
        ["ItemInstId", "integer", "아이템 인스턴스 ID"]
      ]
    }

    // ...
}
```

`Item` 은 특정 아이템 개체를 위한 베이스이다. 아이템도 서버 내에서만 존재할 수 있기에 `bases.Server` 를 믹스인 하였다. 이것을 이용해 몬스터가 아이템을 떨어뜨리는 이벤트를 만든다.

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

> `Monster` 베이스와 `Item` 베이스에 모두 `Server` 베이스가 믹스인 되어있지만 같은 필드는 덮어 써지기에 문제는 없다.

몬스터가 주체이기에 지금까지와는 달리 계정이나 캐릭터 베이스가 믹스인되지 않았다. 또 몬스터 개체의 정보가 먼저 나오도록 믹스인 순서를 조정하였다.  `show` 의 결과는 다음과 같다.

```
$ loglab show
# ...

Event : MonsterDropItem
Description : 몬스터가 아이템을 떨어뜨림
+------------+----------+--------------------+
| Field      | Type     | Description        |
|------------+----------+--------------------|
| DateTime   | datetime | 이벤트 일시        |
| ServerNo   | integer  | 서버 번호          |
| MonTypeId  | integer  | 몬스터 타입 ID     |
| MonInstId  | integer  | 몬스터 인스턴스 ID |
| MapId      | integer  | 맵 번호            |
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

`show` 의 결과는 아래와 같다.

```
$ loglab show
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
| MapId      | integer  | 맵 번호            |
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

> 필드값의 제약은 로그 설계 측면에서 꼭 필요한 것은 아니지만, 뒤에 나올 로그 검증 및 더미 로그 생성 기능을 이용할 때 유용하다.

### 서버 번호에 제약 걸기

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

기존 리스트 `["ServerNo", "integer", "서버 번호"]` 형식에서 오브젝트 형식으로 바뀌었다. 끝에 추가된 `minimum` 은 **제약문** 으로 `ServerNo`의 값을 1 이상으로 제약한다.

`show` 을 실행해보자.

```
$ loglab show
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
Description : 계정 로그아웃
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

`ServerNo` 필드가 있는 모든 이벤트에 `Restrict` 라는 새로운 컬럼이 보이고, `1 이상` 이라는 제약이 표시된다.

제약문은 필드의 타입별로 아래와 같은 것들이 있다.

- `integer` 또는 `number`
  - `minimum` : 포함하는 최소값
  - `maximum` : 포함하는 최대값
  - `exclusiveMinimum` : 제외하는 최소값
  - `exclusiveMaximum` : 제외하는 최대값
- `string`
  - `enum` : 허용하는 문자열의 나열값
  - `minLength` : 문자열의 최소 길이
  - `maxLength` : 문자열의 최대 길이
  - `pattern` : 허용하는 문자열의 정규식 패턴

예를 들어  `ServerNo` 를 100 미만으로 제약하고 싶다면 `exclusiveMaximum` 을 이용한다.

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
          "minimum": 1,
          "exclusiveMaximum": 100
        }
      ]
    },

  //...
}
```

`show` 결과는 아래와 같다.

```
$ loglab show
# ...

Event : Login
Description : 계정 로그인
+----------+----------+-------------------+------------------------+
| Field    | Type     | Description       | Restrict               |
|----------+----------+-------------------+------------------------|
| DateTime | datetime | 이벤트 일시       |                        |
| ServerNo | integer  | 서버 번호         | 1 이상 100 미만        |
| AcntId   | integer  | 계정 ID           | 1 이상                 |
+----------+----------+-------------------+------------------------+

Event : Logout
Description : 계정 로그아웃
+----------+----------+------------------+------------+-----------------+
| Field    | Type     | Description      | Optional   | Restrict        |
|----------+----------+------------------+------------+-----------------|
| DateTime | datetime | 이벤트 일시      |            |                 |
| ServerNo | integer  | 서버 번호        |            | 1 이상 100 미만 |
| AcntId   | integer  | 계정 ID          |            | 1 이상          |
| PlayTime | number   | 플레이 시간 (초) | true       |                 |
+----------+----------+------------------+------------+-----------------+

# ...
```
`1 이상 100 미만` 으로 제약이 표시된다.

예제에서 나온 ID 계열 필드들, 즉 `AcntId`, `CharId`, `MonTypeId`, `MonInstId`, `ItemTypeId`, `ItemInstId` 과 `MapId` 등 에도 0 이상이 되도록 제약을 걸어주면 좋겠다. 그러나, 반복적인 제약을 매번 걸어주는 것은 상당히 번거롭다. 이에 커스텀 타입을 이용하는 방법을 소개하겠다.

### 커스텀 타입

앞에서 말한 것 처럼 Id 필드는 항상 0 이상의 정수 값이 필요하다고 할 때, 아래와 같이 커스텀 타입을 정의하면 편리하다.

```js
{
  //...

  "types": {
    "Id": {
      "type": "integer",
      "minimum": 0
    }
  }

  //...
}
```

랩 파일에 `types` 항목을 만들고, 그 아래 커스텀 타입의 이름 및 특성을 정의한다. 여기서는 `Id` 라는 커스텀 타입을 만들고 0 이상의 정수로 정의하였다. 이것을 이용할 때는 `types.타입이름` 형식으로 지정한다. 아래를 참고하자.

```js
{
  // ...

  "bases": {

    // ...

    "Account": {
      "desc": "계정 정보",
      "mixins": ["bases.Server"],
      "fields": [
        ["AcntId", "types.Id", "계정 ID"]
      ]
    },

  // ...
}
```

이제 `CharId`, `MonTypeId`, `MonInstId`, `ItemTypeId`, `ItemInstId` 과 `MapId` 에 모두 `types.Id` 를 적용하여 간단히 제약을 걸 수 있다.

```js
{
  // ...

  "bases": {

    // ...

    "Monster": {
      "desc": "몬스터 정보",
      "fields": [
        ["MonTypeId", "types.Id", "몬스터 타입 ID"],
        ["MonInstId", "types.Id", "몬스터 인스턴스 ID"]
      ]
    },
    "Item": {
      "desc": "아이템 정보",
      "fields": [
        ["ItemTypeId", "types.Id", "아이템 타입 ID"],
        ["ItemInstId", "types.Id", "아이템 인스턴스 ID"]
      ]
    }

    // ...
}
```

> 기억해 두어야 할 것은, **커스텀 타입을 이용하는 필드에는 추가적인 제약을 걸 수 없다** 는 점이다. 이에, 필드 리스트에 `types.*` 로 커스텀 타입을 지정하는 것은 리스트 형에서만 가능하다.

`show` 을 호출하면, 같은 내용임을 확인할 수 있다.


```
$ loglab show
# ...

Event : Login
Description : 계정 로그인
+----------+----------+-------------------+------------------------+
| Field    | Type     | Description       | Restrict               |
|----------+----------+-------------------+------------------------|
| DateTime | datetime | 이벤트 일시       |                        |
| ServerNo | integer  | 서버 번호         | 1 이상 100 미만        |
| AcntId   | integer  | 계정 ID           | 0 이상                 |
| Platform | string   | 디바이스의 플랫폼 | ['ios', 'aos'] 중 하나 |
+----------+----------+-------------------+------------------------+

Event : Logout
Description : 계정 로그아웃
+----------+----------+------------------+------------+-----------------+
| Field    | Type     | Description      | Optional   | Restrict        |
|----------+----------+------------------+------------+-----------------|
| DateTime | datetime | 이벤트 일시      |            |                 |
| ServerNo | integer  | 서버 번호        |            | 1 이상 100 미만 |
| AcntId   | integer  | 계정 ID          |            | 0 이상          |
| PlayTime | number   | 플레이 시간 (초) | True       |                 |
+----------+----------+------------------+------------+-----------------+

# ...
```

이것은 `show` 명령이 기본적으로 커스텀 타입을 기본 타입으로 바꿔주기 때문이다. 만약, 커스텀 타입을 그대로 보고 싶다면 아래처럼 `-c` 또는 `--custom-type` 옵션을 이용한다.

```
$ loglab show -c
# ...

Type : types.Id
Description : Id 타입
+------------+---------------+------------+
| BaseType   | Description   | Restrict   |
|------------+---------------+------------|
| integer    | Id 타입       | 0 이상     |
+------------+---------------+------------+

Event : Login
Description : 계정 로그인
+----------+----------+-------------------+------------------------+
| Field    | Type     | Description       | Restrict               |
|----------+----------+-------------------+------------------------|
| DateTime | datetime | 이벤트 일시       |                        |
| ServerNo | integer  | 서버 번호         | 1 이상 100 미만        |
| AcntId   | types.Id | 계정 ID           |                        |
| Platform | string   | 디바이스의 플랫폼 | ['ios', 'aos'] 중 하나 |
+----------+----------+-------------------+------------------------+

Event : Logout
Description : 계정 로그아웃
+----------+----------+------------------+------------+-----------------+
| Field    | Type     | Description      | Optional   | Restrict        |
|----------+----------+------------------+------------+-----------------|
| DateTime | datetime | 이벤트 일시      |            |                 |
| ServerNo | integer  | 서버 번호        |            | 1 이상 100 미만 |
| AcntId   | types.Id | 계정 ID          |            |                 |
| PlayTime | number   | 플레이 시간 (초) | True       |                 |
+----------+----------+------------------+------------+-----------------+

# ...
```

이제 출력이 바뀌었다. 먼저 이벤트에 앞서 정의된 커스텀 타입을 보여주고, 이벤트에서 커스텀 타입을 이용하는 필드는 기본 타입으로 변환하지 않고 그대로 보여준다.

### 나열 이용하기

나열 (enum) 은 제약문의 하나로, 특정 값들만 허용하려는 경우 사용한다. 예로 로그인시 게임을 하는 유저 디바이스의 플랫폼 (OS) 필드를 추가해보자.

플랫폼은 `ios` 와 `aos` 두 가지 값만 허용하고 싶은데, 이렇게 특정 값만 허용하기 위해 `enum` 을 사용한다. 다음과 같이 `Login` 이벤트에 `Platform` 필드를 추가한다.

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

`show` 의 결과는 아래와 같다.

```
$ loglab show
# ...

Event : Login
Description : 계정 로그인
+----------+----------+-------------------+------------------------+
| Field    | Type     | Description       | Restrict               |
|----------+----------+-------------------+------------------------|
| DateTime | datetime | 이벤트 일시       |                        |
| ServerNo | integer  | 서버 번호         | 1 이상 100 미만        |
| AcntId   | integer  | 계정 ID           | 1 이상                 |
| Platform | string   | 디바이스의 플랫폼 | ['ios', 'aos'] 중 하나 |
+----------+----------+-------------------+------------------------+

# ...
```

> `enum` 은 `string` 뿐만 아니라, `integer` 와 `number` 타입에 대해서 사용할 수 있다.

나열형 항목의 값에 대해 구체적인 설명을 붙여야 하는 경우도 있다. `Item` 베이스의 `ItemTypeId` 필드에 나열을 이용해 등장할 수 있는 값을 제한하고 설명도 붙여야하는 경우를 생각해 보자.

먼저 기존 `ItemTypeId` 필드의 리스트형 선언 `["ItemInstId", "types.Id", "아이템 인스턴스 ID"]` 을 아래와 같이 오브젝트 형으로 수정한다.

```js
{
  // ...

  "bases": {

    // ...

    "Item": {
      "desc": "아이템 정보",
      "fields": [
        {
            "name": "ItemTypeId",
            "type": "integer",
            "desc": "아이템 타입 ID",
            "enum": [1, 2, 3]
        },
        ["ItemInstId", "types.Id", "아이템 인스턴스 ID"]
      ]
    }

  // ...
}
```

앞에서 설명한 것 처럼, 커스텀 타입은 `fields` 의 리스트 형 항목에서만 사용할 수 있기에 기존 `types.id` 대신 `integer` 로 타입을 변경하였다. 이어서 설명을 추가하기 위해 아래와 같이 수정한다.

```js
{
  // ...

  "bases": {

    // ...

    "Item": {
      "desc": "아이템 정보",
      "fields": [
        {
          "name": "ItemTypeId",
          "type": "integer",
          "desc": "아이템 타입 ID",
          "enum":[
            [1, "칼"],
            [2, "방패"],
            [3, "물약"]
          ]
        },
        ["ItemInstId", "types.Id", "아이템 인스턴스 ID"]
      ]
    }

  // ...
}
```

1, 2 같은 숫자 값 대신 리스트를 항목으로 사용하는데, `[나열값, 나열값_설명]` 의 형식이다. `show` 을 실행해보면 `ItemTypeId` 필드의 제약 컬럼에 각 나열값의 설명이 나오는 것을 알 수 있다.

```
# ...

Event : GetItem
Description : 캐릭터의 아이템 습득
+------------+----------+--------------------+--------------------+
| Field      | Type     | Description        | Restrict           |
|------------+----------+--------------------+--------------------|
| DateTime   | datetime | 이벤트 일시        |                    |
| ServerNo   | integer  | 서버 번호          | 1 이상 100 미만    |
| AcntId     | types.Id | 계정 ID            |                    |
| CharId     | types.Id | 캐릭터 ID          |                    |
| MapId      | types.Id | 맵 번호            |                    |
| PosX       | number   | 맵상 X 위치        |                    |
| PosY       | number   | 맵상 Y 위치        |                    |
| PosZ       | number   | 맵상 Z 위치        |                    |
| ItemTypeId | integer  | 아이템 타입 ID     | 1: 칼              |
|            |          |                    | 2: 방패            |
|            |          |                    | 3: 물약            |
| ItemInstId | types.Id | 아이템 인스턴스 ID |                    |
+------------+----------+--------------------+--------------------+
```

## 로그 파일의 검증

지금까지 설계된 로그의 정보를 이용하여 실제 로그를 검증할 수 있다. `loglab` 의 `verify` 명령으로 검증할 수 있는데, 먼저 도움말을 살펴보자.

```
$ loglab verify --help
Usage: loglab verify [OPTIONS] LOGFILE

  생성된 로그 파일 검증.

Options:
  -l, --labfile TEXT  사용할 랩 파일의 위치를 명시적으로 지정
  -s, --schema TEXT   로그 스키마 경로
  --help              Show this message and exit.
```

`verify` 명령은 생성된 로그 파일의 경로(`LOGFILE`)를 필요로 하는 것을 알 수 있다.

예제에서는 실제 서비스가 없기에, 테스트를 위해 다음과 같은 가상의 로그를 만들어 `fakelog.txt` 파일로 저장하자.

```js
{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "Login", "ServerNo": 1, "AcntId": 1000}
{"DateTime": "2021-08-13T20:21:01+09:00", "Event": "Logout", "ServerNo": 1, "AcntId": 1000}
```

> 한 줄씩 남기는 로그의 특성상, 한 라인 한 라인이 유효한 JSON 객체가 되어야 한다. 이런 형식을 [JSON Lines](https://jsonlines.org/) 라고 한다. 자세한 것은 링크를 참조하자.

이제 로그 검증을 위해 다음과 같은 명령을 내리면, 스키마관련 에러가 발생한다.

```
$ loglab verify fakelog.txt
[랩 파일 : /home/ubuntu/loglab_test/foo.lab.json]
Error: 로그 스키마를 찾을 수 없습니다. schema 명령으로 생성하거나, 스키마의 경로를 옵션으로 지정하세요.
```

`verify` 명령은 로그 파일을 검증하기 위해 *JSON 스키마 형식의 로그 스키마를 필요*로 하는데, 그것을 찾을 수 없다는 것이다. 다음과 같이 `schema` 명령으로 지금까지 작성한 랩 파일에서 JSON 로그 스키마를 만들수 있다.

```
$ loglab schema
[랩 파일 : /home/ubuntu/loglab_test/foo.lab.json]
'/home/ubuntu/loglab_test/.loglab/foo.log.schema.json 에 로그 스키마 저장.
'/home/ubuntu/loglab_test/.loglab/foo.flow.schema.json 에 플로우 스키마 저장.
```

로그랩이 만드는 임시 파일용 디렉토리 `.loglab` 아래 두 가지 스키마가 저장되는데, 하나는 **로그 스키마 (*.log.schema.json)** 이며 다른 하나는 **플로우 스키마 (*.flow.schema.json)** 이다. 로그 스키마는 실제 로그를 검증하는데 사용되고, 플로우 스키마는 더미 로그를 설계할 때 사용되는데 나중에 다룰 것이다.

> 만약, 생성한 로그 스키마가 다른 디렉토리에 있다면 아래와 같이 `verify` 명령의 `-s` 옵셩으로 지정할 수 있다.
> ```
> $ loglab verify fakelog.txt -s /path/to/schema
> ```


스키마 생성 후 다시 `verify` 명령으로 검증을 수행한다.

```
$ loglab verify fakelog.txt
# ...

[로그 스키마 파일 : /home/ubuntu/loglab_test/.loglab/foo.log.schema.json]
Error: [Line: 1] 'Platform' is a required property
{'DateTime': '2021-08-13T20:20:39+09:00', 'Event': 'Login', 'ServerNo': 1, 'AcntId': 1000}
```

`fakelog.txt` 의 첫 번째 줄의 `Login` 이벤트에서 필수인 `Platform` 필드가 빠졌기 때문에 에러가 발생한다. 다음과 같이 수정한다.

```js
{"DateTime": "2021-08-13T20:20:39+09:00", "Event": "Login", "ServerNo": 1, "AcntId": 1000, "Platform": "win"}
{"DateTime": "2021-08-13T20:21:01+09:00", "Event": "Logout", "ServerNo": 1, "AcntId": 1000}
```

의도적으로 잘못된 플랫폼값인 `win` 을 설정했다. 다시 `verify` 해보면,

```
$ loglab verify fakelog.txt
[랩 파일 : /home/ubuntu/loglab_test/foo.lab.json]
[로그 스키마 파일 : /home/ubuntu/loglab_test/.loglab/foo.log.schema.json]
Error: [Line: 1] 'win' is not one of ['ios', 'aos']
{'DateTime': '2021-08-13T20:20:39+09:00', 'Event': 'Login', 'ServerNo': 1, 'AcntId': 1000, 'Platform': 'win'}
```

이번에는 `ios` 또는 `aos` 만 허용한다는 에러가 나온다. `win` 을 `ios` 로 고치고 다시 해보자.

```
$ loglab verify fakelog.txt
[랩 파일 : /home/ubuntu/loglab_test/foo.lab.json]
[로그 스키마 파일 : /home/ubuntu/loglab_test/.loglab/foo.log.schema.json]
```

검증이 문제없이 성공했다. 이런 경우 아무런 메시지가 나오지 않는다.

이 검증 기능을 활용하면 서비스 개발자가 개발한 로그가 약속에 맞게 출력되고 있는지 확인할 때 유용할 것이다.

> 랩 파일 수정 후 스키마를 갱신하지 않으면 의도하지 않는 결과가 나올 수 있다. 수정된 랩 파일에 맞게 검증을 원할 때는 꼭 `schema` 명령을 불러주도록 하자.

## 더미 로그의 생성

실제 로그가 어떻게 생겼는지 미리 살펴볼 수 있다면, 로그를 생성하거나 처리하는 쪽 모두 참고가 될 것이다. `loglab` 에서는 이를 위해 `dummy` 명령을 지원한다.

[TODO]

### 플로우 파일 만들기

[TODO]

## 공용 랩 파일을 통한 로그 표준화

지금까지 예로든 게임 `foo` 를 만드는 `acme` 라는 회사에서, 새로운 PC 온라인 게임 `boo` 를 출시한다고 하자. `boo` 는 `foo` 와 유사하지만 다른 점도 꽤 있다.

회사는 앞으로도 다양한 서비스를 만들고 그 데이터들을 처리 및 분석할 것이기에, 효율성을 위해 **로그의 기본 구조를 표준화** 하고 싶다. 이런 경우 조직 내에서 꼭 필요로하는 로그 구조를 공용 랩 파일로 만든 뒤, 이것을 `foo` 와 `boo` 가 공유하고 확장해 나가는 방식으로 가능할 것이다.

예제에서는 편의를 위해 지금까지의 `foo.lab.json` 의 내용을 정리해 아래와 같은 `acme.lab.json` 파일을 만들었다.

```js
{
	"$schema": "https://raw.githubusercontent.com/haje01/loglab/master/schema/lab.schema.json",
	"domain": {
		"name": "acme",
		"desc": "최고의 게임 회사"
	},
    "types": {
      "Id": {
          "type": "integer",
          "desc": "Id 타입",
          "minimum": 0
      }
  },
	"bases": {
		"Server": {
			"desc": "서버 정보",
			"fields": [
				{
          "name": "ServerNo",
          "desc": "서버 번호",
          "type": "integer",
          "minimum": 1,
          "exclusiveMaximum": 100
        }
			]
		},
		"Account": {
			"desc": "계정 정보",
			"mixins": ["bases.Server"],
			"fields": [
        ["AcntId", "types.Id", "계정 ID"]
			]
		}
	},
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
		"Logout": {
			"desc": "계정 로그인",
			"mixins": ["bases.Account"],
			"fields": [
				["PlayTime", "number", "플레이 시간 (초)", true]
			]
		}
  }
}
```

### 외부 랩 파일 가져오기

먼저 사용할 외부 랩 파일을 로컬로 다운로드 받아야 하는데, `loglab` 의 `fetch` 명령을 통해 할 수 있다. 예로 로그랩 github 저장소에서 테스트용 랩 파일을 다음과 같이 받을 수 있다.

```
$ loglab fetch https://raw.githubusercontent.com/haje01/loglab/master/tests/files/acme.lab.json
```

> 실제로는 `https://www.acmegames.com/loglab/acme.lab.json` 식으로 형식을 갖춘 URL 에서 받을 수 있도록 하자.

받은 랩 파일은 작업 디렉토리 아래 `.loglab/import` 디렉토리에 URL 경로의 마지막 요소와 같은 파일 이름으로 받아진다. 위 예에서는 `.loglab/import/acme.lab.json` 로 저장된다.

`fetch` 는 편의를 위한 명령이다. 다른 방식으로 받은 파일을 동일한 위치에 복사해 넣고 사용해도 괜찮다. 특히 인터넷이 안되는 환경에서는 미리 받아둔 파일을 복사해서 사용하자.

이제 다음과 같은 내용으로 `boo.lab.json` 을 만든다.

```js
{
  "domain": {
    "name": "boo",
    "desc": "최고의 PC 온라인 게임"
  },
  "import": ["acme.lab.json"]
}
```

`import` 리스트에 가져올 외부 랩 파일을 기술한다.

> 하나 이상의 외부 랩 파일을 가져올 수 있으며, 같은 베이스나 필드는 믹스인의 경우와 마찬가지로 나중에 나오는 것이 우선한다.

외부 랩 파일에서 선언한 모든 커스텀 타입, 베이스와 이벤트는 이 랩 파일에서 직접 선언한 것과 같은 효과를 같는다.

`show` 를 해보면 도메인 이름은 `boo` 이고, 가져온 외부 랩 파일의 모든 이벤트에 원래 도메인 이름 `acme` 가 접두어로 붙어 `acme.Login`, `acme.Logout` 식으로 출력되는 것을 알 수 있다.


```
$ loglab show
[랩 파일 : /mnt/e/works/loglab_test/boo.lab.json]

Domain : boo
Description : 최고의 PC 온라인 게임

Event : acme.Login
Description : 계정 로그인
+----------+----------+-------------------+------------------------+
| Field    | Type     | Description       | Restrict               |
|----------+----------+-------------------+------------------------|
| DateTime | datetime | 이벤트 일시       |                        |
| ServerNo | integer  | 서버 번호         | 1 이상 100 미만        |
| AcntId   | integer  | 계정 ID           | 0 이상                 |
| Platform | string   | 디바이스의 플랫폼 | ['ios', 'aos'] 중 하나 |
+----------+----------+-------------------+------------------------+

Event : acme.Logout
Description : 계정 로그인
+----------+----------+------------------+------------+-----------------+
| Field    | Type     | Description      | Optional   | Restrict        |
|----------+----------+------------------+------------+-----------------|
| DateTime | datetime | 이벤트 일시      |            |                 |
| ServerNo | integer  | 서버 번호        |            | 1 이상 100 미만 |
| AcntId   | integer  | 계정 ID          |            | 0 이상          |
| PlayTime | number   | 플레이 시간 (초) | True       |                 |
+----------+----------+------------------+------------+-----------------+
```

만약 외부 랩 파일 내용에 변경이나 추가할 필요가 없다면 이대로 사용하면 되겠지만, 대부분 서비스에 맞게 수정/확장이 필요할 것이다. `acme` 에서 정의된 `Login` 이벤트의 `Platform` 를 PC 온라인 서비스에 맞게 다음처럼 변경해보자.

```js
{
  "$schema": "https://raw.githubusercontent.com/haje01/loglab/master/schema/lab.schema.json",
  "domain": {
    "name": "boo",
    "desc": "최고의 PC 온라인 게임"
  },
  "import": ["acme.lab.json"],
  "events": {
    "Login": {
      "desc": "로그인",
      "mixins": ["acme.events.Login"],
      "fields": [
        {
          "name": "Platform",
          "desc": "PC의 플랫폼",
          "type": "string",
          "enum": [
              "win", "mac", "linux"
          ]
        }
      ]
    }
  }
}
```

`acme` 의 `Login` 이벤트를 믹스인하여 새로운 `Login` 을 만들고, `Platform` 필드의 나열값을 재정의 하고 있다. `show` 를 해보면,

```
$ loglab show
# ...

Domain : boo
Description : 최고의 PC 온라인 게임

Event : Login
Description : 로그인
+----------+----------+---------------+---------------------------------+
| Field    | Type     | Description   | Restrict                        |
|----------+----------+---------------+---------------------------------|
| DateTime | datetime | 이벤트 일시   |                                 |
| ServerNo | integer  | 서버 번호     | 1 이상 100 미만                 |
| AcntId   | integer  | 계정 ID       | 0 이상                          |
| Platform | string   | PC의 플랫폼   | ['win', 'mac', 'linux'] 중 하나 |
+----------+----------+---------------+---------------------------------+

Event : acme.Logout
Description : 계정 로그인
+----------+----------+------------------+------------+-----------------+
| Field    | Type     | Description      | Optional   | Restrict        |
|----------+----------+------------------+------------+-----------------|
| DateTime | datetime | 이벤트 일시      |            |                 |
| ServerNo | integer  | 서버 번호        |            | 1 이상 100 미만 |
| AcntId   | integer  | 계정 ID          |            | 0 이상          |
| PlayTime | number   | 플레이 시간 (초) | True       |                 |
+----------+----------+------------------+------------+-----------------+
```

재정의된 `Login` 이벤트는 `acme.` 접두어가 빠져있으며, `Platform` 필드의 나열값이 바뀐 것을 알 수 있다.

커스텀 타입을 그대로 출력하면 아래와 같다.

```
$ loglab show -c
# ...

Domain : boo
Description : 최고의 PC 온라인 게임

Type : acme.types.Id
Description : Id 타입
+------------+---------------+------------+
| BaseType   | Description   | Restrict   |
|------------+---------------+------------|
| integer    | Id 타입       | 0 이상     |
+------------+---------------+------------+

Event : Login
Description : 계정 로그인
+----------+---------------+---------------+---------------------------------+
| Field    | Type          | Description   | Restrict                        |
|----------+---------------+---------------+---------------------------------|
| DateTime | datetime      | 이벤트 일시   |                                 |
| ServerNo | integer       | 서버 번호     | 1 이상 100 미만                 |
| AcntId   | acme.types.Id | 계정 ID       |                                 |
| Platform | string        | PC의 플랫폼   | ['win', 'mac', 'linux'] 중 하나 |
+----------+---------------+---------------+---------------------------------+

Event : acme.Logout
Description : 계정 로그아웃
+----------+---------------+------------------+------------+-----------------+
| Field    | Type          | Description      | Optional   | Restrict        |
|----------+---------------+------------------+------------+-----------------|
| DateTime | datetime      | 이벤트 일시      |            |                 |
| ServerNo | integer       | 서버 번호        |            | 1 이상 100 미만 |
| AcntId   | acme.types.Id | 계정 ID          |            |                 |
| PlayTime | number        | 플레이 시간 (초) | True       |                 |
+----------+---------------+------------------+------------+-----------------+
```

먼저 외부 랩 파일에서 정의된 `acme.types.Id` 타입이 나오고, 각 이벤트에서 이것을 사용하는 필드들을 확인할 수 있다.

> 외부 랩 파일에서 어떤 타입들이 정의되고 사용되는지 이해하면, 그 외부 랩 파일의 설계를 더 잘 이해하고 활용할 수 있다.

### 복잡한 랩 파일 필터링하기

지금가지 소개한 방법으로 다양한 이벤트를 정의하고, 외부 랩 파일까지 쓰다보면 한 눈에 구조를 파악하기가 점점 힘들어진다. 이럴 때는 `show` 에 필터를 걸어서 보면 편리하다. `show` 명령의 `-n` 또는 `--name` 옵션을 이용해 찾는 타입/베이스/이벤트 이름의 패턴을 줄 수 있다.

예를 들어 캐릭터 관련 이벤트만 보고 싶다면,

```
$ loglab show -n Char
[랩 파일 : /home/ubuntu/loglab_test/foo.lab.json]

Domain : foo
Description : 위대한 모바일 게임

Event : CharLogin
Description : 캐릭터 로그인
+----------+----------+---------------+-----------------+
| Field    | Type     | Description   | Restrict        |
|----------+----------+---------------+-----------------|
| DateTime | datetime | 이벤트 일시   |                 |
| ServerNo | integer  | 서버 번호     | 1 이상 100 미만 |
| AcntId   | integer  | 계정 ID       | 0 이상          |
| CharId   | integer  | 캐릭터 ID     | 0 이상          |
+----------+----------+---------------+-----------------+

Event : CharLogout
Description : 캐릭터 로그아웃
+----------+----------+---------------+-----------------+
| Field    | Type     | Description   | Restrict        |
|----------+----------+---------------+-----------------|
| DateTime | datetime | 이벤트 일시   |                 |
| ServerNo | integer  | 서버 번호     | 1 이상 100 미만 |
| AcntId   | integer  | 계정 ID       | 0 이상          |
| CharId   | integer  | 캐릭터 ID     | 0 이상          |
+----------+----------+---------------+-----------------+
```

다음과 같이 하면 이름에 `types` 가 들어가는 요소들, 즉 타입들만 볼 수 있다.

```
$ loglab show -c -n types
[랩 파일 : /home/ubuntu/loglab_test/foo.lab.json]

Domain : foo
Description : 위대한 모바일 게임

Type : types.Id
Description : Id 타입
+------------+---------------+------------+
| BaseType   | Description   | Restrict   |
|------------+---------------+------------|
| integer    | Id 타입       | 0 이상     |
+------------+---------------+------------+
```

## 기타 기능과 팁 소개

여기서는 로그랩을 활용하는데 도움이 되는 기타 기능들을 소개하겠다.

### HTML 문서 출력

로그의 설계, 개발 그리고 검증 작업이 끝난 후에는, 유관 조직에 로그에 관한 설명서를 공유해야 할 필요가 생긴다. 이런 경우 로그랩의 HTML 출력 기능을 사용하면 유용하다. 다음과 같은 명령으로 간단히 생성할 수 있다.

```
$ loglab html
[랩 파일 : /home/ubuntu/loglab_test/foo.lab.json]

'foo.html' 에 HTML 문서 저장.
```

생성된 `foo.html` 파일을 웹브라우저로 열어보면 다음과 같은 페이지를 확인할 수 있을 것이다.

![html_output](image/html.png)

### 실행 파일 이용과 빌드

인터넷 접근이 자유롭지 않은 환경에서 설치를 위해서는 실행 파일 형태가 편하다. 아래의 링크에서 미리 빌드된 `loglab` 실행 파일을 찾을 수 있다.

[로그랩 릴리즈]](https://github.com/haje01/loglab/releases)

여기에서 OS 에 맞는 압축 파일을 받아서 풀고, 어느 곳에서나 실행될 수 있도록 Path 를 걸어두면 되겠다.


로그랩 코드에서 직접 실행파일을 빌드하기 위해서는 PyInstaller 가 필요하다. [PyInstaller](http://www.pyinstaller.org) 홈페이지를 참고하여 설치하자.

> PyEnv를 사용하는 경우 빌드시 동적 라이브러리를 찾지 못해 에러가 나올 수 있다. 이때는 macOS의 경우 `--enable-framework` 옵션으로 파이썬을 빌드하여 설치해야 한다. 자세한 것은 [이 글](https://github.com/pyenv/pyenv/issues/443)을 참고하자. 리눅스의 경우 `--enable-shared` 옵션으로 빌드한다.

> 윈도우에서 파이썬 3.5를 사용할 때 "ImportError: DLL load failed" 에러가 나오는 경우 [Microsoft Visual C++ 2010 Redistributable Package](https://www.microsoft.com/en-us/download/confirmation.aspx?id=5555)를 설치하자.

윈도우에서 빌드는 로그랩 설치 디렉토리에서 다음과 같이 한다.

```
> tools\build.bat
```

리눅스/macOS 에서는 다음과 같이 빌드한다.

```
$ sh tools/build.sh
```

정상적으로 빌드가 되면, `dist/` 디렉토리 아래 `loglab.exe` (윈도우) 또는 `loglab` (리눅스/macOS) 실행 파일이 만들어진다. 이것을 배포하면 된다.

## 로그랩을 활용하는 다양한 방법

### 레가시 로그 정리용

다양한 레가시 시스템에서 로그가 나오고 있을때, 그것들을 모두 새로운 형식으로 바꾸는 것은 쉽지 않다. 이때는 로그랩을 기존 로그의 구조를 정리하는 용도로만 사용할 수도 있다.

일단 로그랩으로 정리해두면 이후 변동을 추가하기도 용이하고, 필요한 문서를 쉽게 뽑아볼 수 있다.

이후 레가시 시스템이 정비할 기회가 있다면, 로그랩 형식에 맞게 로그 출력을 수정하면 될 것이다.

[TODO]