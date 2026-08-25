# Contributing to Neonize

Terima kasih ingin berkontribusi! Dokumen ini menjelaskan branching model,
standar commit, dan alur rilis project.

## 🌳 Branching Model

```
feature/xxx ──► PR ──► dev ──────────────► PR ──► master
                        │  (CI gate)              │  (CI gate + AUTO RELEASE)
hotfix(x) ──────────────┴── PR langsung ke master juga didukung
```

| Branch | Fungsi | Rilis? |
|---|---|---|
| `dev` | Integration branch — semua feature PR masuk di sini lebih dulu | ❌ hanya CI gate |
| `master` | Always-releasable — merge ke sini memicu rilis otomatis | ✅ auto release |

Model ini adalah **GitHub Flow + staging branch** (gitflow yang disederhanakan):
tidak ada release branch maupun manual version bump — Python Semantic Release
menentukan nomor versi dari commit sejak tag terakhir.

## 📦 Alur Kontribusi

1. Fork & buat branch fitur dari `dev`:
   ```bash
   git checkout dev && git pull
   git checkout -b feat/fitur-anda
   ```
2. Commit menggunakan **Conventional Commits**:
   | Prefix | Efek versi | Contoh |
   |---|---|---|
   | `fix:` | patch (`0.4.4`) | `fix: handle empty media download` |
   | `feat:` | minor (`0.5.0`) | `feat: add schedule message` |
   | `feat!:` / `BREAKING CHANGE:` footer | minor saat 0.x | `feat!: drop Python 3.9` |
   | `chore:`, `docs:`, `ci:`, `test:`, `build:` | tanpa rilis | `ci: tweak workflow` |
3. Push lalu buka **Pull Request ke `dev`** — CI wajib hijau
   (ruff, go vet, proto drift check, pytest, FFI smoke test).
4. Setelah stabil, merge `dev` → `master` via PR → pipeline release berjalan:
   PSR menghitung versi, menulis CHANGELOG.md, membuat tag + GitHub Release,
   membangun shared library per-platform, dan publish wheel ke PyPI.

> 💡 Jika tidak ada commit bertipe `feat:/fix:` sejak tag terakhir, merge ke
> `master` **tidak** menghasilkan rilis — pipeline berhenti dengan aman.

## 🚑 Hotfix

Fix kritis bisa langsung dibuat PR ke `master` (tanpa lewat `dev`) — rilis
otomatis tetap berjalan normal. Sinkronkan kembali `dev` setelahnya:

```bash
git checkout dev && git pull origin master
```

## 🛠️ Development Setup

```bash
git clone https://github.com/krypton-byte/neonize.git
cd neonize

# Install dependencies (Python 3.10+, Go 1.25+ untuk goneonize)
uv sync --dev

# Build shared library lokal (butuh CGO/gcc)
CGO_ENABLED=1 uv run task build goneonize

# Jalankan test
uv run --with pytest python -m pytest tests/
```

### Task yang tersedia (`uv run task <nama>`)

| Task | Fungsi |
|---|---|
| `build goneonize [--smart]` | Build `.so/.dll/.dylib` ke `neonize/`; `--smart` skip bila versi tak berubah |
| `build proto` | Regenerasi protobuf (Go + Python) |
| `proto` | Sync definisi proto terbaru dari whatsmeow main |
| `repack` | Re-tag wheel generic menjadi wheel platform-specific |
| `goneonize_changed` | Cek apakah source goneonize berbeda dari release terakhir |

## 🧹 Standar Kode

- Python: ikuti `ruff check` + `ruff format` (line-length 100)
- Go: `go vet ./...` wajib bersih di `goneonize/`
- Docstring: gaya **Sphinx reST** (`:param:`/`:type:`/`:return:`/`:rtype:`/
  `:raises:`) — konsisten dengan sisa codebase
