# reports — 검증·실행 결과 보고서

이 폴더는 구현 기준 문서가 아니라, 이미 수행한 검증과 실행 결과를 보존하는 보고서 모음입니다.

## 포함 문서
| 문서 | 내용 | 관련 단계 |
|---|---|---|
| `s5-evaluation-report.md` | 더미 fixture 기반 속성 precision/recall 및 dedup 평가 | S5 |
| `s6-codex-cli-report.md` | Codex CLI 로컬 marketplace·실제 변환·질의 시연 결과 | S6 |
| `s7-expanded-validation-report.md` | 합성 100건, Codex subset 20건, 실제 공개 snippet 10건 확장 검증 해설 | S7.5 |
| `s7-expanded-validation-results.json` | S7.5 실행 환경, 명령, 정량 결과, 주요 파일 hash 원본 스냅샷 | S7.5 |
| `s7-7-full-page-dummy-validation-report.md` | 실제 페이지형 합성 더미 300건과 subset 50건 기준 검증 해설 | S7.7 |
| `s7-7-full-page-dummy-validation-results.json` | S7.7 실행 환경, 명령, 정량 결과, 주요 파일 hash 원본 스냅샷 | S7.7 |
| `s7-8-size-info-coverage-report.md` | size_info 표기 패턴 합성 fixture와 실제 Codex CLI 검증 해설 | S7.8 |
| `s7-8-size-info-coverage-results.json` | S7.8 실행 환경, 명령, 정량 결과, 패턴 그룹별 결과 스냅샷 | S7.8 |
| `s8-total-validation-evaluation-report.md` | S8 패키징 전 총검증, 지표 해석, 리스크 평가, 패키징 주의사항 | S8 |

## 보관 원칙
- 사람이 읽는 해설은 `*-report.md`에 둡니다.
- 재실행과 감사 추적에 필요한 원본 결과 JSON은 관련 보고서와 같은 폴더에 둡니다.
- 테스트 입력·expected·actual fixture는 `tests/fixtures/`에 보관하고, 이 폴더에는 결과 해석과 실행 스냅샷만 둡니다.
