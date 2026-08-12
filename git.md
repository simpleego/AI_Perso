# Git 실무 시나리오 3가지

## 시나리오 1: 개인 프로젝트 시작하기 (혼자 작업)

### 상황
웹사이트 개발 프로젝트를 새로 시작하며, 코드 버전 관리를 위해 Git을 도입하고 GitHub에 백업하려고 합니다.

### 단계별 실습

#### 1단계: 프로젝트 초기 설정
```bash
# 프로젝트 폴더 생성
mkdir my-website
cd my-website

# Git 저장소 초기화
git init

# 기본 파일 생성
touch index.html style.css script.js
echo "# My Website Project" > README.md
```

#### 2단계: .gitignore 설정
```bash
# .gitignore 파일 생성
touch .gitignore

# .gitignore 내용 작성 (에디터에서)
node_modules/
*.log
.env
dist/
```

#### 3단계: 첫 커밋
```bash
# 모든 파일을 스테이징
git add .

# 첫 커밋
git commit -m "Initial commit: Add basic project structure"

# 커밋 이력 확인
git log --oneline
```

#### 4단계: GitHub 연동
```bash
# GitHub에서 저장소 생성 후
git remote add origin https://github.com/username/my-website.git

# 원격 저장소로 푸시
git push -u origin main
```

#### 5단계: 개발 진행
```bash
# index.html 작성 후
git add index.html
git commit -m "Add basic HTML structure"

# style.css 작성 후
git add style.css
git commit -m "Add basic CSS styling"

# 원격 저장소 동기화
git push
```

---

## 시나리오 2: 팀 프로젝트에서 기능 개발 (협업)

### 상황
팀 프로젝트에서 "사용자 로그인 기능"을 담당하게 되었습니다. 다른 개발자들과 충돌 없이 작업하기 위해 브랜치를 사용합니다.

### 단계별 실습

#### 1단계: 프로젝트 복제 및 최신 상태 확인
```bash
# 팀 저장소 복제
git clone https://github.com/team/project.git
cd project

# 최신 상태로 업데이트
git pull origin main

# 현재 브랜치 확인
git branch
```

#### 2단계: 기능 브랜치 생성
```bash
# 로그인 기능을 위한 새 브랜치 생성
git checkout -b feature/user-login

# 브랜치 생성 확인
git branch
```

#### 3단계: 기능 개발
```bash
# 로그인 관련 파일 생성/수정
touch login.html login.js
# 파일 내용 작성...

# 변경사항 확인
git status
git diff

# 첫 번째 커밋
git add login.html login.js
git commit -m "Add login form HTML and basic validation"

# 추가 개발...
# login.js 수정 후
git add login.js
git commit -m "Implement login API integration"
```

#### 4단계: 원격 브랜치에 푸시
```bash
# 기능 브랜치를 원격에 푸시
git push -u origin feature/user-login
```

#### 5단계: 메인 브랜치와 동기화 및 병합
```bash
# 메인 브랜치로 전환
git checkout main

# 최신 변경사항 가져오기
git pull origin main

# 기능 브랜치와 병합
git merge feature/user-login

# 원격 저장소에 반영
git push origin main

# 사용 완료된 브랜치 삭제
git branch -d feature/user-login
git push origin --delete feature/user-login
```

---

## 시나리오 3: 실수 복구 및 문제 해결

### 상황
개발 중 실수로 잘못된 코드를 커밋했거나, 파일을 삭제했거나, 이전 버전으로 되돌아가야 하는 상황들을 해결합니다.

### 실습 사례들

#### 사례 1: 아직 커밋하지 않은 변경사항 되돌리기
```bash
# 파일 수정 후 되돌리고 싶을 때
git status
git checkout -- filename.js  # 특정 파일만
git checkout -- .             # 모든 변경사항

# 또는 최신 명령어
git restore filename.js
git restore .
```

#### 사례 2: 스테이징된 파일 취소
```bash
# git add 후 스테이징을 취소하고 싶을 때
git reset HEAD filename.js    # 특정 파일만
git reset HEAD               # 모든 파일

# 또는 최신 명령어
git restore --staged filename.js
```

#### 사례 3: 마지막 커밋 수정
```bash
# 커밋 메시지만 수정
git commit --amend -m "수정된 커밋 메시지"

# 커밋에 파일 추가 (커밋 메시지 유지)
git add forgotten-file.js
git commit --amend --no-edit
```

#### 사례 4: 이전 커밋으로 되돌리기
```bash
# 커밋 이력 확인
git log --oneline

# 특정 커밋으로 되돌리기 (커밋은 유지하되 변경사항만 되돌림)
git revert <커밋해시>

# 마지막 커밋 완전히 취소 (위험!)
git reset --hard HEAD~1

# 특정 커밋 시점으로 완전히 되돌리기 (위험!)
git reset --hard <커밋해시>
```

#### 사례 5: 삭제된 파일 복구
```bash
# 실수로 삭제한 파일 복구
git checkout HEAD -- deleted-file.js

# 특정 커밋에서 파일 복구
git checkout <커밋해시> -- filename.js
```

#### 사례 6: 병합 충돌 해결
```bash
# 병합 시 충돌 발생
git merge feature-branch

# 충돌 파일 확인
git status

# 충돌 파일을 수동으로 수정한 후
git add .
git commit -m "Resolve merge conflict"

# 병합 취소하고 싶을 때
git merge --abort
```

## 각 시나리오별 핵심 포인트

### 시나리오 1 (개인 프로젝트)
- **핵심**: 기본적인 Git 워크플로우 익히기
- **주요 명령어**: `git init`, `git add`, `git commit`, `git push`
- **학습 목표**: Git의 기본 3단계 구조 이해

### 시나리오 2 (팀 협업)
- **핵심**: 브랜치를 활용한 안전한 협업
- **주요 명령어**: `git branch`, `git checkout`, `git merge`, `git pull`
- **학습 목표**: 충돌 없는 협업 방법 습득

### 시나리오 3 (문제 해결)
- **핵심**: 실수 상황에서의 복구 방법
- **주요 명령어**: `git reset`, `git revert`, `git checkout`, `git restore`
- **학습 목표**: 안전하게 이전 상태로 되돌리는 방법

## 실습 진행 팁

1. **각 시나리오마다 실제 폴더를 만들어 진행**
2. **명령어 실행 전후로 `git status`, `git log` 확인 습관화**
3. **실수 상황은 의도적으로 만들어 연습**
4. **GitHub 실제 계정으로 원격 저장소 연동 실습**
5. **팀 시나리오는 2명이 짝을 이뤄 실습하면 더 효과적**
