import database


def test_database_initialization(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(database, "DATABASE_PATH", db_path)

    database.initialize_database()

    assert db_path.exists()


def test_save_and_retrieve_findings(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(database, "DATABASE_PATH", db_path)

    database.initialize_database()

    findings = [
        {
            "category": "deadline",
            "phrase": "due by",
            "context": "Assignment due by November 15.",
            "filename": "assignment.txt",
            "priority": {
                "score": 60,
                "reasons": ["deadline: +30"]
            },
            "dates": []
        }
    ]

    database.save_findings("assignment.txt", findings)

    result = database.get_all_findings()

    assert len(result) == 1
    assert result[0]["category"] == "deadline"
    assert result[0]["priority"]["score"] == 60


def test_old_findings_are_replaced(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(database, "DATABASE_PATH", db_path)

    database.initialize_database()

    database.save_findings("assignment.txt", [
        {"category": "deadline", "phrase": "old deadline"}
    ])

    database.save_findings("assignment.txt", [
        {"category": "reminder", "phrase": "new reminder"}
    ])

    result = database.get_all_findings()

    assert len(result) == 1
    assert result[0]["phrase"] == "new reminder"


def test_file_change_detection(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(database, "DATABASE_PATH", db_path)

    database.initialize_database()

    test_file = tmp_path / "document.txt"
    test_file.write_text("Original content", encoding="utf-8")

    assert database.has_file_changed(test_file) is True

    database.update_file_state(test_file)

    assert database.has_file_changed(test_file) is False

    test_file.write_text("Modified content", encoding="utf-8")

    assert database.has_file_changed(test_file) is True