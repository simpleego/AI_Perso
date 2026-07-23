"""
1-6-5. 장기 메모리 - (1) Memory Store 구조와 기본 CRUD
네임스페이스(폴더) + 키(파일명) 구조를 API 키 없이 직접 실습 (LLM 호출 없음)
"""
from datetime import timedelta
from langgraph.store.memory import InMemoryStore


def main():
    # 메모리 기반 Store 생성 (프로덕션에서는 PostgresStore 사용)
    store = InMemoryStore()

    # ── put: 저장 ─ 네임스페이스는 계층 구조(튜플), 키는 고유 식별자
    store.put(("users", "user-123"), "preferences", {"language": "ko", "theme": "dark"})
    store.put(("users", "user-123"), "profile", {"name": "홍길동", "email": "hong@example.com"})
    store.put(("users", "user-456"), "preferences", {"language": "en", "theme": "light"})

    # ── get: 조회 ─ 네임스페이스 + 키로 특정 메모리 하나를 가져옴
    item = store.get(("users", "user-123"), "preferences")
    print("user-123 선호도:", item.value)   # .value로 저장된 JSON(dict) 접근

    # ── search: 네임스페이스 접두사로 하위 메모리 검색
    results = store.search(("users",))  # users/ 아래 모든 사용자의 메모리
    print(f"\n[users 네임스페이스 검색: {len(results)}건]")
    for r in results:
        print(f"  namespace={r.namespace}, key={r.key}, value={r.value}")

    # ── delete: 삭제
    store.delete(("users", "user-456"), "preferences")
    print("\n삭제 후 user-456 조회:", store.get(("users", "user-456"), "preferences"))  # None

    # ── TTL: 만료 시간 설정 (일정 시간 후 자동 삭제)
    store.put(("sessions", "session-123"), "temp-data",
              {"data": "임시 정보"}, ttl=timedelta(days=7).total_seconds() / 60)  # 분 단위
    print("\nTTL 설정된 임시 데이터 저장 완료 (7일 후 자동 삭제)")


if __name__ == "__main__":
    main()
