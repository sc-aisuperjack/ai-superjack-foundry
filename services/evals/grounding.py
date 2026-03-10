def grounding_score(answer: str, contexts: list[str]) -> float:
    if not contexts:
        return 0.0
    total_hits = sum(1 for context in contexts if context and context[:20].lower() in answer.lower())
    return round(total_hits / len(contexts), 2)
