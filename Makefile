templates = berserk bloodborne stalker

overlays = $(addprefix build/,$(addsuffix /overlay.png,$(templates)))

all: $(overlays)

$(templates): %: build/%/overlay.png

build/%/overlay.png: reference_images/%/reference.png reference_images/%/args.txt
	mkdir -p $(shell dirname $@)
	python3 overlay.py --input $< $$(cat reference_images/$*/args.txt) --output $@

clean:
	rm -rf build

.PHONY: clean $(templates)
