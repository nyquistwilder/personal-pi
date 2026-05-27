set shell := ["bash", "-euo", "pipefail", "-c"]

default: check

shell:
	nix develop

install-hooks:
	prek install --hook-type pre-commit --hook-type commit-msg

fmt:
	nix fmt

fmt-check:
	nix fmt -- --fail-on-change --no-cache

fmt-nix:
	find . -type f -name '*.nix' -not -path './.git/*' -exec nixfmt {} +

fmt-md:
	rumdl fmt .

fmt-toml:
	taplo fmt

fmt-yaml:
	yamlfmt .

fmt-json:
	prettier --write "**/*.{json,jsonc}"

fmt-shell:
	find . -type f \( -name '*.sh' -o -name '*.bash' \) -not -path './.git/*' -exec shfmt -w {} +

lint: lint-nix lint-md lint-toml lint-yaml lint-json lint-actions lint-shell lint-file-names lint-editorconfig lint-spelling

lint-nix:
	statix check .
	deadnix --fail .

lint-md:
	rumdl check .

lint-toml:
	taplo check

lint-yaml:
	yamlfmt -lint .

lint-json:
	while IFS= read -r -d '' file; do jq -e . "$file" >/dev/null; done < <(find . -type f -name '*.json' -not -path './.git/*' -print0)

lint-actions:
	actionlint

lint-shell:
	files=(); while IFS= read -r -d '' file; do files+=("$file"); done < <(find . -type f \( -name '*.sh' -o -name '*.bash' \) -not -path './.git/*' -print0); if [ "${#files[@]}" -gt 0 ]; then shellcheck "${files[@]}"; fi

lint-file-names:
	ls_lint

lint-editorconfig:
	editorconfig-checker

lint-spelling:
	typos

security: security-gitleaks security-trivy

security-gitleaks:
	gitleaks dir . --config .gitleaks.toml --redact --no-banner

security-gitleaks-history:
	gitleaks git . --config .gitleaks.toml --redact --no-banner --log-opts="--all"

security-trivy:
	trivy fs .

flake-check:
	nix flake check

check: fmt-check lint security flake-check

commit-msg-check message_file:
	@message="$(grep -vE '^(#|$)' '{{message_file}}' | head -n 1 || true)"; \
	if [[ "$message" =~ ^(Merge|Revert|fixup!|squash!) ]]; then exit 0; fi; \
	pattern='^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)(\([a-z0-9._-]+\))?!?: .+'; \
	if [[ ! "$message" =~ $pattern ]]; then \
		echo "Commit message must follow Conventional Commits: <type>[optional scope]: <description>"; \
		echo "Allowed types: build, chore, ci, docs, feat, fix, perf, refactor, revert, style, test"; \
		exit 1; \
	fi
