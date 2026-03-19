# Цвета
RED    = \033[0;31m
GREEN  = \033[0;32m
YELLOW = \033[1;33m
BLUE   = \033[0;34m
RESET  = \033[0m

# Константы
UV      = uv run
PYTHON  = python3
PIP     = pip3
DC = docker compose

# Помощь: показать все команды с описанием
.PHONY: help
help:
	@awk -F':.*## ' '/^[a-zA-Z_-]+:.*## / { \
		printf "    \033[36mmake %-12s\033[0m — %s\n", $$1, $$2 \
	} \
	/^[[:space:]]*##==/ { \
		gsub("##==", "", $$0); \
		gsub("[[:space:]]*$$", "", $$0); \
		printf "\033[1;33m🔧 %s\033[0m\n", $$0 \
	}' $(MAKEFILE_LIST)

##==Работа с Docker compose

.PHONY: build
build: ## Собрать и запустить docker контейнеры
	$(DC) up --build
	@echo -e "${GREEN}✅ Готово!"

.PHONY: down
down: ## Удалить контейнеры
	$(DC) down -v
	@echo -e "${GREEN}✅ Готово!"


.PHONY: test
test: ## Запускает интеграционные тесты
	$(DC) down -v
	$(DC) up -d --build
	$(DC) exec -T api $(UV) pytest
