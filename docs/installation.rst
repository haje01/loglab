설치
================

빌드된 실행 파일 설치하기
-----------------------

간편하게 사용하기 위해서는 미리 빌드된 실행 파일 형태가 편할 수 있겠다. 아래의 링크에서 미리 빌드된 `loglab` 실행 파일을 찾을 수 있다 (현재는 윈도우 버전만).

`로그랩 릴리즈 <https://github.com/haje01/loglab/releases>`_

여기에서 OS 에 맞는 압축 파일을 받아서 풀고, 어느 곳에서나 실행될 수 있도록 Path 를 걸어두면 되겠다.

소스 코드로 설치하기
-----------------------

소스 코드 기반으로 LogLab을 설치하기 위해서는 최소 Python 3.7 이상이필요하다. 파이썬이 설치되어 있지 않다면 `파이썬 홈페이지 <https://www.python.org/>`_ 에서 최신 버전의 파이썬을 설치하도록 하자.

추가적으로 패키지 관리자 `uv 의 설치 <https://github.com/astral-sh/uv>`_ 도 필요하다.

LogLab 의 홈페이지는 https://github.com/haje01/loglab 이다. 다음과 같이 git 으로 코드를 받은 뒤, uv 를 통해 설치하자.

.. code-block:: bash

    $ git clone https://github.com/haje01/loglab
    $ uv venv
    $ uv pip install -e .

.. note::

    이미 설치가 되어있는 경우는 ``source .venv/bin/activate`` 만 호출해준다.

설치가 잘 되었다면 로그랩의 커맨드라인 툴인 `loglab` 을 이용할 수 있다. 다음과 같이 입력해보자.

.. code-block:: bash

    $ loglab
    Usage: loglab [OPTIONS] COMMAND [ARGS]...

    Options:
    --help  Show this message and exit.

    Commands:
    html     HTML 문서 출력.
    object   로그 객체 코드 출력.
    schema   로그 검증용 스키마 생성.
    show     로그 구성 요소 출력.
    verify   생성된 로그 파일 검증.
    version  로그랩 버전 표시.

위에서 알 수 있듯 `loglab` 에는 다양한 명령어가 있는데 예제를 통해 하나씩 살펴보도록 하겠다. 먼저 간단히 버전을 확인해보자.

.. code-block:: bash

    $ loglab version
    0.2.4
