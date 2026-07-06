#!/usr/bin/env python3
"""Generate S7.8 synthetic size_info pattern fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "size_info_patterns"
SYNTHETIC_URL_PREFIX = "https://example.com/musinsa-size-info-pattern/"


PATTERN_GROUPS: list[dict[str, Any]] = [
    {
        "group": "letter_comma",
        "cases": [
            ("사이즈 옵션: S, M, L", ["S", "M", "L"]),
            ("구매 가능 사이즈: M, L, XL", ["M", "L", "XL"]),
            ("SIZE OPTION: XS, S, M", ["XS", "S", "M"]),
            ("옵션 사이즈: L, XL, XXL", ["L", "XL", "XXL"]),
        ],
    },
    {
        "group": "letter_slash",
        "cases": [
            ("SIZE: XS / S / M / L / XL", ["XS", "S", "M", "L", "XL"]),
            ("사이즈: S/M/L", ["S", "M", "L"]),
            ("옵션: M | L | XL", ["M", "L", "XL"]),
            ("Size: FREE / M / L", ["FREE", "M", "L"]),
        ],
    },
    {
        "group": "numeric_space",
        "cases": [
            ("사이즈: 90 95 100 105", ["90", "95", "100", "105"]),
            ("SIZE: 85 90 95", ["85", "90", "95"]),
            ("옵션: 100 105 110", ["100", "105", "110"]),
            ("사이즈 선택: 95 100", ["95", "100"]),
        ],
    },
    {
        "group": "women_numeric",
        "cases": [
            ("사이즈 옵션: 44, 55, 66", ["44", "55", "66"]),
            ("SIZE: 55 / 66 / 77", ["55", "66", "77"]),
            ("사이즈: 44 55", ["44", "55"]),
            ("옵션: 66, 77", ["66", "77"]),
        ],
    },
    {
        "group": "brand_numeric",
        "cases": [
            ("브랜드 사이즈: 1 / 2 / 3", ["1", "2", "3"]),
            ("옵션: 0, 1, 2", ["0", "1", "2"]),
            ("SIZE: 2 3 4", ["2", "3", "4"]),
            ("사이즈 선택: 1, 2", ["1", "2"]),
        ],
    },
    {
        "group": "mixed_parentheses",
        "cases": [
            ("사이즈: M(95), L(100), XL(105)", ["M(95)", "L(100)", "XL(105)"]),
            ("옵션: S(90) / M(95) / L(100)", ["S(90)", "M(95)", "L(100)"]),
            ("SIZE: 1(44-55), 2(66), 3(77)", ["1(44-55)", "2(66)", "3(77)"]),
            ("사이즈: FREE(44-66)", ["FREE(44-66)"]),
        ],
    },
    {
        "group": "free_one_size",
        "cases": [
            ("사이즈: FREE", ["FREE"]),
            ("SIZE: ONE SIZE", ["ONE SIZE"]),
            ("옵션: OS", ["OS"]),
            ("사이즈 옵션: FREE, ONE SIZE", ["FREE", "ONE SIZE"]),
        ],
    },
    {
        "group": "measurement_rows",
        "cases": [
            (
                "사이즈 실측:\nM 총장 68cm 어깨 50cm 가슴 58cm 소매 60cm\nL 총장 70cm 어깨 52cm 가슴 60cm 소매 61cm",
                ["M 총장 68cm 어깨 50cm 가슴 58cm 소매 60cm", "L 총장 70cm 어깨 52cm 가슴 60cm 소매 61cm"],
            ),
            (
                "실측 사이즈:\nS 총장 64cm 어깨 46cm 가슴 53cm\nM 총장 66cm 어깨 48cm 가슴 55cm\nL 총장 68cm 어깨 50cm 가슴 57cm",
                ["S 총장 64cm 어깨 46cm 가슴 53cm", "M 총장 66cm 어깨 48cm 가슴 55cm", "L 총장 68cm 어깨 50cm 가슴 57cm"],
            ),
            ("FREE 총장 72cm 가슴 64cm 밑단 62cm", ["FREE 총장 72cm 가슴 64cm 밑단 62cm"]),
            ("1 총장 65cm 어깨 48cm 가슴 56cm\n2 총장 67cm 어깨 50cm 가슴 58cm", ["1 총장 65cm 어깨 48cm 가슴 56cm", "2 총장 67cm 어깨 50cm 가슴 58cm"]),
        ],
    },
    {
        "group": "measurement_table",
        "cases": [
            (
                "사이즈(cm) 총장 어깨 가슴 소매\nM 68 50 58 60\nL 70 52 60 61",
                ["M 총장 68cm 어깨 50cm 가슴 58cm 소매 60cm", "L 총장 70cm 어깨 52cm 가슴 60cm 소매 61cm"],
            ),
            (
                "SIZE(cm) LENGTH SHOULDER CHEST SLEEVE\nS 64 46 53 58\nM 66 48 55 59",
                ["S LENGTH 64cm SHOULDER 46cm CHEST 53cm SLEEVE 58cm", "M LENGTH 66cm SHOULDER 48cm CHEST 55cm SLEEVE 59cm"],
            ),
            (
                "사이즈표\nFREE 총장 71 가슴단면 62 암홀 28",
                ["FREE 총장 71 가슴단면 62 암홀 28"],
            ),
            (
                "실측 정보(cm)\n1 총장 65 어깨 48 가슴 56\n2 총장 67 어깨 50 가슴 58",
                ["1 총장 65cm 어깨 48cm 가슴 56cm", "2 총장 67cm 어깨 50cm 가슴 58cm"],
            ),
        ],
    },
    {
        "group": "model_wear",
        "cases": [
            ("모델 181cm/70kg L 착용", ["모델 181cm/70kg L 착용"]),
            ("여성 모델 170cm S 착용", ["여성 모델 170cm S 착용"]),
            ("남성 모델 178cm 68kg M 사이즈 착용", ["남성 모델 178cm 68kg M 사이즈 착용"]),
            ("LOOKBOOK MODEL 186cm XL 착용", ["LOOKBOOK MODEL 186cm XL 착용"]),
        ],
    },
    {
        "group": "comparison_guide",
        "cases": [
            ("사이즈 비교 가이드: 무신사 스탠다드 M 사이즈 티셔츠와 비슷한 사이즈입니다.", ["사이즈 비교 가이드: 무신사 스탠다드 M 사이즈 티셔츠와 비슷한 사이즈입니다."]),
            ("이 상품은 가슴단면 기준으로 무신사 스탠다드 XS 민소매와 비슷합니다.", ["이 상품은 가슴단면 기준으로 무신사 스탠다드 XS 민소매와 비슷합니다."]),
            ("어깨너비 기준으로 무신사 스탠다드 L 점퍼와 유사한 사이즈입니다.", ["어깨너비 기준으로 무신사 스탠다드 L 점퍼와 유사한 사이즈입니다."]),
            ("기존 착용 상품과 비교하면 100 사이즈 셔츠에 가까운 핏입니다.", ["기존 착용 상품과 비교하면 100 사이즈 셔츠에 가까운 핏입니다."]),
        ],
    },
    {
        "group": "recommendation_noise",
        "cases": [
            ("사이즈 추천: 178cm 70kg 고객은 L을 많이 선택했습니다.\n후기 요약: 사이즈가 적당해요 82%", []),
            ("구매자 사이즈 만족도: 커요 12%, 적당해요 82%, 작아요 6%", []),
            ("내 체형 기준 추천 사이즈는 로그인 후 확인할 수 있습니다.", []),
            ("후기 요약: 사이즈가 여유 있어요. 배송 안내: 오늘 출발.", []),
        ],
    },
]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_reference_actual(path: Path, metadata_path: Path, data: Any) -> None:
    metadata = {}
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata.get("actual_mode") == "codex_cli_actual":
        return
    write_json(path, data)
    write_json(
        metadata_path,
        {
            "actual_mode": "deterministic_reference_actual_pending_cli_run",
            "note": "Generator writes reference actual until a real Codex CLI actual is saved.",
        },
    )


def case_category(index: int) -> tuple[str, str, str, str, list[str], list[str], list[str]]:
    if index % 2 == 0:
        return (
            "outer",
            "jacket",
            "nylon_coach_jacket",
            "아우터 > 재킷 > 나일론/코치 재킷",
            ["black"],
            ["regular"],
            ["spring", "fall"],
        )
    return (
        "top",
        "tshirt",
        "short_sleeve_tshirt",
        "상의 > 티셔츠 > 반소매 티셔츠",
        ["white"],
        ["regular"],
        ["summer"],
    )


def material_for(category: str) -> list[dict[str, Any]]:
    if category == "outer":
        return [
            {
                "part": "shell",
                "name": "nylon",
                "ratio": 100,
                "ratio_status": "explicit",
                "evidence": "겉감 나일론 100%",
            }
        ]
    return [
        {
            "part": "shell",
            "name": "cotton",
            "ratio": 100,
            "ratio_status": "explicit",
            "evidence": "겉감 면 100%",
        }
    ]


def care_for(category: str) -> list[str]:
    return ["hand_wash"] if category == "outer" else ["machine_wash"]


def care_text(category: str) -> str:
    return "관리 방법: 단독 손세탁 권장" if category == "outer" else "관리 방법: 세탁기 사용 가능"


def color_ko(category: str) -> str:
    return "블랙" if category == "outer" else "화이트"


def material_text(category: str) -> str:
    return "소재 정보: 겉감 나일론 100%" if category == "outer" else "소재 정보: 겉감 면 100%"


def build_source_text(title: str, category_path: str, category: str, size_text: str) -> str:
    return "\n".join(
        [
            "[상품 상단]",
            "브랜드: SIZE TEST LABEL",
            f"상품명: {title}",
            f"카테고리: {category_path}",
            f"컬러 옵션: {color_ko(category)}",
            "",
            "[상품 정보]",
            material_text(category),
            "핏: 레귤러핏",
            size_text,
            "추천 계절: 간절기" if category == "outer" else "추천 계절: 여름",
            "추천 상황: 데일리",
            care_text(category),
            "",
            "[노이즈]",
            "첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다.",
        ]
    )


def structured_product(
    product_id: str,
    title: str,
    category: str,
    subcategory: str,
    detail_type: str,
    source_url: str,
    size_info: list[str],
) -> dict[str, Any]:
    missing_fields = ["size_info"] if not size_info else []
    return {
        "product_id": product_id,
        "structured_product": {
            "schema_version": "0.2.0",
            "source": {
                "source_url": source_url,
                "source_title": title,
                "input_mode": "pasted_text",
            },
            "product": {
                "title": title,
                "category": category,
                "subcategory": subcategory,
                "detail_type": detail_type,
                "materials": material_for(category),
                "fit": ["regular"],
                "colors": ["black"] if category == "outer" else ["white"],
                "seasons": ["spring", "fall"] if category == "outer" else ["summer"],
                "tpo_tags": ["daily"],
                "care": care_for(category),
                "size_info": size_info,
            },
            "agent_descriptor": {
                "search_summary": f"{title} size_info 패턴 검증 상품",
                "query_tags": [title, "size_info 패턴", category, detail_type],
                "explainable_reasons": [
                    "합성 size_info 패턴 검증 입력에서 상품 기본 속성과 사이즈 표현을 구조화했습니다."
                ],
            },
            "quality": {
                "missing_fields": missing_fields,
                "ambiguous_fields": [],
                "out_of_scope": False,
                "confidence": "medium" if missing_fields else "high",
            },
        },
    }


def build_fixtures() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    expected_products: list[dict[str, Any]] = []
    metadata: list[dict[str, Any]] = []
    index = 0

    for group in PATTERN_GROUPS:
        group_id = group["group"]
        for variant_index, (size_text, expected_size_info) in enumerate(group["cases"]):
            category, subcategory, detail_type, category_path, _colors, _fit, _seasons = case_category(index)
            product_id = f"sizepat_{index:03d}"
            source_url = f"{SYNTHETIC_URL_PREFIX}{product_id}"
            title = f"SIZE TEST LABEL {group_id} {variant_index + 1:02d}"
            source_text = build_source_text(title, category_path, category, size_text)
            sources.append(
                {
                    "product_id": product_id,
                    "source_title": title,
                    "source_url": source_url,
                    "category_hint": category,
                    "locale": "ko-KR",
                    "source_method": "synthetic_size_info_pattern",
                    "product_text": source_text,
                }
            )
            expected_products.append(
                structured_product(
                    product_id,
                    title,
                    category,
                    subcategory,
                    detail_type,
                    source_url,
                    list(expected_size_info),
                )
            )
            metadata.append(
                {
                    "product_id": product_id,
                    "pattern_group": group_id,
                    "variant_index": variant_index,
                    "category": category,
                    "expected_size_info": list(expected_size_info),
                    "negative_size_info_case": not bool(expected_size_info),
                    "synthetic_source": True,
                }
            )
            index += 1

    return (
        {"cases": sources},
        {"products": expected_products},
        {"pairs": []},
        {"cases": metadata},
    )


def write_prompt(path: Path, title: str, source_payload: dict[str, Any]) -> None:
    cases_json = json.dumps(source_payload, ensure_ascii=False, indent=2)
    prompt = f"""# {title}

Use `src/skills/product-agentizer/SKILL.md`, `references/schema.json`, and `references/taxonomy.json`.
Convert every case below into a raw JSON object with this exact top-level shape:

```json
{{"products":[{{"product_id":"...","structured_product":{{}}}}]}}
```

Rules:
- Return raw JSON only, with no Markdown fences.
- Do not fetch URLs. URLs are synthetic source metadata only.
- Do not judge legal label compliance.
- Preserve product_id values exactly.
- Treat 배송, 쿠폰, 후기 요약, 구매자 만족도, 개인화 추천 문구 as noise unless they directly state static product size attributes.
- Follow the SKILL.md size_info atomization rules exactly.

Input cases:
{cases_json}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(prompt, encoding="utf-8")


def main() -> int:
    sources, expected, labels, metadata = build_fixtures()
    write_json(FIXTURE_DIR / "source_inputs.json", sources)
    write_json(FIXTURE_DIR / "expected_products.json", expected)
    write_reference_actual(FIXTURE_DIR / "actual_products.json", FIXTURE_DIR / "actual_metadata.json", expected)
    write_json(FIXTURE_DIR / "duplicate_labels.json", labels)
    write_json(FIXTURE_DIR / "case_metadata.json", metadata)
    write_prompt(FIXTURE_DIR / "prompt.md", "S7.8 size_info pattern conversion prompt", sources)
    write_prompt(
        FIXTURE_DIR / "prompt_template.md",
        "S7.8 size_info pattern conversion prompt template",
        {"cases": ["<replace with source_inputs.json cases>"]},
    )
    print(json.dumps({"size_info_patterns": len(sources["cases"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
