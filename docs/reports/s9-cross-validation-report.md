# S9 · 독립 교차검증 보고서 (무신사 문제 2 제출물)

작성일: 2026-07-06 KST
대상 branch: `feature/detail-type-category`
검증 시작 commit: `443c9b4` (검증 대상) → 반영 완료 commit: `a7939a8`
관련 Worklog: W-049, W-050, W-052 · Troubleshootinglog: T-014, T-015 · Decisionlog: D-025

## 0. 목적과 범위

이 문서는 제출 직전 최신 worktree(`.worktrees/detail-type-category`)의 산출물·수치·문서·해석이 서로 일치하는지 독립적으로 교차검증하고, 발견한 결함을 어떻게 수정했는지 기록한다. 편의를 위해 요약하지 않고, 실제로 실행한 명령과 확인한 파일을 근거로 남긴다.

검증 대상: 제출 플러그인 구조, 지침 파일 동기화, 3단계 taxonomy, 소재/품질(material_part) 계약, 검증 수치(기본·S7.5·S7.7·S7.8), 해석의 정직성, 로그·기록 정합성, 수치 재현성.

방법: 파일 직접 열람 + 명령 실행 재현. 결함 후보는 3인 적대적 반박 패널(각 이슈를 기각하려 시도)로 검증해 살아남은 것만 확정 이슈로 채택했다.

## 1. 핵심 주장 검증 결과 (전부 사실로 확인)

| 검증 축 | 판정 | 근거 |
|---|---|---|
| 플러그인 구조 (`plugin.json` name=`musinsa-product-agentizer`, `skills: ./skills/`, `SKILL.md` frontmatter) | 통과 | 파일 직접 확인 |
| 지침 동기화 (`AGENTS.md`=`CLAUDE.md`, 정합성 게이트·로그 보존·commit/push 조항) | 통과 | SHA256 동일, 조항 라인 확인 |
| taxonomy 3단 (outer 7/22, top 8/9, 부모 관계 차단) | 통과 | python 계수 + 위반 fixture 실행 |
| 소재/품질 계약 (SKILL·validate.py·fixture) | 통과(개선) | 코드·실행 확인, 아래 3장 |
| 검증 수치 (기본·S7.5·S7.7·S7.8 전 항목) | 통과 | 아래 2장 재현 |
| 해석 정직성 (합성 기준 고지, snippet 탐색 지표 공개, dedup 휴리스틱 명시) | 통과(보강) | 아래 4장 |
| 로그·기록 (Worklog/Decisionlog/Troubleshootinglog 무결성, 비밀정보 부재) | 통과 | 번호 연속성·grep 확인 |

## 2. 수치 재현성 검증

결과 JSON에 보존된 실행 명령을 그대로 재실행해 저장값과 대조했다.

- **저장된 검증 명령 15개 재실행 → 15/15 exit code·수치 정확 일치.** (S7.5 6건, S7.7 7건, S7.8 2건)
- **기본 5건 평가 재실행:** micro precision 0.9868, micro recall 0.8929, dedup accuracy 1.0 → README·s8 보고서 수치와 일치.
- **S7.8 size_info 독립 재계산:** 러너를 거치지 않고 fixture(`size_info_patterns`)에서 직접 TP/FP/FN을 다시 계산 → 97/0/0, 저장값과 일치.

재실행 후 worktree는 clean 상태로 원복했고, 보고서 파일의 수치는 변경되지 않았다.

| 단계 | 대표 수치 | 재현 |
|---|---|---|
| 기본 5건 | P 98.68% / R 89.29% / dedup 100% | 일치 |
| S7.5 Codex subset 20건 | P 97.93% / R 95.95% | 일치 |
| S7.5 실제 공개 snippet 10건 | 탐색 P 65.48% / R 77.46% | 일치 |
| S7.7 subset 50건 | P/R 100% / dedup 100% / cross-cat FP 0 | 일치 |
| S7.8 48건 | size_info P/R 100% / TP·FP·FN 97·0·0 | 일치 |

## 3. 확정 결함과 수정 내역

교차검증에서 확정된 결함을 두 차례(W-049, W-050)에 걸쳐 모두 반영했다.

### 3.1 소재 계약 — material_part 규칙 양방향화 (W-050, T-014)

**문제:** `validate.py`의 material_part 규칙이 단방향이었다. "소재 part가 `unknown`인데 `missing_fields`에 `material_part` 없음"은 차단했지만, 반대로 "모든 part가 알려졌는데 `material_part`를 넣은 허위 표시"는 통과시켰다(직접 실증: 전부 `shell`인 상품에 `material_part`만 넣어도 exit 0).

**수정:** `validate.py`에 역방향 검사 추가 — 모든 part가 알려졌는데 `material_part`가 `missing_fields`에 있으면 차단. SKILL.md·requirements-contract·complete-guide·README에 양방향 규칙 명시. 역방향 회귀 fixture `invalid_spurious_material_part.json` 신규 추가.

### 3.2 negative fixture 이중 함정 격리 (W-050, T-014)

**문제:** `invalid_material_ratio_status.json`, `invalid_detail_type_parent.json`, `invalid_out_of_scope_category.json` 3건이 표적 규칙 외에 `part: "unknown"` + `material_part` 미표시를 부수적으로 포함해, 각각 오류가 2건씩 발생했다. 검증이 exit code 기반이라 표적 규칙이 회귀로 사라져도 material_part 오류로 실패가 유지되어 회귀 감지력이 약했다.

**수정:** 3건 모두 `part: "unknown"` → `"shell"`로 바꿔 표적 규칙 하나만 위반하도록 격리. 격리 후 각 fixture 오류 1건으로 확인.

**검증 결과(전 fixture):**

| fixture | 유형 | exit | 오류 | 표적 규칙 |
|---|---|---|---|---|
| valid_outer.json | valid | 0 | 0 | — |
| valid_top.json | valid | 0 | 0 | — |
| invalid_material_ratio_status.json | invalid | 1 | 1 | ambiguous인데 ratio 숫자 존재 |
| invalid_detail_type_parent.json | invalid | 1 | 1 | detail_type 부모 불일치 |
| invalid_out_of_scope_category.json | invalid | 1 | 1 | 범위 밖 category |
| invalid_missing_detail_type.json | invalid | 1 | 1 | detail_type 키 누락 |
| invalid_missing_quality.json | invalid | 1 | 1 | quality 누락 |
| invalid_unknown_detail_type.json | invalid | 1 | 2* | taxonomy 밖 detail_type |
| invalid_missing_material_part.json | invalid | 1 | 1 | material_part 누락 |
| invalid_spurious_material_part.json | invalid | 1 | 1 | material_part 허위 표시(역방향) |

\* schema enum + custom 검사가 같은 개념을 잡는 의도된 묶음.

### 3.3 문서-코드 정합성 (W-049)

- **dedup 가중치 표 불일치:** complete-guide 표가 실제 `dedup.py`와 달랐다(표 합 1.10, detail_type 누락). 실제 구현(category 0.16, subcategory 0.14, detail_type 0.08, materials 0.18, colors 0.11, fit 0.09, seasons 0.07, tpo_tags 0.07, care 0.04, title 0.06, 합 1.00)에 맞춰 갱신하고, 색상 예시 계산도 0.11 기준으로 수정.
- **taxonomy 표 구버전:** complete-guide 표에 `other_outer`(아우터 7번째), `hoodie`·`other_top`(상의)가 빠져 있었다. taxonomy.json 기준 아우터 7/22·상의 8/9로 보강.
- **detail_type 표현 모호:** requirements-contract가 "선택"으로 기술했으나 schema/validator는 키를 필수(값만 null 허용)로 강제. "필수 키, 값은 taxonomy id 또는 null"로 명확화.
- **valid_outer.json 의미 불일치:** title "오버핏 리넨 블레이저"인데 detail_type이 `trucker_jacket`이었다. taxonomy상 블레이저에 해당하는 `suit_blazer_jacket`으로 수정(둘 다 outer/jacket, validate 통과).

### 3.4 해석의 정직성 (W-049)

- **S7.7 100%의 개선 이력 공개:** 50건 subset의 size_info가 처음 59.65%/33.01%였고, 실패를 보고 SKILL을 보강한 뒤 같은 50건을 재실행해 100%가 된 것임을 README·submission-questions에 명시(신규 blind 성능이 아님).
- **합성 기준 한정 문구:** submission-questions의 100% 문단에 "합성 fixture 기준, 무신사 전체 카탈로그 보장 아님"을 직접 부착.
- **dedup 휴리스틱 고지:** dedup 가중치·임계값이 운영 튜닝값이 아닌 MVP 휴리스틱 baseline임을 제출용 README에도 추가.

### 3.5 패키징 위생·로그 분산 (W-049)

- **로그 분산 리스크(제출 핵심):** `save_log.py`가 세션 cwd 기준으로 저장해 worktree 세션 로그가 worktree `logs/`에 쌓인다. 메인 루트 `logs/`만으로 패키징하면 누락(규정상 "발췌" 위험). 헌법(`CLAUDE.md`/`AGENTS.md`)에 `10.1 로그 분산·병합 원칙`을 추가 — 최종 zip 생성 직전 모든 worktree `logs/`를 원본 복사로 통합, 편집·삭제 금지.
- **불필요 파일 정리:** 자동 생성 캐시 `__pycache__/` 삭제, 자리표시 소멸한 `src/.gitkeep` git 제거. zip 제외 규칙을 헌법 패키징 위생 조항에 명시.

### 3.6 기록·문서 위생 (W-049)

- 기본 5건 수치의 기계 판독 스냅샷 `s5-base-evaluation-results.json` 생성(수치 단일 출처), validation-plan·s8 보고서에 경로 명시.
- S7.5 보고서 생성 시각을 결과 JSON `generated_at_utc`와 일치시킴.
- Decisionlog를 D-024→D-001 내림차순으로 재정렬하고 dedup 휴리스틱 결정을 D-025로 추가.

## 4. 기각된 이슈 (결함 아님)

- **지침 파일 LF/CRLF 차이:** `core.autocrlf=true`의 체크아웃 아티팩트로 blob은 동일, 지침 텍스트도 완전 동일. (3인 중 2인 반박)
- **s5 보고서 98.55%/88.31%:** 확인일(2026-07-04)과 단계가 명시된 역사 스냅샷으로 최신 수치와 구분되어 표기됨.

## 5. 무회귀 검증

3장의 수정(특히 material_part 양방향화)이 기존 산출물을 깨뜨리지 않는지 재확인했다.

- schema fixture 10건 전수: invalid 8건 exit 1(표적 격리), valid 2건 exit 0.
- 저장된 15개 검증 명령 재실행 → 15/15 일치.
- 기본 평가 fixture expected/actual schema-valid True/True, micro P/R 0.9868/0.8929, dedup 1.0 유지.
- `validate.py` py_compile 통과.

즉 기존 100개 expected·subset 어디에도 허위 material_part가 없어, 양방향 규칙 도입에 따른 회귀가 없음을 확인했다.

## 6. 미검증 범위·차후 태스크

- **[후속 해소] S7.7 dedup cross-category 재계산 독립 검증:** `tools/run_s7_7_dedup_cross_category_recheck.py`로 `full_page_dummy/reference_actual_products.json`의 전체 상품쌍 44,850개를 처음부터 재채점했다. score >= 0.45 후보 수 2,788건과 high-confidence cross-category FP 0건이 저장 결과와 일치했다. 결과는 `s7-7-dedup-cross-category-recheck-results.json`, 해설은 `s7-7-dedup-cross-category-recheck-report.md`에 보존했다.
- **logs/ 내용과 submission-questions 답변 대조:** 로그 원본 보존 원칙에 따라 내용을 열지 않고 존재·크기·타임스탬프만 확인.
- **문제 근거 유튜브 영상 내용 대조:** URL 기재 형식만 확인, 영상 내용 미대조.
- **Codex CLI 실제 신규 실행:** 감사 셸에 `codex`가 없어 actual 산출물의 신규 생성은 재현하지 못했고, 저장된 actual 기준 지표 재현으로 대체.

## 7. 결론

교차검증 결과 제출물의 핵심 주장과 수치는 모두 사실로 확인됐고, 발견된 결함(문서-코드 불일치, 해석 투명성 보강 필요, negative fixture 이중 함정, material_part 단방향, 로그 분산 리스크)은 전부 수정·문서화했다. 이후 S7.7 dedup cross-category 재계산 독립 검증까지 추가로 완료되어, 저장된 cross-category 오탐 0건 주장은 별도 재채점으로도 확인됐다. 남은 제한은 로그 원본 내용 미열람, 문제 근거 영상 내용 미대조, 감사 셸의 Codex CLI 신규 실행 미수행처럼 제출 직전 외부·운영 조건에 가까운 범위이며, 제출 차단 사유는 없다. 최종 제출 시에는 헌법 `10.1`에 따라 모든 worktree `logs/`를 원본 그대로 통합하고 패키징 위생 절차를 적용해야 한다.
