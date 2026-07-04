# 무신사 문제 2 · 상품 데이터 에이전트화 변환기 — 구현 계획 (병합 보관본)

> 보관 상태: 2026-07-04 `docs/implementation-plan.md`로 고유 내용을 병합한 뒤 활성 구현 기준에서 제외합니다. 현재 구현 계획은 `docs/implementation-plan.md`를 기준으로 확인합니다.

## Context (왜 이 작업을 하는가)
AX 해커톤 2차 제출 대상 기업·문제를 **무신사 / 문제 2(에이전트화 변환기)**로 확정한다. 무신사 테크리드 인터뷰(공개영상 https://www.youtube.com/watch?v=OLAWeIuiD5Y)의 핵심 비전 — "AI 에이전트가 패션 질문 때 첫 번째로 쓰는 도구가 무신사이길", "동일 상품을 두 번 등록해야 하는 파편화" — 에 정면으로 대응한다.

문제: 무신사 상품 상세정보가 **비정형 텍스트**라 AI 에이전트가 정확·일관·설명 가능하게 질의할 수 없다. 이는 "에이전트 first 도구"가 되기 위한 **전제(에이전트가 이해할 구조화 데이터)**가 없다는 뜻이다.

해결: 상품 상세페이지 텍스트(BYO 입력)를 **정규화된 구조화 속성 + 표준 taxonomy 매핑 + 중복 감지 + 에이전트 질의 descriptor**로 변환하는 Codex 플러그인을 만든다. 공개자료·더미 픽스처만으로 안전하게 시연·검증한다(크롤링 없음).

확정된 스코프(사용자 결정):
- 근거: 인터뷰 공개영상 URL을 1차 출처로 사용 + 공개 사실(무신사 멀티플랫폼·글로벌 확장, 에이전트 커머스)로 보강.
- MVP 카테고리: **아우터·상의 2개 카테고리**. taxonomy를 데이터 주도로 설계해 이후 카테고리 확장 용이.
- 입력 방식: 상품 URL은 출처 메타데이터로만 기록하고, 실제 실행 입력은 사용자가 직접 붙여넣은 상품 상세 텍스트로 제한한다(자동 fetch·크롤링 없음).
- 구성: **SKILL + 결정적 스크립트**(instruction SKILL + 정적 taxonomy/schema 데이터 + Python 검증·중복감지). 확장 여지 열어둠.
- 검증: 로컬 Codex CLI로 실제 설치·실행·시연 가능.

## 제출물 구조 (과제.md 규정)
플러그인 루트 = `src/`. 제출 zip = `src/` + `README.md` + `logs/`. 레포 레이아웃이 그대로 매핑됨(CLAUDE.md 3절).
```
src/
├── .codex-plugin/plugin.json              # 필수 manifest (이 폴더엔 이것만)
└── skills/product-agentizer/
    ├── SKILL.md                            # frontmatter(name, description) + 지시문
    ├── references/
    │   ├── taxonomy.json                   # 아우터/상의 카테고리·소재·핏·계절·TPO 표준용어(공개 기준 근거)
    │   └── schema.json                     # 출력 JSON 스키마
    └── scripts/
        ├── validate.py                     # 출력 JSON 스키마·혼용률합계·필수속성 검증(결정적)
        └── dedup.py                        # 속성 유사도 기반 중복 감지(결정적)
README.md                                    # (제출 루트) 플러그인 설명 — 패키징 단계에서 작성
logs/                                        # tools/save_log.py 훅이 자동 저장(재사용, 손대지 않음)
tests/fixtures/                              # 더미 상품설명+정답라벨, 중복쌍 (제출물 아님, 검증용)
docs/references/                             # 근거·taxonomy 출처 스냅샷(출처 링크 포함)
```

## 재사용 (기존 자산)
- `tools/save_log.py` — 로그 자동 저장 훅. 그대로 사용, 편집 금지(실격 사유).
- 빈 폴더 `src/`, `tests/`, `docs/references/` 이미 존재(.gitkeep).
- 안전·검증 정책은 `docs/validation-plan.md`(검증 데이터 정책)에 확정됨. 선정 전 후보 방향과 안전성 검토 이력은 `docs/archive/plugin-directions_PRE_SELECTION.md`에 보관함.
- Codex 플러그인 규격은 `docs/technical_references/`(Plugins/Build_plugins/Agent_Skills)에서 확인됨: `.codex-plugin/`엔 plugin.json만, skills는 루트, manifest 경로는 `./` 시작, SKILL.md는 name·description frontmatter 필수, description은 발동/비발동 조건을 front-load.

## 구현 단계 (가장 작은 성공 단위부터)

**S1 · 계약·기획 고정 (완료, CLAUDE.md 5절)**
- 완료 내용: `docs/requirements-contract.md`에 입력(붙여넣기 상품 상세 텍스트), 출력(정규화 JSON 스키마), 주요 지표(속성별 precision/recall·중복감지 정확도), 상태·오류 판정, 누락·모호 속성 처리 규칙을 고정.
- 완료 내용: `docs/project-plan.md`·`docs/implementation-plan.md`·`docs/validation-plan.md`를 무신사 문제 2 기준으로 갱신.
- 완료 내용: `docs/company-selection.md` 최종 확정 체크박스 갱신, `Decisionlog.md` D-007 기록.
- 남은 세부 작업: `docs/references/`에 인터뷰 URL + 핵심 인용(원본 영상 대조), 공개 사실(뉴스룸 등) 출처·확인일을 구현 과정에서 보강.
- 완료조건: 계약 문서에 플레이스홀더 없음. 검증: 문서 상호 정합성.

**S2 · 지식 데이터 (taxonomy.json, schema.json)**
- 아우터·상의 2개 카테고리의 표준 속성 vocabulary: 카테고리/서브카테고리, 핏·실루엣, 소재(공개 섬유 표시기준 용어), 컬러, 계절, TPO·스타일 태그, 관리, 사이즈. 데이터 주도(카테고리 추가=데이터 추가).
- 출력 JSON 스키마 정의(필수/선택 속성, 타입, 모호/부족 표기 필드, descriptor 필드).
- 완료조건: 스키마로 유효 JSON을 판별 가능. 검증: 샘플 JSON을 스키마에 통과/실패시켜 확인.

**S3 · SKILL.md 작성**
- frontmatter: name `product-agentizer`, description(front-load: 패션 상품 상세정보→에이전트 질의용 구조화 데이터 변환; 표기 규정 검수(문제1)에는 비발동 명시).
- 본문(명령형): ① 텍스트에서 속성 추출 ② taxonomy 매핑 ③ schema 준수 JSON 생성 ④ 부족·모호 속성 표기 + 에이전트 질의 descriptor 생성 ⑤ `scripts/validate.py`로 출력 검증, 배치면 `scripts/dedup.py`로 중복 감지. 입력·출력·완료조건 명시.
- 완료조건: 한 작업에 집중(CLAUDE 5.1). 검증: 대표 프롬프트로 의도 상황에서만 발동하는지 확인.

**S4 · 스크립트 + manifest (validate.py, dedup.py, plugin.json)**
- `validate.py`: 출력 JSON을 schema.json 대조 + 혼용률 합계≈100 + 필수 속성·taxonomy 용어 유효성 검사. 표준입력/파일 인자로 단독 실행 가능.
- `dedup.py`: 상품 JSON 리스트 입력→속성 유사도로 중복 후보 판별.
- `plugin.json`: name `musinsa-product-agentizer`, version `0.1.0`, description, `"skills": "./skills/"`.
- 완료조건: 스크립트가 더미 입력에 결정적으로 동작. 검증: 아래 S5.

**S5 · 더미 픽스처 검증 (정확성)**
- `tests/fixtures/`에 아우터·상의 더미 상품설명 + 정답 속성 라벨, 중복쌍/비중복쌍 픽스처(합성 — 실제 무신사 데이터 크롤링 금지).
- validate.py·추출 결과로 속성별 precision/recall, dedup.py로 중복 감지 정확도 측정.
- 완료조건: 목표 정확도 달성·수치 기록. 검증: 스크립트 실행 로그.

**S6 · Codex CLI 실제 실행·시연 (end-to-end)**
- 로컬 marketplace 등록→플러그인 설치→새 Codex 스레드에서: 더미 아우터 상품설명 입력→구조화 JSON 출력→샘플 에이전트 질의("여름 하객룩")를 그 JSON 위에서 필터·설명으로 답변하는 흐름 시연.
- 공개 무신사 상품페이지 3~5건은 출처 URL을 기록하고, 사람이 붙여넣은 텍스트로 sanity check한다. 플러그인이 URL을 자동 수집하지 않는다.
- 완료조건: 실제 실행 캡처. 검증: 실행 결과가 설계 흐름과 일치.

**S7 · 제출 문서 (README + 질문 5문항)**
- 루트 `README.md`(제출용): 플러그인이 무엇을/누가/어떻게 작동하는지, 실행 방법(실제 구현 기능만). 질문 5문항 답변 문서 작성(로그·플러그인과 정합).
- 완료조건: README-기능 일치, 5문항이 코드·로그와 모순 없음.

**S8 · 패키징·제출 검증**
- `submission.zip`(src/ + README.md + logs/) 구조 대조: plugin.json 존재, SKILL.md 존재, logs 원본 포함, 비밀정보·크롤러 없음.
- 완료조건: 구조 체크리스트 통과.

## Verification (종합 검증)
1. **구조**: `src/.codex-plugin/plugin.json` 존재, manifest 경로 `./skills/` 유효, submission.zip 레이아웃 일치(`ls`/스크립트).
2. **스크립트 단위**: `python validate.py`, `python dedup.py`를 tests/fixtures에 실행 → 속성 precision/recall·중복 정확도 수치 산출(더미 정답 대비).
3. **Codex 실 실행**: marketplace 등록→설치→새 스레드에서 변환→에이전트 질의 데모(S6). 재현 가능한 명령·입력을 문서화.
4. **공개 sanity**: 공개 상품페이지 소수(출처 기록)로 실입력 확인.
5. **정합성**: requirements-contract ↔ SKILL/스크립트 동작 ↔ README ↔ 질문 5문항 상호 모순 없음.
6. **안전·규정**: 크롤러·비밀정보 없음, 로그 원본 무편집, 근거는 공개 URL·확인일과 함께 기록.

## 열린 리스크
- 인터뷰는 자동 전사본 → 제출 인용문은 **원본 영상(제공된 URL)과 대조**해 정확히 인용(S1에서 처리).
- taxonomy는 MVP(아우터/상의)로 한정 — 데이터 주도라 확장 가능하나, 커버리지 밖 상품은 "범위 밖"으로 처리 명시.
- SKILL이 스크립트를 호출하는 정확한 경로 문법은 공식 문서에 예시가 없음 → S6 실 실행으로 호출 방식 확정(안 되면 instruction-only로 폴백하고 스크립트는 개발자 검증용으로 위치).
