# Troubleshootinglog · AX해커톤 예선 2차 제출(무신사 문제 2)

실제 오류·실패·환경 문제·검증 실패·설계 충돌이 발생하면 기록한다. 같은 문제가 반복되면 새 T-ID를 만들기 전에 기존 T-ID를 먼저 확인한다. (규칙: CLAUDE.md / AGENTS.md 11절)

## 기록 형식
```
### T-00N · 문제 제목
**발생 상황** / **증상** / **확인된 원인** / **조치** / **재발 방지**
```

---

### T-020 · PowerShell에서 `&&` 연결 커밋 명령 실패
**발생 상황**
- 제출 후 작업물 정리 변경분을 commit하고 push하기 위해 PowerShell에서 `git commit ... && git push ...` 형태의 명령을 실행했다.

**증상**
- 현재 PowerShell 환경에서 `&&`가 유효한 statement separator로 인식되지 않아 `The token '&&' is not a valid statement separator` 오류가 발생했다.

**확인된 원인**
- Bash 계열 셸에서 쓰는 명령 연결 습관을 Windows PowerShell 환경에 그대로 적용했다.

**조치**
- 커밋과 push를 한 명령으로 연결하지 않고 별도 명령으로 분리해 실행하기로 했다.

**재발 방지**
- 이 프로젝트의 기본 셸은 PowerShell이므로 명령 연결이 필요하면 `;`를 쓰거나, 실패 전파가 중요한 Git 작업은 아예 별도 tool call로 분리한다.

---

### T-019 · 정리 변경분 스테이징 중 이동 전 경로 pathspec 오류
**발생 상황**
- 제출 후 작업물 구조 정리 변경분을 commit하기 위해 이동·삭제된 파일 경로를 명시해 `git add`를 실행했다.

**증상**
- 이미 `docs/post-submission/claude-cross-validation-prompt.md`로 이동한 뒤 사라진 기존 경로 `docs/claude-cross-validation-prompt.md`를 `git add` 인자로 함께 전달해 `fatal: pathspec ... did not match any files` 오류가 발생했다.

**확인된 원인**
- `git mv`로 rename이 이미 staging 후보 상태가 된 상황에서, 존재하지 않는 이동 전 경로를 다시 직접 add 대상으로 지정했다.

**조치**
- 파일 내용 손상이나 삭제는 없음을 `git status`로 확인했다.
- 이후 staging은 개별 이동 전 경로를 직접 나열하지 않고 `git add -A`로 rename, delete, new file을 한 번에 반영하도록 전환했다.

**재발 방지**
- rename/delete가 섞인 정리 작업에서는 존재하지 않는 이전 경로를 직접 `git add`에 넣지 않는다.
- staging 전에는 `git status --short` 기준의 현재 경로만 add하거나, 무시 규칙을 확인한 뒤 `git add -A`를 사용한다.

---

### T-018 · 제출 zip 재검증 중 PowerShell heredoc·최상위 순서 비교 오탐
**발생 상황**
- README 답변 수정 후 문항별 글자 수와 재생성한 `submission.zip` 구조를 검증했다.

**증상**
- PowerShell에서 Bash heredoc(`python - <<'PY'`) 문법을 다시 사용해 글자 수 확인 명령이 실패했다.
- zip 구조 검사에서 최상위 항목이 `logs,README.md,src` 순서로 반환됐는데, 검사 스크립트가 특정 순서 문자열(`README.md,logs,src`)과 비교해 실패로 판정했다.

**확인된 원인**
- 첫 증상은 T-008과 같은 PowerShell/Bash 문법 혼동이다.
- 두 번째 증상은 zip 구조의 문제가 아니라 검증 명령이 집합 비교가 아닌 순서 의존 문자열 비교를 사용한 문제다.

**조치**
- Python 글자 수 확인은 PowerShell here-string 파이프로 재실행했다.
- zip 최상위 구조 검사는 순서와 무관하게 허용된 top-level 집합(`src`, `README.md`, `logs`)인지 확인하도록 바꿔 재검증했다.
- 재검증 결과 zip 구조, JSON 파싱, Python compile, 비밀정보 패턴 검색이 모두 통과했다.

**재발 방지**
- PowerShell에서는 Bash heredoc 문법을 사용하지 않는다.
- zip 내부 구조 검증에서 엔트리 순서는 의미가 없으므로, top-level 검사는 항상 집합 기준으로 수행한다.

---

### T-017 · PowerShell JSON 검사 중 UTF-8 한국어 taxonomy 오탐
**발생 상황**
- `submission.zip` 압축 해제본의 `taxonomy.json`을 PowerShell `Get-Content -Raw | ConvertFrom-Json`으로 파싱해 보려 했다.

**증상**
- PowerShell 출력에서 한국어가 mojibake로 보였고, `ConvertFrom-Json`이 `Invalid object passed in` 오류를 냈다.

**확인된 원인**
- Windows PowerShell의 기본 인코딩 처리와 콘솔 출력 경로가 UTF-8 한국어 JSON을 안정적으로 다루지 못해 발생한 검증 명령 오탐이었다.
- 같은 파일을 Python `json` 모듈과 `python -m json.tool`로 검증했을 때 repo 원본과 zip 압축 해제본 모두 정상 JSON으로 확인됐다.

**조치**
- JSON 유효성 최종 판정은 Python `json` 파서 기준으로 교차확인했다.
- README 한글 문구 확인은 `rg`와 UTF-8 `Get-Content` 출력으로 확인했다.
- PowerShell heredoc 형태의 Python 실행 시도는 T-008의 기존 재발 유형과 같아, 이후 PowerShell에서는 here-string 파이프 또는 `python -c`를 사용했다.

**재발 방지**
- UTF-8 한국어 JSON의 유효성 검증은 PowerShell `ConvertFrom-Json` 대신 `python -m json.tool` 또는 Python `json.loads(..., encoding='utf-8')` 경로를 우선 사용한다.
- PowerShell에서 Bash heredoc 문법을 사용하지 않는다.

---

### T-016 · zip 검증 중 디렉터리 엔트리의 로그 확장자 오탐
**발생 상황**
- `out/submission.zip` 생성 후 zip 내부 로그 파일 확장자 검증을 수행했다.

**증상**
- 검증 명령이 `logs/worktrees/`, `logs/worktrees/detail-type-category/` 디렉터리 엔트리를 로그 파일처럼 취급해 `invalid log extensions` 오류를 냈다.

**확인된 원인**
- PowerShell의 `ZipFile` 엔트리 목록에는 파일뿐 아니라 일부 디렉터리 엔트리도 포함된다.
- 최초 검증 조건은 `FullName` 기준으로만 필터링해 디렉터리 엔트리를 제외하지 못했다.
- zip 내부 파일 자체에는 문제가 없었고, 로그 파일 5개는 모두 `.jsonl` 형식이었다.

**조치**
- zip 검증 조건을 `ZipArchiveEntry.Name`이 있는 파일 엔트리만 로그 확장자 검사 대상으로 삼도록 바꿔 재검증했다.
- 재검증 결과 파일 엔트리 12개, 디렉터리 엔트리 3개, 로그 파일 5개, 최상위 `logs`, `README.md`, `src`만 존재함을 확인했다.

**재발 방지**
- zip 내부 목록 검증 시 파일 확장자 검사는 파일 엔트리만 대상으로 한다.
- 디렉터리 엔트리는 구조 검증에는 포함하되, 파일 확장자 검증에서는 제외한다.

---

### T-015 · worktree 파일 패치 시 기준 경로 혼동
**발생 상황**
- S7.7 dedup cross-category 독립 재계산 스크립트를 보강하기 위해 `apply_patch`를 실행했다.

**증상**
- 패치 도구가 기본 작업 기준을 메인 루트(`2nd`)로 잡아 `tools/run_s7_7_dedup_cross_category_recheck.py`를 찾지 못했다.

**확인된 원인**
- 실제 작업 파일은 `.worktrees/detail-type-category/tools/` 아래에 있었지만, 패치 입력에는 worktree 상대 경로가 포함되지 않았다.

**조치**
- 패치 대상 경로를 `.worktrees/detail-type-category/tools/run_s7_7_dedup_cross_category_recheck.py`로 명시해 동일 변경을 정상 적용했다.
- 이후 모든 편집 패치는 worktree 상대 경로를 명시해 적용했다.

**재발 방지**
- worktree에서 작업 중이어도 `apply_patch`는 현재 세션 기준 루트가 다를 수 있으므로, 패치 전 대상 파일의 실제 상대 경로를 확인한다.
- shell 명령은 `workdir`로 worktree를 지정하고, `apply_patch`는 패치 파일 경로에 worktree prefix를 명시한다.

### T-014 · invalid fixture 이중 함정으로 회귀 감지력 약화 발견
**발생 상황**
- 독립 교차검증에서 `invalid_material_ratio_status.json`, `invalid_detail_type_parent.json`, `invalid_out_of_scope_category.json` 3건이 표적 규칙 외에 `part: "unknown"` + `material_part` 미표시라는 두 번째 위반을 부수적으로 포함하고 있음을 확인.

**증상**
- 검증은 exit code 기반("실패하면 통과")인데, 함정이 둘이면 표적 규칙(예: detail_type 부모 검사)이 회귀로 사라져도 `material_part` 오류 때문에 exit 1이 유지되어 회귀가 은폐됨. `validate.py`로 3건을 실행하면 각각 오류가 2건씩 나옴.

**확인된 원인**
- 초기 fixture 작성 시 소재부를 `unknown`으로 둔 채 `missing_fields`에 `material_part`를 넣지 않아, T-013에서 도입한 material_part 규칙과 우연히 겹쳤다. 표적 규칙과 무관한 부수 위반이었다.

**조치**
- 3건 모두 `part: "unknown"` → `part: "shell"`로 바꿔 표적 규칙 하나만 위반하도록 격리(각 fixture 오류 1건으로 확인, `invalid_unknown_detail_type.json`은 같은 개념의 schema+custom 2건이라 유지).
- material_part 규칙을 양방향으로 강화(`validate.py`: 모든 part가 알려졌는데 `material_part`가 `missing_fields`에 있으면 차단)하고, 역방향 회귀 fixture `invalid_spurious_material_part.json` 추가.
- 전체 검증 스위트(15개 저장 명령 + 기본 평가) 재실행으로 무회귀 확인.

**재발 방지**
- 새 negative fixture는 "표적 규칙 하나만 위반"을 원칙으로 하고, 추가 시 `validate.py` 실행 결과 오류가 표적 1건(또는 같은 개념의 묶음)인지 확인한다.
**발생 상황**
- `validate.py`에 `part: "unknown"` 소재가 있으면 `quality.missing_fields`에 `material_part`가 있어야 한다는 custom check를 추가한 뒤 기존 검증을 재실행했다.

**증상**
- `tests/fixtures/schema/valid_top.json`이 더 이상 valid fixture로 통과하지 않았다.
- `python tools\run_expanded_validation.py`가 `all_commands_passed false`로 실패했다.
- 실패 항목은 S7.5 `expanded_dummy`, `codex_subset`, `real_sanity` fixture의 `quality.missing_fields`에 `material_part`가 없는 케이스였다.

**확인된 원인**
- SKILL과 요구사항 계약에는 `part: "unknown"`이면 `material_part`를 missing으로 기록해야 한다는 기준이 있었지만, validator가 이를 강제하지 않아 과거 fixture 일부가 느슨한 상태로 남아 있었다.
- `tools/generate_expanded_validation_fixtures.py`는 일부 패턴에만 `material_part`를 수동으로 넣고, 모든 `unknown` 소재에 일반 적용하지 않았다.
- `codex_subset/expected_products.json`과 `real_sanity/actual_products.json`은 보존 fixture라 S7.5 생성기 재실행만으로 자동 보정되지 않았다.

**조치**
- `validate.py`에 `saw_unknown_part` 검사를 추가하고, `quality.missing_fields`에 `material_part`가 없으면 validation error를 반환하도록 했다.
- `valid_top.json`에 `material_part`를 추가했다.
- `generate_expanded_validation_fixtures.py`의 `structured_product()`에서 `materials`에 `part: "unknown"`이 있으면 `material_part`를 자동으로 missing field에 포함하도록 수정했다.
- 생성기를 재실행해 S7.5 expanded/real expected fixture를 갱신했다.
- 생성기가 덮어쓰지 않는 보존 fixture인 `codex_subset/expected_products.json`, `real_sanity/actual_products.json`은 같은 계약 기준으로 기계적으로 보정했다.
- 재실행 결과 `python tools\run_expanded_validation.py`, `python tools\run_full_page_dummy_validation.py`, `python tools\run_size_info_pattern_validation.py`가 모두 통과했다.

**재발 방지**
- SKILL 또는 요구사항 계약의 품질 필드 연결 규칙이 바뀌면 validator와 fixture 생성기를 동시에 확인한다.
- 보존 actual/expected fixture는 생성기 재실행으로 덮어써지지 않을 수 있으므로, 새 validator 규칙 추가 후 전체 fixture validation을 반드시 실행한다.

---

### T-012 · smoke20 Codex 재실행 중 도구 타임아웃과 material_part 누락
**발생 상황**
- `배색 폴리에스터` 보수 라벨 기준을 반영한 뒤, S7.7 `full_page_codex_smoke20` actual을 새 SKILL 기준으로 재실행했다.

**증상**
- 첫 `python tools\run_full_page_codex_smoke20_cli.py --fixture full_page_codex_smoke20 --timeout 2400` 실행이 외부 도구 호출 제한 300초에 걸려 중단됐다.
- 중단 직후 하위 `codex.exe`와 `python.exe` 프로세스가 계속 실행 중이었다.
- 해당 실행이 종료된 뒤 actual은 저장됐지만, `part: "unknown"` 소재가 있는 일부 케이스에서 `quality.missing_fields`의 `material_part`가 누락되어 smoke20 micro recall이 97.32%로 떨어졌다.

**확인된 원인**
- Codex CLI 20건 변환은 300초보다 오래 걸릴 수 있는데, 래퍼 내부 timeout과 도구 호출 timeout을 다르게 설정했다.
- 기존 SKILL은 `part: "unknown"` 사용을 지시했지만, `unknown` 소재가 있을 때 반드시 `quality.missing_fields`에 `material_part`를 추가하라는 연결 규칙이 충분히 명시되어 있지 않았다.

**조치**
- 실행 중이던 `codex.exe` 프로세스가 종료될 때까지 `Wait-Process`로 대기하고, 부분 산출물 상태를 확인했다.
- `docs/requirements-contract.md`와 `src/skills/product-agentizer/SKILL.md`에 `part: "unknown"`이면 `quality.missing_fields`에 `material_part`를 추가한다는 규칙을 명시했다.
- 도구 호출 timeout을 900초로 늘려 `python tools\run_full_page_codex_smoke20_cli.py --fixture full_page_codex_smoke20 --timeout 3600`을 재실행했다.
- 재실행 후 smoke20 actual schema-valid 20/20, micro precision/recall 100.00%, dedup accuracy 100.00%를 확인했다.

**재발 방지**
- Codex CLI 다건 변환은 외부 도구 호출 timeout을 내부 `--timeout`보다 충분히 길게 잡는다.
- `unknown`처럼 품질 필드와 연결되는 값은 추출 지침과 품질 기록 지침을 한 문단 안에서 함께 명시한다.
- timeout 발생 시 같은 fixture를 곧바로 중복 실행하지 않고, 남은 하위 프로세스와 부분 산출물을 먼저 확인한다.

---

### T-011 · S7.8 size_info 패턴 검증 스크립트 상수 누락과 라벨 과정규화
**발생 상황**
- S7.8 `size_info_patterns` fixture와 검증 스크립트를 만든 뒤, `python tools\run_size_info_pattern_validation.py`를 실행했다.

**증상**
- 첫 실행에서 `NameError: SYNTHETIC_URL_PREFIX`가 발생했다.
- 상수 누락을 고친 뒤 실제 Codex CLI actual 기준 검증을 실행하자 schema는 통과했지만 `size_info` precision/recall이 94.85%로 목표치 95%에 미달했다.
- 실패 사례는 `measurement_table` 1건과 `comparison_guide` 4건에 집중됐다.

**확인된 원인**
- `synthetic_source_check()`에서 합성 URL prefix를 확인하도록 작성했지만, 파일 상단에 `SYNTHETIC_URL_PREFIX` 상수를 정의하지 않았다.
- `measurement_table` expected가 입력에는 없는 `cm` 단위를 결과 행에 덧붙이고 있었다.
- `comparison_guide` expected가 입력 문장의 비교 가이드 문구를 짧게 정규화했지만, actual은 입력 문구 전체를 보존했다. 계약상 비교 가이드 문구는 정적 size_info 근거로 보존할 수 있으므로 actual이 틀린 것이 아니라 expected 라벨이 과도하게 정규화된 상태였다.

**조치**
- `tools/run_size_info_pattern_validation.py`에 `SYNTHETIC_URL_PREFIX` 상수를 추가했다.
- `tools/generate_size_info_pattern_fixtures.py`의 `measurement_table` expected를 입력 근거와 동일하게 수정했다.
- `comparison_guide` expected를 입력 문구 전체 보존 기준으로 보정했다.
- 기존 실제 Codex actual은 유지한 채 fixture를 재생성하고 `python tools\run_size_info_pattern_validation.py`를 재실행했다.
- 최종 결과는 schema-valid 48/48, `size_info` precision/recall 100.00%, TP/FP/FN 97/0/0, recommendation_noise false positive 0건으로 통과했다.

**재발 방지**
- 새 source policy check를 추가할 때는 상수 정의와 생성기 prefix가 같은 파일에서 함께 검증되는지 확인한다.
- 실제 Codex actual이 입력 근거를 더 충실히 보존한 경우, 수치를 맞추기 위해 actual을 깎기보다 expected 라벨이 기준 계약과 입력 근거에 맞는지 먼저 확인한다.
- 합성 fixture라도 expected는 입력에 없는 단위나 축약 표현을 임의로 만들지 않는다.

---

### T-010 · S7.7 50건 평가 결과 출력 과다
**발생 상황**
- `full_page_codex_subset` 50건 실제 Codex CLI actual을 생성한 뒤, 평가 결과를 `--pretty`로 확인했다.

**증상**
- 평가 결과 JSON 전체가 길어져 콘솔 출력이 과도하게 커졌고, 필요한 핵심 지표를 즉시 파악하기 어려웠다.

**확인된 원인**
- `tests/evaluate_product_agentizer.py --pretty`는 케이스별 차이와 상세 지표를 모두 출력하므로 50건 이상 검증에서는 대화형 확인용으로 너무 길다.
- 보고서 저장용 전체 JSON과 사람에게 보여줄 요약 지표의 용도를 분리하지 않았다.

**조치**
- PowerShell here-string으로 Python 요약 스크립트를 실행해 `summary`, `validations`, micro metrics, field metrics, dedup metrics, worst cases만 추출했다.
- 이후 `tools/run_full_page_dummy_validation.py`가 필요한 지표를 `docs/reports/s7-7-full-page-dummy-validation-results.json`과 report에 보존하도록 갱신했다.

**재발 방지**
- 30건 이상 평가 결과를 대화형으로 확인할 때는 `--pretty` 전체 출력 대신 요약 추출 스크립트나 report generator를 사용한다.
- 전체 raw 결과는 파일에 보존하고, 대화 보고에는 수용 기준과 원인 분석에 필요한 지표만 선별한다.

---

### T-009 · S7.7 Codex subset 대표성·blind 실행성 문제
**발생 상황**
- S7.7 실제 Codex CLI 검증을 20건 smoke부터 진행하려고 기존 `full_page_codex_subset` 구성을 확인했다.

**증상**
- 기존 50건 subset이 전체 fixture의 앞쪽 50건을 그대로 사용해 아우터 중심으로 치우쳐 있었다.
- 첫 Codex smoke 실행은 repo 루트 read-only에서 수행되어, 모델이 원하면 `tests/fixtures/.../expected_products.json`을 읽을 수 있는 상태였다.
- 첫 격리 workspace 실행 후 micro precision 0.8629, micro recall 0.9149가 나왔고, 주요 차이는 `size_info`, `tpo_tags`, `materials.part`, `quality.missing_fields`에서 발생했다.

**확인된 원인**
- subset 생성 로직이 대표성 기준 없이 `sources[:subset_size]`를 사용했다.
- repo 루트 실행은 expected fixture 접근 가능성을 차단하지 못해 blind extraction 검증 요건과 충돌했다.
- 일부 expected 라벨이 입력 텍스트 근거보다 강했다. 예를 들어 텍스트에는 `출근룩과 포멀`만 있는데 expected에 `layering`을 넣거나, `사이즈 옵션: M, L, XL`을 하나의 문자열로만 라벨링했다.
- 소재 부위가 명시되지 않은 표현을 `shell`로 라벨링한 케이스가 있어 Codex의 `unknown` 판단과 충돌했다.

**조치**
- `full_page_codex_subset` 50건과 `full_page_codex_smoke20` 20건을 category, density, detail_type, duplicate pair를 고려해 대표 선별하도록 생성기를 수정했다.
- `tools/run_full_page_codex_smoke20_cli.py`가 `out/full_page_codex_smoke20_workspace`에 skill과 reference만 복사한 격리 workspace에서 Codex CLI를 실행하도록 변경했다.
- expected 라벨을 입력 근거 기준으로 보정했다. 사이즈 옵션은 개별 값으로 비교하고, 텍스트에 없는 TPO는 제거하며, 부위 미상 소재는 `part: unknown`과 `material_part` missing으로 기록했다.
- 보완 후 `python tools\run_full_page_dummy_validation.py`를 재실행해 smoke20 schema-valid 20/20, micro precision/recall 100.00%, dedup accuracy 100.00%를 확인했다.

**재발 방지**
- 실제 Codex 성능 검증은 expected/actual fixture가 없는 격리 workspace에서 수행한다.
- subset 생성 시 단순 앞부분 slicing을 금지하고 category, density, detail_type, duplicate pair coverage를 확인한다.
- 낮은 지표가 나오면 먼저 fixture 라벨이 입력 텍스트 근거와 일치하는지 확인하고, 수치를 맞추기 위한 완화가 아니라 기준 계약 위반 여부를 분류한다.

---

### T-008 · PowerShell 환경에서 Bash heredoc 명령 사용
**발생 상황**
- S7.7 결과 JSON의 acceptance summary를 빠르게 출력하려고 Python one-liner를 실행했다.

**증상**
- PowerShell에서 `python - <<'PY'` 형태의 Bash heredoc 문법을 사용해 `Missing file specification after redirection operator` 오류가 발생했다.

**확인된 원인**
- 현재 셸은 PowerShell이므로 Bash heredoc 리다이렉션 문법을 사용할 수 없다.
- 이전에도 Windows/PowerShell 환경에서 명령 래퍼 차이로 검증 명령 문제가 발생한 적이 있어 재발 가능성이 있다.

**조치**
- PowerShell here-string을 Python stdin으로 전달하는 `@' ... '@ | python -` 형식으로 바꿔 같은 결과를 확인했다.
- S7.7 검증 자체는 이미 `python tools\run_full_page_dummy_validation.py`로 통과한 상태였고, 이 오류는 결과 조회용 보조 명령에서만 발생했다.

**재발 방지**
- PowerShell 환경에서 여러 줄 Python 스니펫을 실행할 때는 `@' ... '@ | python -` 형식을 사용한다.
- Bash 문법이 필요한 명령은 현재 셸을 먼저 확인한 뒤 사용한다.

---

### T-007 · S7.7 단계 번호 보정 중 문서 문구 일시 불일치
**발생 상황**
- 실제 페이지형 합성 더미 검증 계획을 문서화하면서, 기존 `S7.6`이 이미 3단계 taxonomy 전환 작업에 사용되고 있음을 확인했다.
- 새 검증 단계를 `S7.7`로 조정하는 과정에서 문서 내 단계 번호와 문구를 일괄 보정했다.

**증상**
- 일괄 치환 중 Decisionlog의 단계 흐름 문구가 일시적으로 부자연스럽게 변경되어, `S7.6(3단계 구조 개편)`과 `S7.7 실제 페이지형 합성 더미 검증`의 역할이 명확히 구분되지 않는 상태가 발생했다.

**확인된 원인**
- 새 단계 번호를 뒤늦게 `S7.6`에서 `S7.7`로 변경하면서, 전체 문맥을 고려하지 않은 기계적 치환이 일부 문장에 적용됐다.
- 문서 구조상 `S7.6`은 기존 3-level taxonomy 계획 문서에서 이미 쓰이고 있었으므로, 새 검증 단계는 별도 번호를 부여해야 했다.

**조치**
- Decisionlog의 단계 흐름을 `S7.5 -> S7.6(3단계 구조 개편) -> S7.7 -> S8`로 수정했다.
- `docs/full-page-dummy-validation-plan.md`, `docs/implementation-plan.md`, `docs/validation-plan.md`, `docs/README.md`, `Decisionlog.md`, `Worklog.md`에서 실제 페이지형 합성 더미 검증 참조가 `S7.7`로 통일됐는지 확인했다.
- 실제 페이지형 합성 더미 검증이 이전 단계 번호나 이전 파일명 형태로 남아 있지 않음을 검색으로 확인했다.

**재발 방지**
- 새 단계를 추가하기 전 기존 계획 문서와 report 문서에서 사용 중인 단계 번호를 먼저 검색한다.
- 단계 번호를 변경할 때는 전체 일괄 치환만 사용하지 않고, 역할이 겹치는 기존 단계가 있는지 `rg "S7\\." docs`로 확인한다.
- Worklog와 Decisionlog의 단계 흐름 문장은 최종 커밋 전 별도 검색으로 재확인한다.

---

### T-006 · S7.5 생성기 stale real_sanity ID 잔존
**발생 상황**
- 3단계 taxonomy 전환 후 `real_sanity` fixture와 보고서를 현재 ID로 정리했지만, spec 재리뷰에서 fixture 생성기 내부에 과거 ID가 남아 있음이 발견됐다.

**증상**
- `tools/generate_expanded_validation_fixtures.py`에 `real_outer_limelike_cardigan_2101205`, `real_outer_lenina_cardigan_4332165`가 남아 있었다.
- 같은 위치에 `wool v neck cardigan`, `cardigan_RED`처럼 현재 실제 공개 snippet 입력에서 제거한 영문 raw 단서도 남아 있었다.
- 생성기를 다시 실행하면 현재 committed `real_sanity` fixture와 다른 산출물이 만들어질 수 있어 S7.5 재현성 원칙과 충돌했다.
- 또한 생성기가 최신 synthetic fixture에서 `codex_subset` expected/source를 다시 쓰면서 historical `detail_type: null` 보존 정책과 충돌하는 diff를 만들었다.

**확인된 원인**
- `real_sanity` fixture 파일을 먼저 수동 정리한 뒤, 같은 값을 생성하는 `tools/generate_expanded_validation_fixtures.py`의 real_sanity spec과 duplicate label을 함께 갱신하지 않았다.
- `codex_subset`은 historical Codex 실행 보존 세트인데, 생성기에는 여전히 최신 synthetic fixture에서 subset을 파생해 쓰는 로직이 남아 있었다.

**조치**
- 생성기의 old `real_sanity` product_id를 현재 fixture ID로 교체했다.
- Lenina source title, product text, material evidence를 현재 한국어 snippet과 일치하도록 수정했다.
- 생성기가 `codex_subset`을 덮어쓰지 않도록 변경하고, 해당 정책을 보고서·상세 가이드·구현 계획서에 문서화했다.
- `python tools\generate_expanded_validation_fixtures.py` 재실행 후 `codex_subset` diff가 0임을 확인했다.
- `python tools\run_expanded_validation.py`를 재실행해 `all_commands_passed=true`와 SHA-256 해시 일치를 확인했다.
- spec 재리뷰에서 Pass와 Task 11 진행 가능 판정을 받았다.

**재발 방지**
- fixture 파일을 직접 보완하면 같은 fixture를 생성하는 스크립트와 결과 JSON 해시도 함께 갱신한다.
- historical actual 보존 세트는 생성기 재생성 대상인지, committed fixture 보존 대상인지 명시한다.
- 생성기 재실행 후 `git diff -- tests/fixtures/codex_subset`처럼 보존 세트가 흔들리지 않았는지 별도로 확인한다.

---

### T-005 · docs/reports 경로 일괄 치환 중 중복 경로 발생
**발생 상황**
- S5/S6/S7.5 보고서를 `docs/reports/`로 이동한 뒤, README와 작업 문서의 경로 문자열을 일괄 갱신했다.

**증상**
- `docs/s7-expanded-validation-report.md`를 `docs/reports/s7-expanded-validation-report.md`로 바꾼 뒤, 다시 `s7-expanded-validation-report.md` 단독 문자열을 치환하면서 일부 경로가 `docs/reports/reports/...` 형태로 중복됐다.

**확인된 원인**
- 긴 경로 치환과 파일명 단독 치환을 같은 반복문에서 순차 적용해, 이미 갱신된 경로의 파일명 부분이 한 번 더 치환됐다.

**조치**
- 전체 문서에서 `docs/reports/reports/`를 `docs/reports/`로 되돌렸다.
- 활성 문서와 스크립트 기준으로 중복 경로와 이전 루트 보고서 경로가 남아 있지 않음을 확인했다. 단, Worklog/Troubleshootinglog에는 이동 전 경로와 오류 사례 설명을 감사 추적용으로 남겼다.

**재발 방지**
- 경로 일괄 치환은 긴 경로와 파일명 단독 치환을 섞지 않는다.
- 기계적 치환 직후 `rg "reports/reports|이전경로"`처럼 오류 패턴을 먼저 확인한다.

---

### T-004 · S7.5 확장 검증 fixture 생성·평가 래퍼 오류
**발생 상황**
- S7.5 확장 검증을 구현하면서 합성 100건, Codex subset 20건, 실제 공개 snippet 10건 fixture와 재현성 평가 결과를 생성했다.

**증상**
- fixture 생성기에서 duplicate case를 만들 때 `KeyError: 'product'`가 발생했다.
- 실제 공개 샘플 expected JSON 생성 후 schema 검증에서 일부 필드 구조가 맞지 않았다.
- `tests/evaluate_product_agentizer.py`를 custom 상대 경로로 실행하면 `relative_to(ROOT)` 처리에서 `ValueError`가 발생했다.
- Windows 콘솔 출력 경로에서 평가 결과 JSON의 한글 차이 토큰이 깨져 `docs/reports/s7-expanded-validation-results.json`에 읽기 어려운 값이 들어갔다.
- real sanity 평가에 Codex subset duplicate label을 잘못 사용하면 dedup 평가가 잘못된 기준으로 실행될 수 있었다.

**확인된 원인**
- duplicate 생성 시 wrapper 구조를 고려하지 않고 존재하지 않는 `product` 경로를 참조했다.
- 실제 공개 샘플 spec tuple에서 `size_info`, `missing_fields`, `ambiguous_fields` 위치가 분리되어 있지 않았다.
- 평가 스크립트가 전달받은 상대 경로를 repo root 기준으로 먼저 해석하지 않은 채 `relative_to(ROOT)`를 호출했다.
- Python stdout 인코딩이 Windows 콘솔 기본값을 따라가면서, 상위 검증 스크립트가 UTF-8로 캡처할 때 한글이 손상됐다.
- fixture 그룹마다 중복 라벨 범위가 다르므로 전용 `duplicate_labels.json`이 필요했다.

**조치**
- duplicate title 참조를 `structured_product.product.title` 경로로 수정했다.
- 실제 공개 샘플 spec 구조를 `size_info`, `missing_fields`, `ambiguous_fields`로 명확히 분리했다.
- 평가 스크립트가 상대 경로를 repo root 기준으로 resolve하고, 표시 경로 계산 실패 시 절대 경로로 fallback하도록 수정했다.
- 평가 스크립트의 stdout을 UTF-8로 고정해 결과 JSON의 한글 차이 토큰을 보존했다.
- `codex_subset`과 `real_sanity` 폴더에 각각 전용 `duplicate_labels.json`을 생성했다.
- `python tools\run_expanded_validation.py`를 재실행해 전체 명령 통과와 한글 결과 보존을 확인했다.

**재발 방지**
- wrapper가 있는 JSON fixture는 실제 저장 구조를 기준으로 경로를 참조한다.
- 새 fixture 그룹을 추가할 때는 source, expected, actual, duplicate labels를 같은 폴더에 함께 보존한다.
- 평가·검증 결과를 파일로 저장하는 Windows 환경에서는 stdout/stderr 인코딩을 명시한다.
- custom 경로를 받는 CLI 스크립트는 repo root 기준 상대 경로와 절대 경로를 모두 허용하도록 처리한다.

---

### T-003 · S7 오류 fixture 기대 실패 검증 명령의 종료 코드 처리 오류
**발생 상황**
- S7 제출 README 작성 후, invalid schema fixture 3건이 기대대로 실패하는지 PowerShell 명령으로 확인했다.

**증상**
- `validate.py`가 invalid fixture를 정상적으로 차단해 exit code `1`을 반환했지만, 기대 실패를 통과로 해석하려던 PowerShell 검증 명령 자체가 exit code `1`로 종료됐다.

**확인된 원인**
- `python ... | Out-Null; if ($LASTEXITCODE -ne 1) { exit 1 }` 형태의 명령은 기대한 exit code를 확인하더라도 마지막 native command의 `$LASTEXITCODE`가 남아 PowerShell 프로세스 종료 코드에 영향을 줄 수 있었다.
- 오류 fixture 자체의 문제는 아니며, 검증 래퍼 명령의 종료 코드 처리 문제였다.

**조치**
- 명령을 `if ($LASTEXITCODE -eq 1) { exit 0 } else { exit 1 }` 형태로 바꾸어 기대 실패를 명시적으로 성공 처리했다.
- invalid fixture 3건 모두 수정한 명령으로 재검증했고, 기대대로 통과했다.

**재발 방지**
- 기대 실패를 확인하는 PowerShell 검증 명령은 마지막에 `exit 0` 또는 `exit 1`을 명시해 래퍼 명령의 의미를 분명히 한다.
- 의도된 실패 fixture 자체는 Troubleshooting 대상이 아니지만, 기대 실패를 감싸는 검증 명령이 잘못되어 작업을 우회하게 만들면 T-ID로 기록한다.

---

### T-002 · S6 최종 검증 중 schema fixture 경로 오인
**발생 상황**
- S6 문서화와 커밋 전 검증을 수행하면서 schema fixture 개별 검증 명령을 실행했다.

**증상**
- `tests\fixtures\valid_outer.json`, `tests\fixtures\valid_top.json` 경로로 `validate.py`를 실행해 `No such file or directory` 오류가 발생했다.

**확인된 원인**
- 실제 fixture는 `tests\fixtures\schema\valid_outer.json`, `tests\fixtures\schema\valid_top.json`에 있었으나, 검증 명령을 작성할 때 중간 `schema` 디렉터리를 빠뜨렸다.
- 오류 JSON fixture의 의도된 실패와 달리, 이 문제는 검증 명령 경로 오인이었다.

**조치**
- `rg --files tests src\skills\product-agentizer`와 `Get-ChildItem -Recurse tests\fixtures`로 실제 fixture 구조를 확인했다.
- 올바른 경로로 정상 fixture 2건, 의도된 실패 fixture 3건, S6 Codex 산출물, 통합 평가 스크립트를 재실행했다.
- 최종 검증은 모두 기대 결과와 일치함을 확인했다.

**재발 방지**
- 개별 fixture 검증 명령을 작성하기 전에 `rg --files tests\fixtures`로 실제 경로를 먼저 확인한다.
- README의 기본 검증 명령에는 Git에 포함되지 않는 `out/` 산출물 검증을 넣지 않고, S6 재현 절차는 `docs/reports/s6-codex-cli-report.md`에 분리한다.

---

### T-001 · S6 Codex CLI 검증 중 전역 marketplace·출력 schema·한글 stdin 문제
**발생 상황**
- S6에서 로컬 플러그인 marketplace 등록, Codex CLI 실제 변환, 질의 시연을 검증했다.

**증상**
- `codex plugin list`가 현재 작업과 무관한 기존 전역 marketplace 설정 때문에 실패했다.
- `codex exec --output-schema src\skills\product-agentizer\references\schema.json` 실행 시 Codex response format이 `allOf`를 허용하지 않아 실패했다.
- PowerShell here-string을 `codex exec` stdin으로 직접 넘기면 한글 입력이 일부 깨져 표시됐다.

**확인된 원인**
- 기존 전역 marketplace `openbell-guard-local`이 지원 manifest를 포함하지 않는 경로를 가리키고 있었다.
- `schema.json`은 JSON Schema draft 2020-12 검증용이며, Codex response format의 지원 subset보다 넓은 `allOf` 조건부 검증을 사용한다.
- Windows PowerShell 파이프의 외부 프로세스 stdin 인코딩 경로에서 한글이 안정적으로 전달되지 않았다.

**조치**
- 사용자의 전역 Codex 설정은 임의 수정하지 않았다.
- 임시 `CODEX_HOME=out\codex-s6-home`에서 repo marketplace 등록과 플러그인 설치를 별도 검증했다.
- 실제 변환은 `--output-schema` 없이 raw JSON을 생성한 뒤 `validate.py`로 schema와 custom check를 검증했다.
- 한글 상품 입력은 Python subprocess가 UTF-8로 fixture를 읽어 `codex exec` stdin에 전달하도록 우회했다.
- 질의 시연은 인코딩 안정성을 위해 질의 의도는 ASCII로 전달하고 한국어 답변을 요구했다.

**재발 방지**
- 최종 제출 전 Codex CLI 시연 명령은 `docs/reports/s6-codex-cli-report.md`의 우회 절차를 따른다.
- 전역 plugin browser/install까지 완전히 재현하려면 사용자가 stale marketplace를 제거하거나 유효한 manifest 경로로 수정해야 한다.
- `schema.json`은 `validate.py`의 입력으로 유지하고, Codex `--output-schema`에는 그대로 사용하지 않는다.
