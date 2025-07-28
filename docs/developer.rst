LogLab 개발자 참고
==================

여기에는 로그랩을 개발하는 사람들을 위한 설명을 기술한다. 일반 사용자는
읽지 않아도 문제 없을 것이다.

실행 파일 이용과 빌드
---------------------

로그랩 코드에서 직접 실행파일을 빌드하고 싶다면
`PyInstaller <http://www.pyinstaller.org>`__ 가 필요하다. PyInstaller
홈페이지를 참고하여 설치하자.

.. note::

   PyEnv를 사용하는 경우 빌드시 동적 라이브러리를 찾지 못해 에러가 나올
   수 있다. 이때는 macOS의 경우 ``--enable-framework`` 옵션으로 파이썬을
   빌드하여 설치해야 한다. 자세한 것은 `이
   글 <https://github.com/pyenv/pyenv/issues/443>`__ 을 참고하자.
   리눅스의 경우 ``--enable-shared`` 옵션으로 빌드한다.

윈도우에서 빌드는 로그랩이 별도 ``venv`` 없이 글로벌하게 설치된 것으로
전제한다. 설치 디렉토리에서 다음과 같이 한다.

::

   > tools\build.bat

리눅스/macOS 에서는 다음과 같이 빌드한다.

::

   $ sh tools/build.sh

정상적으로 빌드가 되면, ``dist/`` 디렉토리 아래 ``loglab.exe`` (윈도우)
또는 ``loglab`` (리눅스/macOS) 실행 파일이 만들어진다. 이것을 배포하면
되겠다.

테스트 실행
-----------

자동화된 개발 환경 설정 (권장)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

새로 개선된 자동화된 테스트 환경을 사용하려면:

.. code:: sh

   # 개발 환경 원클릭 설정 (의존성 설치 + pre-commit hooks 설정)
   make setup

   # 전체 테스트 및 품질 검사 실행 (포맷팅, 린팅, 테스트, 커버리지)
   make all

개별 테스트 명령어
~~~~~~~~~~~~~~~~~~

.. code:: sh

   # 기본 테스트 실행
   make test

   # 커버리지 포함 테스트
   make coverage

   # 코드 포맷팅 (black, isort)
   make format

   # 린팅 검사 (flake8)
   make lint

   # 보안 검사 (bandit, safety)
   make security

   # 다언어 코드 생성 테스트
   make test-python    # Python 코드 생성 테스트
   make test-csharp    # C# 코드 생성 테스트 (dotnet 필요)
   make test-cpp       # C++ 코드 생성 테스트 (g++ 필요)

   # 전체 코드 생성 테스트
   make test-codegen

기존 방식 (수동)
~~~~~~~~~~~~~~~~

다음처럼 개발을 위한 추가 의존 패키지를 설치하고,

.. code:: sh

   uv pip install -e ".[dev]"

``pytest`` 로 테스트를 수행한다.

.. code:: sh

   pytest tests/


로그 객체 테스트
-----------------------

여기서는 로그랩을 통해 성성된 언어별 로그 객체 코드를 테스트하는 방법을 설명한다.

Python 로그 객체 테스트
~~~~~~~~~~~~~~~~~~~~~~~~~

로그 객체를 위한 파이썬 파일을 생성하고

.. code:: sh

   loglab object example/foo.lab.json py -o tests/loglab_foo.py

``tests/`` 디렉토리로 가서 테스트를 실행한다.

.. code:: sh

   pytest test_log_objects_python.py

C# 로그 객체 테스트
~~~~~~~~~~~~~~~~~~~

C# 코드 실행을 위한 설치가 필요하다.

.. code:: sh

   sudo apt update
   sudo apt install -y wget apt-transport-https software-properties-common

   wget https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb
   sudo dpkg -i packages-microsoft-prod.deb
   sudo apt update

   sudo apt install -y dotnet-sdk-8.0

다음으로 로그 객체 파일을 생성하고

.. code:: sh

   loglab object example/foo.lab.json cs -o tests/cstest/loglab_foo.cs

``tests/cstest/`` 디렉토리로 이동 후 실행한다.

::

   dotnet run

.. _c-로그-객체-테스트-1:

C++ 로그 객체 테스트
~~~~~~~~~~~~~~~~~~~~~~~~~

테스트를 위해 먼저 ``gtest`` 를 설치가 필요하다.

.. code:: sh

   sudo apt install libgtest-dev

다음으로 로그 객체를 위한 헤더 파일을 생성하고

.. code:: sh

   loglab object example/foo.lab.json cpp -o tests/loglab_foo.h

``tests/`` 디렉토리로 가서 테스트 코드를 빌드하고

.. code:: sh

   g++ -std=c++17 -I. test_log_objects_cpp.cpp -lgtest -lgtest_main -lpthread -o test_log_objects_cpp

다음처럼 실행한다.

.. code:: sh

   ./test_log_objects_cpp

   Running main() from ./googletest/src/gtest_main.cc
   [==========] Running 2 tests from 1 test suite.
   [----------] Global test environment set-up.
   [----------] 2 tests from StringTest
   [ RUN      ] StringTest.Serialize
   [       OK ] StringTest.Serialize (0 ms)
   [ RUN      ] StringTest.SerializeAfterReset
   [       OK ] StringTest.SerializeAfterReset (0 ms)
   [----------] 2 tests from StringTest (0 ms total)

   [----------] Global test environment tear-down
   [==========] 2 tests from 1 test suite ran. (0 ms total)
   [  PASSED  ] 2 tests.

자동화된 테스트 및 CI/CD
------------------------

LogLab은 포괄적인 테스트 자동화 시스템을 갖추고 있다:

GitHub Actions CI/CD
~~~~~~~~~~~~~~~~~~~~

-  **자동 테스트**: 모든 push 및 pull request에서 자동 실행
-  **다중 Python 버전**: 3.9, 3.10, 3.11, 3.12 지원
-  **크로스 언어 테스트**: Python, C#, C++ 코드 생성 검증
-  **품질 검사**: 린팅, 보안 검사, 커버리지 리포팅

Pre-commit Hooks
~~~~~~~~~~~~~~~~~

개발 중 코드 품질을 자동으로 보장:

.. code:: sh

   # pre-commit hooks 설치 (make setup에 포함됨)
   pre-commit install

   # 모든 파일에 대해 수동 실행
   pre-commit run --all-files

의존성 자동 관리
~~~~~~~~~~~~~~~~

-  **Dependabot**: 주간 의존성 업데이트 자동 PR
-  **보안 업데이트**: 취약점 발견 시 자동 알림
-  **그룹화된 업데이트**: 개발/프로덕션 의존성 별도 관리

성능 및 통합 테스트
~~~~~~~~~~~~~~~~~~~

.. code:: sh

   # 성능 테스트 실행
   pytest tests/test_performance.py -v

   # 전체 통합 테스트
   pytest tests/test_integration.py -v

추가 문자열 현지화
------------------

개발이 진행됨에 따라 새로이 추가된 문자열들 중 현지화 대상인 것들은
다음처럼 처리한다.

``xgettext`` 가 설치되어 있지 않으면 다음처럼 설치 후,

::

   sudo apt install gettext

다국어 문자열을 출력하는 것은 ``util.py`` 에 정의된 함수를 이용하는 것이 관례이다. 다음 명령어로 새로 추가된 문자열을 추출한다.

.. code:: bash

   xgettext -o messages.pot util.py

이 ``messages.pot`` 파일에서 새로 추가된 텍스트를 참고하여 언어별
``.po`` 파일 (예: ``locales/en_US/LC_MESSAGES/messages.po``) 에 번역하여
추가한다.

이후 언어별로 다음처럼 ``.mo`` 파일로 컴파일한다.

.. code:: bash

   msgfmt locales/en_US/LC_MESSAGES/base.po -o locales/en_US/LC_MESSAGES/base.mo


버전 업데이트
----------------

일정 분량 이상의 새로운 기능이 추가되거나 버그가 수정되면 버전을 업데이트해야 한다. 업데이트는 다음과 같은 절차로 진행된다.

1. **변경 사항 기록**: `CHANGELOG.md` 파일에 변경 사항을 기록한다.
2. **버전 번호 업데이트**: ``version.py``, ``docs/conf.py`` 및 ``README.md`` 파일내 버전 번호를 업데이트한다.
3. **버전 태깅**: Git 에서 새로운 버전을 태깅하고 원격 저장소에도 ``push`` 한다.
