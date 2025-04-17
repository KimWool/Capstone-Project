# backend/app/services/embedding.py

from typing import List

def embed_text(text: str) -> List[float]:
    """
    텍스트를 벡터(임베딩)로 변환하는 함수의 스텁(placeholder) 구현입니다.
    실제로는 OpenAI 임베딩 API나 SentenceTransformers 같은 모델을 사용하세요.
    여기서는 편의상 길이 768의 0.0 벡터를 반환하도록 합니다.
    """
    # TODO: 실제 임베딩 모델로 교체
    return [0.0] * 768
