Title: 로그 표준화와 LogLab
Author: Jeong Ju Kim

# 로그 표준화의 과제와 방향 #
로그 표준화란?
로그 표준화는 회사나 조직에서 로그의 수집, 분석, 활용에 용이하도록 서로 다른 서비스간 로그의 형식을 일관성있게 하고, 향후의 변경 및 추가 작업도 예측 가능한 방식을 따르도록 하여 관련 리소스 최적화와 데이터의 가치를 높이려는 활동을 말한다.

로그 표준화는 단순히 한 차례로 제정으로 끝나는 것이 아니라, 지속적인 의견 수렴, 개선 그리고 활용을 통해 관계자들이 함께 만들어 나가는 활동이다.

로그 표준화 위원회
로그 표준화는 한 두 사람의 힘으로 단기간에 이루어 질 수 없기에, 로그 표준화를 위한 위원회를 제안한다. 위원회는 사내의 다양한 분야에서 로그 관련 업무를 맡고 있는 담당자들로 구성되며, 다음과 같은 일을 수행한다.

- 로그 표준안 협의
- 로그 표준 명세 작성
- 로그 표준화 관련 툴의 개발
- 로그 표준 전파 및 서비스 별 담당자와 커뮤니케이션
- 개선안 반영


표준의 다양한 필요성
로그 표준화의 목적에 동의하는 것은 어렵지 않으나, 조직 구성원 각자의 역할 및 입장에서 바라본 로그 표준화는 다양한 필요성을 가진다.

서비스 개발자
- 코딩에 참고할 수 있는 로그 문서를 제공하는가?
- 표준을 따르되, 필요에 따라 로그의 추가/변경이 용이한가?
- 내가 생성한 로그가 표준을 만족하는지 테스트할 수 있는가?
- 개발 언어에서 쉽게 쓸 수 있는 로그 객체나 출력기를 제공하는가?

시스템 엔지니어
- 배포나 서버 증/감설에 용이한 구조를 가지고 있는가?
- 로그 출력 미디어가 설치 및 운영에 용이한가?

데이터 엔지니어
- 로그의 출력 대상이 적절한 미디어(파일, RDB, 하둡 등)로 가능한가?
- 로그 수집/정리에 필요한 문서 및 샘플을 제공하는가?
- 로그 구조 변경시 버전 관리가 용이한가?

분석/데이터 과학자
- 로그 분석에 필요한 문서 및 샘플을 제공하는가?
- 분석에 필요한 충분한 정보를 담고 있는가?
- 로그 구조 변경시 버전 관리가 용이한가?

경영자 및 관리부서
- 신규 서비스를 위한 가이드 문서가 존재하는가?
- 인력 이탈이나 교체에 대응하도록 일관된 형식을 갖는가?
- 운영 지표 추출에 충분한 정보를 담고 있는가?
- 해외 서비스를 위한 다국어 문서를 지원하는가?


로그 표준의 요건
앞에서 말한 다양한 필요성을 만족하고, 건강한 표준으로서의 로그 작성 및 활용을 위해서 다음과 같은 요건을 제안한다.

로그 명세를 URL을 통해 누구나 접근이 가능하도록 공개
- 다양한 관련자의 공유/활용을 위해 공개는 필수적이다.
- 로그의 내용과 달리, 로그의 명세는 보안 및 개인정보에 민감하지 않다.
- URL을 통해 제공하는 것으로, 다양한 명세 파일이 산재하는 혼란을 피할 수 있다.

독점 포맷과 바이너리 형식이 아닐 것
- 특정 업체의 상용 스프레드 쉬트나 워드 프로세스로 기술된 명세는 접근성 문제가 발생할 수 있다.
- 바이너리 포맷은 버전 관리가 어렵다.

로그 명세는 독립적인 형식(Formulation) 언어로 기술할 것
- 자연어로 기술된 표준은 모호성이 상존하기에, 논리적 완결성을 가진 언어를 사용하는 것이 바람직하다.
- SQL이나 특정 프로그래밍 언어에 의존한 기술은, 로그 표준을 위한 다양한 필요성을 만족시킬 수 없다.

개발측에도 도움이 되는 방법론
- 퍼블리셔의 입장을 강요하는 표준이 아니라, 개발측에 실질적인 도움이 되는 방법론으로서 자리메김 할것.


로그 표준화의 방향
앞의 요건을 만족하도록 아래와 같은 표준화 방향을 제안한다.

- 로그 정의용 언어를 만들고, 이를 활용하여 로그 표준안을 기술한다.
- 위원회는 함께 표준 로그 명세를 설계하고, 관련 툴을 개발해 제공한다.
- 개발측은 이것을 준수/확장하여 실제 서비스 로그를 개발한다.
- 로그 표준안 및 이를 활용한 서비스별 로그 명세의 관리는 Github의 공개 저장소를 사용한다.


로그 설계 프레임웍의 개발
앞의 방향에 맞도록 다음과 같은 기능의 로그 설계 프레임웍을 개발한다.

객체 지향적 로그 설계
- 기존 로그의 정의서를 보면 이벤트는 다양하나 많은 중복 속성이 있음을 알 수 있다.
- 중복에는 필요없는 비용과 오류가 따르기 마련이다.
- 객체 지향적 로그 설계로 이런 단점을 방지하고, 로그의 유지 보수성을 좋게 한다.

로그 문서 생성
- 로그 정의 언어로 기술한 로그 명세에서 자동으로 다양한 포맷(Text, HTML, Markdown)의 로그 설명 문서를 자동 생성한다.
- 로그 명세에 다국어 설명이 포함되면 해당 언어를 위한 문서도 생성한다.

샘플 로그 생성
로그 명세에는 실제 로그와 같지 않더라도, 유용한 샘플 로그 생성에 충분한 정보를 담고 있다. 샘플로그 생성 기능으로,

- 개발자는 로그의 예를 보며 로그 코딩 작업을 할 수 있다.
- 데이터 엔지니어는 서비스 오픈전에 미리 수집/처리 개발을 진행할 수 있다.
- 데이터 과학자는 샘플 기반으로 지표 및 분석의 틀을 미리 준비할 수 있다.

샘플 로그의 출력은 다양한 포맷(JSON, CSV/TSV, SQL)을 지원한다.

로그 검증
- 개발 측에서 생성된 로그가 로그 정의에 맞는지 테스트 기능을 제공한다.

로그 스키마 생성
- 다양한 로그 출력 미디어 지원을 위해, 로그 정의에서 RDB, Parquet 등 로그 스키마를 자동 생성


표준 로그의 내용
좋은 그릇도 나쁜 음식이 담겨 있으면 의미가 없을 것이다. 앞에서 말한 방식을 사용해 작성될 로그 표준 명세에는 어떤 내용이 담겨야 할까? 구체적인 명세는 앞으로 인터뷰를 통해 로그 정의 언어로 작성될 것이며, 이곳에는 어떤 종류의 이벤트를 어떻게 남겨야 하는지에 대한 원칙을 기록할 예정이다.

[[TODO]]

작업 산출물
앞에서 말한 방향에 의거하여, 위원회는 다음과 같은 3 가지를 산출물을 제공한다.

1. 로그 정의용 언어
2. 이 언어로 기술된 확장 가능한 로그 표준
3. 로그 개발 및 활용에 도움을 주는 툴

개발측은 이 산출물을 활용해 다음과 같은 2 가지의 산출물을 생산한다.

1. 로그 표준안 기반으로 서비스의 필요에 맞게 수정/확장된 로그 명세
2. 서비스 로그 명세에 맞는 로그를 생성하는 서비스 코드


레가시의 수용

회사에는 조직 내/외부에서 개발한 다양한 서비스의 로그가 생성/활용 되고 있다. 일관된 형태는 아닐지라도, 이 로그들은 다양한 경험과 지식의 산물인 것이다. 표준화 위원회는 다음 두 가지 방법으로 기존 레가시를 포용할 수 있겠다.

기존 로그의 노하우를 새 표준에 반영
- 기존 로그를 만들고 활용한 담당자들과 인터뷰를 통해, 왜 그런 로그가 왜 만들어 졌고, 어떻게 사용되고 있는지 파악.
- 그 노하우를 살려 새로운 로그 표준에 반영.

임포터를 통해 표준 로그 형태로 변환
- 스프레드쉬트나 워드프로세스 파일로 된 기존 로그의 명세가 있는 경우, 그것을 가져오기 위한 스크립트를 작성.
- 기존 로그도 새로운 로그 표준으로 변환될 경우, 유지 보수성이 좋아지고 프레임웍이 제공할 다양한 툴을 활용할 수 있을 것.


----

# LogLab (가안) #
소개와 설치

로그랩은 로그를 설계하고 활용하기 위한 툴이다. 크게 다음과 같은 기능을 가지고 있다:

- 로그를 객체지향적으로 설계
- 설계된 로그의 문서 출력
- 설계된 로그의 샘플(가짜) 로그 생성
- 로그가 설계에 맞게 작성되었는지 검증

로그랩은 https://github.com/haje01/loglab 에서 받을 수 있다. [[TODO]]

```
$ git checkout https://github.com/haje01/loglab
$ pip install -e .
```

으로 설치하자.

로그랩은 '메타파일'로 불리는 JSON 파일에 로그 명세를 기술하는 것으로 로그를 설계한다. 메타파일은 로그랩에서 제공하는 JSON 스키마 형식에 맞추어 작성하며, 확장자는 .meta.json 을 사용한다. VSCode 등 JSON 스키마를 지원하는 에디터를 이용하면 편집이 용이할 것이다.

간단한 로그 명세 만들기

로그랩의 사용법을 빠르게 살펴보기위해, 애크미(Acme)라는 가상의 게임 회사의 foo 라는 모바일 게임을 위한 메타파일을 만들어 보자.

```
{
	"events": {
		"Login": {
			"desc": "유저 로그인.",
		}
	}
}
```

events 요소 아래에 사용할 로그 이벤트 요소를 정의하면 된다. 여기서는 Login 이벤트를 정의하고 있다. desc 요소에 이벤트의 설명을 기입한다.

이 파일을 foo.meta.json 이라는 파일명으로 저장하고, 로그랩의 문서 출력 기능을 이용해 보겠다. 문서 출력은 다음과 같은 명령으로 한다.

```
$ loglab -m foo.meta.json doc
```

이 명령은 -m 인자로 사용할 메타파일을 지정한 후, doc 부명령으로 문서를 생성한다. 다음과 같이 출력된다.
```
Event : Login
Description: 유저 로그인.
+------------+----------+---------------+------------+
| Property   | Type     | Description   | Required   |
|------------+----------+---------------+------------+
| Datetime   | datetime | 이벤트 일시   |  true      |
| Event      | string   | 이벤트 타입   |  true      |
+------------+----------+---------------+------------+
```
Login 에 대한 문서가 출력된다. 각 속성별로 행이 나오고, 속성 이름(Property), 타입(Type), 설명(Description), 필수 여부(Required) 컬럼으로 속성을 설명하고 있다. Required가 true인 속성은 해당 이벤트에 꼭 필요한 필수 속성이며, false인 경우 없어도 무관한 선택 속성이다. 기본적으로 모든 속성은 필수 속성이다.

첫 행에 만들어 주지 않은 Datetime 이라는 속성이 보인다. 모든 로그 이벤트는 출력 시간이 꼭 필요하기에, 로그랩에서 자동으로 만들어 주는 속성이다. 다음으로 Event는 이벤트의 종류를 나타낸다. 문서 출력시 원하지 않는 컬럼은 --exclude-column 인자로 무시할 수 있다. Required를 제외하고 다시 문서를 보면,

```
$ loglab -m foo.meta.json doc --exclude-column required

Event : Login
Description: 유저 로그인.
+------------+----------+---------------+
| Property   | Type     | Description   |
|------------+----------+---------------+
| Datetime   | datetime | 이벤트 일시   |
| Event      | string   | 이벤트 타입   |
+------------+----------+---------------+
```

Required 컬럼이 빠진 문서가 출력된다.

이제 여기에 로그인한 서버ID 속성을 추가해 보자. 속성은 이벤트 객체 아래 props 요소를 이용한다. 로그랩의 이벤트 및 속성의 이름은 각 단어의 시작을 대문자로(Pascal Case) 한다.

```
{
	"events": {
		"Login": {
			"desc": "유저 로그인.",
			"props": [
				["ServerNo", "integer", "서버 번호"]
			]
		}
	}
}
```
props 는 어레이 값으로, 하나 이상의 속성을 기술할 수 있다. 각 속성은 어레이 형식 또는 객체 형식으로 기술할 수 있다. 어레이 형식은 간단히 속성을 추가할 때 유용하며 [속성_이름, 속성_타입, 속성_설명, 필수여부(생략가능)]의 순으로 기술한다. 객체 형식은 이후에 살펴보겠다.

다시 문서를 출력해 보자.
```
$ loglab -m foo.meta.json doc

Event : Login
Description: 유저 로그인.
+------------+----------+---------------+-----------+
| Property   | Type     | Description   | Required  |
|------------+----------+---------------+-----------+
| Datetime   | datetime | 이벤트 일시   |  true     |
| Event      | string   | 이벤트 타입   |  true     |
| ServerNo   | integer  | 서버 번호     |  true     |
+------------+----------+---------------+-----------+
```
ServerNo가 추가된 것을 알 수 있다. 이제 Logout 이벤트를 새로 추가해 보자.

```{
	"events": {
		"Login": {
			"desc": "유저 로그인.",
			"props": [
				["ServerNo", "integer", "서버 번호"]
			]
		},
		"Logout": {
			"desc": "유저 로그아웃.",
			"props": [
				["ServerNo", "integer", "서버 번호"]
			]
		}
	}
}
```
다시 문서를 보면

```
$ loglab -m foo.meta.json doc --skip required --exclude-column required

Event : Login
Description: 유저 로그인.
+------------+----------+---------------+
| Property   | Type     | Description   |
|------------+----------+---------------|
| Datetime   | datetime | 이벤트 일시   |
| Event      | string   | 이벤트 타입   |
| ServerNo   | integer  | 서버 번호     |
+------------+----------+---------------+

Event : Logout
Description: 유저 로그아웃.
+------------+----------+---------------+
| Property   | Type     | Description   |
|------------+----------+---------------|
| Datetime   | datetime | 이벤트 일시   |
| Event      | string   | 이벤트 타입   |
| ServerNo   | integer  | 서버 번호     |
+------------+----------+---------------+
```
로그아웃 이벤트가 추가된 것을 알 수 있다.

위에서 같은 ServerNo 속성이 로그인과 로그아웃에서 중복되고 있는데, 객체 참조 기능을 이용하여 리팩토링해 보자.

```
{
	"bases": {
		"Common": {
			"desc": "공통 요소."
			"props": [
				["ServerNo", "integer", "서버 번호"]
			]
		}
	},
	"events": {
		"Login": {
			"desc": "유저 로그인.",
			"mixins": ["bases.Common"]
		},
		"Logout": {
			"desc": "유저 로그아웃.",
			"mixins": ["bases.Common"]
		}
	}
}
```
참조될  공통 속성을 bases 요소 아래 베이스 요소 형식으로 정의하면 된다. 베이스 요소는 이벤트와 비슷하나, 직접 출력되지 않고, 이벤트 요소나 다른 Base 요소에서 참조되기 위한 용도이다.

Login/Logout 이벤트에서는 mixins 요소를 통해 참조할 하나 이상의 베이스나 이벤트 요소를 기술할 수 있다. bases.Common의 bases는 루트 요소의 이름이고, Common은 참조할 베이스 요소의 이름이다. 이벤트 요소를 참조하려면 events.이벤트_이름 식이 된다.

만약 mixins에 하나 이상의 요소가 있고 그들간 겹치는 속성이 있으면, 나중에 등장하는 것의 속성이 우선하게 된다.

참조되는 측과 참조하는 측에 같은 요소가 겹치면, 참조하는 측의 것을 사용하게 된다. 예를 들어 위의 bases.Common 과 events.Login 모두에 desc 요소가 있는데, 이 경우 Login 의 desc 요소가 우선하게 된다.

수정된 메타파일로 다시 문서를 출력하면, 리팩토링 전과 같은 결과를 확인할 수 있을 것이다.


샘플 로그와 속성값 제약하기

실제 로그가 어떻게 생겼는지 미리 살펴볼 수 있다면, 로그를 만들거나 처리하는 입장에서 도움이 될 것이다. 로그랩에서는 다음과 같이 샘플 로그를 생성할 수 있다.

```$ loglab -m foo.meta.json sample

{
	"Logout": {
		"Datetime": "2019-11-13T20:20:39+09:00",
		"ServerNo": -1932
	}
}
{
	"Login": {
		"Datetime": "2019-11-13T20:20:40+09:00",
		"ServerNo": 94840191
	}
}
{
	"Login": {
		"Datetime": "2019-11-13T20:20:41+09:00",
		"ServerNo": -3948
	}
}
{
	"Logout": {
		"Datetime": "2019-11-13T20:20:42+09:00",
		"ServerNo": 114938
	}
}
```
임의의 이벤트 로그가 4개 생성이 되었다. Datetime 속성은 현재 시간에서 증가하는 식으로 채워진다. 로그랩의 날자 및 시간 형식은 RFC3339를 따른다. (https://json-schema.org/latest/json-schema-validation.html#RFC3339)

ServerNo 속성의 값은 좀 특이한데, 지나치게 큰 값이나 음의 수가 섞여서 나오고 있다. 이는 속성의 타입인 integer형에 맞춰 임의의 값이 채워지기 때문이다. 좀 더 그럴듯한 서버 번호를 위해 속성 값에 제약을 추가할 수 있다. 단, 제약을 지정하기 위해서는 props 아래 속성값을 리스트형이 아닌 객체형으로 기술해야 한다.

```
{
	"bases": {
		"Common": {
			"desc": "공통 요소."
			"props": [
				{
					"name": "ServerNo",
					"desc": "서버 번호",
					"type": "integer",
					"minimum": 1,
					"maximum": 10
				}
			]
		}
	},
	"events": {
		"Login": {
			"desc": "유저 로그인.",
			"mixins": ["bases.Common"]
		},
		"Logout": {
			"desc": "유저 로그아웃.",
			"mixins": ["bases.Common"]
		}
	}
}
```
속성을 객체형으로 기술할 때는 name, type, desc 등이 필수 요소이며, 필요에 따라 제약 등 다양한 추가 요소를 기술할 수 있다.

다시 샘플 로그를 보면
```
$ loglab -m foo.meta.json sample

{
	"Logout": {
		"Datetime": "2019-11-13T20:20:39+09:00",
		"ServerNo": 3
	}
}
{
	"Login": {
		"Datetime": "2019-11-13T20:20:40+09:00",
		"ServerNo": 9
	}
}
{
	"Login": {
		"Datetime": "2019-11-13T20:20:41+09:00",
		"ServerNo": 1
	}
}
{
	"Logout": {
		"Datetime": "2019-11-13T20:20:42+09:00",
		"ServerNo": 4
	}
}
```
여전히 임의의 속성값이나, 제약에 맞춰 좀 더 그럴듯해 보인다. 문서에서도 속성의 제약을 확인할 수 있다.
```
$ loglab -m foo.meta.json doc --exclude-column required

Event : Login
Description: 유저 로그인.
+------------+----------+-----------------+------------------+
| Property   | Type     | Description     | Constraint       |
|------------+----------+-----------------+------------------+
| Datetime   | datetime | 이벤트 일시     |                  |
| Event      | string   | 이벤트 타입     |                  |
| ServerNo   | integer  | 서버 번호       | 1이상 10이하     |
+------------+----------+-----------------+------------------+

Event : Logout
Description: 유저 로그아웃.
+-------------+----------+----------------+----------------+
| Property    | Type     | Description    | Constraint     |
|-------------+----------+----------------+----------------+
| Datetime    | datetime | 이벤트 일시    |                |
| Event       | string   | 이벤트 타입    |                |
| ServerNo    | integer  | 서버 번호      | 1이상 10이하   |
+-------------+----------+----------------+----------------+
```
이러한 속성값 제약은 나중에 설명할 로그 검증시에도 유용하게 사용될 수 있다. 위와 같이 로그랩 요소의 속성에 제약을 가할 때는 JSON 스키마의 방식을 따른다. 다양한 제약 방법이 있으니 https://json-schema.org/understanding-json-schema/reference/index.html 을 참고하자.


이제, 공통 요소와 별도로 이벤트별 속성을 사용해 보자. 예로 Login에는 Platform 속성을, Logout에는 PlayTime 속성을 추가하겠다.
```
{
	"bases": {
		"Common": {
			"desc": "공통 요소."
			"props": [
				{
					"name": "ServerNo",
					"desc": "서버 번호",
					"type": "integer",
					"minimum": 1,
					"maximum": 10
				}
			]
		}
	},
	"events": {
		"Login": {
			"desc": "유저 로그인.",
			"mixins": ["bases.Common"],
			"props": [
				{
					"name": "Platform",
					"desc": "디바이스 플랫폼",
					"type": "string":,
					"enum": ["ios", "aos"]
				}
			]
		},
		"Logout": {
			"desc": "유저 로그아웃.",
			"mixins": ["bases.Common"],
			"props": [
				{
					"name": "PlayTime",
					"desc": "플레이 시간(분)."
					"type": "integer",
					"minimum": 0
				}
			]
		}
	}
}
```
Login에 추가된 Platform 속성은 유저가 로그인시 이용한 모바일 디바이스의 플랫폼을 가정했다. string 타입이되 enum으로 나열형 제약이 있다. enum은 리스트 값을 가지며 여기에 등록된 값만 허용된다. Logout에 추가된 PlayTime은 유저가 로그인 후 로그아웃까지 플레이한 시간을 의미하며 분을 단위로 한다. 0이상 값만 허용하는 제약이 있다.

이제 다시 로그 문서를 살펴보자.
```
$ loglab -m foo.meta.json doc --exclude-column required

Event : Login
Description: 유저 로그인.
+------------+----------+-----------------+------------------+
| Property   | Type     | Description     | Constraint       |
|------------+----------+-----------------+------------------+
| Datetime   | datetime | 이벤트 일시     |                  |
| Event      | string   | 이벤트 타입     |                  |
| ServerNo   | integer  | 서버 번호       | 1이상 10이하     |
| Platform   | string   | 디바이스 플랫폼 | ios, aos 중 선택 |
+------------+----------+-----------------+------------------+

Event : Logout
Description: 유저 로그아웃.
+-------------+----------+----------------+----------------+
| Property    | Type     | Description    | Constraint     |
|-------------+----------+----------------+----------------+
| Datetime    | datetime | 이벤트 일시    |                |
| Event       | string   | 이벤트 타입    |                |
| ServerNo    | integer  | 서버 번호      | 1이상 10이하   |
| PlayTime    | integer  | 세션 시간(분)  | 0 이상         |
+-------------+----------+----------------+----------------+
```
이벤트별로 새로운 속성이 추가되었다. Login 이벤트에는 Platform 속성이, Logout 이벤트에는 PlayTime 속성에 대한 설명이 나오는 것을 알 수 있다.


로그의 검증

개발자는 잘 정의된 명세와 거기에서 생성된 문서 및 샘플을 참고해 로그 코드를 만들었다 하더라도, 여전히 생성된 로그가 표준에 적합한지 확인하고 싶을 수 있다. 로그랩의 로그 검증 기능을 이용하면 생성된 로그의 표준 준수 여부를 확인하고, 만약 문제가 되는 부분이 있다면 어디에서 어떤 문제가 있는지 알 수 있다.

예를 들어 다음과 같은 내용의 JSON 로그파일 my_log.json이 있다고 하자.
```
{
	"Login": {
		"Datetime": "2019-11-13T20:20:41+09:00",
        "ServerNo": 1,
        "Platform": ios
	}
}
{
	"Logout": {
		"Datetime": "2019-11-13T20:21:42+09:00",
		"ServerNo": "1"
	}
}
```

아래의 명령으로 이것을 검증할 수 있다.
```
$ loglab -m foo.meta.json verify my_log.json

Error: Not a valid JSON file.
  json.decoder.JSONDecodeError: Expecting value: line 5 column 21 (char 100)
```
먼저 발생한 문제는 이 로그 파일이 유효한 JSON 파일이 아니라는 것이다. 위의 Platform 속성의 값인 ios 에 문자열을 위한 쿼테이션 마크가 없기 때문. 이를 "ios"로 수정하여 다시 돌려보자.
```
$ loglab -m foo.meta.json verify my_log.json

Error: Value type mismatch.
  'ServerNo' is not of type 'integer'
```
앞에서 integer 형으로 명시한 ServerNo의 값에 정수가 아닌 문자열 "1"이 온 것이 문제이다. 이것도 1로 수정하여 다시 돌려보자.
```
$ loglab -m foo.meta.json verify my_log.json

Error: Required property 'PlayTime' does not exist!
```
Logout 이벤트에  (기본적으로)필수로 선언된 PlayTime 속성이 존재하지 않아 발생한 문제이다. PlayTime을 추가해 다시 검증하면 이제 모든 문제가 해결될 것이다.

```
$ loglab -m foo.meta.json verify my_log.json

`my_log.json` is a valid log file!
```

공용 메타파일의 이용

지금까지는 단순히 하나의 서비스를 위한 로그 메타파일을 작성해 보았다. 만약 조직에서 운용하는 하나 이상의 서비스가 존재하고, 그 로그들이 표준적인 형식을 유지하도록 하려면 어떻게 해야 할까?

로그랩에서는 메타파일들간 공통점을 리팩토링해 공용 메타파일을 만들고, 다른 메타파일이 그것을 참조하여 일관성을 지키도록 할 수 있다.

앞에서 살펴본 가상의 애크미 게임 회사의 모바일 게임 foo 외에, 새로운 온라인 게임 boo 를 만들고 있다고 하자. 이 회사는 두 서비스가 공통 표준을 따르기를 원하고, 이에 애크미를 위한 공용 메타파일을 작성하기로 한다.

foo의 내용을 대부분 차용해 아래처럼 acme.meta.json 을 작성한다.

```
{
    "info": {
		"name": "애크미 로그 표준",
		"desc": "애크미의 로그 표준 명세. 자세한 것은 https://github.com/acme/loglab 을 참고하세요."""
    },
	"bases": {
		"Common": {
			"props": [
				{
					"name": "ServerNo",
					"type": "integer",
					"minimum": 1,
					"maximum": 10
				}
			]
		}
	},
	"events": {
		"Login": {
			"desc": "로그인",
			"mixins": ["bases.Common"],
			"props": [
				{
					"name": "Platform",
					"desc": "디바이스 플랫폼",
					"type": "string",
				}
			]
		},
		"Logout": {
			"desc": "로그아웃",
			"mixins": ["bases.Common"],
			"props": [
				{
					"name": "PlayTime",
					"desc": "플레이 시간(분)."
					"type": "integer",
					"minimum": 0
				}
			]
		}
	}
}
```
특징 적인 것은 가장 먼저 나오는 info 요소이다. 여기에 메타파일에 관한 여러 정보 요소를 기술할 수 있다. name은 메타파일의 이름이고, desc 는 메타파일에 관한 추가적인 설명이다. 다양한 메타파일을 사용할 때 도움이 될 것이다.

나머지는 기존에 foo 메타파일의 내용 중, 모바일 특화된 내용인 Platform의 enum 을 제외한 대부분 요소를 가져왔다. 문서를 출력해보면, 다음과 같이 나온다.
```
$ loglab -m acme.meta.json doc --exclude-column required

Meta : 애크미 로그 표준
Meta Description: 애크미의 로그 표준 명세. 자세한 것은 https://github.com/acme/loglab 을 참고하세요.

Event : Login
Description: 유저 로그인.
+------------+----------+-----------------+------------------+
| Property   | Type     | Description     | Constraint       |
|------------+----------+-----------------+------------------+
| Datetime   | datetime | 이벤트 일시     |                  |
| Event      | string   | 이벤트 타입     |                  |
| ServerNo   | integer  | 서버 번호       | 1이상 10이하     |
| Platform   | string   | 디바이스 플랫폼 |                  |
+------------+----------+-----------------+------------------+

Event : Logout
Description: 유저 로그아웃.
+-------------+----------+----------------+----------------+
| Property    | Type     | Description    | Constraint     |
|-------------+----------+----------------+----------------+
| Datetime    | datetime | 이벤트 일시    |                |
| Event       | string   | 이벤트 타입    |                |
| ServerNo    | integer  | 서버 번호      | 1이상 10이하   |
| PlayTime    | integer  | 세션 시간(분)  | 0 이상         |
+-------------+----------+----------------+----------------+
```
이제 기존의 foo 메타파일이 이것을 참조하도록 foo.meta.json을 아래와 같이 수정한다.
```
{
	"info": {
		"name": "foo 로그 명세",
		"desc": "모바일 게임 foo의 로그 명세. 자세한 것은 https://github.com/acme/loglab/foo 를 참고하세요
	},
	"metas": [
		["https://github.com/acme/loglab/aceme.meta.json", "acme"]
	],
	"events": {
		"Login": {
			"mixins": ["acme.events.Login"],
			"props": [
				{
					"name": "Platform",
					"enum": ["ios", "aos"]
				}
			]
		}
	}
}
```
새로운 metas 요소가 보인다.  여기에 참조하는 공용 메타파일을 [메타파일_URL, 메타파일_별칭] 형식으로 하나 이상 등록할 수 있다.

이런 식으로 다른 외부 메타파일을 참조하면, 다음과 같은 효과가 있다.

- mixins에서 별칭을 통해 외부 메타파일의 베이스나 이벤트 요소를 참조 할 수 있다.
- 샘플 로그나 로그 스키마 생성시, 참조된 메타파일에 있는 이벤트 요소도 자동으로 생성된다.
- 참조되는 측과 참조하는 측에 같은 요소가 겹치면, 참조하는 측의 것이 우선한다.

위 파일에서는 Login 이벤트의 Platform 속성의 enum 만 지정하고 있지만, 문서를 출력해보면,
```
$ loglab -m foo.meta.json doc --exclude-column required

Meta : foo 로그 명세
Meta Description: 모바일 게임 foo의 로그 명세. 자세한 것은 https://github.com/acme/loglab/foo 를 참고하세요.

Event : Login
Description: 유저 로그인.
+------------+----------+-----------------+------------------+
| Property   | Type     | Description     | Constraint       |
|------------+----------+-----------------+------------------+
| Datetime   | datetime | 이벤트 일시     |                  |
| Event      | string   | 이벤트 타입     |                  |
| ServerNo   | integer  | 서버 번호       | 1이상 10이하     |
| Platform   | string   | 디바이스 플랫폼 | ios, aos 중 선택 |
+------------+----------+-----------------+------------------+

Event : Logout
Description: 유저 로그아웃.
+-------------+----------+----------------+----------------+
| Property    | Type     | Description    | Constraint     |
|-------------+----------+----------------+----------------+
| Datetime    | datetime | 이벤트 일시    |                |
| Event       | string   | 이벤트 타입    |                |
| ServerNo    | integer  | 서버 번호      | 1이상 10이하   |
| PlayTime    | integer  | 세션 시간(분)  | 0 이상         |
+-------------+----------+----------------+----------------+
```
메타파일 참조를 이용하기 전과같이 Login과 Logout 두 이벤트의 모든 속성이 잘 출력되는 것을 확인할 수 있다.

마찬가지로 boo의 메타파일 boo.meta.json 도 아래와 같이 작성하고,
```
{
	"info": {
		"name": "boo 로그 명세",
		"desc": "온라인 게임 boo의 로그 명세. 자세한 것은 https://github.com/acme/loglab/boo 를 참고하세요
	},
	"metas": [
		["https://github.com/acme/loglab/aceme.meta.json", "acme"]
	],
	"events": {
		"Login": {
			"mixins": ["acme.events.Login"],
			"props": [
				{
					"name": "Platform",
					"enum": ["pc", "mac", "linux"]
				}
			]
		}
	}
}
```
문서를 출력해보자.
```
$ loglab -m foo.meta.json doc --exclude-column required

Meta : boo 로그 명세
Meta Description: 온라인 게임 boo의 로그 명세. 자세한 것은 https://github.com/acme/loglab/boo 를 참고하세요.

Event : Login
Description: 유저 로그인.
+------------+----------+-----------------+------------------------+
| Property   | Type     | Description     | Constraint             |
|------------+----------+-----------------+------------------------+
| Datetime   | datetime | 이벤트 일시     |                        |
| Event      | string   | 이벤트 타입     |                        |
| ServerNo   | integer  | 서버 번호       | 1이상 10이하           |
| Platform   | string   | 디바이스 플랫폼 | pc, mac, linux 중 선택 |
+------------+----------+-----------------+------------------------+

Event : Logout
Description: 유저 로그아웃.
+-------------+----------+----------------+----------------+
| Property    | Type     | Description    | Constraint     |
|-------------+----------+----------------+----------------+
| Datetime    | datetime | 이벤트 일시    |                |
| Event       | string   | 이벤트 타입    |                |
| ServerNo    | integer  | 서버 번호      | 1이상 10이하   |
| PlayTime    | integer  | 세션 시간(분)  | 0 이상         |
+-------------+----------+----------------+----------------+
```
이런 방식으로 기본 로그 구조는 공유하면서, 서비스별로 특화된 내용만 추가/갱신할 수 있게 된다.

[[TODO]]