# ArtCraft Studio 0.41.1 — model ids and request fields

Every id below is the exact `#[serde(rename = "…")]` wire value from
`crates/schema/public/enums/src/common/generation/`. The app's live menu is fetched from the
server (`GET /v1/omni_gen/models/image`, `…/video`), so this set is **what the 0.41.1 code can
decode, not a promise of what the server currently offers**.

Count method: `awk '/^pub enum CommonImageModel/,/^}/' <file> | grep -c 'rename = "'`.

## Image — 24 ids (`common_image_model.rs`)

```
flux_1_dev            flux_1_schnell       flux_pro_1p1          flux_pro_1p1_ultra
gpt_image_1           gpt_image_1p5        gpt_image_2           gpt_image_2p5_flare
gpt_image_2p5_sunburst grok_imagine_image  grok_imagine_image_q  midjourney_7
midjourney_7_niji     midjourney_8         nano_banana           nano_banana_2
nano_banana_pro       seedream_4           seedream_4p5          seedream_5_lite
seedream_5p0_pro      seedream_5p0_pro_u   qwen_edit_2511_angles flux_2_lora_angles
```

`qwen_edit_2511_angles` and `flux_2_lora_angles` are angle-manipulation models: they take
`adjust_horizontal_angle`, `adjust_vertical_angle`, `adjust_zoom`.

## Video — 46 ids (`common_video_model.rs`), 3 deprecated

```
grok_video*            grok_imagine_video    grok_imagine_video_1p5  flux_3
flux_3_draft           kling_1p6_pro         kling_2p1_pro          kling_2p1_master
kling_2p5_turbo_pro    kling_2p6_pro         kling_3p0_standard     kling_3p0_pro
happy_horse_1p0        wan_3p0               wan_3p0_prime          minimax_h3
minimax_h3_turbo       minimax_h3_ultra      seedance_1p0_lite      seedance_1p5_pro
seedance_2p0           seedance_2p0_fast     seedance_2p0_bp        seedance_2p0_bp_fast
seedance_2p0_u         seedance_2p0_u_fast   seedance_2p0_bpu       seedance_2p0_bpu_fast
seedance_2p0_mini      seedance_2p0_bp_mini  seedance_2p0_bpu_mini  seedance_2p5_preview
seedance_2p5           seedance_2p5_u        sora_2                 sora_2_pro
veo_2                  veo_3                 veo_3_fast             veo_3p1
veo_3p1_fast           veo_3p1_lite          vidu_q3                vidu_q3_turbo
preview_model          preview_model_fast
```

The three `#[deprecated]` ids are `grok_video` (superseded by `grok_imagine_video`),
`seedance_2p0_u` and `seedance_2p0_u_fast` — the latter two "never launched and unroutable; kept
only so historical database rows keep decoding" (`common_video_model.rs`). The `bpu` pair is not
deprecated.

## Audio — 5 (`common_audio_model.rs`)

```
suno_music  suno_remix  suno_sounds  suno_sample  seed_audio_1p0
```

## Mesh / 3D object — 11 (`common_mesh_model.rs`)

```
hunyuan_3d_2p0  hunyuan_3d_2p1  hunyuan_3d_3  hunyuan_3d_3_sketch
hunyuan_3d_3p1_pro  hunyuan_3d_3p1_rapid  hunyuan_3d_3p1_part  hunyuan_3d_3p1_topology
tripo3d_h3p1  meshy_v6  rodin_2p5_fast
```

`hunyuan_3d_3p1_part` and `…_topology` take a **mesh file**, not text or images.

## Gaussian splat / world — 7 (`common_splat_model.rs`)

```
marble_0p1_mini  marble_0p1_plus  marble_1p0  marble_1p0_draft  marble_1p1  marble_1p1_plus
triposplat
```

## Option values shared by the request types

| Enum | Values (`snake_case` wire form) |
|---|---|
| `CommonResolution` | `one_k`, `two_k`, `three_k`, `four_k`, `half_k`, `four_eighty_p`, `seven_twenty_p`, `ten_eighty_p` |
| `CommonQuality` | `auto`, `max`, `xhigh`, `high`, `medium`, `low` |
| `CommonAspectRatio` | `auto`, `square`, `square_hd`, `wide`, `tall`, `wide_three_by_two`, `wide_four_by_three`, `wide_five_by_four`, `wide_sixteen_by_nine`, `wide_twenty_one_by_nine`, `tall_two_by_three`, `tall_three_by_four`, `tall_four_by_five`, `tall_nine_by_sixteen`, `tall_nine_by_twenty_one`, `auto_2k`, `auto_3k`, `auto_4k` |
| `CommonBitrate` | `normal`, `high` |
| `CommonVideoOutputFormat` | `mp4`, `mov` |
| `GenerationProvider` | `artcraft`, `fal`, `grok`, `midjourney`, `sora`, `world_labs`, `higgsfield`, `krea`, `leonardo`, `magnific`, `openart`, `picsart`, `pixverse`, `runway` (14 declared; the 0.41.1 desktop only routes the first six) |

Not every model accepts every value. **Ask the server** — the model list carries
`aspect_ratio_options`, `resolution_options`, `quality_options`, `batch_size_options`, and
`is_disabled` per model.

## Per-model capability fields (`GET /v1/omni_gen/models/image`)

`OmniGenImageModelDetails` (copied permissively in
`crates/api_clients/artcraft/artcraft_client/src/endpoints/omni_gen/models/image/omni_gen_list_image_models.rs`):

| Field | Meaning |
|---|---|
| `full_name`, `model_creator` | display grouping |
| `text_prompt_supported`, `text_prompt_max_length` | prompt gate and character budget |
| `negative_text_prompt_supported`, `negative_text_prompt_max_length` | negative prompt support |
| `image_refs_supported`, `image_refs_max` | reference/ingredient image count |
| `has_fixed_editing_aspect_ratio`, `aspect_ratio_default_when_editing` | edit-mode constraints |
| `aspect_ratio_options`, `resolution_options`, `quality_options`, `batch_size_*` | accepted options |
| `is_disabled` | hidden or unavailable for this account |

Read these before building a request instead of guessing from a model name.
