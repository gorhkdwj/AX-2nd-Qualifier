# Troubleshootinglog · AX해커톤 예선 2차 제출(무신사 문제 2)

실제 오류·실패·환경 문제·검증 실패·설계 충돌이 발생하면 기록한다. 같은 문제가 반복되면 새 T-ID를 만들기 전에 기존 T-ID를 먼저 확인한다. (규칙: CLAUDE.md / AGENTS.md 11절)

## 기록 형식
```
### T-00N · 문제 제목
**발생 상황** / **증상** / **확인된 원인** / **조치** / **재발 방지**
```

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
