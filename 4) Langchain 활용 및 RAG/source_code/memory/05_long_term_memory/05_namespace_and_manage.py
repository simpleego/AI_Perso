"""
1-6-5. 장기 메모리 - (5) 네임스페이스 검색과 메모리 관리
여러 사용자의 데이터를 검색/삭제하는 관리 기능 (LLM 호출 없이 실습 가능)
"""
from langgraph.store.memory import InMemoryStore


def search_all_users_preferences(store, preference_key: str) -> str:
    """모든 사용자 네임스페이스에서 특정 선호도를 가진 사용자 검색"""
    results = store.search(("users",))  # "users" 접두사 아래 전체 검색

    matching_users = []
    for result in results:
        if result.key != "preferences":  # preferences 키만 대상으로 필터링
            continue
        prefs = result.value
        if preference_key in prefs:
            matching_users.append({
                "user_id": result.namespace[1],   # ("users", "<user_id>")에서 추출
                "value": prefs[preference_key],
            })
    return f"{len(matching_users)}명의 사용자가 {preference_key} 설정을 가지고 있습니다. {matching_users}"


def delete_user_data(store, user_id: str) -> str:
    """특정 사용자의 데이터를 완전히 삭제 (개인정보 삭제 요청 대응)"""
    namespace = ("users", user_id)
    store.delete(namespace, "profile")           # 프로필 삭제
    store.delete(namespace, "purchase-history")  # 구매 이력 삭제
    return f"{user_id} 사용자 데이터가 삭제되었습니다."


def main():
    store = InMemoryStore()

    # 실습 데이터 구성
    store.put(("users", "user-1"), "preferences", {"theme": "dark", "language": "ko"})
    store.put(("users", "user-2"), "preferences", {"theme": "light"})
    store.put(("users", "user-3"), "preferences", {"language": "en"})
    store.put(("users", "user-1"), "profile", {"name": "홍길동"})
    store.put(("users", "user-1"), "purchase-history", [{"product": "노트북"}])

    # 네임스페이스 검색
    print(search_all_users_preferences(store, "theme"))
    print(search_all_users_preferences(store, "language"))

    # 사용자 데이터 삭제
    print("\n" + delete_user_data(store, "user-1"))
    print("삭제 확인:", store.get(("users", "user-1"), "profile"))  # None


if __name__ == "__main__":
    main()
