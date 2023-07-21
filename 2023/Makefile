templates = berserk berserk-egg berserk-armor berserk-casca berserk-puck1

overlays = $(addprefix build/,$(addsuffix /overlay.png,$(templates)))

all: $(overlays)

$(templates): %: build/%/overlay.png

build/%/overlay.png: reference_images/%/reference.png reference_images/%/args.txt reference_images/%/credits.txt monkey.user.js.template overlay.py
	mkdir -p $(shell dirname $@)
	python3 overlay.py --input $< $$(cat reference_images/$*/args.txt) --output $@ --script-template monkey.user.js.template --credits reference_images/$*/credits.txt

clean:
	rm -rf build

.PHONY: clean $(templates)
