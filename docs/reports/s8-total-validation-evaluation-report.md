# S8 총검증 및 평가 보고서

## 요약

- 검증 기준 작업물: `.worktrees/detail-type-category`
- Git branch: `feature/detail-type-category`
- 기준 commit: `321b9ae` (`test: align material part labeling`)
- 검증일: 2026-07-06 KST
- 결론: S8 패키징 직전 품질 기준으로 핵심 기능, 스키마, taxonomy 3-level 구조, 재현 검증, 비밀정보 스캔은 통과 상태다.
- 주의: 최신 구현은 별도 worktree에 있고, 원본 `logs/`는 메인 작업 디렉터리에만 있다. 최종 `submission.zip` 생성 시 최신 worktree의 `src/`, `README.md`와 메인 작업 디렉터리의 원본 `logs/`를 함께 포함해야 한다.

## 검증 범위

이번 총검증은 다음 항목을 대상으로 했다.

- 제출 플러그인 구조: `src/.codex-plugin/plugin.json`, `src/skills/product-agentizer/SKILL.md`, `references/`, `scripts/`
- 지침 파일 동기화: `AGENTS.md`, `CLAUDE.md`
- taxonomy 3-level 구조: `category -> subcategory -> detail_type`
- schema validator: 정상 fixture 통과와 비정상 fixture 차단
- 평가기: `tests/evaluate_product_agentizer.py`
- S7.5 확장 검증: 합성 100건, Codex subset 20건, 실제 공개 snippet 10건
- S7.7 페이지형 합성 검증: full-page dummy 300건, Codex subset 50건, smoke20 20건
- S7.8 size_info 패턴 검증: 48건
- dedup 검증: 중복 후보 판정과 cross-category false duplicate
- 보안 점검: 비밀정보 형태의 API key, token, private key 패턴 검색

## 실행 명령

```powershell
git status --short --branch
Get-FileHash AGENTS.md,CLAUDE.md -Algorithm SHA256
python -m py_compile tools\generate_expanded_validation_fixtures.py tools\generate_full_page_dummy_fixtures.py tools\generate_size_info_pattern_fixtures.py tools\run_expanded_validation.py tools\run_full_page_dummy_validation.py tools\run_size_info_pattern_validation.py tools\run_full_page_codex_smoke20_cli.py tests\evaluate_product_agentizer.py src\skills\product-agentizer\scripts\validate.py src\skills\product-agentizer\scripts\dedup.py
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\valid_outer.json
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\valid_top.json
python tests\evaluate_product_agentizer.py --pretty
python tools\run_expanded_validation.py
python tools\run_full_page_dummy_validation.py
python tools\run_size_info_pattern_validation.py
rg -n --hidden --glob '!logs/**' --glob '!out/**' --glob '!.git/**' --glob '!__pycache__/**' -e 'sk-proj-[A-Za-z0-9_-]{20,}' -e 'sk-[A-Za-z0-9]{20,}' -e 'ghp_[A-Za-z0-9]{30,}' -e 'github_pat_[A-Za-z0-9_]{60,}' -e 'Bearer\s+[A-Za-z0-9._-]{20,}' -e 'AKIA[0-9A-Z]{16}' -e 'xox[baprs]-[A-Za-z0-9-]{20,}' -e '-----BEGIN (RSA|OPENSSH|EC|DSA|PRIVATE) KEY-----' .
git diff --check
```

## 구조 검증 결과

| 항목 | 결과 | 평가 |
|---|---:|---|
| 최신 worktree Git 상태 | 원격 branch와 동기화 | 통과 |
| `AGENTS.md` / `CLAUDE.md` 해시 | 동일 | 통과 |
| plugin manifest | `musinsa-product-agentizer`, `skills: ./skills/` | 통과 |
| 필수 skill 파일 | `src/skills/product-agentizer/SKILL.md` 존재 | 통과 |
| schema/taxonomy/scripts | 제출 플러그인 내부에 존재 | 통과 |
| taxonomy outer | subcategory 7개, detail_type 22개 | 통과 |
| taxonomy top | subcategory 8개, detail_type 9개 | 통과 |
| `logs/` 위치 | 메인 작업 디렉터리에만 존재 | 패키징 시 주의 |

## 스키마 검증 결과

정상 fixture인 `valid_outer.json`, `valid_top.json`은 모두 schema-valid로 통과했다.

비정상 fixture는 모두 실패해야 하는 방식으로 정상 차단됐다.

| fixture | 결과 | 차단 의미 |
|---|---:|---|
| `invalid_detail_type_parent.json` | 실패 처리 | detail_type이 선택 category/subcategory에 속하지 않으면 차단 |
| `invalid_material_ratio_status.json` | 실패 처리 | ratio 상태와 값 계약이 맞지 않으면 차단 |
| `invalid_missing_detail_type.json` | 실패 처리 | 3-level 구조의 필수 detail_type 누락 차단 |
| `invalid_missing_quality.json` | 실패 처리 | 품질 메타데이터 누락 차단 |
| `invalid_out_of_scope_category.json` | 실패 처리 | MVP 범위 밖 category 차단 |
| `invalid_unknown_detail_type.json` | 실패 처리 | taxonomy에 없는 detail_type 차단 |

평가: schema와 validator는 현재 계약 문서의 핵심 제약을 잘 강제하고 있다. 특히 3-level taxonomy 전환 이후 parent-child 관계 차단 fixture가 포함되어 있어, `재킷` 계열과 `코트` 계열 detail_type이 잘못된 부모에 붙는 문제를 방지할 수 있다.

## 기본 평가 fixture 결과

`python tests\evaluate_product_agentizer.py --pretty`의 기본 5건 fixture 결과는 다음과 같다.

| 지표 | 결과 |
|---|---:|
| schema-valid | expected 5/5, actual 5/5 |
| micro precision | 98.65% |
| micro recall | 89.02% |
| dedup accuracy | 100.00% |

차이는 주로 `materials`, `colors`, `seasons`, `tpo_tags`, `size_info`의 오래된 수작업 대표 fixture에서 발생했다. 이 fixture는 S7.7 이후의 주 acceptance 기준이 아니라 초기 평가기 동작 확인용에 가깝다.

평가: 제출 패키지에는 `tests/`가 포함되지 않으므로 직접 제출 리스크는 낮다. 다만 내부 문서를 보는 사람이 혼동할 수 있으므로, 시간이 남으면 기본 fixture를 최신 계약 기준으로 갱신하거나 legacy fixture임을 주석화하는 것이 좋다.

## S7.5 확장 검증 결과

| 항목 | 결과 |
|---|---:|
| 합성 expected 100건 schema-valid | True |
| 합성 self-check micro precision | 100.00% |
| 합성 self-check micro recall | 100.00% |
| 합성 self-check dedup accuracy | 100.00% |
| Codex subset 20건 schema-valid | True |
| Codex subset 20건 micro precision | 95.52% |
| Codex subset 20건 micro recall | 95.85% |
| Codex subset 20건 dedup accuracy | 100.00% |
| 실제 공개 snippet 10건 schema-valid | True |
| 실제 공개 snippet 10건 exploratory micro precision | 64.38% |
| 실제 공개 snippet 10건 exploratory micro recall | 76.30% |
| 실제 공개 snippet 10건 detail_type precision/recall | 100.00% / 100.00% |
| cross-category high-confidence false duplicate | 0건 |

평가: S7.5의 Codex subset은 acceptance 기준인 precision 95% 이상, recall 85% 이상을 통과한다. 실제 공개 snippet 10건의 탐색 지표는 낮지만, 이는 전체 페이지를 저장하지 않고 짧은 사실 snippet만 남긴 실험의 특성 때문에 expected label과 Codex의 보수적 missing 처리 방식이 충돌한 결과다. 따라서 이 수치는 운영 품질의 최종 지표가 아니라 "짧은 snippet 기준에서는 정보 부족 충돌이 발생한다"는 리스크 탐색 자료로 해석해야 한다.

## S7.7 페이지형 합성 검증 결과

| 항목 | 결과 |
|---|---:|
| full_page_dummy | 300건 |
| category 분포 | outer 150건, top 150건 |
| 정보 밀도 분포 | sparse 60건, medium 120건, full 90건, noisy_ambiguous 30건 |
| outer detail_type 최소 커버리지 | 6건 |
| top detail_type 최소 커버리지 | 14건 |
| expected schema-valid | True, 300건 |
| reference actual schema-valid | True, 300건 |
| self-check micro precision | 100.00% |
| self-check micro recall | 100.00% |
| self-check detail_type precision/recall | 100.00% / 100.00% |
| self-check dedup accuracy | 100.00% |
| Codex subset 50건 actual schema-valid | True, 50건 |
| Codex subset 50건 micro precision | 100.00% |
| Codex subset 50건 micro recall | 100.00% |
| Codex subset 50건 TP / FP / FN | 763 / 0 / 0 |
| Codex subset detail_type precision/recall | 100.00% / 100.00% |
| Codex subset materials precision/recall | 100.00% / 100.00% |
| Codex subset size_info precision/recall | 100.00% / 100.00% |
| Codex subset missing_fields precision/recall | 100.00% / 100.00% |
| Codex subset dedup accuracy | 100.00% |
| smoke20 schema-valid | True, 20건 |
| smoke20 micro precision/recall | 100.00% / 100.00% |
| smoke20 dedup accuracy | 100.00% |
| 자동 fetch | 0건 |
| 실제 상품 원문 저장 | 0건 |
| 법적 적합/부적합 판정 | 0건 |
| cross-category high-confidence false duplicate | 0건 |

평가: 현재 제출 품질 판단에서 가장 강한 근거는 S7.7이다. 실제 상품 페이지를 그대로 저장하지 않으면서도 sparse, medium, full, noisy_ambiguous 입력을 포함한 페이지형 합성 데이터를 만들었고, 실제 Codex CLI actual 50건에서 100%를 달성했다. 이는 현재 SKILL과 schema/taxonomy 계약이 같은 입력 계약 안에서는 매우 안정적으로 작동함을 보여준다.

다만 S7.7 역시 실제 운영 전체 카탈로그 검증은 아니다. 데이터가 합성 fixture이므로 "무신사 전체 상품 페이지에서 100% 성능"을 의미하지 않는다. 심사 제출 설명에서는 "실제 페이지형 입력을 모사한 재현 가능한 합성 검증"이라고 표현해야 한다.

## S7.8 size_info 패턴 검증 결과

| 항목 | 결과 |
|---|---:|
| expected schema-valid | True |
| actual schema-valid | True |
| actual checked | 48건 |
| size_info precision | 100.00% |
| size_info recall | 100.00% |
| TP / FP / FN | 97 / 0 / 0 |
| recommendation_noise false positive | 0건 |
| 자동 fetch | 0건 |
| 실제 상품 원문 저장 | 0건 |
| 법적 적합/부적합 판정 | 0건 |

패턴 그룹별로 `brand_numeric`, `comparison_guide`, `free_one_size`, `letter_comma`, `letter_slash`, `measurement_rows`, `measurement_table`, `mixed_parentheses`, `model_wear`, `numeric_space`, `women_numeric`이 모두 precision/recall 100.00%를 기록했다. `recommendation_noise`는 추출 대상이 아닌 추천 문구가 size_info로 들어가지 않는지 확인하는 negative group이며, false positive 0건이다.

평가: size_info는 이전 baseline에서 가장 취약한 필드였다. S7.7 baseline은 size_info precision 59.65%, recall 33.01%였으나, schema 변경 없이 SKILL 지침만 보강한 뒤 S7.7 subset과 S7.8 패턴 검증에서 100.00%를 달성했다. 현재 MVP에서는 schema 변경 없이 유지하는 판단이 타당하다.

## 보안 검증 결과

비밀정보 형태의 패턴 검색 결과, `logs/`, `out/`, `.git/`, `__pycache__/`를 제외한 커밋 대상 영역에서 다음 패턴은 발견되지 않았다.

- OpenAI API key 형태: `sk-...`, `sk-proj-...`
- GitHub token 형태: `ghp_...`, `github_pat_...`
- Bearer token 형태
- AWS access key 형태
- Slack token 형태
- private key header 형태

평가: 커밋 대상 영역 기준 비밀정보 노출 징후는 발견되지 않았다. 단, `logs/`는 과제 규정상 원본 그대로 제출해야 하므로 사후 편집하지 않는다. 최종 패키징 전에는 zip 내부에 의도치 않은 임시 파일이나 `out/`이 들어가지 않았는지만 별도로 확인하면 된다.

## 지표 해석

- schema-valid: JSON 구조가 `schema.json`과 validator의 추가 계약을 만족하는지 보는 지표다. 100%가 아니면 플러그인 출력으로 사용할 수 없다.
- precision: actual이 추출했다고 주장한 값 중 expected와 맞은 비율이다. 낮으면 없는 값을 만들어내거나 잘못 추정하는 오탐이 많다는 뜻이다.
- recall: expected에 있는 값 중 actual이 찾아낸 비율이다. 낮으면 입력에 있는 정보를 놓치는 누락이 많다는 뜻이다.
- micro precision/recall: 모든 필드의 TP/FP/FN을 합쳐 계산한 전체 속성 품질 지표다.
- detail_type precision/recall: 3-level taxonomy의 가장 세부 분류를 맞히는지 보는 핵심 지표다.
- size_info precision/recall: 사이즈 옵션, 실측, 모델 착용, 비교 가이드 등을 구조화하는 품질 지표다.
- dedup accuracy: 중복 후보 판정이 expected duplicate/distinct label과 일치한 비율이다.
- cross-category high-confidence false duplicate: 다른 category 사이에서 높은 점수의 잘못된 중복 후보가 나왔는지 보는 안전 지표다. 현재 0건이다.
- automatic fetch count: 검증 중 외부 상품 페이지를 자동으로 가져왔는지 보는 윤리·재현성 지표다. 현재 0건이다.
- legal compliance judgment count: 상품별 법적 적합/부적합을 판정했는지 보는 지표다. 현재 0건이며, 이 프로젝트는 법적 판정 대신 누락·모호 필드 표시만 한다.

## 종합 평가

현재 결과는 S8 패키징으로 넘어갈 수 있는 수준이다.

강점은 다음과 같다.

- 제출 플러그인 구조가 단순하고 필수 진입점이 명확하다.
- taxonomy가 3-level로 확장되어 향후 bottom, bag 등 범위 확장에도 구조적으로 유리하다.
- `outer`와 `top` MVP 범위 안에서는 detail_type 커버리지가 충분히 확보되어 있다.
- 소재 부위, 소재 혼용률, size_info처럼 법적·실무적 오해가 생기기 쉬운 필드를 보수적으로 처리한다.
- S7.7과 S7.8은 입력, expected, actual, 명령, 결과 JSON, 주요 파일 hash가 보존되어 재현성이 높다.
- 검증 데이터는 자동 fetch 없이 합성 또는 짧은 공개 snippet 방식으로 구성되어 제출 윤리 리스크를 줄였다.

남은 리스크는 다음과 같다.

- 최신 산출물은 `feature/detail-type-category` worktree에 있으므로, 메인 루트에서 바로 패키징하면 오래된 파일을 담을 위험이 있다.
- 원본 `logs/`는 최신 worktree가 아니라 메인 작업 디렉터리에 있다. 최종 zip 생성 시 반드시 별도로 포함해야 한다.
- 기본 5건 평가 fixture는 legacy 성격이 남아 있어 최신 S7.7 결과와 수치가 다르다. 제출물에는 포함되지 않지만 내부 검토자가 보면 혼동할 수 있다.
- S7.7의 100%는 합성 페이지형 데이터와 보존된 Codex actual 기준이다. 실제 무신사 전체 상품 페이지에서의 보장 수치로 표현하면 안 된다.
- dedup 가중치와 임계값은 운영 데이터 기반 튜닝값이 아니라 MVP 휴리스틱이다. 운영 전환 시 실제 라벨 데이터로 precision/recall을 보며 조정해야 한다.

## 패키징 전 권장 조치

1. 최신 worktree 기준으로 `src/`와 `README.md`를 사용한다.
2. 메인 작업 디렉터리의 원본 `logs/`를 zip에 그대로 포함한다.
3. `submission.zip` 내부 구조가 `src/.codex-plugin/plugin.json`, `README.md`, `logs/`를 포함하는지 확인한다.
4. `docs/`, `tests/`, `tools/`, `out/`은 제출 정책상 기본 제외한다.
5. zip 생성 후 압축 파일 내부를 한 번 더 검사한다.
6. 최종 제출 직전 비밀정보 패턴 검색과 `git status`를 다시 확인한다.

## 최종 판정

판정: 조건부 통과.

조건은 패키징 경로와 로그 포함 방식이다. 기능 구현과 재현 검증 자체는 현재 기준으로 통과했으며, 남은 가장 큰 위험은 코드 품질보다 제출 패키지 구성 실수다.
