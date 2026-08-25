# 📋 Plan Modernisasi Workflow Development & Release — neonize

> Status: **PROPOSAL** · Dibuat: Agustus 2026 · Target: migrasi dari bump-my-version ke
> Python Semantic Release (PSR) v10 + overhaul pipeline release & CI

---

## 1. Assessment — Kenapa Workflow Sekarang Bermasalah

Setelah analisis menyeluruh, ini temuan konkret (bukan sekadar perasaan "berantakan" 😄):

### 1.1 Versioning — banyak sumber kebenaran yang saling kontradiksi

| Lokasi | Nilai saat ini | Masalah |
|---|---|---|
| `neonize/__init__.py` | `0.3.13` | ❌ Stale, tidak sinkron |
| `goneonize/version.go` | `0.4.3.post0` | Sumber versi goneonize |
| `neonize/download.py` | `0.4.3.post0` | Di-sync manual saat release |
| `.bumpversion.toml` | `0.4.3.post0` | Duplikat sumber kebenaran |

Empat file, tiga nilai berbeda. Versi Python package yang ter-publish di PyPI bahkan
berbeda dari versi goneonize-nya sendiri.

### 1.2 `release.yml` — desain rapuh

- **Bump versi diduplikasi 5×** — job `android`, `zig`, `linux`, `darwin`, dan `release`
  masing-masing menjalankan `bump-my-version` secara independen (race-prone, boros compute).
- **Input mismatch**: workflow menerima `inputs.version_type` tapi env membaca
  `github.event.inputs.version_major` dst. → variabel env tersebut **selalu kosong**.
- **`continue-on-error: true` di semua job build** → release bisa "sukses" padahal build gagal,
  dan release final tetap jalan dengan artefak kosong/sebagian.
- **Bump manual via dropdown** (`major/minor/patch/post`) — bukan berbasis commit, rawan
  human error, dan tidak menghasilkan changelog.
- Skema `X.Y.Z.postN` custom — bukan SemVer, bikin tooling standar (termasuk PSR) tidak bisa
  mem-parse-nya.
- Job build **commit langsung ke master** dari dalam step shell (`git push origin HEAD:master`)
  — bypass code review.

### 1.3 Toolchain drift antara lokal vs CI

| Tool | Lokal (fakta) | CI (release.yml) | Efek |
|---|---|---|---|
| protoc | 34.1 (pembuat artefak committed) | **21.12** | Regenerasi hasil CI ≠ file committed |
| protoc-gen-go | v1.36.12 | v1.36.10 | Header generated file selalu churn |

### 1.4 Hal lain yang mengganggu

- ❌ Tidak ada `CHANGELOG.md` — rilis notes hanya `generate_release_notes` GitHub.
- ❌ Tidak ada **CI untuk PR** (lint/test/build gate) — `master` bisa rusak kapan saja;
  semua quality check baru terjadi saat release.
- ⚠️ `autobump.yml` (daily whatsmeow update) menjalankan 6 formatter sekaligus
  (autopep8, autoflake, isort, black, gofumpt, ruff) → PR berisi ribuan baris noise format,
  sulit di-review, dan `go get -u` tanpa verifikasi build.
- ⚠️ Rebuild goneonize **selalu penuh** untuk 10+ target platform walau tidak ada perubahan
  di `goneonize/` — release lambat dan mahal.

---

## 2. Prinsip Target

1. **Single source of truth** — satu commit = satu versi, ditentukan otomatis dari
   Conventional Commits, tidak pernah diketik manual.
2. **Trunk-based** — `master` selalu releasable; rilis dipicu oleh merge, bukan tombol manual.
3. **Build hanya yang berubah** — goneonize (Go/CGO) hanya di-rebuild bila `goneonize/**`
   berubah; kalau tidak, pakai ulang artefak dari release sebelumnya.
4. **Fail fast, fail loud** — tidak ada `continue-on-error` di jalur kritikal.
5. **Reproducible** — toolchain di-pin identik antara lokal & CI.

---

## 3. Versioning: Python Semantic Release

### 3.1 Temuan riset (sudah diverifikasi empiris di sandbox ✅)

| Temuan | Implikasi |
|---|---|
| PSR v10.6.1 **murni tag-driven** — versi dasar diambil dari git tag terakhir yang cocok `tag_format`, BUKAN dari `version_variables` | Migrasi butuh **bootstrap tag** SemVer murni (mis. `0.4.3`) sebagai anchor |
| Pattern default `version_variables` **mendukung sintaks Go `version := "..."`** dan single-quote Python `'...'` ✅ | Tidak perlu script sync custom — PSR langsung rewrite `version.go` & `download.py` |
| `0.4.3.post0` **tidak parseable** sebagai SemVer → PSR fallback ke `0.1.0` | Skema `.postN` **harus ditinggalkan**, ganti pure SemVer |

### 3.2 Konfigurasi yang diusulkan (`pyproject.toml`)

```toml
[tool.semantic_release]
version_variables = [                      # PSR rewrite otomatis di release commit:
    "neonize/__init__.py:__version__",     #   versi Python package (dibaca pdm-backend)
    "neonize/download.py:__GONEONIZE_VERSION__",
    "goneonize/version.go:version",        #   sintaks `version := "..."` ✅ terverifikasi
]
tag_format = "{version}"                   # tanpa prefix "v" → kompatibel URL download lama
allow_zero_version = true                  # project masih 0.x
major_on_zero = false                      # breaking change → naik minor (0.x), bukan loncat 1.0.0
commit_parser = "conventional"             # feat:/fix:/perf! → minor/patch/major otomatis
build_command = "uv build"                 # (opsional) wheel dibangun saat versioning
changelog.insertion_flag = "<!-- version list -->"

[tool.semantic_release.branches.master]
match = "(master)"
prerelease = false

[tool.semantic_release.changelog.default_templates]
changelog_file = "CHANGELOG.md"
```

**Aturan bump otomatis** (Conventional Commits, konsisten dengan gaya commit repo saat ini):

| Commit | Bump | Contoh |
|---|---|---|
| `fix: ...` | patch → `0.4.4` | bug fix RejectCall |
| `feat: ...` | minor → `0.5.0` | fitur baru ala PR #200 |
| `feat!:` / `BREAKING CHANGE:` footer | minor → `0.6.0` (karena 0.x) | ubah API |
| `chore:/docs:/ci:/test:` | tidak release | maintenance |

### 3.3 Langkah bootstrap (sekali, manual)

1. Samakan semua file versi ke `0.4.3` (pure SemVer).
2. Buat anchor tag: `git tag 0.4.3 && git push origin 0.4.3`.
3. Sejak titik ini PSR mengambil alih — bump berikutnya dihitung dari commit sejak tag itu.

> ⚠️ Konsekuensi: versi berikutnya adalah `0.4.4`/`0.5.0` — tidak ada lagi `.postN`.
> Tag lama (`0.4.3.post0` dll.) biarkan saja; PSR mengabaikannya (regex tag tidak match).

---

## 4. Pipeline Release Baru

### 4.1 Arsitektur

```
                        push ke master (merge PR)
                                 │
                    ┌────────────▼────────────┐
                    │  job: release-version    │
                    │  python-semantic-release │
                    │  • hitung versi dr commit│
                    │  • rewrite 3 file versi  │
                    │  • generate CHANGELOG.md │
                    │  • commit + tag + push   │
                    │  • buat GitHub Release   │
                    └────────────┬────────────┘
                          release? ─── no → selesai (hanya CI lint/test)
                                 │ yes (output: version, tag)
        ┌────────────────────────┼────────────────────────┐
        ▼                        ▼                        ▼
  job: changes             job: build-goneonize      job: build-python
  (paths-filter:           HANYA jika goneonize/**   wheel + repack per OS/arch,
   goneonize/** berubah?)  berubah → matrix CGO      EMBED .so dari:
                           build (android/zig/linux/  • artefak build-goneonize (baru), ATAU
                           darwin/windows)            • asset release SEBELUMNYA (skip build!)
        │                        │                        │
        └────────────────────────┴───────────┬────────────┘
                                             ▼
                              job: publish
                              • gh release upload <tag> sharedlib/*
                              • uv publish → PyPI (PYPI_TOKEN)
```

### 4.2 Poin desain penting

1. **Hanya job `release-version` yang menyentuh git** — tidak ada lagi commit/push
   tersebar di job build. Build jobs checkout di **ref tag** yang baru dibuat (immutable).
2. **Trigger**: `on: push` ke `master` (+ `workflow_dispatch` untuk re-run). Tidak ada lagi
   dropdown major/minor/patch — PSR yang putuskan dari commit. Kalau tidak ada commit
   releasable, PSR exit dengan "no release" dan pipeline berhenti hemat.
3. **Tanpa `continue-on-error`** — kegagalan build = release gagal, terlihat merah.
4. **Permissions minimal**: `contents: write` untuk job PSR; job build hanya butuh read.
5. **Idempoten & aman di-re-run**: checkout by tag; publish job upload asset dengan
   clobber check.

### 4.3 Smart rebuild — jawaban atas pertanyaan Anda: **ya, bisa!**

Repo ini sudah punya pondasinya (`tools/build_goneonize_decision.py` yang bandingkan md5
source vs release terakhir), tinggal dimodernisasi dengan pendekatan deklaratif:

```yaml
changes:
  runs-on: ubuntu-latest
  outputs:
    goneonize: ${{ steps.filter.outputs.goneonize }}
  steps:
    - uses: actions/checkout@v4
      with: { fetch-depth: 0 }
    - uses: dorny/paths-filter@v3
      id: filter
      with:
        base: ${{ needs.release-version.outputs.previous_tag }}   # tag sebelumnya
        filters: |
          goneonize:
            - 'goneonize/**'
            - '!goneonize/version.go'     # bump versi saja ≠ perlu rebuild
```

- **goneonize berubah** → matrix build CGO penuh (android arm64/arm/amd64/386, windows
  amd64/arm64/386, linux amd64/arm64/riscv64/s390x, darwin amd64/arm64).
- **goneonize TIDAK berubah** (kasus mayoritas: cuma fix Python) → download `.so/.dll/.dylib`
  dari release GitHub sebelumnya (`tools/download.py` sudah persis melakukan ini!), langsung
  lanjut build wheel + repack. **Estimasi hemat 60–80% waktu release.**

---

## 5. CI untuk Pull Request (yang selama ini hilang)

File baru `.github/workflows/ci.yml`, trigger `pull_request` + `push` (non-release):

| Check | Perintah | Waktu |
|---|---|---|
| Lint Python | `ruff check && ruff format --check` | ~5 dtk |
| Type proto sync | `uv run task build proto && git diff --exit-code` | ~30 dtk |
| Build Go | `cd goneonize && go build ./... && go vet ./...` | ~1 mnt |
| Test | `pytest tests/` | ~10 dtk |
| Import smoke test | load binder + built `.so` (linux amd64) | ~30 dtk |
| Release check | `semantic-release --strict version --print` (validasi konfigurasi) | ~5 dtk |

Branch protection: require CI hijau + minimal 1 review sebelum merge ke `master`.

---

## 6. Dependency Automation (perbaikan `autobump.yml`)

Masalah sekarang: 6 formatter + lint mutation menghasilkan PR noise raksasa tiap hari.

Usulan:
1. **Pisahkan concern** — satu PR hanya deps, satu PR hanya proto:
   - `chore(deps): update whatsmeow & golang deps` → **tidak memicu release** (PSR skip `chore`).
   - `chore(proto): sync whatsapp proto definitions` → idem.
2. **Hapus langkah auto-format mutation** (autopep8/autoflake/black/isort/gofumpt) dari
   automation — formatting adalah tanggung jawab pre-commit hook lokal + CI check, bukan bot.
3. **Gate kualitas di PR automation**: `go build && go vet && pytest` harus hijau sebelum
   PR dibuat/di-merge.
4. Frekuensi: mingguan cukup (`cron: 0 0 * * 1`); daily untuk lib yang jarang rilis itu waste.
5. Pertimbangkan **Renovate** sebagai alternatif enterprise-grade (grouping, lockfile-aware),
   tapi opsional — YAML di atas sudah 80% perbaikan.

---

## 7. Cleanup Artefak Lama

| Item | Aksi |
|---|---|
| `.bumpversion.toml` | ❌ hapus |
| `bump_version.sh` | ❌ hapus |
| `bump-my-version` di `[dependency-groups] dev` | ❌ ganti `python-semantic-release` |
| Taskipy `version update major/minor/patch/post` di `tools/version_cli.py` | 🔧 sisakan `info` & `--set-url`; hapus subcommand bump (PSR menggantikan) |
| `tools/flow.py` (hook BVHOOK_* bumpversion) | ❌ hapus (logika goneonize-changed sudah digantikan paths-filter) |
| `tools/version.py` | 🔧 sederhanakan — masih dipakai `--smart` build & github url |
| `protoc 21.12` di semua workflow | 🔧 pin `34.1` (sesuai pembuat artefak committed) |
| `protoc-gen-go@v1.36.10` | 🔧 pin ikut versi `google.golang.org/protobuf` di go.mod (v1.36.12) |
| Commit `uv.lock` ke git | ✅ wajib — reproducible builds (saat ini untracked!) |

---

## 8. Roadmap Implementasi

| Fase | Isi | Estimasi |
|---|---|---|
| **F1** | Bootstrap versi: samakan 3 file ke `0.4.3`, commit `uv.lock`, tambah config `[tool.semantic_release]` + dep PSR, hapus bump-my-version artifacts | 1 sesi |
| **F2** | Rewrite `release.yml`: job `release-version` (PSR action) + `changes` (paths-filter) + matrix build conditional + `publish`. Hapus duplikasi bump | 1–2 sesi |
| **F3** | New `ci.yml` (lint/build/test/smoke) + branch protection guide | 1 sesi |
| **F4** | Rapikan `autobump.yml` (pisah deps/proto, buang formatter, gate build) | ½ sesi |
| **F5** | Bootstrap tag `0.4.3`, dry-run release penuh (`--noop` lalu rilis uji), dokumentasikan di `CONTRIBUTING.md` | 1 sesi |

Urutan aman: F1 → F3 → F4 dulu (tidak menyentuh rilis), F2 terakhir setelah CI stabil.

---

## 9. Risiko & Mitigasi

| Risiko | Mitigasi |
|---|---|
| Konsumen yang pin ke tag `.postN` lama | Tag lama tidak dihapus; hanya skema baru yang berubah |
| `download.py` versi release harus = nama tag | Sudah terjamin: PSR menulis file itu sendiri dengan nilai = tag |
| First PSR run salah hitung (belum ada tag SemVer) | Bootstrap tag `0.4.3` WAJIB sebelum enable pipeline (F5) |
| Matrix build gagal di arch eksotis (riscv64/s390x) | Tetap ada, tapi sekarang gagal = release gagal (jujur); bisa dipindah ke `continue-on-error` + warning eksplisit kalau mau toleran |
| PyPI publish ganda (job zig/linux/darwin semua `uv publish`) | Di pipeline baru hanya **satu** job publish |
| Token PAT scope | `GITHUB_TOKEN` bawaan cukup utk PSR (contents: write); `PAT` lama tetap utk setup-protoc |

---

## 10. Keputusan yang Perlu Disepakati

1. ✅/❌ Drop skema `.postN` → pure SemVer `MAJOR.MINOR.PATCH` (rekomendasi: **ya**).
2. ✅/❌ Breaking change saat 0.x = naik minor (`major_on_zero: false`) atau tetap naik ke 1.0.0?
3. ✅/❌ Rilis otomatis on-push-to-master, atau tetap semi-manual via `workflow_dispatch`
   (PSR tetap yang menentukan nomor versinya)?
4. ✅/❌ Arch eksotis (riscv64, s390x) gagal-hard atau best-effort?
5. Renovate vs YAML autobump yang dirapikan?

---
*Dokumen ini hasil analisis codebase + eksperimen PSR 10.6.1 langsung. Siap dieksekusi fase demi fase.*
