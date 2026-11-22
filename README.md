# ai-programming-test

# 성적 CSV 검사 프로그램

## ① 무엇을 하나요 (What)

성적 CSV 파일을 읽어 유효한 점수는 유지하고, 형식이 맞지 않거나 범위를 벗어난 데이터는 건너뛴 뒤 그 사유를 기록합니다.

## ② 왜 만들었나요 (Why)

성적 CSV 파일에는 정상적인 점수뿐만 아니라 빈 이름이나 점수, 범위를 벗어난 점수, 잘못된 형식의 데이터 등이 포함될 수 있습니다. 이러한 데이터 때문에 프로그램이 정상적으로 작동하지 않거나 잘못된 결과를 내는 상황을 방지하고 싶었습니다. 따라서 다양한 CSV 입력 상황에서도 유효한 데이터는 유지하고, 문제가 있는 데이터는 건너뛰면서 그 이유를 확인할 수 있도록 만들었습니다.

## ③ 어떻게 쓰나요 (How)

```bash
# 설치
pip install pytest pytest-cov

# 프로그램 실행
python load_scores.py scores.csv

# 테스트 실행
python -m pytest

# 커버리지 포함 테스트 실행
python -m pytest --cov=load_scores --cov-report=term-missing
```

## ④ 어떻게 테스트하나요

직접 작성한 테스트는 정상 파일, 없는 파일, 헤더만 있는 파일, 점수의 경계값을 확인합니다.
AI가 생성한 테스트는 정상·예외·경계값 및 여러 형태의 잘못된 CSV 데이터를 확인합니다.

```bash
python -m pytest test_load_scores.py test_ai_A.py test_ai_B.py --cov=load_scores --cov-report=term-missing
```

테스트 수정과 최종 실행이 끝난 뒤 아래 화면을 붙여 넣으세요.

```text
============================= test session starts =============================
collected 51 items

test_load_scores.py .........                                            [ 17%]
test_ai_A.py ...................F..                                      [ 60%]
test_ai_B.py ....................                                        [100%]

=========================== short test summary output =========================
FAILED test_ai_A.py::test_directory_instead_of_file
50 passed, 1 failed

Name             Stmts   Miss  Cover   Missing
---------------------------------------------------
load_scores.py      45      9    80%   77-86
TOTAL               45      9    80%
```

실행 날짜 기준 최종 결과는 직접 작성한 테스트 9개가 모두 통과했습니다.
AI 테스트 A는 22개 중 21개가 통과했고, 디렉터리 입력 케이스에서 Windows 환경의 `PermissionError`가 발생했습니다.
AI 테스트 A가 기대한 `IsADirectoryError`와 다른 예외였으며, 받았던 테스트 코드는 그대로 유지했습니다.
AI 테스트 B는 20개가 모두 통과했습니다.

| 구분 | 직접 작성 | AI 테스트 A | AI 테스트 B |
| --- | ---: | ---: | ---: |
| 테스트 케이스 | 9개 | 22개 | 20개 |
| 통과 | 9개 | 21개 | 20개 |
| 실패 | 0개 | 1개 | 0개 |
| 커버리지 | 80% | 80% | 80% |

## ⑤ 파일 구성

| 파일 | 하는 일 |
| --- | --- |
| `load_scores.py` | 성적 CSV를 읽고 유효한 점수와 건너뛴 행을 반환합니다. |
| `scores.csv` | 정상 데이터와 여러 종류의 잘못된 데이터를 포함한 실습 파일입니다. |
| `empty.csv` | 헤더만 있는 빈 데이터 파일입니다. |
| `test_load_scores.py` | 직접 작성한 정상·예외·경계값 테스트입니다. |
| `test_ai_A.py` | 함수 코드를 입력해 AI가 생성한 테스트입니다. |
| `test_ai_B.py` | 명세만 입력해 AI가 생성한 테스트입니다. |
| `bug3_logic.py` | AI 테스트 함정 실험에 사용할 논리 오류 예제입니다. |


## ⑥ 만든 사람 · AI를 어디에 썼는지

- 만든 사람 : 2026100357 / 유하운
- AI를 쓴 곳 : AI 테스트 코드 A/B 생성 요청과 테스트 결과 비교에 사용했습니다.
- 내가 직접 판단한 것 : 직접 작성한 경계값 테스트가 UTF-8 인코딩과 잘못된 CSV 열 구조 때문에 실패한다는 원인을 확인했고, 임시 CSV를 두 열 구조로 수정했습니다. 실행 결과를 보고 직접 테스트는 모두 통과한다고 판단했습니다. AI 테스트 A의 디렉터리 입력 실패는 프로그램이 잘못된 것이 아니라 Windows 환경의 예외 차이로 판단했으며, 받은 AI 코드는 그대로 유지했습니다.

## 라이선스

MIT License