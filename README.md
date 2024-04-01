# Google Appengine on Windows

I was writing this in python because that is my comfort zone.

IT FAILED BADLY.

I was able to get th eentire script working but creating conda envs from windows in to linux was leading to segmentation faults.

I scrapped it entirely.


On the plus side, the entire process is way simpler now.

- Step -1: Clone or download (and extract) the repo (Obivious, now that I think about it.)
- Step 0: Open terminal in the downloaded folder.
- Step 1: Run step_1.ps1 from powershell.

```powershell
.\step_1.ps1
```

- Step 1.5: After completion, open bash in the same terminal window by typing bash.
- Step 2: Run step_2.sh from bash

```bash
./step_2.sh
```

You are done. Run any GAE apps using `runapp` command.
