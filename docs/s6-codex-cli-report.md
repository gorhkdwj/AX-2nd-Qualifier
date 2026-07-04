# S6 Codex CLI 실제 실행 검증 결과

확인일: 2026-07-04 KST

## 목적
S6의 목적은 S4/S5에서 만든 플러그인 구성물이 로컬 Codex CLI 환경에서 설치 후보로 인식되고, 실제 Codex 실행 흐름에서 상품 상세 텍스트를 구조화 JSON으로 변환한 뒤 질의 설명에 활용될 수 있는지 확인하는 것이다.

## 환경
- Codex CLI: `codex-cli 0.142.5`
- 작업 루트: `C:\Users\gorhk\AX_Hackathon\Jocoding_AX해커톤\2nd`
- 실행 입력 정책: BYO pasted text만 사용. URL은 `example.com` 출처 메타데이터로만 사용.
- 생성 출력: `out/s6-codex-output-outer-down-vest.json`, `out/s6-codex-query-answer.txt`

## 로컬 marketplace 구성
repo-scoped marketplace 파일을 추가했다.

- 파일: `.agents/plugins/marketplace.json`
- marketplace name: `ax-2nd-local`
- plugin: `musinsa-product-agentizer`
- source path: `./src`

임시 `CODEX_HOME`에서 아래 흐름을 검증했다.

```powershell
New-Item -ItemType Directory -Force out\codex-s6-home
$env:CODEX_HOME = (Join-Path (Get-Location) 'out\codex-s6-home')
codex plugin marketplace add . --json
codex plugin list --available --json
codex plugin add musinsa-product-agentizer@ax-2nd-local --json
```

결과:
- marketplace 등록 성공: `ax-2nd-local`
- available plugin 확인 성공: `musinsa-product-agentizer@ax-2nd-local`
- 로컬 플러그인 설치 성공: `out/codex-s6-home/plugins/cache/ax-2nd-local/musinsa-product-agentizer/0.1.0`

## 전역 Codex 환경 제약
전역 `codex plugin list`는 현재 작업과 무관한 기존 marketplace 설정(`openbell-guard-local`)이 지원 manifest를 포함하지 않는 경로를 가리켜 실패했다. 이번 작업에서는 사용자의 전역 Codex 설정을 임의 수정하지 않았다.

대신 다음을 분리해 확인했다.
- 임시 `CODEX_HOME`: marketplace 등록·플러그인 설치 검증
- 전역 인증 환경: `codex exec` smoke test와 실제 변환·질의 시연 검증

## Codex exec smoke test
```powershell
codex exec --ephemeral -C . --sandbox read-only -o out\s6-smoke.txt "Return exactly: CODEX_EXEC_OK"
```

결과:
- 성공
- 출력: `CODEX_EXEC_OK`

## 변환 시연
대상 fixture:
- `tests/fixtures/evaluation/source_inputs.json`의 `outer_down_vest`

초기 시도에서 `--output-schema`는 현재 `schema.json`의 `allOf`를 Codex response format이 허용하지 않아 실패했다. 이후 schema 강제 옵션 없이 raw JSON 출력을 요청하고, 생성물을 `validate.py`로 검증했다.

PowerShell 파이프에서 한글 입력이 깨질 수 있어, Python subprocess로 fixture를 UTF-8로 읽어 `codex exec` stdin에 전달했다.

생성 결과 요약:
- title: `카키 릴랙스 다운 베스트`
- category/subcategory: `outer` / `vest`
- materials:
  - `shell:nylon:explicit:100`
  - `fill:duck_down:explicit:80`
  - `fill:goose_down:explicit:20`
- colors: `khaki`
- seasons: `fall`, `winter`
- tpo_tags: `layering`, `outdoor`, `travel`
- size_info: `L 기준 총장 68cm`, `여유 있는 암홀`

검증:
```powershell
python src\skills\product-agentizer\scripts\validate.py out\s6-codex-output-outer-down-vest.json --pretty
```

결과:
- `valid: true`
- `checked: 1`
- `errors: []`

## 질의 시연
구조화 JSON을 기반으로 “winter travel layering outerwear로 적합한가”를 물어 한국어 답변을 생성했다. 한글 질의 문구는 Windows CLI 표시에서 깨질 수 있어, 질의 의도는 ASCII로 전달하고 답변은 한국어로 요구했다.

결과 요약:
- 겨울 여행용 레이어링 아우터에 적합하다고 답변
- 근거로 `outer`, `vest`, `winter`, `layering`, `travel`, `outdoor`, `relaxed`, `여유 있는 암홀`, `duck_down 80%`, `goose_down 20%`를 사용
- JSON에 없는 방수성, 방풍성, 중량, 보온 등급은 판단할 수 없다고 한계를 명시

## 해석
- 플러그인 패키징: repo marketplace를 통해 로컬 플러그인 후보 등록과 설치가 가능함을 확인했다.
- Codex 실행: 전역 인증 환경에서 `codex exec`가 작동하고, skill 지침 파일과 taxonomy/schema를 참조한 변환 결과가 schema-valid임을 확인했다.
- S5 보완 효과: 직전 recall 미달 원인이던 `goose_down`, `khaki`, `travel`, `암홀` 정보가 이번 Codex 출력에서는 유지됐다.
- 남은 제약: 전역 plugin list/add 명령은 기존 사용자 설정의 stale marketplace 때문에 바로 사용하기 어렵다. 전역 설치까지 완전히 확인하려면 사용자가 해당 marketplace를 제거하거나 유효한 manifest 경로로 고쳐야 한다.
