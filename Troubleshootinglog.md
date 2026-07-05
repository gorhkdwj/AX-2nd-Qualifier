# Troubleshootinglog · AX해커톤 예선 2차 제출(무신사 문제 2)

실제 오류·실패·환경 문제·검증 실패·설계 충돌이 발생하면 기록한다. 같은 문제가 반복되면 새 T-ID를 만들기 전에 기존 T-ID를 먼저 확인한다. (규칙: CLAUDE.md / AGENTS.md 11절)

## 기록 형식
```
### T-00N · 문제 제목
**발생 상황** / **증상** / **확인된 원인** / **조치** / **재발 방지**
```

---

### T-004 · S7.5 확장 검증 fixture 생성·평가 래퍼 오류
**발생 상황**
- S7.5 확장 검증을 구현하면서 합성 100건, Codex subset 20건, 실제 공개 snippet 10건 fixture와 재현성 평가 결과를 생성했다.

**증상**
- fixture 생성기에서 duplicate case를 만들 때 `KeyError: 'product'`가 발생했다.
- 실제 공개 샘플 expected JSON 생성 후 schema 검증에서 일부 필드 구조가 맞지 않았다.
- `tests/evaluate_product_agentizer.py`를 custom 상대 경로로 실행하면 `relative_to(ROOT)` 처리에서 `ValueError`가 발생했다.
- Windows 콘솔 출력 경로에서 평가 결과 JSON의 한글 차이 토큰이 깨져 `docs/s7-expanded-validation-results.json`에 읽기 어려운 값이 들어갔다.
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
- README의 기본 검증 명령에는 Git에 포함되지 않는 `out/` 산출물 검증을 넣지 않고, S6 재현 절차는 `docs/s6-codex-cli-report.md`에 분리한다.

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
- 최종 제출 전 Codex CLI 시연 명령은 `docs/s6-codex-cli-report.md`의 우회 절차를 따른다.
- 전역 plugin browser/install까지 완전히 재현하려면 사용자가 stale marketplace를 제거하거나 유효한 manifest 경로로 수정해야 한다.
- `schema.json`은 `validate.py`의 입력으로 유지하고, Codex `--output-schema`에는 그대로 사용하지 않는다.
