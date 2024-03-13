SOURCE_DIR := src
BUILD_DIR := build_default-gcc
INCLUDE_DIR := include

ifeq (${VERBOSE}, 1)
QUIET ?=
else
QUIET ?= @
endif


SRC_FILES := $(wildcard $(SOURCE_DIR)/*.c)
HEADER_FILES := $(wildcard $(INCLUDE_DIR)/*.h)
OBJ_FILES := $(patsubst $(SOURCE_DIR)/%.c, $(BUILD_DIR)/src/%.o, $(SRC_FILES))


$(info Source files: $(SRC_FILES))
$(info Header files: $(HEADER_FILES))
$(info Object files: $(OBJ_FILES))

.DEFAULT_GOAL := all


$(BUILD_DIR)/src/%.o: $(SOURCE_DIR)/%.c $(HEADER_FILES)
	${QUIET}mkdir -p $(dir $@)
	gcc -c -o $@ $< -I$(INCLUDE_DIR)

$(BUILD_DIR)/executable: $(OBJ_FILES)
	gcc -o $@ $^ -lm

all: $(BUILD_DIR)/executable