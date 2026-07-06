# 제출 질문 5문항 답변 초안

이 문서는 과제 제출 폼에 옮기기 쉬운 답변 초안입니다. 루트 `README.md`에도 같은 취지의 답변을 포함했습니다.

## 1. 무엇을, 누가, 어떤 상황에서 쓰나요?

`Musinsa Product Agentizer`는 패션 상품 상세 텍스트를 AI 에이전트가 질의 가능한 구조화 상품 JSON으로 바꾸는 Codex 플러그인입니다. 무신사처럼 많은 브랜드와 상품 데이터를 다루는 패션 플랫폼의 상품 운영자, 데이터 담당자, 에이전트 커머스 실험 담당자, 또는 심사자가 사용할 수 있습니다.

사용자는 상품 상세페이지에서 텍스트를 직접 붙여넣습니다. 플러그인은 그 텍스트에서 상품명, 카테고리, 소재, 핏, 색상, 계절, TPO, 관리, 사이즈 정보를 추출하고, 에이전트가 검색·필터·비교·설명에 사용할 수 있는 JSON으로 정리합니다.

## 2. 왜 이 문제를 선택했나요?

무신사 테크리드 인터뷰 공개자료에서 기술 파편화, 동일 상품 중복 등록, 에이전트가 패션 질문에 사용할 첫 번째 도구가 되고 싶다는 방향성이 확인됐습니다. 상품 상세 텍스트는 사람에게는 읽히지만 AI 에이전트가 일관되게 질의하기에는 비정형성이 큽니다.

그래서 "상품 상세정보를 에이전트가 재사용 가능한 데이터로 바꾸는 문제"를 선택했습니다. 범위는 아우터와 상의 MVP로 좁혔고, 입력은 사용자가 직접 붙여넣은 텍스트로 제한했습니다. 이렇게 하면 공개 자료와 더미 fixture만으로 안전하게 구현·검증할 수 있고, 자동 크롤링이나 비공개 데이터 의존을 피할 수 있습니다.

## 3. 플러그인은 어떻게 작동하나요?

Codex가 `product-agentizer` skill을 사용해 붙여넣은 상품 텍스트에서 속성을 추출합니다. 추출한 값은 `taxonomy.json`의 표준 id로 정규화하고, `schema.json`에 맞는 JSON으로 만듭니다.

소재 혼용률은 입력 텍스트에 숫자가 명시된 경우에만 `explicit`으로 기록합니다. 숫자가 없거나 "터치", "블렌드"처럼 모호한 표현이면 값을 추정하지 않고 `missing` 또는 `ambiguous`로 표시합니다. 생성된 JSON은 `validate.py`로 검증할 수 있고, 여러 상품 JSON은 `dedup.py`로 중복 후보를 계산할 수 있습니다.

## 4. AI를 어떻게 활용했나요?

AI는 공개 자료 조사, 후보 기업 비교, 문제 선정, 요구사항 계약 문서 작성, taxonomy/schema 설계, skill 지침 작성, 검증 스크립트 작성, 평가 fixture 설계, Codex CLI 실행 시연, 확장 검증 데이터 구성, README 작성에 사용했습니다.

중요한 결정은 `Decisionlog.md`에 남겼고, 실제 작업 이력은 `Worklog.md`, 문제 해결 이력은 `Troubleshootinglog.md`에 기록했습니다. 로그는 과제 규정에 맞게 원본 그대로 `logs/`에 보관합니다.

## 5. 어떻게 검증했나요?

검증은 다섯 층으로 수행했습니다.

1. `schema.json`과 `validate.py`로 정상 JSON은 통과하고 오류 fixture는 실패하는지 확인했습니다.
2. 더미 상품 5건의 expected/predicted JSON을 비교해 속성 precision/recall을 산출하고, 중복쌍 10개에서 `dedup.py`의 정확도를 확인했습니다.
3. 로컬 Codex CLI에서 실제로 상품 텍스트를 구조화 JSON으로 변환하고, 그 출력이 `validate.py`를 통과하는지 확인했습니다.
4. 패키징 전 S7.5에서 합성 100건, Codex subset 20건, 실제 공개 snippet 10건의 입력·expected·actual·평가 결과·실행 명령·hash를 보존해 재실행 가능하게 만들었습니다.
5. S7.7에서 실제 페이지형 합성 더미 300건과 대표 subset 50건을 만들고, 50건은 expected fixture가 없는 격리 workspace에서 실제 Codex CLI로 실행해 운영형 입력 대응력을 확인했습니다.

현재 S7.5 Codex subset 20건 기준 actual schema-valid는 100%(20/20), micro precision은 95.52%, micro recall은 95.85%입니다. 다만 이 subset은 3단계 taxonomy 도입 이전의 historical actual을 보존한 세트라 `detail_type`은 expected/actual 모두 `null`이고 해당 필드의 precision/recall은 `not_applicable`입니다. actual은 schema `0.2.0` 호환을 위해 `schema_version`과 `detail_type: null`만 추가한 마이그레이션본입니다.

S7.7 50건 representative subset은 schema-valid 100%(50/50), micro precision 99.74%, micro recall 99.74%, `detail_type` precision/recall 100.00%, `size_info` precision/recall 100.00%, dedup accuracy 100.00%를 기록했습니다. 합성 self-check는 precision/recall 100.00%이지만 blind extraction 성능이 아니라 coverage/self-check이며, 실제 공개 snippet은 자동 fetch 없이 짧은 factual snippet만 사용했고 법적 적합/부적합 판정은 하지 않았습니다.
