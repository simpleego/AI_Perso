## Git
<img width="1018" height="858" alt="image" src="https://github.com/user-attachments/assets/3d813746-5da7-4e38-bbdc-0aa9ccb8794c" />

--- 
<img width="100%"  alt="image" src="https://github.com/user-attachments/assets/94ca8f7b-348a-4308-9048-63772a78b414" />


---  

<img width="100%"  alt="image" src="https://github.com/user-attachments/assets/aa0d198a-13a5-4f6d-89be-9390654d7eb6" />

--- 

<img width="100%"  alt="image" src="https://github.com/user-attachments/assets/9ee3c886-7725-4a68-b1fa-9c6c8c9334ee" />

--- 

### 1. Git 소개 및 개념 (10분)
**Git이란?**
- 분산 버전 관리 시스템(Distributed Version Control System)
- 코드 변경 이력을 추적하고 관리
- 여러 개발자가 동시에 작업할 수 있게 해주는 도구

**왜 Git을 사용하는가?**
- 코드 백업 및 복구
- 변경 이력 추적
- 브랜치를 통한 병렬 개발
- 팀 협업 지원

**기본 개념**
- Repository(저장소): 프로젝트 파일과 버전 정보를 저장하는 공간
- Commit: 변경사항을 저장하는 단위
- Branch: 독립적인 개발 라인
- Working Directory, Staging Area, Repository의 3단계 구조

### 2. Git 설치 및 초기 설정 (5분)
```bash
# Git 설치 확인
git --version

# 사용자 정보 설정
git config --global user.name "이름"
git config --global user.email "이메일"

# 설정 확인
git config --list
```

### 3. 기본 Git 명령어 (20분)

**저장소 생성 및 초기화**
```bash
# 새 저장소 생성
git init

# 기존 저장소 복제
git clone <URL>
```

**파일 추가 및 커밋**
```bash
# 파일 상태 확인
git status

# 파일을 스테이징 영역에 추가
git add <파일명>
git add .  # 모든 변경된 파일

# 커밋 생성
git commit -m "커밋 메시지"

# 변경 이력 확인
git log
git log --oneline  # 간단한 형태
```

**파일 변경사항 확인**
```bash
# 변경사항 확인
git diff
git diff --staged  # 스테이징된 변경사항
```

### 4. 브랜치 개념 및 활용 (15분)

**브랜치 기본 명령어**
```bash
# 브랜치 목록 확인
git branch

# 새 브랜치 생성
git branch <브랜치명>

# 브랜치 전환
git checkout <브랜치명>
git switch <브랜치명>  # 최신 명령어

# 브랜치 생성과 전환을 동시에
git checkout -b <브랜치명>
git switch -c <브랜치명>
```

**브랜치 병합**
```bash
# 브랜치 병합
git merge <브랜치명>

# 브랜치 삭제
git branch -d <브랜치명>
```

### 5. 원격 저장소 연동 (8분)

**원격 저장소 설정**
```bash
# 원격 저장소 추가
git remote add origin <URL>

# 원격 저장소 확인
git remote -v
```

**Push와 Pull**
```bash
# 원격 저장소로 업로드
git push origin <브랜치명>
git push -u origin main  # 최초 푸시

# 원격 저장소에서 다운로드
git pull origin <브랜치명>
git fetch  # 다운로드만, 병합 X
```

### 6. 실무 팁 및 문제 해결 (2분)

**유용한 명령어**
```bash
# 마지막 커밋 수정
git commit --amend

# 파일 되돌리기
git checkout -- <파일명>
git restore <파일명>

# 커밋 되돌리기
git reset --soft HEAD~1  # 커밋만 취소
git reset --hard HEAD~1  # 완전히 되돌리기
```

**좋은 커밋 메시지 작성법**
- 첫 줄에 간략한 요약 (50자 이내)
- 명령형으로 작성 ("Add", "Fix", "Update")
- 구체적이고 명확하게

## 강의 진행 팁

1. **실습 위주로 진행**: 각 명령어를 직접 따라해보도록 유도
2. **시각적 자료 활용**: Git의 3단계 구조나 브랜치 모델을 그림으로 설명
3. **실제 시나리오 사용**: 간단한 프로젝트를 만들어 실습
4. **자주 하는 실수들**: `.gitignore` 파일, 커밋 메시지 작성법 등 언급
5. **Q&A 시간 확보**: 마지막에 질문 받을 시간 남겨두기

이 구성으로 Git의 핵심 기능들을 효율적으로 전달할 수 있을 것입니다. 수강자의 수준에 따라 내용의 깊이를 조절하시면 됩니다.
