# 검증 계획 · 무신사 상품 데이터 에이전트화 변환기

기능을 만들 때마다 영향 범위에 맞게 검증한다. 검증하지 못한 부분은 숨기지 않고 `미검증 범위`에 적는다. 실패한 테스트를 삭제·완화하지 않고 원인을 수정한다.

## 검증 항목
- 문제 근거: 무신사 문제 2가 공개 자료로 실제 확인되는가. 핵심 근거는 무신사 테크리드 인터뷰 공개영상과 전사본, 보강 근거는 공개 조사 보고서에 둔다.
- 문서-코드 정합성: `docs/requirements-contract.md`와 실제 플러그인 동작 일치 여부
- README-기능 일치: README에 쓴 기능이 실제로 동작하는지
- 제출물/배포물 구조: `submission.zip` 기준 — `src/.codex-plugin/plugin.json` 존재, `src/skills/product-agentizer/SKILL.md` 존재, 루트에 `README.md`·`logs/` 존재
- 로그 무결성: `logs/` 내용이 훅으로 자동 저장된 원본 그대로이며 사후 편집이 없는가
- 질문 5문항 정합성: 답변 내용이 실제 로그·플러그인 코드와 모순되지 않는가
- 안전성: 플러그인이 제3자 사이트 자동 크롤링, 비밀정보 사용, 내부/비공개 데이터 의존을 하지 않는가

## 검증 방법과 도구
- 공개 자료 검증: 실제 URL 접속 및 내용 대조. 제출 인용문은 원본 영상 기준으로 재확인한다.
- 스키마 검증: `validate.py`가 `jsonschema`로 `schema.json`을 검증한다. 정상 JSON과 오류 JSON을 각각 통과/실패시키는 테스트를 둔다. `jsonschema`가 설치되어 있지 않으면 설치 안내와 함께 실패하도록 한다.
- 속성 추출 검증: 더미 상품설명과 정답 JSON을 비교해 속성별 precision/recall을 산출한다.
- taxonomy 매핑 검증: 자유표기(예: 리넨/린넨/마)와 표준용어 매핑 결과가 기대값과 일치하는지 확인한다.
- 소재 혼용률 검증: 입력에 숫자 혼용률이 명시된 경우만 `ratio_status: explicit`과 숫자 `ratio`를 허용한다. 미기재·모호 표현은 `ratio: null`과 `missing`/`ambiguous` 상태여야 하며, 부위가 다르면 `part`가 분리되어야 한다.
- 중복 감지 검증: 같은 상품의 다른 표현 쌍과 비중복 쌍을 나누어 `dedup.py` 결과를 비교한다.
- 중복 감지 가중치 검증: 현재 가중치와 임계값은 휴리스틱 baseline이므로, 실제 운영 적용 시에는 라벨링된 상품쌍으로 precision, recall, false positive, false negative를 비교해 가중치와 threshold를 조정한다. 이번 MVP 검증은 운영 최적화가 아니라 설명 가능한 baseline의 재현성과 오탐·미탐 사례 확인에 둔다.
- 제출 구조 검증: 폴더 구조 수동 점검(`ls`, `rg --files`) + 체크리스트 대조
- 로그 무결성: `tools/save_log.py` 훅 동작 결과와 `logs/` 파일 존재 여부 확인, 수동 수정 금지
- 비밀정보 검증: commit·패키징 전 API key/token/password 패턴 검색

## 검증 데이터 정책
플러그인이 상품정보 텍스트를 다룰 때, 검증용 데이터는 아래 원칙을 따른다. 선정 전 후보 방향에서 정리한 안전성 검토 이력은 `docs/archive/plugin-directions_PRE_SELECTION.md`에 보관한다.
- **도구 정확성 검증 = 합성(더미) 픽스처 우선**: 정답 라벨을 아는 통제된 입력(정상/경계/오류/부정 케이스)을 직접 만들어 precision/recall을 측정한다.
- **문제 실재성 = 공개 출처 인용**: 인터뷰 공개영상, 전사본, 기업 조사 근거를 URL·확인일과 함께 기록한다.
- **현실성 점검 = 소수 공개 샘플**: 공개 무신사 상품페이지 10건은 출처 메타데이터와 사람이 붙여넣은 짧은 factual snippet으로 sanity check한다. 플러그인이 URL을 자동으로 가져오지 않는다.
- **입력은 BYO 텍스트**: 사용자가 상품 상세 텍스트를 직접 붙여넣는다. URL은 출처 기록용 메타데이터일 뿐 실행 입력을 자동 수집하는 주소가 아니다.
- **지식원 = 공개 표준·공개 taxonomy·프로젝트 내 정적 데이터**: 내부 카탈로그, 판매 데이터, 비공개 고객 데이터는 사용하지 않는다.
- **소재 혼용률 = 입력 근거 기반 구조화만 수행**: 숫자 혼용률과 부위는 입력 텍스트에 명시된 경우에만 기록한다. 적법/위법 판정은 하지 않고, 미기재·모호 표현은 `quality`에 남긴다.
- **금지선**: 제3자 사이트 대량 크롤링, 제3자 UGC(리뷰·커뮤니티) 대량 수집, robots.txt·이용약관 위반, 비밀정보 입력 금지. 이 정책을 위반해야만 성립하는 기능은 제출물에서 제외한다.

## 목표 수치
- 속성 추출: 필수 속성 기준 precision/recall을 산출하고, 실패 사례를 표로 기록한다. S5 더미 fixture 기준 현재 결과는 micro precision 98.55%, micro recall 88.31%다.
- 중복 감지: 더미 중복쌍/비중복쌍에서 정확도와 오탐·미탐 사례를 기록한다. S5 더미 fixture 기준 현재 결과는 duplicate accuracy 100.00%(10/10)다.
- 스키마 검증: 정상 샘플은 통과, 필수 필드 누락·타입 오류·지원 범위 밖 카테고리·혼용률 상태 불일치는 실패해야 한다.
- S7.5 확장 검증: 합성 expected 100건 schema-valid 100%, Codex subset 20건 actual schema-valid 100%, Codex subset micro precision 95% 이상, micro recall 85% 이상, dedup accuracy 95% 이상, cross-category high-confidence false duplicate 0건을 목표로 한다.
- S7.5 현재 결과: 합성 expected 100/100 schema-valid, 합성 self-check precision/recall 100.00%, 합성 dedup 100.00%(20/20), Codex subset schema-valid 20/20, micro precision 95.52%, micro recall 95.85%, 실제 공개 snippet actual schema-valid 10/10, 자동 fetch 0건, 법적 적합/부적합 판정 0건이다. 합성 self-check는 `detail_type` coverage와 평가 도구 정합성 확인용이며 blind extraction 성능으로 해석하지 않는다. Codex subset은 historical actual 보존을 우선해 `detail_type` expected/actual이 모두 `null`이고 해당 필드는 `not_applicable`이다. actual은 schema `0.2.0` 호환을 위해 `schema_version`과 `detail_type: null`만 추가한 마이그레이션본이다. 상세 원본은 `docs/reports/s7-expanded-validation-results.json`에 보존한다.
- S7.7 실제 페이지형 합성 더미 검증: 실제 상품 페이지 원문을 저장하지 않고, `sparse`, `medium`, `full`, `noisy_ambiguous` 정보 밀도별 합성 상세페이지 입력을 만든다. 목표는 expected/reference actual schema-valid 100%, Codex subset actual schema-valid 100%, `detail_type` precision/recall 95% 이상, dedup accuracy 95% 이상, cross-category high-confidence false duplicate 0건이다. Sparse 입력에서는 모든 세부 필드 recall을 높이는 것이 아니라 hallucinated ratio/care 0건과 missing/ambiguous 판단 정확도를 중점 확인한다.
- S7.7 현재 결과: `full_page_dummy` 300건, representative `full_page_codex_subset` 50건, 실제 Codex CLI smoke용 `full_page_codex_smoke20` 20건을 생성했다. 정보 밀도 분포는 sparse 60건, medium 120건, full 90건, noisy/ambiguous 30건이다. category 분포는 outer 150건, top 150건이며 detail_type 최소 커버리지는 outer 6회, top 14회다. 기준 검증 결과 expected/reference actual schema-valid 100%, self-check micro precision/recall 100.00%, detail_type precision/recall 100.00%, dedup accuracy 100.00%, 자동 fetch 0건, 실제 상품 원문 저장 0건, 법적 적합/부적합 판정 0건, cross-category high-confidence false duplicate 0건이다. `full_page_codex_smoke20`은 expected가 없는 격리 workspace에서 실제 Codex CLI로 실행했고 schema-valid 20/20, micro precision/recall 100.00%, detail_type precision/recall 100.00%, dedup accuracy 100.00%를 확인했다. `full_page_codex_subset` 50건도 같은 격리 실행 방식으로 실제 Codex CLI actual을 생성해 보존했다. SKILL-only `size_info` 원자화와 소재 부위 보수 라벨 기준 정렬 후 subset 결과는 schema-valid 50/50, micro precision 100.00%, micro recall 100.00%, `detail_type` precision/recall 100.00%, `materials` precision/recall 100.00%, `size_info` precision/recall 100.00%, dedup accuracy 100.00%다. schema는 `0.2.0`을 유지했고, schema v0.3 size_info 객체화 계획은 `docs/size-info-schema-change-plan.md`에 조건부 계획으로 보존한다.
- S7.8 size_info 표기 패턴 보강 검증: 실제 상품 원문을 저장하지 않고, 문자 옵션, 숫자 옵션, `FREE`/`ONE SIZE`, 괄호 혼합 표기, 실측 행, 표 형태 실측, 모델 착용, 비교 가이드, 추천·후기 noise를 합성 fixture로 확장한다. 목표는 expected/actual schema-valid 100%, `size_info` precision/recall 95% 이상, 추천·후기 noise false positive 0건이다.
- S7.8 현재 결과: `size_info_patterns` 48건을 생성했고 expected fixture가 없는 격리 workspace에서 실제 Codex CLI actual을 생성했다. actual schema-valid 48/48, `size_info` precision/recall 100.00%, true/false positive/false negative 97/0/0, recommendation_noise false positive 0건, 자동 fetch 0건, 실제 상품 원문 저장 0건, 법적 적합/부적합 판정 0건이다. 이는 실제 판매 데이터 전체 기준이 아니라 확장 합성 표기 패턴 기준 검증이다.

## 미검증 범위
- Codex CLI에서 더미 fixture 1건을 구조화 JSON으로 변환하고 질의 설명에 활용하는 흐름은 S6에서 검증했다. 단, 전역 plugin list/add 명령은 기존 사용자 설정의 stale marketplace 때문에 완전 자동화하지 못했고, 임시 `CODEX_HOME`에서 로컬 플러그인 설치를 별도 확인했다.
- 실제 공개 무신사 상품페이지 10건의 사람이 붙여넣은 짧은 snippet 기반 sanity check는 S7.5에서 수행했다. 다만 이는 전체 상세페이지 성능 벤치마크가 아니라 안전한 현실성 점검이므로, 실제 공개 샘플의 precision/recall은 acceptance threshold로 쓰지 않는다.
- 실제 페이지형 운영 입력에 더 가까운 검증은 S7.7의 합성 상세페이지형 더미데이터와 S7.8의 size_info 표기 패턴 확장 fixture로 수행했다. 이 검증은 실제 페이지 전체 복제나 로컬 전용 비공개 검증을 사용하지 않고, 모든 입력·expected·기준 actual·평가 결과를 커밋 가능한 합성 데이터로 보존하는 방식이다. 20건 smoke, 50건 representative subset, 48건 size_info pattern 모두 실제 Codex CLI actual까지 검증했다. 남은 범위는 실제 무신사 내부 카탈로그 전체 커버리지와 운영 적용 효과이며, 이는 비공개 데이터가 필요하므로 검증 대상이 아니다.
- 실제 무신사 내부 카탈로그 전체 커버리지와 운영 적용 효과는 비공개 데이터가 필요하므로 검증 대상이 아니다.
- 심사위원의 실제 채점 기준(AI+심사자 평가)은 외부 프로세스이므로 이 문서로 사전 검증 불가.
