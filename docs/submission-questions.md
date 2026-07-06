# 제출 질문 5문항 답변 초안

이 문서는 과제 제출 폼에 옮기기 쉬운 답변 초안입니다. 루트 `README.md`에도 같은 취지의 답변을 포함했습니다.

## 1. 무엇을, 누가, 어떤 상황에서 쓰나요?

Musinsa Product Agentizer는 사용자가 붙여넣은 패션 상품 상세 텍스트를 Codex가 검색·필터·비교에 쓸 수 있는 표준 JSON으로 바꾸는 플러그인입니다. 무신사 상품 운영자, 카탈로그 데이터 담당자, AI 에이전트 실험 담당자가 신규 상품 등록, 기존 상품 정보 정비, 중복 후보 확인, 패션 질의 응답용 데이터 준비 상황에서 사용합니다. 상품 상세페이지에는 상품명, 소재, 색상, 사이즈, 관리법, 착용 맥락이 문장·표·마케팅 문구로 섞여 있어 에이전트가 "봄에 입는 블랙 재킷", "실측 사이즈가 있는 상의", "같은 상품으로 보이는 등록건"처럼 일관되게 질의하기 어렵습니다. 이 플러그인은 그 비정형 텍스트를 category/subcategory/detail_type, materials, colors, seasons, size_info, quality 메모로 정리해 막힌 지점을 풀어 줍니다.

## 2. 왜 이 문제를 선택했나요?

이 문제를 고른 이유는 무신사가 공개 인터뷰에서 AI 에이전트와 상품 데이터 통합을 중요한 방향으로 말했고, 여러 서비스·플랫폼 확장 과정에서 기술 파편화와 동일 상품 중복 등록 부담을 언급했기 때문입니다. 실제로 패션 커머스의 상품 상세정보는 사람에게 보여 주기 위한 문장과 표로 구성되어, 직원은 상품 속성을 표준 항목으로 다시 정리해야 하고 고객 또는 에이전트는 자연어 질문을 해도 정확한 필터·비교 근거를 얻기 어렵습니다. 예를 들어 소재 혼용률, 부위별 소재, 계절, 핏, 실측 사이즈가 상품마다 다른 표현으로 적혀 있으면 AI가 같은 기준으로 답하기 어렵습니다. 따라서 "상품 데이터를 에이전트가 재사용 가능한 구조로 바꾸는 일"을 무신사 문제 2의 핵심으로 잡았습니다.

출처: https://www.youtube.com/watch?v=OLAWeIuiD5Y

## 3. 플러그인은 어떻게 작동하나요?

사용자가 상품 상세 텍스트를 붙여넣으면 Codex가 `product-agentizer` skill을 호출해 상품명, category, subcategory, detail_type, 소재, 색상, 계절, TPO, 관리법, size_info를 추출합니다. 분류와 표준값은 `taxonomy.json`의 3단계 구조(category → subcategory → detail_type)와 alias를 기준으로 맞추고, 최종 출력은 `schema.json` 계약에 맞춘 JSON입니다. 소재 혼용률은 입력에 숫자가 명시된 경우에만 `explicit`으로 기록하고, "터치", "블렌드", "혼용"처럼 비율이 없는 표현은 추정하지 않고 `missing` 또는 `ambiguous`로 남깁니다. 부위가 불명확한 소재는 `part: unknown`으로 두고 `quality.missing_fields`에 `material_part`를 기록합니다. 생성 JSON은 `validate.py`가 schema, taxonomy, detail_type 부모 관계, material_part 양방향 규칙을 확인합니다. 여러 상품 JSON은 `dedup.py`가 소재·색상·핏·계절·TPO·관리·제목 유사도를 가중 합산해 중복 후보를 냅니다. URL은 출처 메타데이터일 뿐 자동으로 열지 않고, 법적 적합/부적합 판정이나 추천 랭킹은 수행하지 않습니다.

## 4. AI를 어떻게 활용했나요?

AI에는 공개 자료 조사, 후보 기업 비교, 문제 정의 초안, 요구사항 계약, taxonomy/schema 설계, SKILL 작성, validator·dedup 스크립트, fixture 생성, Codex CLI 검증, README·보고서 초안, Claude Code 교차검증을 맡겼습니다. 직접 판단한 부분은 무신사 문제 2 확정, MVP를 outer/top으로 제한한 점, 자동 크롤링·비공개 데이터·법적 적합성 판정을 제외한 점, 실제 공개 상품 전체 복사 대신 짧은 공개 snippet과 합성 페이지형 데이터로 검증한 점입니다. 막혔던 지점은 size_info 누락, material_part 단방향 검증, invalid fixture 이중 함정, worktree 로그 분산, PowerShell UTF-8 검사 오탐이었습니다. 해결은 SKILL 지침 보강, validator 규칙 양방향화, fixture 격리, 로그 source-separated 통합, Python JSON 파서 재검증으로 진행했습니다. 받아들이지 않은 제안은 로컬 전용 비공개 검증 데이터 보존, 실제 사이트 자동 수집, size_info schema 객체화 즉시 적용입니다. 각각 윤리·제출 정합성·일정 리스크 때문에 제외하거나 후속 계획으로만 남겼습니다.

## 5. 어떻게 검증했나요?

정상 예시는 "린넨 블레이저, 겉감 린넨 55% 레이온 45%, 블랙, 봄가을, M 어깨 45cm" 같은 입력입니다. 플러그인은 이를 outer/jacket/suit_blazer_jacket, materials explicit, colors black, seasons spring·fall, size_info로 구조화하고 `validate.py`가 통과시킵니다. 비슷한 블레이저 2건은 `dedup.py`에서 duplicate 후보로 잡았습니다. 예외 상황도 확인했습니다. category가 bottom이면 범위 밖이라 차단하고, detail_type이 부모 subcategory와 맞지 않으면 실패합니다. 소재 part가 unknown인데 `material_part`가 없거나, 반대로 모두 알려졌는데 `material_part`를 허위로 넣어도 차단합니다. 검증은 기본 5건 P 98.68%/R 89.29%/dedup 100%, S7.7 페이지형 합성 50건과 S7.8 size_info 48건에서 실제 Codex CLI actual 기준 100%를 확인했습니다. 다만 100%는 합성 fixture 기준이며 무신사 전체 운영 성능 보장은 아닙니다. 실제 공개 snippet은 정보 부족 리스크를 보는 sanity check로 낮은 탐색 지표도 기록했습니다.
