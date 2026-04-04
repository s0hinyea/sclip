Shot Detection — Your Main Question
Your current approach of combining audio RMS peaks with muzzle flash detection is directionally correct but both implementations have significant weaknesses.
Audio detection problems:
avg_rms * 1.5 as your threshold is fragile. This means a clip where the player fires constantly will have a high average RMS, making quieter shots (suppressed weapons, shots at distance) fall below the threshold and get missed. A better approach is:

Use librosa.onset.onset_detect instead of rolling your own RMS peak detection. It is specifically designed for this and handles dynamic audio much better
Or use a short-term vs long-term energy ratio rather than a static multiplier. Compare RMS of a small window against a much longer window so the threshold adapts locally rather than globally

Muzzle flash detection problems:
This is the bigger issue. Your ROI is hardcoded to pixel coordinates (1141, 652). This will break on:

Any resolution other than whatever you tested on
Any weapon held in a different position
Any agent whose hand position differs
Spectator mode clips

Brightness threshold of averageBGR >= 200 will also trigger on smokes clearing, flashes, bright map areas, and Reyna's Devour animation among other things.
A better approach for muzzle flash:

Make the ROI relative to frame dimensions, not absolute pixels
Use frame differencing instead of raw brightness — compare the current frame to the previous one and look for sudden localized brightness spikes in the weapon area specifically
This catches the flash as an event rather than a static bright region

Does the dual signal validation approach make sense?
Yes, the concept is right. Requiring both audio and visual confirmation reduces false positives significantly. However your current implementation may actually be too strict — there will be real shots where the muzzle flash is obscured by a wall corner or ability effect but the audio is clean. Consider a confidence scoring system rather than a hard AND:

Audio peak alone: 60% confidence
Muzzle flash alone: 50% confidence
Both together: 95% confidence
Output shots above a confidence threshold rather than requiring both


Workflow Assessment
The overall pipeline makes sense: upload → extract audio and video → detect events → cross validate → return results. That is the right sequence.
What is missing is a preprocessing step before any detection happens. You need to normalize the input early:

Detect resolution and normalize to a standard size
Detect and handle variable frame rates (30fps vs 60fps vs 144fps clips will behave differently)
Check for and handle corrupted or short clips gracefully

Right now if someone uploads a 144fps clip recorded at 1440p your ROI coordinates and RMS thresholds will both behave differently than expected.

Technology Assessment
Python and FastAPI — correct choice. OpenCV and Librosa are the right tools for this work. Python is the standard for CV and signal processing and you are not leaving performance on the table at this stage.
React frontend — fine for now but Create React App is outdated. It is no longer maintained and the ecosystem has moved on. When you have time, migrate to Vite. It is faster, lighter, and actively maintained. Not urgent but worth doing before you launch.
MoviePy for audio extraction — replace this. MoviePy is slow, has heavy dependencies, and is overkill for just pulling an audio track. You already have FFmpeg as a dependency — use it directly to extract audio. One FFmpeg subprocess call is faster and more reliable than MoviePy for this specific task.
The hardcoded ROI is your most urgent technical debt. Everything else can be improved iteratively but this will cause immediate failures the moment someone uploads a clip that does not match your exact test setup.

What I Would Prioritize Right Now

Replace the hardcoded ROI with resolution-relative coordinates immediately
Swap MoviePy audio extraction for direct FFmpeg
Replace the static RMS threshold with librosa.onset.onset_detect
Add input normalization before the pipeline runs
Move from binary shot validation to confidence scoring

The bones are good. The fragility around hardcoded values and static thresholds is what will hurt you most when real users throw unexpected clips at it.