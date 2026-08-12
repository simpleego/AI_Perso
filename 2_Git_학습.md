# Git 명령어 기반 3시간 강의자료

## 1. 강의 개요

### 교육 대상

* Git을 처음 접하는 학생
* 비전공자 및 프로그래밍 입문자
* Windows 환경에서 VS Code 또는 명령창을 사용하는 학습자

### 실습 환경

Windows에서는 **Git Bash** 사용을 권장합니다. Git Bash를 사용하면 Windows에서도 Linux와 유사한 명령어를 사용할 수 있어 수업 진행이 편리합니다.

필요 프로그램:

* Git
* Git Bash
* VS Code 또는 메모장
* 선택 사항: GitHub 계정

### 학습 목표

3시간 수업을 마치면 학생은 다음 작업을 수행할 수 있어야 합니다.

1. Git 저장소를 생성할 수 있다.
2. 파일 변경 사항을 확인하고 Commit할 수 있다.
3. Commit 기록을 조회할 수 있다.
4. 잘못된 변경과 Commit을 되돌릴 수 있다.
5. Branch를 만들고 병합할 수 있다.
6. Merge Conflict를 해결할 수 있다.
7. 원격 저장소의 기본 개념을 이해할 수 있다.

---

# 2. 전체 시간 구성

| 시간          | 학습 내용                  | 핵심 명령어                                  |
| ----------- | ---------------------- | --------------------------------------- |
| 00:00~00:10 | Git 개념과 구조             | 개념 설명                                   |
| 00:10~00:20 | Git 설치 확인과 환경 설정       | `git --version`, `git config`           |
| 00:20~00:40 | 저장소 생성과 첫 Commit       | `git init`, `git add`, `git commit`     |
| 00:40~00:50 | 변경 상태와 이력 조회           | `git status`, `git diff`, `git log`     |
| 00:50~01:00 | `.gitignore`와 보안 파일 관리 | `.gitignore`, `git rm --cached`         |
| 01:00~01:10 | 휴식                     |                                         |
| 01:10~01:40 | 파일 수정과 변경 취소           | `git restore`, `git commit --amend`     |
| 01:40~02:00 | Commit 취소와 복구          | `git revert`, `git reset`               |
| 02:00~02:10 | 휴식                     |                                         |
| 02:10~02:35 | Branch 생성과 Merge       | `git branch`, `git switch`, `git merge` |
| 02:35~02:50 | 충돌 발생과 해결              | Merge Conflict                          |
| 02:50~03:00 | 원격 저장소와 종합 실습          | `git remote`, `git push`, `git pull`    |

---

# 1교시: Git 기본 개념과 Commit

## 00:00~00:10 Git이란 무엇인가

Git은 파일의 변경 이력을 저장하고 관리하는 **분산 버전 관리 시스템**입니다.

Git을 사용하면 다음 작업이 가능합니다.

* 누가 파일을 변경했는지 확인
* 언제 변경했는지 확인
* 어떤 내용을 변경했는지 확인
* 이전 버전으로 복구
* 여러 개발자가 동시에 작업
* 기능별로 Branch를 분리하여 개발

## Git과 GitHub의 차이

| 구분    | Git                     | GitHub                 |
| ----- | ----------------------- | ---------------------- |
| 종류    | 버전 관리 프로그램              | Git 저장소 호스팅 서비스        |
| 실행 위치 | 개인 컴퓨터                  | 인터넷 서버                 |
| 주요 역할 | 변경 이력 관리                | 공유, 협업, 백업             |
| 대표 명령 | `git add`, `git commit` | `git push`, `git pull` |
| 인터넷   | 없어도 사용 가능               | 대부분 필요                 |

Git은 프로그램이고, GitHub는 Git 저장소를 인터넷에서 관리하는 서비스입니다.

---

## Git의 세 가지 영역

```text
작업 폴더
Working Directory
      │
      │ git add
      ▼
스테이징 영역
Staging Area
      │
      │ git commit
      ▼
로컬 저장소
Local Repository
      │
      │ git push
      ▼
원격 저장소
Remote Repository
```

### 핵심 의미

* 작업 폴더: 현재 파일을 작성하고 수정하는 공간
* 스테이징 영역: 다음 Commit에 포함할 파일을 선택하는 공간
* 로컬 저장소: Commit이 저장되는 내 컴퓨터의 저장소
* 원격 저장소: GitHub와 같은 인터넷 저장소

학생들이 가장 먼저 이해해야 하는 흐름은 다음과 같습니다.

```text
파일 수정 → git add → git commit
```

---

## 00:10~00:20 Git 설치 확인과 사용자 설정

### 1. Git 설치 확인

Git Bash를 실행하고 다음 명령어를 입력합니다.

```bash
git --version
```

출력 예:

```text
git version 2.x.x
```

명령어를 찾을 수 없다는 오류가 나오면 Git이 설치되지 않았거나 환경변수 설정이 잘못된 것입니다.

---

### 2. 사용자 이름 설정

각 학생은 자신의 이름을 입력합니다.

```bash
git config --global user.name "Student Name"
```

예:

```bash
git config --global user.name "Hong Gildong"
```

---

### 3. 사용자 이메일 설정

```bash
git config --global user.email "student@example.com"
```

GitHub 계정을 사용할 경우 GitHub에 등록한 이메일을 사용할 수 있습니다.

---

### 4. 기본 Branch 이름 설정

```bash
git config --global init.defaultBranch main
```

앞으로 새 저장소의 기본 Branch 이름을 `main`으로 설정합니다.

---

### 5. 한글 파일명 표시 설정

```bash
git config --global core.quotepath false
```

한글 파일명이 Git 상태 화면에서 코드값으로 표시되는 현상을 줄일 수 있습니다.

---

### 6. 설정 확인

```bash
git config --global --list
```

특정 설정만 확인할 수도 있습니다.

```bash
git config user.name
git config user.email
```

### 실습 확인 문제

다음 명령어의 차이를 설명하게 합니다.

```bash
git config --global user.name "Hong Gildong"
git config user.name
```

정답:

* 첫 번째 명령어: 사용자 이름을 설정
* 두 번째 명령어: 현재 설정된 이름을 조회

---

## 00:20~00:40 저장소 생성과 첫 번째 Commit

## 실습 프로젝트 생성

### 1. 실습 폴더 생성

```bash
mkdir git-3h-lab
```

### 2. 폴더 이동

```bash
cd git-3h-lab
```

### 3. 현재 위치 확인

```bash
pwd
```

Windows Git Bash 출력 예:

```text
/c/Users/student/git-3h-lab
```

---

## Git 저장소 생성

```bash
git init
```

출력 예:

```text
Initialized empty Git repository in .../git-3h-lab/.git/
```

현재 폴더에 `.git`이라는 숨김 폴더가 생성됩니다.

`.git` 폴더에는 다음 정보가 저장됩니다.

* Commit 이력
* Branch 정보
* 설정 정보
* 파일 변경 추적 정보

`.git` 폴더를 삭제하면 해당 폴더는 더 이상 Git 저장소가 아닙니다.

---

## 현재 상태 확인

```bash
git status
```

출력 예:

```text
On branch main

No commits yet

nothing to commit
```

---

## 첫 번째 파일 생성

```bash
echo "# Git 3-Hour Lab" > README.md
```

파일 내용 확인:

```bash
cat README.md
```

출력:

```text
# Git 3-Hour Lab
```

PowerShell에서는 다음 명령어도 사용할 수 있습니다.

```powershell
Get-Content README.md
```

---

## 파일 상태 확인

```bash
git status
```

출력 예:

```text
Untracked files:
  README.md
```

`Untracked`는 Git이 아직 관리하지 않는 파일이라는 뜻입니다.

---

## 스테이징 영역에 등록

```bash
git add README.md
```

다시 상태를 확인합니다.

```bash
git status
```

출력 예:

```text
Changes to be committed:
  new file: README.md
```

---

## 첫 번째 Commit 생성

```bash
git commit -m "docs: add README"
```

출력 예:

```text
[main (root-commit) a1b2c3d] docs: add README
 1 file changed, 1 insertion(+)
```

### Commit의 의미

Commit은 현재 프로젝트의 상태를 저장한 하나의 버전입니다.

```text
Commit 1
README.md 최초 생성
```

---

## 두 번째 파일 생성과 Commit

```bash
echo "Name: Student" > profile.txt
echo "Interest: AI" >> profile.txt
```

상태 확인:

```bash
git status
```

스테이징:

```bash
git add profile.txt
```

Commit:

```bash
git commit -m "feat: add student profile"
```

---

## 여러 파일을 한 번에 등록

```bash
git add .
```

현재 폴더 이하의 변경 파일을 모두 스테이징합니다.

초보자에게는 편리하지만, 원하지 않는 파일까지 포함할 수 있으므로 Commit 전에 반드시 확인합니다.

```bash
git status
```

---

## 좋은 Commit 메시지 작성법

Commit 메시지는 변경 내용을 짧고 명확하게 작성합니다.

```bash
git commit -m "feat: add login function"
git commit -m "fix: correct login validation"
git commit -m "docs: update README"
git commit -m "test: add login test"
git commit -m "refactor: simplify user service"
```

자주 사용하는 접두어:

| 접두어        | 의미         |
| ---------- | ---------- |
| `feat`     | 기능 추가      |
| `fix`      | 오류 수정      |
| `docs`     | 문서 변경      |
| `test`     | 테스트 추가     |
| `refactor` | 코드 구조 개선   |
| `chore`    | 설정 및 기타 작업 |

좋지 않은 예:

```bash
git commit -m "수정"
git commit -m "작업"
git commit -m "완료"
```

좋은 예:

```bash
git commit -m "feat: add student profile"
```

---

## 00:40~00:50 상태·차이·기록 확인

## 상태 확인

```bash
git status
```

짧은 형식으로 확인:

```bash
git status -s
```

또는:

```bash
git status -sb
```

출력 예:

```text
## main
 M profile.txt
?? new-file.txt
```

의미:

| 표시   | 의미              |
| ---- | --------------- |
| `M`  | 수정된 파일          |
| `A`  | 추가된 파일          |
| `D`  | 삭제된 파일          |
| `??` | Git이 추적하지 않는 파일 |

---

## 파일 수정

```bash
echo "Goal: Learn Git" >> profile.txt
```

변경 내용 확인:

```bash
git diff
```

`git diff`는 작업 폴더와 스테이징 영역의 차이를 보여줍니다.

---

## 스테이징한 내용 확인

```bash
git add profile.txt
git diff --staged
```

`git diff --staged`는 다음 Commit에 포함될 내용을 보여줍니다.

---

## Commit 생성

```bash
git commit -m "docs: add learning goal"
```

---

## Commit 기록 조회

```bash
git log
```

주요 정보:

* Commit 해시
* 작성자
* 작성 일시
* Commit 메시지

간단하게 조회:

```bash
git log --oneline
```

출력 예:

```text
c8d91af docs: add learning goal
2e24b73 feat: add student profile
f671d20 docs: add README
```

그래프 형태로 조회:

```bash
git log --oneline --graph --decorate --all
```

---

## 특정 Commit 내용 확인

```bash
git show HEAD
```

`HEAD`는 현재 선택된 최신 Commit을 의미합니다.

이전 Commit 확인:

```bash
git show HEAD~1
```

Commit 해시를 이용한 조회:

```bash
git show c8d91af
```

Commit 해시는 학생마다 다릅니다.

---

## 00:50~01:00 `.gitignore`와 중요 파일 보호

Python과 AI 프로젝트에서는 다음 파일을 Git에 올리지 않는 것이 중요합니다.

* `.env`
* API Key
* 가상환경 폴더
* 캐시 파일
* 대용량 모델 파일
* 개인 설정 파일

## `.gitignore` 생성

```bash
echo ".env" > .gitignore
echo ".venv/" >> .gitignore
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
```

내용 확인:

```bash
cat .gitignore
```

출력:

```text
.env
.venv/
venv/
__pycache__/
*.pyc
```

Commit:

```bash
git add .gitignore
git commit -m "chore: add gitignore"
```

---

## `.env` 파일이 제외되는지 확인

```bash
echo "OPENAI_API_KEY=test-key" > .env
git status
```

`.env` 파일은 상태 목록에 나타나지 않아야 합니다.

### 중요 보안 원칙

API Key를 GitHub에 올려서는 안 됩니다.

```env
OPENAI_API_KEY=실제_API_KEY
LANGSMITH_API_KEY=실제_API_KEY
```

이와 같은 파일은 반드시 `.gitignore`에 등록해야 합니다.

---

## 이미 Git이 추적하는 파일을 제외할 때

`.gitignore`는 이미 Commit된 파일에는 자동 적용되지 않습니다.

예를 들어 `.env` 파일을 이미 Commit했다면 다음 명령을 사용합니다.

```bash
git rm --cached .env
```

그다음 Commit합니다.

```bash
git commit -m "security: stop tracking env file"
```

이 명령은 로컬 파일은 유지하고 Git 추적만 해제합니다.

---

# 01:00~01:10 휴식

휴식 전에 다음 세 가지를 확인합니다.

```bash
git status
git log --oneline
git branch
```

정상 상태 예:

```text
On branch main
nothing to commit, working tree clean
```

---

# 2교시: 변경 취소와 Commit 복구

## 01:10~01:25 작업 파일 변경 취소

## 파일 변경

```bash
echo "Temporary content" >> profile.txt
```

변경 확인:

```bash
git diff
```

현재 파일 내용을 확인합니다.

```bash
cat profile.txt
```

---

## 수정 내용을 취소

```bash
git restore profile.txt
```

다시 확인합니다.

```bash
git diff
cat profile.txt
```

추가했던 `Temporary content`가 사라집니다.

### 주의

```bash
git restore profile.txt
```

이 명령은 Commit되지 않은 수정 내용을 삭제합니다. 취소하면 일반적인 방법으로 복구하기 어렵습니다.

---

## 01:25~01:40 스테이징 취소와 Commit 수정

## 파일 수정

```bash
echo "City: Seoul" >> profile.txt
```

스테이징:

```bash
git add profile.txt
```

상태 확인:

```bash
git status
```

---

## 스테이징만 취소

```bash
git restore --staged profile.txt
```

상태 확인:

```bash
git status
```

파일의 수정 내용은 남아 있지만, 스테이징 영역에서는 제거됩니다.

다시 스테이징하고 Commit합니다.

```bash
git add profile.txt
git commit -m "docs: add city"
```

---

## 마지막 Commit 메시지 수정

잘못된 Commit 메시지를 작성했다고 가정합니다.

```bash
echo "Favorite: Python" >> profile.txt
git add profile.txt
git commit -m "수정"
```

마지막 Commit 메시지를 변경합니다.

```bash
git commit --amend -m "docs: add favorite language"
```

기록 확인:

```bash
git log --oneline
```

### `--amend`의 특징

* 마지막 Commit만 수정
* Commit 메시지 수정 가능
* 빠뜨린 파일 추가 가능
* 기존 Commit 해시가 변경됨

---

## Commit에 파일을 빠뜨린 경우

```bash
echo "Level: Beginner" >> profile.txt
git add profile.txt
git commit --amend --no-edit
```

`--no-edit`는 기존 Commit 메시지를 유지합니다.

---

## 01:40~02:00 Commit 취소와 복구

## 안전한 Commit 취소: `git revert`

잘못된 내용을 Commit합니다.

```bash
echo "This line is incorrect" >> README.md
git add README.md
git commit -m "docs: add incorrect content"
```

기록 확인:

```bash
git log --oneline
```

잘못된 최신 Commit을 취소합니다.

```bash
git revert --no-edit HEAD
```

기록 확인:

```bash
git log --oneline
```

결과는 다음과 같은 형태입니다.

```text
9bd83af Revert "docs: add incorrect content"
5c84a21 docs: add incorrect content
```

`git revert`는 기존 기록을 삭제하지 않고, 반대 작업을 수행하는 새로운 Commit을 만듭니다.

협업 저장소에서는 `reset`보다 `revert`가 안전합니다.

---

## `git reset`의 개념

`git reset`은 Commit 위치를 이전으로 이동합니다.

### 1. Commit만 취소하고 변경 내용 유지

```bash
git reset --soft HEAD~1
```

결과:

* Commit 취소
* 스테이징 상태 유지
* 파일 내용 유지

### 2. Commit과 스테이징을 취소하고 변경 내용 유지

```bash
git reset --mixed HEAD~1
```

또는:

```bash
git reset HEAD~1
```

결과:

* Commit 취소
* 스테이징 취소
* 파일 내용 유지

### 3. 모든 변경 내용 삭제

```bash
git reset --hard HEAD~1
```

결과:

* Commit 취소
* 스테이징 취소
* 파일 수정 내용 삭제

### 매우 중요한 주의사항

```bash
git reset --hard
```

는 작업 내용을 삭제할 수 있으므로 초보자는 신중하게 사용해야 합니다.

---

## 복구 명령어 비교

| 상황                   | 명령어                        |
| -------------------- | -------------------------- |
| Commit하지 않은 파일 수정 취소 | `git restore 파일명`          |
| 스테이징 취소              | `git restore --staged 파일명` |
| 마지막 Commit 수정        | `git commit --amend`       |
| 공유된 Commit 안전하게 취소   | `git revert 커밋`            |
| 로컬 Commit 위치 이동      | `git reset`                |

---

# 02:00~02:10 휴식

학생 확인 문제:

1. `git restore profile.txt`는 무엇을 취소하는가?
2. `git restore --staged profile.txt`는 무엇을 취소하는가?
3. 협업 저장소에서 `revert`가 `reset`보다 안전한 이유는 무엇인가?

정답:

1. 작업 폴더의 수정 내용을 취소한다.
2. 스테이징만 취소하고 파일 내용은 유지한다.
3. 기존 Commit 이력을 삭제하지 않고 취소 Commit을 추가하기 때문이다.

---

# 3교시: Branch, Merge, Conflict, Remote

## 02:10~02:25 Branch 생성

Branch는 기존 코드에 영향을 주지 않고 독립적으로 작업하는 공간입니다.

```text
main
  │
  ├── feature/profile
  │
  └── feature/login
```

## 현재 Branch 확인

```bash
git branch
```

출력:

```text
* main
```

별표는 현재 사용 중인 Branch를 의미합니다.

---

## 새 Branch 생성

```bash
git branch feature/skills
```

Branch 목록 확인:

```bash
git branch
```

출력:

```text
  feature/skills
* main
```

---

## Branch 이동

```bash
git switch feature/skills
```

또는 생성과 이동을 동시에 수행합니다.

```bash
git switch -c feature/contact
```

이전 Git 버전에서는 다음 명령어를 사용할 수 있습니다.

```bash
git checkout -b feature/contact
```

수업에서는 `git switch` 사용을 권장합니다.

---

## Branch에서 작업

`feature/skills` Branch로 이동합니다.

```bash
git switch feature/skills
```

파일 생성:

```bash
echo "Python" > skills.txt
echo "Git" >> skills.txt
echo "LangChain" >> skills.txt
```

Commit:

```bash
git add skills.txt
git commit -m "feat: add skills"
```

기록 확인:

```bash
git log --oneline --graph --decorate --all
```

---

## main Branch로 이동

```bash
git switch main
```

파일 목록 확인:

```bash
ls
```

`skills.txt`가 보이지 않을 수 있습니다. 해당 파일은 `feature/skills` Branch에서 생성했기 때문입니다.

---

## 02:25~02:35 Branch 병합

`feature/skills`의 작업을 `main`에 합칩니다.

현재 Branch 확인:

```bash
git branch
```

현재 위치가 `main`인지 확인합니다.

병합:

```bash
git merge feature/skills
```

파일 확인:

```bash
ls
cat skills.txt
```

기록 확인:

```bash
git log --oneline --graph --decorate --all
```

작업이 끝난 Branch 삭제:

```bash
git branch -d feature/skills
```

Branch 목록 확인:

```bash
git branch
```

---

## Branch 기본 작업 흐름

```bash
git switch main
git switch -c feature/new-function

# 파일 작성 및 수정

git add .
git commit -m "feat: add new function"

git switch main
git merge feature/new-function
git branch -d feature/new-function
```

---

## 02:35~02:50 Merge Conflict 실습

Merge Conflict는 두 Branch에서 같은 파일의 같은 부분을 다르게 수정했을 때 발생합니다.

## 1. 기준 파일 생성

```bash
git switch main
echo "Favorite language: Python" > preference.txt
git add preference.txt
git commit -m "docs: add preference"
```

---

## 2. 새로운 Branch 생성

```bash
git switch -c feature/java
```

파일 수정:

```bash
echo "Favorite language: Java" > preference.txt
git add preference.txt
git commit -m "docs: change preference to Java"
```

---

## 3. main에서 같은 파일 수정

```bash
git switch main
echo "Favorite language: Python and AI" > preference.txt
git add preference.txt
git commit -m "docs: update preference on main"
```

---

## 4. 병합 시도

```bash
git merge feature/java
```

충돌 메시지 예:

```text
CONFLICT (content): Merge conflict in preference.txt
Automatic merge failed; fix conflicts and then commit the result.
```

상태 확인:

```bash
git status
```

---

## 5. 충돌 파일 확인

```bash
cat preference.txt
```

내용 예:

```text
<<<<<<< HEAD
Favorite language: Python and AI
=======
Favorite language: Java
>>>>>>> feature/java
```

의미:

```text
<<<<<<< HEAD
현재 Branch의 내용
=======
병합하려는 Branch의 내용
>>>>>>> feature/java
```

---

## 6. 충돌 해결

두 내용을 합쳐서 파일을 다시 작성합니다.

```bash
echo "Favorite languages: Python, Java, and AI" > preference.txt
```

수정된 파일을 스테이징합니다.

```bash
git add preference.txt
```

병합 Commit을 생성합니다.

```bash
git commit -m "merge: resolve preference conflict"
```

확인:

```bash
git status
git log --oneline --graph --decorate --all
```

Branch 삭제:

```bash
git branch -d feature/java
```

---

## 충돌 해결 절차

```text
1. git status로 충돌 파일 확인
2. 파일 열기
3. <<<<<<<, =======, >>>>>>> 부분 확인
4. 필요한 내용만 남기기
5. 충돌 표시 제거
6. git add
7. git commit
```

병합 자체를 취소하려면 다음 명령어를 사용합니다.

```bash
git merge --abort
```

---

# 02:50~03:00 원격 저장소 실습

GitHub 인증 문제로 수업이 지연되는 것을 방지하기 위해 먼저 로컬에서 원격 저장소를 모의 실습할 수 있습니다.

## 방법 1. 로컬 원격 저장소 모의 실습

현재 실습 폴더의 상위 폴더로 이동합니다.

```bash
cd ..
```

Bare 저장소를 생성합니다.

```bash
git init --bare class-remote.git
```

Bare 저장소는 작업 파일 없이 Git 이력만 저장하는 원격 저장소용 구조입니다.

다시 기존 저장소로 이동합니다.

```bash
cd git-3h-lab
```

원격 저장소 등록:

```bash
git remote add origin ../class-remote.git
```

등록 확인:

```bash
git remote -v
```

출력 예:

```text
origin  ../class-remote.git (fetch)
origin  ../class-remote.git (push)
```

원격 저장소에 업로드:

```bash
git push -u origin main
```

`-u` 옵션을 한 번 사용하면 이후부터 다음과 같이 간단히 실행할 수 있습니다.

```bash
git push
```

---

## 저장소 복제

상위 폴더로 이동:

```bash
cd ..
```

복제:

```bash
git clone class-remote.git student-copy
```

복제된 저장소 이동:

```bash
cd student-copy
```

이력 확인:

```bash
git log --oneline
```

---

## 복제 저장소에서 변경

사용자 설정이 없다면 설정합니다.

```bash
git config user.name "Student Two"
git config user.email "student2@example.com"
```

파일 수정:

```bash
echo "Remote collaboration practice" >> README.md
```

Commit과 Push:

```bash
git add README.md
git commit -m "docs: add collaboration note"
git push
```

---

## 원래 저장소에서 변경 내용 받기

원래 저장소로 이동합니다.

```bash
cd ../git-3h-lab
```

원격 변경 내용을 받습니다.

```bash
git pull
```

파일 확인:

```bash
cat README.md
```

---

## 원격 저장소 명령어 정리

| 명령어                        | 역할                      |
| -------------------------- | ----------------------- |
| `git remote -v`            | 원격 저장소 확인               |
| `git remote add origin 주소` | 원격 저장소 등록               |
| `git clone 주소`             | 원격 저장소 복제               |
| `git fetch`                | 원격 이력만 가져오기             |
| `git pull`                 | 원격 이력을 받고 현재 Branch에 반영 |
| `git push`                 | 로컬 Commit을 원격으로 전송      |

```text
git pull = git fetch + git merge
```

---

# 실제 GitHub 저장소 연결

GitHub에서 README 없이 빈 저장소를 생성한 후 다음 명령어를 실행합니다.

```bash
git remote add origin https://github.com/사용자이름/저장소이름.git
git branch -M main
git push -u origin main
```

이미 `origin`이라는 원격 저장소가 등록되어 있다면 URL을 변경합니다.

```bash
git remote set-url origin https://github.com/사용자이름/저장소이름.git
```

확인:

```bash
git remote -v
```

Push:

```bash
git push -u origin main
```

---

# 3. 최종 종합 실습

## 실습 문제

다음 작업을 명령어만 사용하여 수행합니다.

1. `git-final-test` 폴더를 생성한다.
2. Git 저장소로 초기화한다.
3. `README.md`를 생성한다.
4. 첫 번째 Commit을 생성한다.
5. `feature/member` Branch를 생성한다.
6. `member.txt` 파일을 추가한다.
7. Branch 작업을 Commit한다.
8. `main` Branch에 병합한다.
9. 사용이 끝난 Branch를 삭제한다.
10. 전체 이력을 그래프로 확인한다.

---

## 정답 명령어

```bash
mkdir git-final-test
cd git-final-test

git init

echo "# Git Final Test" > README.md

git add README.md
git commit -m "docs: add README"

git switch -c feature/member

echo "Name: Student" > member.txt
echo "Role: Developer" >> member.txt

git add member.txt
git commit -m "feat: add member information"

git switch main

git merge feature/member

git branch -d feature/member

git status
git log --oneline --graph --decorate --all
```

---

# 4. 학생 평가 기준

| 평가 항목      |  배점 | 확인 내용                   |
| ---------- | --: | ----------------------- |
| 저장소 생성     |  10 | `git init` 실행 여부        |
| 파일 생성      |  10 | README 파일 존재 여부         |
| 스테이징       |  10 | `git add` 사용 여부         |
| Commit     |  20 | Commit 2개 이상            |
| Commit 메시지 |  10 | 의미 있는 메시지 작성            |
| Branch     |  15 | 기능 Branch 생성 여부         |
| Merge      |  15 | main에 정상 병합 여부          |
| 이력 확인      |  10 | `git log --graph` 실행 여부 |
| 합계         | 100 |                         |

---

# 5. 핵심 명령어 요약표

## 설정

```bash
git --version
git config --global user.name "이름"
git config --global user.email "이메일"
git config --global init.defaultBranch main
git config --global --list
```

## 저장소

```bash
git init
git clone 저장소주소
```

## 상태와 차이

```bash
git status
git status -s
git diff
git diff --staged
```

## 스테이징과 Commit

```bash
git add 파일명
git add .
git commit -m "메시지"
git commit --amend
```

## 이력

```bash
git log
git log --oneline
git log --oneline --graph --decorate --all
git show HEAD
```

## 취소와 복구

```bash
git restore 파일명
git restore --staged 파일명
git revert 커밋해시
git reset --soft HEAD~1
git reset --mixed HEAD~1
git reset --hard HEAD~1
```

## Branch와 Merge

```bash
git branch
git branch 브랜치이름
git switch 브랜치이름
git switch -c 브랜치이름
git merge 브랜치이름
git branch -d 브랜치이름
git merge --abort
```

## 원격 저장소

```bash
git remote -v
git remote add origin 저장소주소
git remote set-url origin 저장소주소
git fetch
git pull
git push
git push -u origin main
```

---

# 6. 수업에서 반드시 강조할 핵심 원칙

## 원칙 1. 작업 전 상태 확인

```bash
git status
```

## 원칙 2. Commit 전 변경 내용 확인

```bash
git diff
git diff --staged
```

## 원칙 3. Commit은 하나의 작업 단위로 생성

좋은 예:

```text
사용자 로그인 기능 추가
회원가입 오류 수정
README 설치 방법 추가
```

좋지 않은 예:

```text
로그인 추가 + README 수정 + 불필요한 파일 삭제 + 설정 변경
```

## 원칙 4. Push 전에 Pull

협업 환경에서는 원격 저장소의 변경 사항을 먼저 확인합니다.

```bash
git pull
git push
```

## 원칙 5. API Key를 Commit하지 않기

```gitignore
.env
*.key
credentials.json
```

## 원칙 6. 이해하지 못한 상태에서 `--hard` 사용 금지

```bash
git reset --hard
```

이 명령어는 작업 내용을 삭제할 수 있습니다.

---

# 7. 수업 종료 확인 문제

### 문제 1

`git add`의 역할은 무엇인가?

**정답:** 변경 파일을 다음 Commit에 포함하도록 스테이징 영역에 등록한다.

### 문제 2

`git commit`의 역할은 무엇인가?

**정답:** 스테이징된 변경 내용을 하나의 버전으로 로컬 저장소에 저장한다.

### 문제 3

`git push`와 `git pull`의 차이는 무엇인가?

**정답:**

* `push`: 로컬 Commit을 원격 저장소로 전송
* `pull`: 원격 저장소의 Commit을 로컬로 가져와 반영

### 문제 4

Branch를 사용하는 이유는 무엇인가?

**정답:** 기존 코드에 영향을 주지 않고 기능이나 작업을 독립적으로 개발하기 위해서이다.

### 문제 5

Merge Conflict가 발생하는 주요 이유는 무엇인가?

**정답:** 서로 다른 Branch에서 같은 파일의 같은 부분을 다르게 수정했기 때문이다.

### 문제 6

협업 중 이미 공유된 Commit을 취소할 때 권장되는 명령어는 무엇인가?

```bash
git revert 커밋해시
```

### 문제 7

Git이 현재 파일 상태를 보여주는 명령어는 무엇인가?

```bash
git status
```

---

# 8. 강사용 진행 권장 비율

| 구분         | 시간 비율 |
| ---------- | ----: |
| 개념 설명      |   20% |
| 강사 명령어 시연  |   30% |
| 학생 개별 실습   |   40% |
| 문제 해결 및 복습 |   10% |

강사가 명령어를 여러 개 한꺼번에 제시하기보다 다음 순서로 진행하는 것이 효과적입니다.

```text
강사 설명
→ 명령어 한 줄 실행
→ 학생 실행
→ 결과 화면 확인
→ 다음 명령어 진행
```

특히 다음 세 명령어는 각 단계마다 반복하도록 지도하는 것이 좋습니다.

```bash
git status
git diff
git log --oneline
```
