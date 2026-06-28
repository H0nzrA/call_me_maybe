# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: trakotoz <trakotoz@student.42antananarivo  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/06/28 15:03:02 by trakotoz          #+#    #+#              #
#    Updated: 2026/06/28 18:25:38 by trakotoz         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


NAME		:= call_me_maybe
CONFIG_FILE	:= pyproject.toml
SDK			:= llm_sdk
SRC			:= src

HF		:= .huggingface
CACHE	:= .cache
VENV	:= .venv-$(NAME)

PYTHON		:= python
DEBUGGER	:= pdb

UV			:= uv
URUN		:= $(UV) run
UDEBUG		:= $(URUN) $(PYTHON) -m pdb

export UV_PROJECT_ENVIRONMENT	:= ./$(VENV)
export UV_CACHE_DIR				:= ./$(CACHE)
export HF_HOME					:= ./$(HF)

RM	:= rm -rf

# Color
C_RESET		:= \033[0m
C_GREEN		:= \033[032m
C_YELLOW	:= \033[33m
C_BLUE		:= \033[34m
C_MAGENTA	:= \033[35m

all			: install

check		:
	@ echo "$(C_MAGENTA)- Check utilities$(C_RESET)"
	@ command -v $(PYTHON) > /dev/null 2>&1 || { \
		echo "$(C_YELLOW)Error: Python is not installed$(C_RESET)"; \
		exit 1; \
	}
	@ command -v $(UV) > /dev/null 2>&1 || { \
		echo "$(C_YELLOW)Error: UV is not installed$(C_RESET)"; \
		exit 1; \
	}

init		: check
	@ echo "$(C_MAGENTA)- Initialization$(C_RESET)"
	@ if [ ! -d $(VENV) ]; then \
		$(UV) venv $(VENV); \
		echo "$(C_GREEN)-- Virtual environment created: $(VENV)$(C_RESET)"; \
	fi
	@ if [ ! -f $(CONFIG_FILE) ]; then \
		$(UV) init . --name $(PROJECT); \
		echo "$(C_GREEN)$(PROJECT)-- Project initialized successfully.$(C_RESET)"; \
	else \
		echo "$(C_BLUE)$(PROJECT)-- Project already initialized.$(C_RESET)"; \
	fi

install		: init
	@ echo "$(C_MAGENTA)- Installation/Synchronization of dependencies...$(C_RESET)"
	@ $(UV) sync

run			: install
	@ echo "$(C_MAGENTA)- Run project$(C_RESET)"
	@ $(URUN) $(PYTHON) -m $(SRC) $(ARGS)

debug		: install
	@ echo "$(C_MAGENTA)- Run project (debug mode)$(C_RESET)"
	@ $(UDEBUG) -m $(SRC)

clean		:
	@ echo "$(C_MAGENTA)- Removing python cache$(C_RESET)"
	@ find . -name "__pycache__" -type d -exec $(RM) {} +
	@ find . -name ".mypy_cache" -type d -exec $(RM) {} +
	@ find . -name "*.pyc" -type f -exec $(RM) {} +

fclean		: clean
	@ echo "$(C_MAGENTA)- Removing all python virtual environment and generated file$(C_RESET)"
	@ $(RM) $(VENV) $(CACHE) $(HF)

re			: fclean all

lint		: install
	@ echo "$(C_MAGENTA)- Project readability, lint standard$(C_RESET)"
	@ $(URUN) flake8 $(SRC)
	@ $(URUN) mypy $(SRC) \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict	: install
	@ echo "$(C_MAGENTA)- Project readability, lint strict$(C_RESET)"
	@ $(URUN) flake8 $(SRC)
	@ $(URUN) mypy --strict $(SRC)

add			:
	@ echo "$(C_MAGENTA)- Adding dependencies$(C_RESET)"
	@ $(UV) add $(DEP)

remove		:
	@ echo "$(C_MAGENTA)- Removing dependencies$(C_RESET)"
	@ $(UV) remove $(DEP)

tree		:
	@ echo "$(C_MAGENTA)- Project tree dependencies$(C_RESET)"
	@ $(UV) tree

pydoc		: install
	@ $(URUN) pydocstyle $(SRc)

.PHONY		: all check init install run debug clean fclean re lint lint-strict add remove tree
