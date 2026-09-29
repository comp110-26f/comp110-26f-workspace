# Harder, Better, Faster, Stronger tribute

After implementing your list utilities, run `uv run python -m list_utils.song`
from the **daftcomp** project directory. The supplied decoder reconstructs eight
tracks of 992 sixteenth-note steps at 125 BPM, lasting 119.04 seconds.

This is a Daft Punk tribute adapted from a supplied MIDI file. The MIDI is not
included in the student workspace and contained no author or composer attribution
metadata. The arrangement reduces chords to individual pitches, combines some
parts, maps percussion to kick/snare/hat sounds, and approximates the instruments
with pulse and triangle voices. It is an educational arrangement, not a claim
to reproduce the commercial recording faithfully.

The chord line's payload has 496 entries; `halftime` restores it to 992 steps.
The other seven parts retain their full timing. The decoder uses all six list
functions and never applies `halftime` to drum tracks, which do not accept HOLD.
Keep the supplied launch tempo at 125 BPM to stay within the player's two-minute
limit. You can stop playback at any time.
