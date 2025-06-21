# ────────────────────────────────────────────────────────────────────────────
# Software3-Lab — Makefile
#
#  Targets:
#    make build-rust     # build Rust tokenizer wheel
#    make build-cpp      # compile libvector.so
#    make test           # pytest + coverage
#    make lint           # ruff + mypy
#    make dev            # hot-reload FastAPI on :8080
#    make build          # docker build
#    make run            # docker run -p 8080:8080
#    make helm-up        # helm upgrade/install release
#    make tf-plan        # terraform plan
#    make tf-apply       # terraform apply
# ────────────────────────────────────────────────────────────────────────────

PYTHON        ?= python3
IMAGE_TAG     ?= trojan3877/software3-lab:0.1.0
HELM_CHART    ?= infra/helm/software3-lab
HELM_RELEASE  ?= software3-lab
KUBE_NS       ?= software3
TF_DIR        ?= infra/terraform

# ───────────────────────── Rust & C++ ─────────────────────────
.PHONY: build-rust
build-rust:
	cd rust/tokenizer && \
		pip install maturin==1.5.1 && \
		maturin develop --release

.PHONY: build-cpp
build-cpp:
	g++ -O3 -shared -std=c++17 -fPIC cpp/vector_math.cpp -o cpp/libvector.so

# ───────────────────────── Python ─────────────────────────────
.PHONY: test
test: build-rust build-cpp
	coverage run -m pytest -q
	coverage report -m

.PHONY: lint
lint:
	$(PYTHON) -m pip install --quiet ruff mypy
	ruff pipelines tests
	mypy pipelines --ignore-missing-imports

.PHONY: dev
dev: build-rust build-cpp
	uvicorn pipelines.evaluate:app --reload --port 8080

# ───────────────────────── Docker ─────────────────────────────
.PHONY: build
build:
	docker build -t $(IMAGE_TAG) .

.PHONY: run
run:
	docker run -p 8080:8080 $(IMAGE_TAG)

# ───────────────────────── Helm ───────────────────────────────
.PHONY: helm-up
helm-up:
	helm upgrade --install $(HELM_RELEASE) $(HELM_CHART) \
	  --namespace $(KUBE_NS) --create-namespace

.PHONY: helm-uninstall
helm-uninstall:
	helm uninstall $(HELM_RELEASE) --namespace $(KUBE_NS)

# ───────────────────────── Terraform ──────────────────────────
.PHONY: tf-init
tf-init:
	cd $(TF_DIR) && terraform init

.PHONY: tf-plan
tf-plan:
	cd $(TF_DIR) && terraform plan

.PHONY: tf-apply
tf-apply:
	cd $(TF_DIR) && terraform apply

.PHONY: tf-destroy
tf-destroy:
	cd $(TF_DIR) && terraform destroy
