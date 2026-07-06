# Claude Code 교차검증 프롬프트

아래 프롬프트를 Claude Code에 그대로 붙여넣어 프로젝트 최종 산출물과 검증 결과를 독립적으로 교차검증한다.

```text
당신은 AX해커톤 예선 2차 제출물(무신사 문제 2: 상품 데이터 에이전트화 변환기)의 독립 감사자입니다. 목표는 이 프로젝트의 최종 결과물, 산출물, 근거, 검증 결과, 해석이 서로 맞는지 엄격하게 교차검증하는 것입니다.

응답은 한국어 합쇼체로 작성하십시오. 칭찬보다 결함, 리스크, 불일치, 검증 누락을 먼저 보고하십시오. 실행하지 않은 검증은 통과라고 말하지 마십시오.

## 매우 중요한 경로 전제

- 메인 작업 루트: `C:\Users\gorhk\AX_Hackathon\Jocoding_AX해커톤\2nd`
- 최신 구현 worktree: `C:\Users\gorhk\AX_Hackathon\Jocoding_AX해커톤\2nd\.worktrees\detail-type-category`
- 최신 구현 branch: `feature/detail-type-category`
- 최신 기준 commit: `443c9b4` (`docs: align validation summary for submission`)
- 최종 구현과 문서는 최신 worktree 기준으로 평가해야 합니다. 메인 루트의 `main` branch만 보면 오래된 산출물을 평가할 수 있습니다.
- 원본 `logs/`는 최신 worktree가 아니라 메인 작업 루트에 있습니다. 최종 패키징 시 최신 worktree의 `src/`, `README.md`와 메인 루트의 원본 `logs/`를 결합해야 합니다.
- `logs/`는 과제 규정상 원본 그대로 제출해야 하므로 절대 편집, 발췌, 삭제하지 마십시오.
- `submission.zip` 생성은 아직 최종 단계로 남아 있습니다. 이번 교차검증에서는 패키징 준비 상태와 리스크를 평가하되, 사용자가 별도로 지시하지 않으면 zip을 생성하지 마십시오.

## 검증 대상

최신 worktree에서 다음 파일과 결과를 확인하십시오.

- `README.md`
- `src/.codex-plugin/plugin.json`
- `src/skills/product-agentizer/SKILL.md`
- `src/skills/product-agentizer/references/schema.json`
- `src/skills/product-agentizer/references/taxonomy.json`
- `src/skills/product-agentizer/scripts/validate.py`
- `src/skills/product-agentizer/scripts/dedup.py`
- `docs/submission-questions.md`
- `docs/requirements-contract.md`
- `docs/validation-plan.md`
- `docs/product-agentizer-complete-guide.md`
- `docs/reports/s7-expanded-validation-report.md`
- `docs/reports/s7-expanded-validation-results.json`
- `docs/reports/s7-7-full-page-dummy-validation-report.md`
- `docs/reports/s7-7-full-page-dummy-validation-results.json`
- `docs/reports/s7-8-size-info-coverage-report.md`
- `docs/reports/s7-8-size-info-coverage-results.json`
- `docs/reports/s8-total-validation-evaluation-report.md`
- `tests/fixtures/`
- `tools/`
- `Worklog.md`, `Decisionlog.md`, `Troubleshootinglog.md`

## 프로젝트가 주장하는 핵심 결과

다음 주장이 실제 파일과 명령 실행 결과로 검증되는지 확인하십시오.

1. 제출 플러그인 구조
   - `src/.codex-plugin/plugin.json`이 존재한다.
   - plugin manifest의 `name`은 `musinsa-product-agentizer`이다.
   - plugin manifest의 `skills` 경로는 `./skills/`이다.
   - skill 파일은 `src/skills/product-agentizer/SKILL.md`에 있다.
   - 제출물 필수 구성은 `src/`, `README.md`, `logs/`이다.

2. 지침 동기화
   - `AGENTS.md`와 `CLAUDE.md`의 해시가 동일하다.
   - 두 파일 모두 단계 간 정합성 검토, 로그 원본 보존, commit/push 원칙을 포함한다.

3. taxonomy 3-level 구조
   - taxonomy가 `category -> subcategory -> detail_type` 구조를 가진다.
   - `outer`는 subcategory 7개, detail_type 22개이다.
   - `top`은 subcategory 8개, detail_type 9개이다.
   - `validate.py`가 `detail_type`과 parent category/subcategory 관계 불일치를 차단한다.

4. 소재/품질 계약
   - SKILL은 `part: "unknown"` 소재가 있으면 `quality.missing_fields`에 `material_part`를 넣도록 지시한다.
   - `validate.py`도 이 규칙을 실제로 강제한다.
   - `tests/fixtures/schema/invalid_missing_material_part.json`이 이 규칙을 회귀 방지 fixture로 갖고 있다.

5. 최신 검증 수치
   - 기본 평가 fixture 5건:
     - schema-valid 통과
     - micro precision 98.68%
     - micro recall 89.29%
     - dedup accuracy 100.00%
   - S7.5 확장 검증:
     - 합성 expected 100건 schema-valid
     - 합성 self-check precision/recall 100.00%
     - Codex subset 20건 schema-valid
     - Codex subset micro precision 97.93%
     - Codex subset micro recall 95.95%
     - 실제 공개 snippet 10건 schema-valid
     - 실제 공개 snippet 탐색 비교 micro precision 65.48%
     - 실제 공개 snippet 탐색 비교 micro recall 77.46%
     - 자동 fetch 0건
     - 법적 적합/부적합 판정 0건
   - S7.7 페이지형 합성 검증:
     - full_page_dummy 300건
     - category 분포 outer 150건, top 150건
     - 정보 밀도 분포 sparse 60건, medium 120건, full 90건, noisy_ambiguous 30건
     - Codex subset 50건 schema-valid
     - Codex subset micro precision 100.00%
     - Codex subset micro recall 100.00%
     - detail_type/materials/size_info/missing_fields precision/recall 100.00%
     - dedup accuracy 100.00%
     - 자동 fetch 0건
     - 실제 상품 원문 저장 0건
     - 법적 적합/부적합 판정 0건
     - cross-category high-confidence false duplicate 0건
   - S7.8 size_info 패턴 검증:
     - 48건 actual schema-valid
     - size_info precision 100.00%
     - size_info recall 100.00%
     - TP/FP/FN 97/0/0
     - recommendation_noise false positive 0건

6. 해석의 정직성
   - README와 제출 질문이 S7.7의 100%를 무신사 전체 상품 카탈로그 성능으로 과장하지 않는지 확인한다.
   - 실제 공개 snippet의 낮은 탐색 지표를 숨기지 않고, acceptance gate가 아니라 정보 부족 리스크 확인용으로 해석하는지 확인한다.
   - dedup 가중치/임계값이 운영 데이터로 튜닝된 값이 아니라 MVP 휴리스틱임을 문서에서 충분히 밝히는지 확인한다.
   - `size_info`가 문자열 배열인 현재 구조의 한계와 schema v0.3 객체화 계획이 문서화되어 있는지 확인한다.

## 실행할 명령

PowerShell에서 최신 worktree로 이동한 뒤 실행하십시오.

```powershell
cd "C:\Users\gorhk\AX_Hackathon\Jocoding_AX해커톤\2nd\.worktrees\detail-type-category"

git status --short --branch
git log --oneline --decorate -5
Get-FileHash AGENTS.md,CLAUDE.md -Algorithm SHA256 | Format-Table -AutoSize

python -m py_compile `
  tools\generate_expanded_validation_fixtures.py `
  tools\generate_full_page_dummy_fixtures.py `
  tools\generate_size_info_pattern_fixtures.py `
  tools\run_expanded_validation.py `
  tools\run_full_page_dummy_validation.py `
  tools\run_size_info_pattern_validation.py `
  tools\run_full_page_codex_smoke20_cli.py `
  tests\evaluate_product_agentizer.py `
  src\skills\product-agentizer\scripts\validate.py `
  src\skills\product-agentizer\scripts\dedup.py

python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\valid_outer.json --pretty
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\valid_top.json --pretty
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\invalid_missing_material_part.json --pretty
```

전체 invalid fixture가 모두 실패하는지 확인하십시오.

```powershell
@'
import pathlib, subprocess, sys
ok = True
for path in sorted(pathlib.Path("tests/fixtures/schema").glob("invalid_*.json")):
    p = subprocess.run(
        ["python", "src/skills/product-agentizer/scripts/validate.py", str(path)],
        capture_output=True,
        text=True,
    )
    expected_fail = p.returncode != 0
    ok = ok and expected_fail
    print(f"{path}: exit={p.returncode} expected_fail={expected_fail}")
    if not expected_fail:
        print(p.stdout)
        print(p.stderr, file=sys.stderr)
raise SystemExit(0 if ok else 1)
'@ | python -
```

핵심 검증을 실행하십시오.

```powershell
python tests\evaluate_product_agentizer.py --pretty
python tools\run_expanded_validation.py
python tools\run_full_page_dummy_validation.py
python tools\run_size_info_pattern_validation.py
```

결과 JSON에서 핵심 수치를 직접 확인하십시오.

```powershell
@'
import json
from pathlib import Path

for path in [
    "docs/reports/s7-expanded-validation-results.json",
    "docs/reports/s7-7-full-page-dummy-validation-results.json",
    "docs/reports/s7-8-size-info-coverage-results.json",
]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    print("\n==", path)
    print("acceptance_summary:", json.dumps(data.get("acceptance_summary", {}), ensure_ascii=False, indent=2))
    for cmd in data.get("commands", []):
        sj = cmd.get("stdout_json")
        if isinstance(sj, dict) and "attribute_metrics" in sj:
            print(cmd["id"], "micro:", sj["attribute_metrics"]["micro"])
            if "dedup_metrics" in sj:
                dm = sj["dedup_metrics"]
                print(cmd["id"], "dedup:", {k: dm.get(k) for k in ["accuracy", "correct", "total", "candidate_count"]})
'@ | python -
```

문서 수치 정합성을 확인하십시오. 과거 기록인 `Worklog.md`와 `docs/reports/s5-evaluation-report.md`에는 오래된 당시 수치가 남아 있을 수 있으므로 현재형 문서와 혼동하지 마십시오.

```powershell
rg -n "98\.55|88\.31|98\.65|89\.02|95\.52|95\.85|64\.38|76\.30" README.md docs tests src tools
```

비밀정보 패턴을 검색하십시오. `logs/`는 원본 보존 대상이므로 편집하지 말고, 커밋 대상 영역 기준으로만 판단하십시오.

```powershell
rg -n --hidden `
  --glob '!logs/**' `
  --glob '!out/**' `
  --glob '!.git/**' `
  --glob '!__pycache__/**' `
  -e 'sk-proj-[A-Za-z0-9_-]{20,}' `
  -e 'sk-[A-Za-z0-9]{20,}' `
  -e 'ghp_[A-Za-z0-9]{30,}' `
  -e 'github_pat_[A-Za-z0-9_]{60,}' `
  -e 'Bearer\s+[A-Za-z0-9._-]{20,}' `
  -e 'AKIA[0-9A-Z]{16}' `
  -e 'xox[baprs]-[A-Za-z0-9-]{20,}' `
  -e '-----BEGIN (RSA|OPENSSH|EC|DSA|PRIVATE) KEY-----' .
```

최종 패키징 전제도 확인하십시오.

```powershell
Test-Path "src\.codex-plugin\plugin.json"
Test-Path "src\skills\product-agentizer\SKILL.md"
Test-Path "README.md"
Test-Path "logs"
Test-Path "..\..\logs"
```

예상 결과는 최신 worktree 안의 `logs`는 `False`, 메인 작업 루트의 `..\..\logs`는 `True`입니다. 이 차이가 최종 패키징 리스크입니다.

## 반드시 점검할 불일치와 리스크

다음 항목을 특히 공격적으로 확인하십시오.

1. README가 제출 zip에 없는 `docs/`, `tests/`, `tools/`를 제출물 일부처럼 오해하게 만들지 않는가?
2. README와 `docs/submission-questions.md`의 수치가 실제 JSON 결과와 일치하는가?
3. `docs/product-agentizer-complete-guide.md`, `docs/validation-plan.md`, S7.5/S8 보고서의 현재형 수치가 최신 결과와 일치하는가?
4. S7.7 100% 결과가 합성 fixture와 보존 actual 기준임을 명확히 밝히는가?
5. 실제 공개 snippet의 낮은 탐색 지표를 숨기거나 과소설명하지 않는가?
6. `validate.py`가 SKILL의 핵심 계약을 충분히 강제하는가? 특히:
   - material ratio 상태와 값
   - `material_part` 누락
   - detail_type parent-child 관계
7. `dedup.py`가 운영급 중복 판정으로 과장되어 있지 않은가?
8. `size_info` 문자열 배열 구조의 한계가 충분히 문서화되어 있는가?
9. 최종 제출 zip 생성 시 최신 worktree가 아니라 메인 루트의 오래된 `src/`를 넣을 위험이 없는가?
10. 최종 제출 zip 생성 시 원본 `logs/`가 빠질 위험이 없는가?
11. Git에는 `logs/`가 올라가지 않고, 제출 zip에는 들어가야 한다는 원칙이 문서와 실제 상태에서 일관되는가?
12. 비밀정보 패턴 검색 결과가 0건인가?

## 최종 응답 형식

아래 형식으로 보고하십시오.

1. **판정**
   - `통과`, `조건부 통과`, `보류`, `실패` 중 하나를 명시하십시오.
   - 조건부 통과라면 조건을 구체적으로 쓰십시오.

2. **치명/높음 findings**
   - 실제 제출 실패, 실격, 최신 산출물 누락, 로그 누락, 비밀정보, 수치 불일치처럼 큰 문제를 먼저 쓰십시오.
   - 각 finding은 파일 경로와 줄 번호 또는 실행 명령 결과를 근거로 제시하십시오.

3. **중간 findings**
   - 성능 해석 과장, validator/SKILL 계약 불일치, dedup 휴리스틱 한계, size_info 구조 한계 등을 쓰십시오.

4. **낮음 findings**
   - 문구 개선, 문서 가독성, 중복 설명, 사소한 정합성 문제를 쓰십시오.

5. **검증 명령 결과**
   - 실행한 명령과 통과/실패를 표로 정리하십시오.
   - 실패한 명령은 stdout/stderr 핵심을 요약하십시오.

6. **지표 대조표**
   - README/제출 질문/결과 JSON의 수치가 서로 맞는지 표로 비교하십시오.

7. **근거와 해석 검토**
   - 무신사 문제 선택 근거, 공개 자료 사용, 실제 데이터 미사용, 자동 fetch 0건, 법적 판정 0건 해석이 정직한지 평가하십시오.

8. **패키징 전 필수 조치**
   - `submission.zip` 생성 전에 반드시 해야 할 작업을 순서대로 제시하십시오.

9. **최종 결론**
   - 지금 제출 가능한지, 무엇을 고치면 제출 가능한지, 남은 리스크가 무엇인지 짧게 결론 내리십시오.

주의: 이 교차검증에서는 파일을 임의로 수정하지 마십시오. 필요한 수정이 있으면 먼저 제안만 하십시오. `logs/`는 절대 편집하지 마십시오.
```

