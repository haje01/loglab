설치
================

**uv 기반 설치 (권장)**

먼저 Python 용 패키지 매니저인 `uv` 의 설치가 필요하다. `uv 설치 페이지 <https://docs.astral.sh/uv/getting-started/installation>`_ 를 참고하여 사용자의 환경에 맞게 설치하도록 한다.

이제 다음과 같은 `uv` 명령으로 LogLab 을 설치한다.

.. code:: bash

    uv tool install --from git+https://github.com/haje01/loglab.git loglab

.. note::

    만약 기존에 설치된 loglab 을 최신 버전으로 업그레이드하고 싶다면, 다음처럼 진행한다.

    .. code:: bash

        uv tool upgrade loglab


**소스 코드로 설치**

최신 소스 코드를 기반으로 다음처럼 개발용으로 설치도 가능하다.

.. code:: bash

    git clone https://github.com/haje01/loglab
    cd loglab
    uv venv
    source .venv/bin/activate
    uv pip install -e .

설치가 잘 되었다면 로그랩의 커맨드라인 툴인 `loglab` 을 이용할 수 있다. 다음과 같이 입력해보자.

.. code:: bash

    $ loglab

    Usage: loglab [OPTIONS] COMMAND [ARGS]...

    LogLab 메인 CLI 그룹.

    LogLab의 모든 명령어들을 그룹화하는 메인 진입점.

    Options:
    -v, --verbose  디버깅 정보 출력 레벨 증가 (-v: INFO, -vv: DEBUG)
    --help         Show this message and exit.

    Commands:
    html     랩 파일로부터 HTML 문서를 생성.
    object   랩 파일로부터 로그 작성용 코드 객체를 생성.
    schema   랩 파일로부터 로그 검증용 JSON 스키마를 생성.
    show     랩 파일의 내용을 텍스트 형태로 출력.
    verify   실제 로그 파일이 스키마에 맞는지 검증.
    version  로그랩의 현재 버전을 표시.

.. code-block:: bash

    $ loglab
    Usage: loglab [OPTIONS] COMMAND [ARGS]...

    Options:
    -v, --verbose  디버깅 정보 출력 레벨 증가 (-v: INFO, -vv: DEBUG)
    --help         Show this message and exit.

    Commands:
    html     랩 파일로부터 HTML 문서를 생성.
    object   랩 파일로부터 로그 작성용 코드 객체를 생성.
    schema   랩 파일로부터 로그 검증용 JSON 스키마를 생성.
    show     랩 파일의 내용을 텍스트 형태로 출력.
    verify   실제 로그 파일이 스키마에 맞는지 검증.
    version  로그랩의 현재 버전을 표시.

위에서 알 수 있듯 `loglab` 에는 다양한 명령어가 있는데 예제를 통해 하나씩 살펴보도록 하겠다. 먼저 간단히 버전을 확인해보자.

.. code-block:: bash

    $ loglab version
    0.3.0
