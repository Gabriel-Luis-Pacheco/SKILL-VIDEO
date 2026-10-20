# Known limitations and evidence policy

**What was technically tested**: GitHub CI runs Python validators, a reproducible video/audio render smoke, ffprobe media checks, captured frames and a contact sheet. A local 7s proof was also inspected at several frames for basic composition. These checks establish technical functioning only.

**What has not been proven**:
- That the resulting demo is artistically superior to work from creative studios or marketing teams (including OpenAI, Anthropic and Duolingo).
- That using this skill improves video watch-time, conversion, ROI or advertiser outcomes on a real campaign.
- That Remotion sample snippets are compiled/tested in CI (the runnable, test-covered sample is Pillow+FFmpeg).
- That all external video generators, After Effects, Rive, Blender or third-party plugins are available in the agent's runtime.
- That a metadata/asset manifest check certifies rights, consent, style fidelity, accessible use or commercial claims.
- That sample frames imply the whole film has smooth motion, no flicker or convincing sound.

**How to close those gaps**: run paired production tests with equal brief/model/tools/assets/budget, have independent blinded reviewers see full final renders, record footage/render credits and human time, test comprehension among target users, and evaluate platform performance with controlled experiments only when ethically and statistically appropriate. Publish losses and regressions. Use source references to refresh vendor APIs before each real job.

**Stop rule**: if a check was not performed, mark UNKNOWN; if a required tool/asset is missing, name it and give the highest-fidelity achievable output without pretending it is finished.

## Version 4.0 validation boundary

New modules `brief_router.py`, `campaign_results.py`, `independent_review.py`, and `new_video_project.py` are deterministic **support tools**. A valid report means inputs satisfied a contract, not that brand accuracy, statistical causality, independent reviewer identity or artistic superiority was verified. The accompanying example fixtures are explicitly synthetic. Passing unit tests does not mean the skill is objectively the world's best.

The priority for a future benchmark is a diverse, randomized production challenge evaluated with actual renders and blinded human raters plus — when appropriate — experimentally controlled commercial performance. See docs/EVALUATION_RUNBOOK.md.
