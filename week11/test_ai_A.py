
import pytest

from load_scores import load_scores, MIN_SCORE, MAX_SCORE


def write_csv(tmp_path, content):
    """테스트용 CSV 파일 생성"""
    path = tmp_path / "scores.csv"
    path.write_text(content, encoding="utf-8")
    return path


# ---------------------------------
# 1. 정상 입력 테스트
# ---------------------------------

def test_load_valid_scores(tmp_path):
    path = write_csv(
        tmp_path,
        "이름,점수\n"
        "홍길동,90\n"
        "김철수,80\n"
        "이영희,70\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [
        ("홍길동", 90),
        ("김철수", 80),
        ("이영희", 70),
    ]
    assert skipped == []


def test_load_score_with_whitespace(tmp_path):
    path = write_csv(
        tmp_path,
        "이름,점수\n"
        " 홍길동 , 90 \n"
    )

    kept, skipped = load_scores(path)

    assert kept == [("홍길동", 90)]
    assert skipped == []


def test_load_empty_lines_are_ignored(tmp_path):
    path = write_csv(
        tmp_path,
        "이름,점수\n"
        "\n"
        "홍길동,90\n"
        "\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [("홍길동", 90)]
    assert skipped == []


def test_load_utf8_bom_file(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text(
        "이름,점수\n홍길동,90\n",
        encoding="utf-8-sig"
    )

    kept, skipped = load_scores(path)

    assert kept == [("홍길동", 90)]
    assert skipped == []


# ---------------------------------
# 2. 경계값 테스트
# ---------------------------------

@pytest.mark.parametrize(
    "score",
    [MIN_SCORE, MAX_SCORE]
)
def test_score_boundary_values(tmp_path, score):
    path = write_csv(
        tmp_path,
        f"이름,점수\n홍길동,{score}\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [("홍길동", score)]
    assert skipped == []


@pytest.mark.parametrize(
    "score",
    [-1, 101]
)
def test_score_out_of_range(tmp_path, score):
    path = write_csv(
        tmp_path,
        f"이름,점수\n홍길동,{score}\n"
    )

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [
        (2, f"홍길동,{score}", "점수가 0~100 밖")
    ]


# ---------------------------------
# 3. 잘못된 데이터 테스트
# ---------------------------------

def test_empty_name(tmp_path):
    path = write_csv(
        tmp_path,
        "이름,점수\n"
        ",90\n"
    )

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [
        (2, ",90", "이름이 비어 있음")
    ]


def test_empty_score(tmp_path):
    path = write_csv(
        tmp_path,
        "이름,점수\n"
        "홍길동,\n"
    )

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [
        (2, "홍길동,", "점수가 비어 있음")
    ]


@pytest.mark.parametrize(
    "raw",
    ["abc", "90.5", "점수", "10a"]
)
def test_non_integer_score(tmp_path, raw):
    path = write_csv(
        tmp_path,
        f"이름,점수\n홍길동,{raw}\n"
    )

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [
        (2, f"홍길동,{raw}", "점수가 정수가 아님")
    ]


# ---------------------------------
# 4. CSV 열 개수 오류 테스트
# ---------------------------------

@pytest.mark.parametrize(
    "row",
    [
        "홍길동",
        "홍길동,90,추가정보",
        "홍길동,90,추가,정보",
    ]
)
def test_invalid_column_count(tmp_path, row):
    path = write_csv(
        tmp_path,
        f"이름,점수\n{row}\n"
    )

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [
        (2, row, "열 개수가 2가 아님")
    ]


# ---------------------------------
# 5. 여러 오류가 섞인 경우
# ---------------------------------

def test_mixed_valid_and_invalid_rows(tmp_path):
    path = write_csv(
        tmp_path,
        "이름,점수\n"
        "홍길동,90\n"
        ",80\n"
        "김철수,\n"
        "이영희,abc\n"
        "박민수,101\n"
        "최유리,0\n"
        "정우성,100\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [
        ("홍길동", 90),
        ("최유리", 0),
        ("정우성", 100),
    ]

    assert skipped == [
        (3, ",80", "이름이 비어 있음"),
        (4, "김철수,", "점수가 비어 있음"),
        (5, "이영희,abc", "점수가 정수가 아님"),
        (6, "박민수,101", "점수가 0~100 밖"),
    ]


# ---------------------------------
# 6. 예외 테스트
# ---------------------------------

def test_file_not_found(tmp_path):
    path = tmp_path / "not_exist.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(path)


def test_directory_instead_of_file(tmp_path):
    with pytest.raises(IsADirectoryError):
        load_scores(tmp_path)


# ---------------------------------
# 7. 헤더만 있는 파일
# ---------------------------------

def test_header_only_file(tmp_path):
    path = write_csv(tmp_path, "이름,점수\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == []


# ---------------------------------
# 8. 빈 파일
# ---------------------------------

def test_completely_empty_file(tmp_path):
    path = write_csv(tmp_path, "")

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == []
