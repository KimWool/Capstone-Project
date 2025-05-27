# migrate_keywords.py

import json
import psycopg2

# ✅ PostgreSQL 연결 설정
conn = psycopg2.connect(
    host="localhost",
    dbname="capstone",
    user="capstone_user",
    password="1234"
)
cur = conn.cursor()

# ✅ JSON 파일 경로
json_path = "./jeonse_keyword_entries.json"  # 필요시 절대 경로로 변경

# ✅ JSON 파일 로드
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# ✅ DB 삽입
inserted = 0
skipped = 0

for item in data:
    keyword = item.get("keyword", "").strip()
    text = item.get("text", "").strip()

    if not keyword or not text:
        print(f"⚠️ 스킵됨 (빈 keyword/text): '{keyword}'")
        skipped += 1
        continue

    try:
        cur.execute("""
            INSERT INTO keywords (keyword, description)
            VALUES (%s, %s)
            ON CONFLICT (keyword) DO NOTHING;
        """, (keyword, text))
        inserted += 1
    except Exception as e:
        print(f"❌ 에러 발생: {e} → '{keyword}'")

# ✅ 커밋 및 종료
conn.commit()
cur.close()
conn.close()

print(f"\n✅ 마이그레이션 완료: {inserted}개 삽입, {skipped}개 스킵됨")
