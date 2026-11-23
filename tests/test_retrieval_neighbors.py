from app import retrieval


def test_neighbors_stay_in_document_and_keep_unique_pages(monkeypatch):
    pages = [
        {
            "page_id": f"{document}-p{number:03d}",
            "document_id": document,
            "page": number,
            "title": f"{document} page {number}",
            "content": f"本文 {document} {number}",
        }
        for document in ("lec01-main", "lec02-main")
        for number in (1, 2, 3)
    ]
    target = [p for p in pages if p["document_id"] == "lec02-main"]
    hits = [
        {**target[1], "distance": 0.1},
        {**target[0], "distance": 0.2},
        {**target[2], "distance": 0.3},
    ]
    monkeypatch.setattr(retrieval, "search", lambda query: hits)
    monkeypatch.setattr(retrieval, "load_pages", lambda: pages)

    results = retrieval.search_with_neighbors("質問")

    # 前後ページが直接ヒットしていても重複せず、検索順位も保つ。
    assert results == hits


def test_neighbors_add_full_page_information(monkeypatch):
    pages = [
        {
            "page_id": f"lec02-main-p{number:03d}",
            "document_id": "lec02-main",
            "page": number,
            "title": f"ページ{number}",
            "content": f"本文{number}",
        }
        for number in (1, 2, 3)
    ]
    hit = {**pages[1], "distance": 0.1}
    monkeypatch.setattr(retrieval, "search", lambda query: [hit])
    monkeypatch.setattr(retrieval, "load_pages", lambda: pages)

    results = retrieval.search_with_neighbors("質問")

    assert results == [hit, pages[0], pages[2]]