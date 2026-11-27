
import pytest

from load_scores import load_scores


def write_csv(tmp_path, content):
    """테스트용 CSV 파일 생성"""
    path = tmp_path / "scores.csv"
    path.write_text(content, encoding="utf-8")
    return path


# --------------------------------------------------
# ① 파일이 없는 경우
# --------------------------------------------------

def test_file_not_found(tmp_path):
    path = tmp_path / "not_exists.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(path)


# --------------------------------------------------
# ② 헤더만 있는 경우
# --------------------------------------------------

def test_header_only(tmp_path):
    path = write_csv(tmp_path, "이름,점수\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == []


# --------------------------------------------------
# ③ 열 개수가 2개가 아닌 경우
# --------------------------------------------------

@pytest.mark.parametrize(
    "line",
    [
        "홍길동\n",          # 열 1개
        "홍길동,90,추가정보\n",  # 열 3개
        "홍길동,90,추가,정보\n", # 열 4개
    ]
)
def test_invalid_column_count(tmp_path, line):
    path = write_csv(tmp_path, "이름,점수\n" + line)

    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1
    assert skipped[0][1] == line.rstrip("\n")


# --------------------------------------------------
# ④ 점수가 비었거나 정수가 아닌 경우
# --------------------------------------------------

@pytest.mark.parametrize(
    "line",
    [
        "홍길동,\n",       # 점수 없음
        "홍길동,abc\n",    # 문자
        "홍길동,90.5\n",   # 실수
        "홍길동,점수\n",   # 숫자가 아닌 문자열
    ]
)
def test_invalid_score_format(tmp_path, line):
    path = write_csv(tmp_path, "이름,점수\n" + line)

    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1
    assert skipped[0][1] == line.rstrip("\n")


# --------------------------------------------------
# ⑤ 점수가 0~100 범위를 벗어나는 경우
# --------------------------------------------------

@pytest.mark.parametrize(
    "score",
    [
        -1,
        101,
        -100,
        200,
    ]
)
def test_score_out_of_range(tmp_path, score):
    line = f"홍길동,{score}\n"
    path = write_csv(tmp_path, "이름,점수\n" + line)

    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1
    assert skipped[0][1] == line.rstrip("\n")


# --------------------------------------------------
# ⑥ 이름이 비어 있는 경우
# --------------------------------------------------

def test_empty_name(tmp_path):
    path = write_csv(tmp_path, "이름,점수\n,90\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1


# --------------------------------------------------
# ⑦ 정상적인 데이터
# --------------------------------------------------

def test_valid_scores(tmp_path):
    path = write_csv(
        tmp_path,
        "이름,점수\n"
        "홍길동,90\n"
        "김철수,80\n"
        "이영희,100\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [
        ("홍길동", 90),
        ("김철수", 80),
        ("이영희", 100),
    ]
    assert skipped == []


# --------------------------------------------------
# ⑧ 점수 경계값: 0점과 100점
# --------------------------------------------------

@pytest.mark.parametrize("score", [0, 100])
def test_score_boundary_values(tmp_path, score):
    path = write_csv(
        tmp_path,
        f"이름,점수\n홍길동,{score}\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [("홍길동", score)]
    assert skipped == []


# --------------------------------------------------
# ⑨ 같은 이름이 중복되어도 모두 유지
# --------------------------------------------------

def test_duplicate_names_are_kept(tmp_path):
    path = write_csv(
        tmp_path,
        "이름,점수\n"
        "홍길동,90\n"
        "김철수,80\n"
        "홍길동,70\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [
        ("홍길동", 90),
        ("김철수", 80),
        ("홍길동", 70),
    ]
    assert skipped == []


# --------------------------------------------------
# ⑩ 빈 줄은 기록 없이 건너뜀
# --------------------------------------------------

def test_blank_lines_are_ignored(tmp_path):
    path = write_csv(
        tmp_path,
        "이름,점수\n"
        "\n"
        "홍길동,90\n"
        "\n"
        "\n"
        "김철수,80\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [
        ("홍길동", 90),
        ("김철수", 80),
    ]
    assert skipped == []


# --------------------------------------------------
# ⑪ 건너뛴 줄의 줄번호, 원본 줄, 이유 확인
# --------------------------------------------------

def test_skipped_record_contains_line_number_and_reason(tmp_path):
    path = write_csv(
        tmp_path,
        "이름,점수\n"
        "홍길동,90\n"
        "김철수,abc\n"
        ",80\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [("홍길동", 90)]
    assert len(skipped) == 2

    assert skipped[0][0] == 3
    assert skipped[0][1] == "김철수,abc"
    assert skipped[0][2] != ""

    assert skipped[1][0] == 4
    assert skipped[1][1] == ",80"
    assert skipped[1][2] != ""
