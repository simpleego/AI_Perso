import hashlib

while True:
    password = input("비밀번호를 입력하세요(종료하려면 exit 입력): ")

    if password == "exit":
        print("프로그램을 종료합니다.")
        break

    # SHA-256 알고리즘을 사용해 비밀번호 해싱
    hashed = hashlib.sha256(password.encode("utf-8")).hexdigest()

    print("입력한 비밀번호:", password)
    print("해시값:", hashed)
    print("-" * 40)