<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/midi`**

**quick ref:**
> /midi [0-7]

**description:**

```
play a midi note, more information, search midiOutShortMsg for MCI api.
-- a note msg is 0x00[XX:Velocity][XX:Note][9X:9channel]
-- @param note: 0-127: 128 note keys. where 60 is middle-C key. 
-- @param velocity: usually how hard a key is pressed. 0-128. default to 64
-- @param channel: 0-15 channels. default to channel 0

/midi 0x00403C90    play a raw note 3C with velocity 40 in channel 0. 
/midi [1-7]		 do la me fa so la si     
/midi a[1-7]     lower tone
/midi g[1-7]     higher tone
```

<!-- END_AUTOGEN-->
