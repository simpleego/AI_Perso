# pip 명령어 정리

`pip`는 Python 패키지를 설치·삭제·조회·관리하는 명령어입니다.

## 1. 기본 형식

```bash
pip 명령어 [옵션] [패키지명]
```

Python 환경을 명확히 지정하려면 다음 형식을 권장합니다.

```bash
python -m pip 명령어
```

예:

```bash
python -m pip install pandas
```

---

## 2. 패키지 설치: `install`

패키지를 설치합니다.

```bash
pip install 패키지명
```

예:

```bash
pip install numpy
pip install pandas matplotlib
```

특정 버전 설치:

```bash
pip install numpy==2.1.0
```

최소 버전 지정:

```bash
pip install "numpy>=2.0"
```

버전 범위 지정:

```bash
pip install "numpy>=1.26,<3.0"
```

최신 버전으로 업그레이드:

```bash
pip install --upgrade numpy
```

`requirements.txt`에 있는 패키지를 한꺼번에 설치:

```bash
pip install -r requirements.txt
```

현재 프로젝트를 설치:

```bash
pip install .
```

개발 중인 프로젝트를 편집 가능 모드로 설치:

```bash
pip install -e .
```

캐시를 사용하지 않고 설치:

```bash
pip install --no-cache-dir 패키지명
```

---

## 3. 패키지 삭제: `uninstall`

설치된 패키지를 삭제합니다.

```bash
pip uninstall 패키지명
```

예:

```bash
pip uninstall numpy
```

확인 질문 없이 삭제:

```bash
pip uninstall -y numpy
```

여러 패키지 삭제:

```bash
pip uninstall -y numpy pandas matplotlib
```

---

## 4. 설치된 패키지 목록: `list`

현재 환경에 설치된 패키지와 버전을 출력합니다.

```bash
pip list
```

업데이트할 수 있는 패키지 확인:

```bash
pip list --outdated
```

최신 상태인 패키지 확인:

```bash
pip list --uptodate
```

---

## 5. 패키지 상세 정보: `show`

특정 패키지의 버전, 설치 위치, 의존성 등을 확인합니다.

```bash
pip show 패키지명
```

예:

```bash
pip show langchain
```

주요 출력 정보:

```text
Name
Version
Summary
Location
Requires
Required-by
```

여러 패키지 조회:

```bash
pip show numpy pandas
```

---

## 6. 설치 목록 저장: `freeze`

현재 설치된 패키지를 `requirements.txt` 형식으로 출력합니다.

```bash
pip freeze
```

파일로 저장:

```bash
pip freeze > requirements.txt
```

저장된 환경을 다른 컴퓨터에서 재설치:

```bash
pip install -r requirements.txt
```

`pip freeze` 결과 예:

```text
numpy==2.1.0
pandas==2.2.3
requests==2.32.3
```

### `pip list`와 `pip freeze` 차이

| 명령어          | 용도                        |
| ------------ | ------------------------- |
| `pip list`   | 사람이 보기 좋은 설치 목록           |
| `pip freeze` | `requirements.txt` 저장용 형식 |

---

## 7. 의존성 검사: `check`

설치된 패키지들의 의존성 충돌 여부를 검사합니다.

```bash
pip check
```

정상인 경우:

```text
No broken requirements found.
```

문제가 있는 경우:

```text
package-a requires package-b<2.0, but you have package-b 2.1
```

패키지를 여러 개 설치한 후 오류가 발생하면 먼저 실행해볼 수 있습니다.

---

## 8. Python 환경 검사: `inspect`

현재 Python 환경과 설치된 패키지 정보를 구조화된 형식으로 출력합니다.

```bash
pip inspect
```

결과는 주로 JSON 형식이며, 환경 분석이나 자동화 도구에서 활용됩니다.

파일로 저장:

```bash
pip inspect > environment.json
```

일반적인 패키지 확인에는 `pip list`, 상세 확인에는 `pip show`가 더 편리합니다.

---

## 9. 패키지 다운로드: `download`

패키지를 설치하지 않고 파일만 다운로드합니다.

```bash
pip download 패키지명
```

예:

```bash
pip download numpy
```

특정 폴더에 다운로드:

```bash
pip download numpy -d packages
```

`requirements.txt`에 있는 패키지 전체 다운로드:

```bash
pip download -r requirements.txt -d packages
```

다운로드한 파일로 오프라인 설치:

```bash
pip install --no-index --find-links=packages numpy
```

---

## 10. Wheel 파일 생성: `wheel`

패키지를 Wheel 배포 파일인 `.whl` 형식으로 빌드합니다.

```bash
pip wheel 패키지명
```

예:

```bash
pip wheel requests
```

저장 폴더 지정:

```bash
pip wheel requests -w wheels
```

`requirements.txt` 전체를 Wheel로 준비:

```bash
pip wheel -r requirements.txt -w wheels
```

오프라인 설치 환경이나 배포용 패키지를 준비할 때 사용합니다.

---

## 11. 패키지 해시 생성: `hash`

다운로드한 패키지 파일의 해시값을 계산합니다.

```bash
pip hash 파일명
```

예:

```bash
pip hash numpy-2.1.0-cp312-cp312-win_amd64.whl
```

출력 예:

```text
--hash=sha256:...
```

패키지 파일이 변조되지 않았는지 검증하거나, 보안이 강화된 `requirements.txt`를 만들 때 사용합니다.

---

## 12. 패키지 인덱스 정보: `index`

PyPI 같은 패키지 저장소에서 제공하는 버전 정보를 확인합니다.

```bash
pip index versions 패키지명
```

예:

```bash
pip index versions numpy
```

특정 패키지의 설치 가능한 버전 목록을 확인할 때 유용합니다.

---

## 13. 패키지 검색: `search`

PyPI에서 패키지를 검색하는 명령입니다.

```bash
pip search 검색어
```

예:

```bash
pip search langchain
```

다만 `pip search`는 PyPI 측 검색 API 제한으로 정상적으로 작동하지 않을 수 있습니다. 일반적으로는 PyPI 웹사이트에서 검색하거나 다음처럼 버전을 조회합니다.

```bash
pip index versions langchain
```

---

## 14. 캐시 관리: `cache`

pip가 다운로드한 패키지 캐시를 확인하고 삭제합니다.

캐시 위치 확인:

```bash
pip cache dir
```

캐시 정보 확인:

```bash
pip cache info
```

캐시 파일 목록:

```bash
pip cache list
```

특정 패키지 캐시 삭제:

```bash
pip cache remove numpy
```

전체 캐시 삭제:

```bash
pip cache purge
```

설치 문제가 반복되거나 캐시가 너무 커졌을 때 사용합니다.

---

## 15. 설정 관리: `config`

pip의 로컬 또는 전역 설정을 관리합니다.

설정 목록 확인:

```bash
pip config list
```

설정 파일과 값 확인:

```bash
pip config debug
```

기본 패키지 저장소 설정:

```bash
pip config set global.index-url https://pypi.org/simple
```

설정 삭제:

```bash
pip config unset global.index-url
```

일반 사용자는 자주 사용하지 않지만, 프록시나 사설 패키지 저장소를 사용할 때 필요합니다.

---

## 16. 디버그 정보: `debug`

Python, pip, 운영체제, 인증서, 호환 가능한 Wheel 태그 등의 정보를 출력합니다.

```bash
pip debug
```

자세한 정보:

```bash
pip debug --verbose
```

패키지 설치 시 다음과 같은 문제가 발생했을 때 유용합니다.

```text
No matching distribution found
Could not build wheels
Unsupported wheel
```

---

## 17. 자동완성 기능: `completion`

터미널에서 pip 명령어 자동완성을 설정할 때 사용합니다.

Bash 예:

```bash
pip completion --bash
```

PowerShell 예:

```powershell
pip completion --powershell
```

일반적인 패키지 관리 작업에서는 거의 사용하지 않습니다.

---

## 18. 도움말: `help`

전체 도움말:

```bash
pip help
```

특정 명령 도움말:

```bash
pip help install
```

다음 형식도 가능합니다.

```bash
pip install --help
pip uninstall --help
pip list --help
```

---

## 19. Lock 파일 생성: `lock`

프로젝트의 패키지 버전과 의존성을 고정한 Lock 파일을 생성합니다.

```bash
pip lock
```

입력 파일 지정 예:

```bash
pip lock -r requirements.txt
```

Lock 파일은 개발 환경, 테스트 환경, 배포 환경에서 동일한 패키지 버전을 설치하도록 돕습니다.

다만 사용하는 pip 버전에 따라 실험적 기능이거나 지원 방식이 달라질 수 있으므로 다음 명령으로 실제 옵션을 확인하는 것이 좋습니다.

```bash
pip lock --help
```

---

# 자주 사용하는 핵심 명령어

```bash
# pip 버전 확인
python -m pip --version

# pip 자체 업그레이드
python -m pip install --upgrade pip

# 패키지 설치
python -m pip install pandas

# 특정 버전 설치
python -m pip install pandas==2.2.3

# 패키지 업그레이드
python -m pip install --upgrade pandas

# 설치된 패키지 확인
python -m pip list

# 패키지 상세 정보
python -m pip show pandas

# 패키지 삭제
python -m pip uninstall pandas

# 의존성 충돌 확인
python -m pip check

# 설치 환경 저장
python -m pip freeze > requirements.txt

# 저장된 환경 복원
python -m pip install -r requirements.txt
```

# Colab과 Jupyter Notebook에서 사용

노트북 셀에서는 `%pip` 사용이 권장됩니다.

```python
%pip install pandas
```

여러 패키지 설치:

```python
%pip install langchain langchain-openai python-dotenv
```

업그레이드:

```python
%pip install --upgrade langchain
```

`!pip install`도 가능하지만, 현재 노트북 커널의 Python 환경과 다른 환경에 설치될 수 있으므로 `%pip`가 더 안전합니다.

# Windows 가상환경에서 권장 순서

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
venv\Scripts\activate

# pip 업그레이드
python -m pip install --upgrade pip

# 패키지 설치
python -m pip install numpy pandas matplotlib

# 설치 결과 저장
python -m pip freeze > requirements.txt

# 의존성 검사
python -m pip check
```

가장 중요한 명령은 `install`, `uninstall`, `list`, `show`, `freeze`, `check` 여섯 가지입니다.
