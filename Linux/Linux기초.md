# Google Colab 터미널로 배우는 리눅스 기초 실습

## 1. 수업 개요

### 수업 시간

총 4시간

* 1교시: 리눅스 이해와 시스템 탐색
* 2교시: 파일과 디렉터리 관리
* 3교시: 텍스트 검색과 파이프라인
* 4교시: 권한, 프로세스, 셸 스크립트
* 각 교시 50분, 휴식 10분 기준

### 실습 환경

* Google Colab
* Ubuntu Linux 기반 런타임
* 별도의 리눅스 설치 없이 웹 브라우저에서 실습
* 명령어는 Colab 코드 셀에서 실행

### 학습 목표

수업을 마치면 다음 작업을 수행할 수 있다.

1. 리눅스 운영체제의 특징을 설명할 수 있다.
2. 현재 위치와 디렉터리 구조를 확인할 수 있다.
3. 파일과 폴더를 생성, 복사, 이동, 삭제할 수 있다.
4. 파일 내용을 검색하고 필요한 데이터만 추출할 수 있다.
5. 파이프와 리다이렉션을 사용할 수 있다.
6. 리눅스 파일 권한을 이해하고 변경할 수 있다.
7. 간단한 Bash 셸 스크립트를 작성하고 실행할 수 있다.

---

# 2. Colab에서 리눅스 명령어 실행하기

## 2.1 `!` 기호 사용

Colab에서 리눅스 명령어를 실행할 때는 명령어 앞에 `!`를 붙인다.

```bash
!pwd
```

```bash
!ls
```

```bash
!date
```

## 2.2 여러 명령어 실행

한 셀에서 여러 리눅스 명령어를 실행하려면 `%%bash`를 사용한다.

```bash
%%bash

echo "첫 번째 명령어"
pwd
ls
```

`%%bash`는 반드시 셀의 첫 번째 줄에 작성한다.

## 2.3 디렉터리 이동

다음 명령은 실행되지만 다른 셀에는 이동 결과가 유지되지 않을 수 있다.

```bash
!cd /content
```

Colab에서 작업 디렉터리를 지속적으로 변경하려면 `%cd`를 사용하는 것이 좋다.

```bash
%cd /content
```

현재 위치 확인:

```bash
!pwd
```

---

# 3. Colab 리눅스 환경의 특징

Google Colab은 일반적으로 Ubuntu Linux 기반의 임시 가상환경을 제공한다.

## 주요 특징

### 1. 대소문자를 구분한다

리눅스에서는 다음 두 파일을 서로 다른 파일로 처리한다.

```text
Linux.txt
linux.txt
```

### 2. 디렉터리가 계층 구조로 구성된다

리눅스의 최상위 디렉터리는 `/`이다.

```text
/
├── bin
├── content
├── dev
├── etc
├── home
├── proc
├── tmp
├── usr
└── var
```

### 3. 대부분의 자원을 파일처럼 다룬다

리눅스에서는 일반 파일뿐만 아니라 시스템 정보, 장치, 프로세스 정보도 파일 형태로 접근한다.

예:

```text
/proc/cpuinfo
/proc/meminfo
/dev/null
```

### 4. 여러 명령어를 연결할 수 있다

파이프 `|`를 사용하여 한 명령의 결과를 다른 명령의 입력으로 전달할 수 있다.

```bash
!ls -al | head
!ls -al | tail
!ls -al | more
```

### 5. 다중 사용자와 권한 체계를 지원한다

파일마다 소유자와 읽기, 쓰기, 실행 권한이 존재한다.

```bash
!ls -l
```

### 6. 프로세스 단위로 프로그램을 관리한다

실행 중인 프로그램은 프로세스로 관리되며 각각 PID라는 번호를 가진다.

```bash
!ps
```

### 7. 오픈소스 생태계를 기반으로 한다

Ubuntu, Debian, Rocky Linux 등 다양한 배포판이 존재하며 서버, 클라우드, AI 개발환경에서 폭넓게 사용된다.

---

# 1교시: 리눅스 이해와 시스템 탐색

## 수업 목표

* Colab의 운영체제 정보를 확인한다.
* 사용자와 시스템 정보를 확인한다.
* 절대 경로와 상대 경로를 구분한다.
* 리눅스 디렉터리 구조를 탐색한다.

---

## 1-1. 운영체제 정보 확인

### 커널 정보 확인

```bash
!uname -a
```

주요 출력 내용:

* Linux: 운영체제 커널
* x86_64: CPU 아키텍처
* Ubuntu: 기반 운영체제 정보

간단히 커널 이름만 확인한다.

```bash
!uname
```

커널 버전 확인:

```bash
!uname -r
```

### 리눅스 배포판 확인

```bash
!cat /etc/os-release
```

확인할 내용:

```text
NAME
VERSION
ID
VERSION_ID
```

### 실습 문제

다음 명령어를 실행하고 결과를 기록한다.

```bash
!uname -r
!cat /etc/os-release
!python --version
```

질문:

1. Colab은 어떤 리눅스 배포판을 사용하는가?
2. 현재 Linux 커널 버전은 무엇인가?
3. 현재 Python 버전은 무엇인가?

---

## 1-2. 사용자 정보 확인

현재 사용자를 확인한다.

```bash
!whoami
```

사용자 ID와 그룹을 확인한다.

```bash
!id
```

Colab에서는 일반적으로 `root` 사용자로 실행될 수 있다. 실제 결과는 `whoami` 명령으로 확인해야 한다.

### 일반 리눅스와 Colab의 차이

일반 리눅스 서버에서는 다음처럼 일반 사용자 계정을 사용하는 경우가 많다.

```text
ubuntu
student
developer
```

Colab에서는 높은 권한을 가진 사용자로 동작하는 경우가 많지만, 실행환경은 임시로 제공된다.

---

## 1-3. 현재 시간과 시스템 정보

현재 날짜와 시간을 확인한다.

```bash
!date
```

CPU 개수 확인:

```bash
!nproc
```

CPU 정보 일부 확인:

```bash
!lscpu | head
```

메모리 정보 확인:

```bash
!free -h
```

디스크 사용량 확인:

```bash
!df -h
```

명령어 옵션에서 `-h`는 사람이 읽기 쉬운 단위로 출력한다는 의미이다.

```text
K: KB
M: MB
G: GB
```

---

## 1-4. 현재 위치 확인

현재 작업 중인 디렉터리를 확인한다.

```bash
!pwd
```

`pwd`는 다음 단어의 약자이다.

```text
Print Working Directory
```

Colab의 기본 작업 디렉터리는 일반적으로 다음과 같다.

```text
/content
```

---

## 1-5. 디렉터리 목록 확인

현재 위치의 파일과 폴더를 확인한다.

```bash
!ls
```

자세히 확인:

```bash
!ls -l
```

숨김 파일까지 확인:

```bash
!ls -al
```

파일 크기를 읽기 쉬운 형식으로 표시:

```bash
!ls -alh
```

### 주요 옵션

| 옵션   | 의미                  |
| ---- | ------------------- |
| `-l` | 자세한 정보 표시           |
| `-a` | 숨김 파일 포함            |
| `-h` | 파일 크기를 읽기 쉬운 단위로 표시 |
| `-t` | 수정 시간 순으로 정렬        |
| `-r` | 역순 정렬               |

최근 수정된 파일부터 확인:

```bash
!ls -lt
```

---

## 1-6. 루트 디렉터리 탐색

리눅스 최상위 디렉터리를 확인한다.

```bash
!ls /
```

주요 디렉터리:

| 디렉터리       | 역할            |
| ---------- | ------------- |
| `/`        | 최상위 디렉터리      |
| `/content` | Colab 작업 공간   |
| `/home`    | 일반 사용자 홈 디렉터리 |
| `/etc`     | 시스템 설정 파일     |
| `/usr`     | 프로그램과 라이브러리   |
| `/var`     | 로그와 변경되는 데이터  |
| `/tmp`     | 임시 파일         |
| `/proc`    | 프로세스와 시스템 정보  |
| `/dev`     | 장치 파일         |

CPU 정보 파일 확인:

```bash
!head -n 10 /proc/cpuinfo
```

메모리 정보 확인:

```bash
!head -n 10 /proc/meminfo
```

이 실습은 리눅스의 핵심 특징인 “시스템 정보도 파일 형태로 접근할 수 있다”는 점을 보여준다.

---

## 1-7. 절대 경로와 상대 경로

### 절대 경로

최상위 디렉터리 `/`부터 시작하는 전체 경로이다.

```text
/content/linux_lab/data
```

### 상대 경로

현재 디렉터리를 기준으로 표시한다.

```text
data
./data
../data
```

경로 기호:

| 기호   | 의미         |
| ---- | ---------- |
| `/`  | 최상위 디렉터리   |
| `.`  | 현재 디렉터리    |
| `..` | 상위 디렉터리    |
| `~`  | 사용자 홈 디렉터리 |

홈 디렉터리 확인:

```bash
!echo $HOME
```

---

## 1교시 확인 문제

1. 현재 작업 디렉터리를 확인하는 명령어는 무엇인가?
2. 숨김 파일을 포함하여 목록을 확인하는 명령어는 무엇인가?
3. `/`는 무엇을 의미하는가?
4. `.`과 `..`의 차이는 무엇인가?
5. 현재 사용자를 확인하는 명령어는 무엇인가?
6. 리눅스가 파일 이름의 대소문자를 구분하는 이유를 실습으로 확인해 보자.

### 대소문자 구분 실습

```bash
%%bash

cd /content
touch Linux.txt
touch linux.txt
ls -l Linux.txt linux.txt
```

실습 후 삭제:

```bash
!rm -f /content/Linux.txt /content/linux.txt
```

---

# 2교시: 파일과 디렉터리 관리

## 수업 목표

* 실습 디렉터리를 구성한다.
* 파일과 폴더를 생성한다.
* 파일을 복사, 이동, 삭제한다.
* 파일 내용을 확인하고 수정한다.
* 와일드카드를 사용할 수 있다.

---

## 2-1. 실습 폴더 준비

기존 실습 폴더가 있으면 삭제하고 새로 생성한다.

```bash
!rm -rf /content/linux_lab
```

> `rm -rf`는 휴지통을 거치지 않고 삭제하므로 실제 서버에서는 매우 주의해서 사용해야 한다.

실습 폴더 생성:

```bash
!mkdir -p /content/linux_lab
```

작업 디렉터리 이동:

```bash
%cd /content/linux_lab
```

현재 위치 확인:

```bash
!pwd
```

---

## 2-2. 디렉터리 생성

하나의 디렉터리 생성:

```bash
!mkdir docs
```

여러 디렉터리 생성:

```bash
!mkdir data logs scripts backup
```

하위 디렉터리까지 한 번에 생성:

```bash
!mkdir -p project/src/python
```

전체 디렉터리 확인:

```bash
!find . -maxdepth 3 -type d
```

`mkdir -p`는 상위 디렉터리가 없으면 함께 생성한다.

---

## 2-3. 빈 파일 생성

빈 파일 생성:

```bash
!touch docs/readme.txt
```

여러 파일 생성:

```bash
!touch data/file1.txt data/file2.txt data/file3.txt
```

파일 확인:

```bash
!ls -l docs data
```

`touch`는 파일이 없으면 새 파일을 만들고, 파일이 있으면 수정 시간을 갱신한다.

---

## 2-4. 파일에 내용 저장

`echo` 명령으로 문자열을 출력한다.

```bash
!echo "Hello Linux"
```

출력 결과를 파일에 저장한다.

```bash
!echo "Hello Linux" > docs/readme.txt
```

파일 내용 확인:

```bash
!cat docs/readme.txt
```

내용 추가:

```bash
!echo "Google Colab Linux Practice" >> docs/readme.txt
```

다시 확인:

```bash
!cat docs/readme.txt
```

### `>`와 `>>` 차이

| 기호   | 기능               |
| ---- | ---------------- |
| `>`  | 기존 내용을 지우고 새로 저장 |
| `>>` | 기존 내용의 마지막에 추가   |

다음 명령을 실행하여 차이를 확인한다.

```bash
%%bash

cd /content/linux_lab

echo "첫 번째 내용" > docs/test.txt
echo "두 번째 내용" > docs/test.txt
cat docs/test.txt
```

결과에는 `두 번째 내용`만 남는다.

```bash
%%bash

cd /content/linux_lab

echo "첫 번째 내용" > docs/test.txt
echo "두 번째 내용" >> docs/test.txt
cat docs/test.txt
```

결과에는 두 줄이 모두 남는다.

---

## 2-5. 여러 줄 파일 만들기

다음과 같이 여러 줄의 파일을 만들 수 있다.

```bash
%%bash

cd /content/linux_lab

cat > data/students.csv <<'EOF'
name,team,score
kim,A,85
lee,B,92
park,A,78
choi,B,95
jung,A,88
han,C,72
EOF
```

내용 확인:

```bash
!cat data/students.csv
```

---

## 2-6. 파일 내용 확인 명령어

전체 내용 확인:

```bash
!cat data/students.csv
```

처음 3줄 확인:

```bash
!head -n 3 data/students.csv
```

마지막 3줄 확인:

```bash
!tail -n 3 data/students.csv
```

파일의 줄 수 확인:

```bash
!wc -l data/students.csv
```

단어 수와 문자 수까지 확인:

```bash
!wc data/students.csv
```

### 주요 명령어

| 명령어     | 기능          |
| ------- | ----------- |
| `cat`   | 전체 내용 출력    |
| `head`  | 앞부분 출력      |
| `tail`  | 뒷부분 출력      |
| `wc -l` | 줄 수 계산      |
| `file`  | 파일 형식 확인    |
| `stat`  | 파일 상세 정보 확인 |

파일 형식 확인:

```bash
!file data/students.csv
```

파일 상세 정보:

```bash
!stat data/students.csv
```

---

## 2-7. 파일 복사

파일 복사:

```bash
!cp docs/readme.txt backup/readme_copy.txt
```

확인:

```bash
!ls -l backup
```

디렉터리 전체 복사:

```bash
!cp -r docs backup/docs_copy
```

확인:

```bash
!find backup -maxdepth 2
```

---

## 2-8. 파일 이동과 이름 변경

파일 이동:

```bash
!mv data/file1.txt backup/
```

파일 이름 변경:

```bash
!mv data/file2.txt data/sample.txt
```

확인:

```bash
!find . -maxdepth 2 -type f
```

리눅스에서 `mv`는 파일 이동과 이름 변경에 모두 사용한다.

---

## 2-9. 파일과 디렉터리 삭제

파일 삭제:

```bash
!rm data/file3.txt
```

빈 디렉터리 삭제:

```bash
!mkdir empty_dir
!rmdir empty_dir
```

내용이 있는 디렉터리 삭제:

```bash
!rm -r backup/docs_copy
```

강제 삭제:

```bash
!rm -rf 삭제할_디렉터리
```

### 주의

리눅스의 `rm` 명령은 일반적으로 휴지통을 사용하지 않는다.

다음과 같은 명령은 매우 위험하다.

```bash
rm -rf /
```

```bash
rm -rf /*
```

실습 환경에서도 경로를 정확히 확인한 후 삭제한다.

```bash
!pwd
!ls
```

---

## 2-10. 와일드카드

여러 파일 생성:

```bash
!touch data/report_{01..05}.txt
```

확인:

```bash
!ls data
```

### `*` 사용

`.txt`로 끝나는 모든 파일:

```bash
!ls data/*.txt
```

### `?` 사용

문자 하나를 의미한다.

```bash
!ls data/report_0?.txt
```

### 대괄호 사용

지정된 문자 중 하나를 의미한다.

```bash
!ls data/report_0[1-3].txt
```

---

## 2교시 실습 과제

다음 구조를 명령어로 만든다.

```text
linux_lab
├── assignment
│   ├── input
│   ├── output
│   └── source
└── backup
```

조건:

1. `assignment` 아래에 `input`, `output`, `source`를 생성한다.
2. `input`에 `data1.txt`, `data2.txt`, `data3.txt`를 생성한다.
3. `data1.txt`에 `Linux 기본 실습`을 저장한다.
4. `data1.txt`를 `output/result.txt`로 복사한다.
5. `data2.txt`의 이름을 `sample.txt`로 변경한다.
6. 생성된 전체 파일 목록을 출력한다.

### 정답 예시

```bash
%%bash

cd /content/linux_lab

mkdir -p assignment/{input,output,source}

touch assignment/input/data1.txt
touch assignment/input/data2.txt
touch assignment/input/data3.txt

echo "Linux 기본 실습" > assignment/input/data1.txt

cp assignment/input/data1.txt assignment/output/result.txt

mv assignment/input/data2.txt assignment/input/sample.txt

find assignment -type f
```

---

# 3교시: 텍스트 검색과 파이프라인

## 수업 목표

* 파일에서 특정 문자열을 검색한다.
* 데이터의 일부 열을 추출한다.
* 정렬과 중복 제거를 수행한다.
* 파이프로 명령어를 연결한다.
* 파일을 조건에 따라 검색한다.

---

## 3-1. 파이프의 개념

파이프 기호는 다음과 같다.

```text
|
```

왼쪽 명령의 출력 결과를 오른쪽 명령의 입력으로 전달한다.

```bash
!명령어1 | 명령어2
```

예:

```bash
!ls -al | head -n 5
```

처리 과정:

```text
ls -al의 결과
      ↓
head 명령에 전달
      ↓
처음 5줄만 출력
```

리눅스는 작고 단순한 명령어를 파이프로 연결하여 복잡한 작업을 수행하는 특징이 있다.

---

## 3-2. 문자열 검색: grep

학생 데이터에서 `kim` 검색:

```bash
!grep "kim" data/students.csv
```

팀 A 검색:

```bash
!grep ",A," data/students.csv
```

대소문자 구분 없이 검색:

```bash
!grep -i "KIM" data/students.csv
```

줄 번호 포함:

```bash
!grep -n "A" data/students.csv
```

일치하지 않는 행 출력:

```bash
!grep -v ",A," data/students.csv
```

### 주요 옵션

| 옵션   | 의미           |
| ---- | ------------ |
| `-i` | 대소문자 무시      |
| `-n` | 줄 번호 표시      |
| `-v` | 일치하지 않는 행 표시 |
| `-c` | 일치하는 행 개수    |
| `-r` | 하위 디렉터리까지 검색 |

팀 A 학생 수:

```bash
!grep -c ",A," data/students.csv
```

---

## 3-3. 열 추출: cut

CSV 파일에서 첫 번째 열 추출:

```bash
!cut -d',' -f1 data/students.csv
```

두 번째 열 추출:

```bash
!cut -d',' -f2 data/students.csv
```

이름과 점수 추출:

```bash
!cut -d',' -f1,3 data/students.csv
```

옵션 의미:

```text
-d',' : 구분자를 쉼표로 설정
-f1   : 첫 번째 필드 선택
```

---

## 3-4. 정렬: sort

학생 점수 데이터 확인:

```bash
!cut -d',' -f3 data/students.csv
```

문자열 기준 정렬:

```bash
!cut -d',' -f3 data/students.csv | sort
```

숫자 기준 정렬:

```bash
!tail -n +2 data/students.csv | cut -d',' -f3 | sort -n
```

내림차순 정렬:

```bash
!tail -n +2 data/students.csv | cut -d',' -f3 | sort -nr
```

옵션:

| 옵션   | 의미         |
| ---- | ---------- |
| `-n` | 숫자로 정렬     |
| `-r` | 역순 정렬      |
| `-u` | 중복 제거 후 정렬 |

---

## 3-5. 중복 계산: uniq

팀 정보 추출:

```bash
!tail -n +2 data/students.csv | cut -d',' -f2
```

팀 종류 확인:

```bash
!tail -n +2 data/students.csv | cut -d',' -f2 | sort | uniq
```

팀별 인원 계산:

```bash
!tail -n +2 data/students.csv | cut -d',' -f2 | sort | uniq -c
```

`uniq`는 연속된 중복 항목을 처리하므로 일반적으로 먼저 `sort`를 사용한다.

---

## 3-6. 줄 수 계산: wc

전체 줄 수:

```bash
!wc -l data/students.csv
```

제목 행을 제외한 학생 수:

```bash
!tail -n +2 data/students.csv | wc -l
```

팀 A 학생 수:

```bash
!grep ",A," data/students.csv | wc -l
```

---

## 3-7. awk를 이용한 데이터 처리

`awk`는 열 단위 텍스트 처리에 적합한 명령어다.

이름만 출력:

```bash
!awk -F',' 'NR > 1 {print $1}' data/students.csv
```

이름과 점수 출력:

```bash
!awk -F',' 'NR > 1 {print $1, $3}' data/students.csv
```

80점 이상 학생 출력:

```bash
!awk -F',' 'NR > 1 && $3 >= 80 {print $1, $3}' data/students.csv
```

전체 평균 계산:

```bash
!awk -F',' 'NR > 1 {sum += $3; count++} END {print "평균:", sum/count}' data/students.csv
```

팀 A 평균:

```bash
!awk -F',' 'NR > 1 && $2 == "A" {sum += $3; count++} END {print "A팀 평균:", sum/count}' data/students.csv
```

---

## 3-8. 파일 검색: find

현재 디렉터리 아래의 모든 파일 검색:

```bash
!find . -type f
```

모든 디렉터리 검색:

```bash
!find . -type d
```

`.txt` 파일 검색:

```bash
!find . -name "*.txt"
```

`report`로 시작하는 파일 검색:

```bash
!find . -name "report*"
```

파일 크기가 0인 빈 파일 검색:

```bash
!find . -type f -empty
```

특정 디렉터리 깊이까지만 검색:

```bash
!find . -maxdepth 2 -type f
```

---

## 3-9. 리다이렉션과 파이프 결합

`.txt` 파일 목록을 저장한다.

```bash
!find . -name "*.txt" > txt_file_list.txt
```

내용 확인:

```bash
!cat txt_file_list.txt
```

팀 A 학생을 파일로 저장:

```bash
!grep ",A," data/students.csv > data/team_a.csv
```

80점 이상 학생 저장:

```bash
!awk -F',' 'NR > 1 && $3 >= 80 {print $0}' data/students.csv > data/high_score.csv
```

결과 확인:

```bash
!cat data/high_score.csv
```

---

## 3-10. tee 명령

`tee`는 결과를 화면에 출력하면서 파일에도 저장한다.

```bash
!grep ",A," data/students.csv | tee data/team_a_result.txt
```

결과는 화면에도 출력되고 파일에도 저장된다.

---

## 3교시 종합 실습

다음 로그 파일을 생성한다.

```bash
%%bash

cd /content/linux_lab

cat > logs/app.log <<'EOF'
2026-07-18 09:00:01 INFO login user=kim
2026-07-18 09:02:10 INFO search user=lee
2026-07-18 09:03:20 WARNING slow_response user=park
2026-07-18 09:05:11 ERROR database_timeout user=lee
2026-07-18 09:06:30 INFO logout user=kim
2026-07-18 09:08:42 ERROR invalid_token user=choi
2026-07-18 09:10:03 WARNING high_memory user=park
2026-07-18 09:12:17 ERROR database_timeout user=han
EOF
```

### 문제 1

전체 로그 줄 수를 구한다.

```bash
!wc -l logs/app.log
```

### 문제 2

`ERROR` 로그만 출력한다.

```bash
!grep "ERROR" logs/app.log
```

### 문제 3

오류 발생 횟수를 계산한다.

```bash
!grep -c "ERROR" logs/app.log
```

### 문제 4

오류 종류만 추출한다.

```bash
!awk '$3 == "ERROR" {print $4}' logs/app.log
```

### 문제 5

오류 종류별 발생 횟수를 계산한다.

```bash
!awk '$3 == "ERROR" {print $4}' logs/app.log | sort | uniq -c
```

예상 결과:

```text
2 database_timeout
1 invalid_token
```

### 문제 6

오류 로그를 별도의 파일로 저장한다.

```bash
!grep "ERROR" logs/app.log > logs/error.log
```

### 문제 7

화면 출력과 파일 저장을 동시에 수행한다.

```bash
!grep "WARNING" logs/app.log | tee logs/warning.log
```

---

## 3교시 확인 문제

1. 파이프 `|`의 역할은 무엇인가?
2. 특정 문자열을 검색하는 명령어는 무엇인가?
3. 숫자 기준 내림차순 정렬 명령은 무엇인가?
4. 파일 목록을 검색하는 명령어는 무엇인가?
5. `>`와 `>>`의 차이는 무엇인가?
6. `tee` 명령은 어떤 상황에서 유용한가?

---

# 4교시: 권한, 프로세스, 셸 스크립트

## 수업 목표

* 파일 권한 표시 방법을 이해한다.
* 실행 권한을 추가할 수 있다.
* 실행 중인 프로세스를 확인할 수 있다.
* 간단한 Bash 스크립트를 작성할 수 있다.
* 실습 결과를 압축 파일로 백업할 수 있다.

---

## 4-1. 파일 권한 확인

파일 상세 정보 확인:

```bash
!ls -l docs/readme.txt
```

출력 예:

```text
-rw-r--r-- 1 root root 42 Jul 18 09:30 readme.txt
```

권한 부분:

```text
-rw-r--r--
```

구조:

```text
- | rw- | r-- | r--
    사용자  그룹  기타 사용자
```

첫 번째 문자:

| 문자  | 의미     |
| --- | ------ |
| `-` | 일반 파일  |
| `d` | 디렉터리   |
| `l` | 심볼릭 링크 |

권한 문자:

| 문자  | 의미       |
| --- | -------- |
| `r` | 읽기       |
| `w` | 쓰기       |
| `x` | 실행       |
| `-` | 해당 권한 없음 |

---

## 4-2. 권한의 숫자 표현

각 권한에는 숫자가 대응된다.

| 권한     | 숫자 |
| ------ | -: |
| 읽기 `r` |  4 |
| 쓰기 `w` |  2 |
| 실행 `x` |  1 |

권한 조합:

| 숫자 | 권한    |
| -: | ----- |
|  7 | `rwx` |
|  6 | `rw-` |
|  5 | `r-x` |
|  4 | `r--` |
|  0 | `---` |

예:

```text
755 = rwxr-xr-x
644 = rw-r--r--
700 = rwx------
```

---

## 4-3. 실행 스크립트 생성

스크립트 파일을 만든다.

```bash
%%bash

cd /content/linux_lab

cat > scripts/hello.sh <<'EOF'
#!/bin/bash

echo "안녕하세요."
echo "리눅스 셸 스크립트 실습입니다."
echo "현재 시간: $(date)"
echo "현재 위치: $(pwd)"
echo "현재 사용자: $(whoami)"
EOF
```

파일 확인:

```bash
!cat scripts/hello.sh
```

권한 확인:

```bash
!ls -l scripts/hello.sh
```

직접 실행을 시도한다.

```bash
!./scripts/hello.sh
```

실행 권한이 없으면 다음과 같은 오류가 발생할 수 있다.

```text
Permission denied
```

실행 권한 추가:

```bash
!chmod u+x scripts/hello.sh
```

다시 확인:

```bash
!ls -l scripts/hello.sh
```

스크립트 실행:

```bash
!./scripts/hello.sh
```

---

## 4-4. chmod 사용법

사용자에게 실행 권한 추가:

```bash
!chmod u+x scripts/hello.sh
```

모든 사용자에게 실행 권한 추가:

```bash
!chmod a+x scripts/hello.sh
```

숫자로 권한 지정:

```bash
!chmod 755 scripts/hello.sh
```

일반 문서 권한 설정:

```bash
!chmod 644 docs/readme.txt
```

권한 확인:

```bash
!ls -l scripts/hello.sh docs/readme.txt
```

---

## 4-5. 프로세스 확인

현재 셸의 프로세스 확인:

```bash
!ps
```

전체 프로세스 확인:

```bash
!ps aux | head
```

Python 관련 프로세스 검색:

```bash
!ps aux | grep python
```

CPU 사용량이 높은 순으로 일부 확인:

```bash
!ps aux --sort=-%cpu | head
```

메모리 사용량이 높은 순으로 확인:

```bash
!ps aux --sort=-%mem | head
```

시스템 상태를 한 번만 출력:

```bash
!top -b -n 1 | head -n 15
```

Colab에서는 대화형 `top`보다 `top -b -n 1` 방식이 실습에 적합하다.

---

## 4-6. 백그라운드 프로세스와 종료

다음 실습은 `sleep` 프로세스를 백그라운드로 실행한 후 종료한다.

```bash
%%bash

sleep 30 &

PID=$!

echo "실행된 프로세스 PID: $PID"

ps -p $PID

kill $PID

echo "프로세스를 종료했습니다."
```

핵심 기호:

| 기호         | 의미                  |
| ---------- | ------------------- |
| `&`        | 백그라운드 실행            |
| `$!`       | 마지막 백그라운드 프로세스의 PID |
| `kill PID` | 해당 프로세스 종료          |

---

## 4-7. 종료 상태 확인

정상 명령 실행:

```bash
%%bash

ls /content

echo "종료 코드: $?"
```

실패하는 명령 실행:

```bash
%%bash

ls /존재하지_않는_디렉터리

echo "종료 코드: $?"
```

일반적으로:

```text
0: 정상 종료
0 이외: 오류 발생
```

셸 스크립트와 자동화에서는 종료 코드가 매우 중요하다.

---

## 4-8. Bash 변수

변수 생성:

```bash
%%bash

course="Linux Basic"

echo "$course"
```

숫자 변수:

```bash
%%bash

student_count=20

echo "학생 수: $student_count"
```

명령어 결과를 변수에 저장:

```bash
%%bash

today=$(date +%Y-%m-%d)

echo "오늘 날짜: $today"
```

---

## 4-9. 반복문

여러 파일을 반복해서 출력한다.

```bash
%%bash

cd /content/linux_lab

for file in data/*.txt
do
    echo "파일명: $file"
done
```

숫자 반복:

```bash
%%bash

for number in 1 2 3 4 5
do
    echo "현재 숫자: $number"
done
```

범위 사용:

```bash
%%bash

for number in {1..5}
do
    echo "실습 번호: $number"
done
```

---

## 4-10. 조건문

파일 존재 여부 확인:

```bash
%%bash

cd /content/linux_lab

file="data/students.csv"

if [ -f "$file" ]
then
    echo "$file 파일이 존재합니다."
else
    echo "$file 파일이 없습니다."
fi
```

디렉터리 존재 여부 확인:

```bash
%%bash

cd /content/linux_lab

if [ -d "logs" ]
then
    echo "logs 디렉터리가 존재합니다."
else
    echo "logs 디렉터리가 없습니다."
fi
```

---

# 5. 최종 종합 실습: 로그 분석 자동화 스크립트

## 실습 목표

앞에서 학습한 다음 기능을 하나의 스크립트로 구성한다.

* 변수
* 날짜 명령어
* 디렉터리 생성
* grep
* awk
* sort
* uniq
* wc
* 리다이렉션
* 파일 권한
* 압축

---

## 5-1. 보고서 디렉터리 생성

```bash
!mkdir -p /content/linux_lab/reports
```

---

## 5-2. 로그 분석 스크립트 작성

```bash
%%bash

cd /content/linux_lab

cat > scripts/analyze_log.sh <<'EOF'
#!/bin/bash

LOG_FILE="logs/app.log"
REPORT_DIR="reports"
TODAY=$(date +%Y-%m-%d_%H-%M-%S)

if [ ! -f "$LOG_FILE" ]
then
    echo "[ERROR] 로그 파일이 존재하지 않습니다."
    exit 1
fi

mkdir -p "$REPORT_DIR"

TOTAL_COUNT=$(wc -l < "$LOG_FILE")
ERROR_COUNT=$(grep -c "ERROR" "$LOG_FILE")
WARNING_COUNT=$(grep -c "WARNING" "$LOG_FILE")

REPORT_FILE="$REPORT_DIR/report_$TODAY.txt"

{
    echo "리눅스 로그 분석 보고서"
    echo "생성 시간: $(date)"
    echo "분석 파일: $LOG_FILE"
    echo "--------------------------------"
    echo "전체 로그 수: $TOTAL_COUNT"
    echo "ERROR 수: $ERROR_COUNT"
    echo "WARNING 수: $WARNING_COUNT"
    echo
    echo "[오류 종류별 발생 횟수]"
    awk '$3 == "ERROR" {print $4}' "$LOG_FILE" | sort | uniq -c
    echo
    echo "[ERROR 상세 내용]"
    grep "ERROR" "$LOG_FILE"
} > "$REPORT_FILE"

echo "[OK] 분석 보고서가 생성되었습니다."
echo "$REPORT_FILE"
EOF
```

---

## 5-3. 실행 권한 추가

```bash
!chmod 755 scripts/analyze_log.sh
```

권한 확인:

```bash
!ls -l scripts/analyze_log.sh
```

---

## 5-4. 스크립트 실행

```bash
!./scripts/analyze_log.sh
```

생성된 보고서 확인:

```bash
!ls -l reports
```

보고서 내용 확인:

```bash
!cat reports/report_*.txt
```

---

## 5-5. 전체 실습 결과 압축

`tar` 명령으로 실습 폴더를 압축한다.

```bash
%cd /content
```

```bash
!tar -czf linux_lab_backup.tar.gz linux_lab
```

압축 파일 확인:

```bash
!ls -lh linux_lab_backup.tar.gz
```

압축 파일 내부 목록 확인:

```bash
!tar -tzf linux_lab_backup.tar.gz | head -n 20
```

압축 옵션:

| 옵션  | 의미             |
| --- | -------------- |
| `c` | 새로운 압축 파일 생성   |
| `z` | gzip 방식 사용     |
| `f` | 압축 파일 이름 지정    |
| `t` | 압축 파일 내부 목록 확인 |
| `x` | 압축 해제          |

압축 해제 예:

```bash
!mkdir -p /content/restore_test
!tar -xzf /content/linux_lab_backup.tar.gz -C /content/restore_test
```

확인:

```bash
!find /content/restore_test -maxdepth 3
```

---

# 6. 최종 평가 문제

## 문제 1

현재 작업 디렉터리를 확인하는 명령어를 작성하시오.

```text
정답: pwd
```

## 문제 2

숨김 파일을 포함하여 파일 목록을 자세히 확인하는 명령어를 작성하시오.

```text
정답: ls -al
```

## 문제 3

`sample`이라는 디렉터리를 생성하는 명령어를 작성하시오.

```text
정답: mkdir sample
```

## 문제 4

`a.txt`를 `backup` 디렉터리에 복사하는 명령어를 작성하시오.

```text
정답: cp a.txt backup/
```

## 문제 5

`a.txt`의 이름을 `b.txt`로 변경하는 명령어를 작성하시오.

```text
정답: mv a.txt b.txt
```

## 문제 6

`app.log` 파일에서 `ERROR`가 포함된 행만 찾는 명령어를 작성하시오.

```text
정답: grep "ERROR" app.log
```

## 문제 7

현재 디렉터리 아래의 모든 `.py` 파일을 검색하는 명령어를 작성하시오.

```text
정답: find . -name "*.py"
```

## 문제 8

`result.txt` 파일의 줄 수를 출력하는 명령어를 작성하시오.

```text
정답: wc -l result.txt
```

## 문제 9

`run.sh` 파일에 실행 권한을 추가하는 명령어를 작성하시오.

```text
정답: chmod +x run.sh
```

## 문제 10

`ls -al`의 결과 중 처음 5줄만 출력하는 명령어를 작성하시오.

```text
정답: ls -al | head -n 5
```

---

# 7. 도전 과제

## 도전 과제 1: 고득점 학생 분석

`students.csv` 파일에서 다음 결과를 출력한다.

1. 80점 이상 학생
2. 점수가 높은 순서
3. 전체 평균
4. 팀별 인원수

### 정답 예시

80점 이상 학생:

```bash
!awk -F',' 'NR > 1 && $3 >= 80 {print $1, $3}' /content/linux_lab/data/students.csv
```

점수가 높은 순서:

```bash
!tail -n +2 /content/linux_lab/data/students.csv | sort -t',' -k3,3nr
```

전체 평균:

```bash
!awk -F',' 'NR > 1 {sum += $3; count++} END {print sum/count}' /content/linux_lab/data/students.csv
```

팀별 인원수:

```bash
!tail -n +2 /content/linux_lab/data/students.csv | cut -d',' -f2 | sort | uniq -c
```

---

## 도전 과제 2: 자동 백업 스크립트

다음 조건을 만족하는 `backup.sh` 스크립트를 작성한다.

1. 현재 날짜와 시간이 파일 이름에 포함되어야 한다.
2. `/content/linux_lab`을 압축해야 한다.
3. 압축 파일은 `/content/backup_files`에 저장해야 한다.
4. 완료 후 압축 파일의 크기를 출력해야 한다.

### 정답 예시

```bash
%%bash

cat > /content/linux_lab/scripts/backup.sh <<'EOF'
#!/bin/bash

SOURCE="/content/linux_lab"
BACKUP_DIR="/content/backup_files"
NOW=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_FILE="$BACKUP_DIR/linux_lab_$NOW.tar.gz"

mkdir -p "$BACKUP_DIR"

tar -czf "$BACKUP_FILE" "$SOURCE"

echo "[OK] 백업 완료"
ls -lh "$BACKUP_FILE"
EOF

chmod 755 /content/linux_lab/scripts/backup.sh
```

실행:

```bash
!/content/linux_lab/scripts/backup.sh
```

---

# 8. Colab에서 실습할 때 주의할 점

## 8.1 런타임을 종료하면 파일이 사라질 수 있다

Colab의 `/content` 디렉터리는 임시 저장 공간이다.

다음 상황에서는 파일이 사라질 수 있다.

* 런타임 다시 시작
* 런타임 연결 해제
* 장시간 미사용
* 세션 종료

중요한 파일은 다운로드하거나 Google Drive에 저장해야 한다.

## 8.2 `!cd`는 유지되지 않을 수 있다

다음 두 명령은 서로 다른 셸에서 실행될 수 있다.

```bash
!cd /content/linux_lab
!pwd
```

디렉터리를 지속적으로 변경하려면 다음을 사용한다.

```bash
%cd /content/linux_lab
```

여러 명령어를 동일한 셸에서 실행하려면 다음을 사용한다.

```bash
%%bash

cd /content/linux_lab
pwd
ls
```

## 8.3 대화형 명령어 사용에 제한이 있다

다음 명령은 Colab에서 사용하기 불편할 수 있다.

```text
nano
vim
top
less
```

대신 다음 방법을 사용할 수 있다.

```bash
!top -b -n 1 | head
```

```bash
!cat 파일명
```

```bash
!head 파일명
```

```bash
!tail 파일명
```

## 8.4 `rm` 명령은 신중하게 사용한다

삭제 전 현재 위치와 파일 목록을 확인한다.

```bash
!pwd
!ls -al
```

경로는 가능하면 절대 경로로 작성한다.

```bash
!rm -rf /content/linux_lab/temp
```

## 8.5 일반 서버와 Colab은 다르다

Colab은 리눅스 명령어를 학습하기에는 적합하지만 완전한 서버 운영환경은 아니다.

제한될 수 있는 기능:

* `systemctl`
* 서버 재부팅
* 사용자 계정 영구 생성
* SSH 서버 운영
* 장기간 백그라운드 서비스 실행
* 영구적인 패키지 설치
* 네트워크 포트 직접 공개

---

# 9. 핵심 명령어 요약

| 구분   | 명령어          | 기능          |
| ---- | ------------ | ----------- |
| 시스템  | `uname -a`   | 시스템 정보      |
| 시스템  | `whoami`     | 현재 사용자      |
| 시스템  | `date`       | 날짜와 시간      |
| 시스템  | `free -h`    | 메모리 사용량     |
| 시스템  | `df -h`      | 디스크 사용량     |
| 경로   | `pwd`        | 현재 위치       |
| 경로   | `cd`         | 디렉터리 이동     |
| 목록   | `ls -al`     | 파일 목록       |
| 생성   | `mkdir`      | 디렉터리 생성     |
| 생성   | `touch`      | 빈 파일 생성     |
| 확인   | `cat`        | 파일 내용 출력    |
| 확인   | `head`       | 파일 앞부분 출력   |
| 확인   | `tail`       | 파일 뒷부분 출력   |
| 복사   | `cp`         | 파일 복사       |
| 이동   | `mv`         | 이동 또는 이름 변경 |
| 삭제   | `rm`         | 파일 삭제       |
| 검색   | `grep`       | 문자열 검색      |
| 검색   | `find`       | 파일 검색       |
| 처리   | `cut`        | 열 추출        |
| 처리   | `sort`       | 정렬          |
| 처리   | `uniq`       | 중복 처리       |
| 처리   | `wc`         | 줄, 단어, 문자 수 |
| 처리   | `awk`        | 열 기반 데이터 처리 |
| 권한   | `chmod`      | 파일 권한 변경    |
| 프로세스 | `ps`         | 프로세스 확인     |
| 프로세스 | `kill`       | 프로세스 종료     |
| 압축   | `tar`        | 파일 묶기와 압축   |
| 도움말  | `명령어 --help` | 명령어 사용법 확인  |

---

# 10. 수업 마무리 정리

이번 실습에서 확인한 리눅스의 핵심 특징은 다음과 같다.

1. 리눅스는 대소문자를 구분한다.
2. 모든 파일과 디렉터리는 `/` 아래의 계층 구조로 관리된다.
3. 시스템 정보와 장치도 파일처럼 접근할 수 있다.
4. 하나의 명령어가 하나의 역할을 수행한다.
5. 파이프로 여러 명령어를 연결할 수 있다.
6. 파일마다 읽기, 쓰기, 실행 권한이 존재한다.
7. 실행 중인 프로그램은 프로세스로 관리된다.
8. 셸 스크립트를 이용해 반복 작업을 자동화할 수 있다.
9. Colab은 Ubuntu 기반 리눅스 실습환경이지만 데이터가 임시로 저장된다.
10. 리눅스 명령어는 AI, 데이터 분석, 서버, 클라우드 개발의 기초가 된다.

수업에서는 1교시와 2교시는 강사가 함께 입력하고, 3교시부터는 명령어 일부를 빈칸으로 제시한 뒤 학생이 완성하게 하면 실습 효과가 높습니다.
